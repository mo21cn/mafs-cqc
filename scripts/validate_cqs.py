#!/usr/bin/env python
"""CQC-P0 deterministic validator for CandidateQuestionSet v0.1 artifacts.

Contract CQC-P0-MINIMAL-DIGESTION-SURFACE-v0.1 section 11.

Checks (machine-only; never scores scientific quality):
  schema valid
  artifact_id present
  schema_version present
  source hash matches
  question_id unique
  statement non-empty
  every source_trace exact quote exists verbatim in narrative
  dependency target exists
  no self-dependency
  dependency DAG acyclic
  resolution_condition non-empty
  uncertainty is null or text
  questions[] non-empty

Usage:
  python scripts/validate_cqs.py <artifact.json>...
  python scripts/validate_cqs.py <artifact.json> --check-inputs examples/inputs
  python scripts/validate_cqs.py examples/outputs/*.json --json   (machine mode)

Exit code 0 iff all checked artifacts pass; 1 otherwise.
"""
from __future__ import annotations

import argparse
import glob as globmod
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mini_jsonschema import UnsupportedSchemaFeatureError, validate as schema_validate

PKG_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PKG_ROOT / "schemas" / "candidate_question_set.v0.1.schema.json"


def load_schema() -> dict:
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"MISSING_SCHEMA: {SCHEMA_PATH}")
    _check_schema_keywords_deep(schema)
    return schema


def _check_schema_keywords_deep(node, path="schema"):
    if isinstance(node, dict):
        if "properties" in node:
            for k, sub in node["properties"].items():
                _check_schema_keywords_deep(sub, f"{path}.properties.{k}")
        if "items" in node and isinstance(node["items"], dict):
            _check_schema_keywords_deep(node["items"], f"{path}.items")
    elif not isinstance(node, (list, str, int, float, bool, type(None))):
        raise UnsupportedSchemaFeatureError(f"bad schema node at {path}: {type(node).__name__}")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _topological_order_ok(questions: list[dict]) -> list[str]:
    """Return error list; acyclic check via repeated removal of zero-in-degree nodes."""
    ids = [q["question_id"] for q in questions]
    id_set = set(ids)
    deps = {q["question_id"]: list(q.get("dependencies") or []) for q in questions}
    errors: list[str] = []
    for qid, dl in deps.items():
        for d in dl:
            if d == qid:
                errors.append(f"{qid}: self-dependency")
            elif d not in id_set:
                errors.append(f"{qid}: dependency target {d} does not exist")
    remaining = {qid for qid in ids}
    while remaining:
        removable = [qid for qid in remaining
                     if all(d not in remaining for d in deps.get(qid, []))]
        if not removable:
            cycle = sorted(remaining)
            errors.append(f"dependency cycle among: {', '.join(cycle)}")
            break
        for qid in removable:
            remaining.discard(qid)
    return errors


def validate_artifact(artifact: dict, narrative_file: Path | None = None) -> dict:
    schema = load_schema()
    result = {
        "schema_valid": False,
        "source_hash_valid": False,
        "question_id_unique": True,
        "exact_trace_valid": False,
        "dependency_dag_valid": False,
        "narrative_file_match": None,
        "errors": [],
        "question_count": 0,
    }
    errs = schema_validate(artifact, schema)
    if errs:
        result["errors"] = errs[:30]
        return result
    result["schema_valid"] = True

    questions = artifact["questions"]
    result["question_count"] = len(questions)

    # source hash
    actual = sha256_text(artifact["source_narrative"])
    if actual == artifact["source_narrative_sha256"]:
        result["source_hash_valid"] = True
    else:
        result["errors"].append("source_narrative_sha256 does not match re-computed SHA-256")

    # narrative file cross-check (identity/lineage anchor)
    if narrative_file is not None:
        text = narrative_file.read_text(encoding="utf-8")
        file_sha = sha256_text(text)
        result["narrative_file_match"] = (
            file_sha == artifact["source_narrative_sha256"]
            and text == artifact["source_narrative"]
        )
        if not result["narrative_file_match"]:
            result["errors"].append(
                f"narrative file {narrative_file.name} does not match embedded source_narrative")

    # question_id uniqueness
    ids = [q["question_id"] for q in questions]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        result["question_id_unique"] = False
        result["errors"].append(f"duplicate question_id: {', '.join(dupes)}")

    # exact source traces (verbatim)
    trace_ok = True
    for q in questions:
        for tr in q.get("source_trace") or []:
            quote = tr["exact_quote"]
            if quote not in artifact["source_narrative"]:
                trace_ok = False
                result["errors"].append(
                    f"{q['question_id']}: exact_quote not found verbatim in narrative: {quote[:80]!r}")
    result["exact_trace_valid"] = trace_ok

    # dependency DAG
    dep_errors = _topological_order_ok(questions)
    if dep_errors:
        result["errors"].extend(dep_errors)
    else:
        result["dependency_dag_valid"] = True

    result["ok"] = (
        result["schema_valid"]
        and result["source_hash_valid"]
        and result["question_id_unique"]
        and result["exact_trace_valid"]
        and result["dependency_dag_valid"]
        and (result["narrative_file_match"] is not False)
        and not result["errors"]
    )
    return result


def infer_narrative_file(artifact_path: Path, inputs_dir: Path | None) -> Path | None:
    if inputs_dir is None:
        return None
    tag = artifact_path.stem  # cqs_A_gf_em -> narrative_A_gf_em.md
    if tag.startswith("cqs_"):
        tag = tag[4:]
    cand = inputs_dir / f"narrative_{tag}.md"
    return cand if cand.is_file() else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate CandidateQuestionSet v0.1 artifacts")
    ap.add_argument("artifacts", nargs="+")
    ap.add_argument("--check-inputs", type=Path, default=None,
                    help="cross-check embedded narrative against examples/inputs files")
    ap.add_argument("--json", action="store_true", dest="machine", help="machine-readable output")
    args = ap.parse_args(argv)

    schema = load_schema()
    _check_schema_keywords_deep(schema)

    results = []
    failed = False
    # expand globs ourselves (PowerShell does not expand wildcards for native exes)
    paths: list[Path] = []
    for raw in args.artifacts:
        if any(ch in raw for ch in "*?"):
            paths.extend(Path(p) for p in sorted(globmod.glob(raw)))
        else:
            paths.append(Path(raw))
    if not paths:
        print("NO_ARTIFACTS: no files matched the given arguments", file=sys.stderr)
        return 1
    for p in paths:
        if not p.is_file():
            failed = True
            results.append({"file": str(p), "ok": False, "errors": ["file not found"]})
            continue
        try:
            artifact = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            failed = True
            results.append({"file": str(p), "ok": False, "errors": [f"invalid JSON: {e}"]})
            continue
        nf = infer_narrative_file(p, args.check_inputs)
        res = validate_artifact(artifact, nf)
        res["file"] = str(p)
        if not res.get("ok"):
            failed = True
        results.append(res)

    if args.machine:
        print(json.dumps({"schema": str(SCHEMA_PATH), "artifacts": results,
                          "all_ok": not failed}, indent=2, ensure_ascii=False))
    else:
        for r in results:
            status = "PASS" if r.get("ok") else "FAIL"
            print(f"{status}  {r['file']}  (questions={r.get('question_count')})")
            for e in r.get("errors", []):
                print(f"      - {e}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
