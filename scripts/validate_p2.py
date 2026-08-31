#!/usr/bin/env python
"""CQC-P2 validator (contract CQC-P2-ARTIFACT-COMMITMENT-BOUNDARY-PROJECTION-LOSS-STRESS-v0.1).

Validates ONLY deterministic facts:
  - P2 semantic package completeness (6 cases)
  - CQS schema compatibility (P0 contract), source hashes, exact traces, DAG, render
  - projection_review presence (records exist; content NOT semantically judged)
  - R1/R2 revision-topology truth: content-hash self-consistency, derived-from
    bindings, current / superseded / stale (incl. transitive stale) vs expected_state
  - repository hygiene (--hygiene, git-tracked bytecode only)

NEVER judges: projection loss, semantic fidelity, false precision, granularity,
question-type correctness, scientific dependency truth.

Usage:
  python scripts/validate_p2.py [--json] [--hygiene]
Exit 0 iff all checks pass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_cqs import validate_artifact  # noqa: E402
from render_cqs import render  # noqa: E402

PKG = Path(__file__).resolve().parents[1]
SEM = PKG / "benchmarks" / "p2" / "semantic"
RT = PKG / "benchmarks" / "p2" / "revision_topology"

SEM_REQUIRED = {
    "source_narrative.txt", "case_metadata.json", "candidate_question_set.json",
    "human_render.md", "evaluation/projection_review.json",
}


def csha(content) -> str:
    return hashlib.sha256(json.dumps(content, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# --------------------------------------------------------------- semantic part
def validate_semantic(errors: list) -> dict:
    cases = sorted([d for d in SEM.iterdir() if d.is_dir()])
    out = {"case_count": len(cases), "schema_valid": 0, "hash_valid": 0,
           "trace_valid": 0, "dag_valid": 0, "render_valid": 0, "review_present": 0}
    for c in cases:
        missing = [f for f in SEM_REQUIRED if not (c / f).is_file()]
        if missing:
            errors.append(f"p2/semantic/{c.name}: missing {missing}")
            continue
        art = json.loads((c / "candidate_question_set.json").read_text(encoding="utf-8"))
        v = validate_artifact(art)
        # RA1: initial first-pass artifact must be preserved and recoverable
        init_p = c / "candidate_question_set.initial.json"
        if not init_p.is_file():
            errors.append(f"p2/semantic/{c.name}: initial first-pass CQS not preserved (candidate_question_set.initial.json missing)")
        # RA1: if a re-digestion record exists, lineage + revised validity must hold
        rec_p = c / "evaluation" / "redigestion_record.json"
        if rec_p.is_file():
            rec = json.loads(rec_p.read_text(encoding="utf-8"))
            if rec.get("prior_artifact_sha256") != sha256_file(init_p):
                errors.append(f"p2/semantic/{c.name}: prior_artifact_sha256 does not bind the preserved initial CQS")
            if rec.get("revised_artifact_sha256") != sha256_file(c / "candidate_question_set.json"):
                errors.append(f"p2/semantic/{c.name}: revised_artifact_sha256 does not bind the current CQS")
            if rec.get("revised_artifact_id") != art.get("artifact_id"):
                errors.append(f"p2/semantic/{c.name}: revised_artifact_id does not match current CQS")
            if rec.get("diagnosis_source") != "HO+ChatGPT P2 acceptance":
                errors.append(f"p2/semantic/{c.name}: re-digestion diagnosis_source must be HO+ChatGPT P2 acceptance")
            if rec.get("revised_artifact_id") == rec.get("prior_artifact_id"):
                errors.append(f"p2/semantic/{c.name}: retry mislabeled as re-digestion (revised id == prior id)")
        # RA1: final semantic adjudication must be present and no longer pending
        pr = json.loads((c / "evaluation" / "projection_review.json").read_text(encoding="utf-8"))
        fa = pr.get("final_semantic_adjudication") or {}
        st = fa.get("status")
        if not st or st == "PENDING_HO_CHATGPT":
            errors.append(f"p2/semantic/{c.name}: final_semantic_adjudication missing or still pending")
        if st and st not in ("FAIL_REPAIR_REQUIRED", "PASS_WITH_CAVEAT",
                             "PRODUCTIVE_INSTABILITY_PRESERVED", "BOUNDARY_UNRESOLVED_PRESERVED", "PASS"):
            errors.append(f"p2/semantic/{c.name}: illegal final_semantic_adjudication.status {st!r}")
        if v["schema_valid"]:
            out["schema_valid"] += 1
        if v["source_hash_valid"]:
            out["hash_valid"] += 1
        if v["exact_trace_valid"]:
            out["trace_valid"] += 1
        if v["dependency_dag_valid"]:
            out["dag_valid"] += 1
        if render(art) == (c / "human_render.md").read_text(encoding="utf-8"):
            out["render_valid"] += 1
        if (c / "evaluation" / "projection_review.json").is_file():
            out["review_present"] += 1
        if not v["ok"]:
            errors.append(f"p2/semantic/{c.name}: CQS invalid: {v['errors'][:3]}")
        if not v["schema_valid"] or not v["source_hash_valid"] or not v["exact_trace_valid"] \
                or not v["dependency_dag_valid"] or render(art) != (c / "human_render.md").read_text(encoding="utf-8"):
            errors.append(f"p2/semantic/{c.name}: mechanical validation incomplete")
    return out


# ---------------------------------------------------------- revision topology
def _load_artifacts(fdir: Path) -> dict[str, dict]:
    arts = {}
    for f in fdir.glob("*_r*.json"):
        arts[f"{f.stem.rsplit('_r', 1)[0]}@{f.stem.rsplit('_r', 1)[1]}"] = json.loads(f.read_text(encoding="utf-8"))
    return arts


def _state_of(aid: str, rev: int, arts: dict, currents: dict, memo: dict) -> str:
    key = f"{aid}@{rev}"
    if key in memo:
        return memo[key]
    if key not in arts:
        return "missing"
    a = arts[key]
    if a.get("content_sha256") != csha(a.get("content")):
        memo[key] = "invalid"
        return memo[key]
    cur = currents.get(aid)
    if rev != cur:
        memo[key] = "superseded"
        return memo[key]
    for b in a.get("source_bindings") or []:
        src = f"{b['artifact_id']}@{b['revision']}"
        if src not in arts or arts[src].get("content_sha256") != b.get("content_sha256"):
            memo[key] = "stale"
            return memo[key]
        if b["revision"] != currents.get(b["artifact_id"]):
            memo[key] = "stale"
            return memo[key]
        if _state_of(b["artifact_id"], b["revision"], arts, currents, memo) != "current":
            memo[key] = "stale"
            return memo[key]
    memo[key] = "current"
    return memo[key]


def validate_topology(scenario_dir: Path, errors: list) -> dict:
    fixtures = scenario_dir / "fixtures"
    arts = _load_artifacts(fixtures)
    series = json.loads((fixtures / "series.json").read_text(encoding="utf-8"))
    expected = json.loads((scenario_dir / "expected_state.json").read_text(encoding="utf-8"))
    report = {"scenario": expected["scenario"], "stages": []}
    ok = True
    for stage in expected["stages"]:
        currents = stage["current_revisions"]
        memo: dict = {}
        actual = {}
        for key in stage["expected"]:
            aid, rev = key.rsplit("@", 1)
            actual[key] = _state_of(aid, int(rev), arts, currents, memo)
        match = actual == stage["expected"]
        ok = ok and match
        report["stages"].append({"stage": stage["stage"], "expected": stage["expected"],
                                 "actual": actual, "match": match})
        if not match:
            errors.append(f"{scenario_dir.name}/{stage['stage']}: state mismatch")
    (scenario_dir / "validation_report.json").write_bytes(
        (json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    return {"ok": ok, "scenario": expected["scenario"]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", dest="machine")
    ap.add_argument("--hygiene", action="store_true")
    args = ap.parse_args(argv)

    if not (PKG / "benchmarks" / "p2").is_dir():
        print("NO_P2_BENCHMARK: benchmarks/p2 not present; nothing to validate.")
        return 0

    errors: list[str] = []
    sem = validate_semantic(errors)
    topo = []
    for sd in sorted(RT.iterdir()):
        if sd.is_dir() and (sd / "expected_state.json").is_file():
            topo.append(validate_topology(sd, errors))

    hygiene = None
    if args.hygiene:
        tracked = subprocess.run(["git", "ls-files"], cwd=PKG, capture_output=True,
                                 text=True, timeout=15).stdout.splitlines()
        pycs = [t for t in tracked if t.endswith(".pyc") or "__pycache__" in t]
        hygiene = {"committed_bytecode": pycs}
        if pycs:
            errors.append(f"repository hygiene: bytecode committed: {pycs[:5]}")

    report = {
        "semantic": sem,
        "revision_topology": [{"scenario": t["scenario"], "ok": t["ok"]} for t in topo],
        "all_ok": not errors and all(t["ok"] for t in topo),
        "errors": errors[:20],
        "hygiene": hygiene,
    }
    if args.machine:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"semantic cases={sem['case_count']} (schema {sem['schema_valid']}/"
              f"hash {sem['hash_valid']}/trace {sem['trace_valid']}/dag {sem['dag_valid']}/"
              f"render {sem['render_valid']}/review {sem['review_present']})")
        for t in topo:
            print(("PASS" if t["ok"] else "FAIL"), t["scenario"])
        for e in errors:
            print(f"      - {e}")
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
