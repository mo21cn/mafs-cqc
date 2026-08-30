#!/usr/bin/env python
"""CQC-P1 benchmark package validator (contract CQC-P1-REAL-TASK-DIGESTION-REPLAY-
REDIGESTION-LINEAGE-v0.1 sections 12-14, 17).

Validates ONLY deterministic facts:
  - benchmark package completeness (per-case folder structure)
  - raw input sha256 matches case_metadata.input_sha256
  - Arm B CandidateQuestionSet: P0 schema + source hash + exact traces + DAG
  - Arm C re-digestion lineage: prior artifact exists + hash matches + explicit
    conflict + diagnosis + revised artifact differs and re-validates
  - deterministic render reproducibility for arm_b/arm_c human_render.md
  - repository hygiene (no bytecode) when run with --hygiene

NEVER judges: semantic equivalence, coverage, granularity, dependency truth,
intent fidelity, repair quality (those belong to HO + ChatGPT adjudication).

Usage:
  python scripts/validate_p1.py                # scan benchmarks/p1/ (if present)
  python scripts/validate_p1.py --json         # machine mode
  python scripts/validate_p1.py --hygiene      # include bytecode check
Exit 0 iff all checks pass; 1 otherwise.
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
BENCH = PKG / "benchmarks" / "p1"

REQUIRED_FILES = {
    "raw_narrative.txt",
    "case_metadata.json",
    "arm_a/downstream_preparation.json",
    "arm_a/human_render.md",
    "arm_b/candidate_question_set.json",
    "arm_b/downstream_preparation.json",
    "arm_b/human_render.md",
    "evaluation/comparison.json",
    "evaluation/adjudication.md",
}
ARM_C_FILES = {
    "arm_c/failure_diagnosis.json",
    "arm_c/revised_candidate_question_set.json",
    "arm_c/downstream_preparation.json",
    "arm_c/human_render.md",
}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha256_text(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def validate_case(case_dir: Path, errors: list, case_results: list) -> dict:
    res = {"case_id": case_dir.name, "ok": True, "checks": {}}
    # 1. completeness
    missing = [f for f in REQUIRED_FILES if not (case_dir / f).is_file()]
    if missing:
        errors.append(f"{case_dir.name}: missing files: {missing}")
        res["checks"]["package_complete"] = False
        res["ok"] = False
        return res
    res["checks"]["package_complete"] = True

    meta = json.loads((case_dir / "case_metadata.json").read_text(encoding="utf-8"))

    # 2. raw input hash
    raw_text = (case_dir / "raw_narrative.txt").read_text(encoding="utf-8")
    raw_sha = sha256_text(raw_text)
    if raw_sha != meta.get("input_sha256"):
        errors.append(f"{case_dir.name}: raw_narrative.txt sha256 mismatch with case_metadata.input_sha256")
        res["checks"]["raw_hash_valid"] = False
        res["ok"] = False
    else:
        res["checks"]["raw_hash_valid"] = True

    # 3. arm_b CQS validation (P0 contract, unchanged)
    cqs_b = json.loads((case_dir / "arm_b" / "candidate_question_set.json").read_text(encoding="utf-8"))
    vb = validate_artifact(cqs_b)
    res["checks"]["arm_b_schema_valid"] = vb["schema_valid"]
    res["checks"]["arm_b_source_hash_valid"] = vb["source_hash_valid"]
    res["checks"]["arm_b_exact_trace_valid"] = vb["exact_trace_valid"]
    res["checks"]["arm_b_dependency_dag_valid"] = vb["dependency_dag_valid"]
    if not vb["ok"]:
        errors.append(f"{case_dir.name}: arm_b CQS invalid: {vb['errors'][:5]}")
        res["ok"] = False

    # 4. arm_b render reproducibility
    rb = (case_dir / "arm_b" / "human_render.md").read_text(encoding="utf-8")
    if render(cqs_b) != rb:
        errors.append(f"{case_dir.name}: arm_b human_render.md not reproducible from CQS JSON")
        res["checks"]["arm_b_render_reproducible"] = False
        res["ok"] = False
    else:
        res["checks"]["arm_b_render_reproducible"] = True

    # 5. arm_c lineage (only if triggered)
    arm_c_dir = case_dir / "arm_c"
    if arm_c_dir.is_dir():
        missing_c = [f for f in ARM_C_FILES if not (arm_c_dir / f).is_file()]
        if missing_c:
            errors.append(f"{case_dir.name}: arm_c incomplete: {missing_c}")
            res["checks"]["arm_c_complete"] = False
            res["ok"] = False
        else:
            res["checks"]["arm_c_complete"] = True
        fd = json.loads((arm_c_dir / "failure_diagnosis.json").read_text(encoding="utf-8"))
        revised = json.loads((arm_c_dir / "revised_candidate_question_set.json").read_text(encoding="utf-8"))
        vr = validate_artifact(revised)
        res["checks"]["arm_c_revised_schema_valid"] = vr["schema_valid"]
        res["checks"]["arm_c_revised_dag_valid"] = vr["dependency_dag_valid"]
        prior_ok = True
        lineage_errors = []
        if not fd.get("observed_conflict"):
            lineage_errors.append("failure_diagnosis.json missing observed_conflict")
        if not fd.get("diagnosis"):
            lineage_errors.append("failure_diagnosis.json missing diagnosis")
        if not fd.get("implicated_fields"):
            lineage_errors.append("failure_diagnosis.json missing implicated_fields")
        prior_ref = fd.get("prior_artifact_sha256")
        if not prior_ref:
            lineage_errors.append("failure_diagnosis.json missing prior_artifact_sha256")
        else:
            prior_artifact = (case_dir / "arm_b" / "candidate_question_set.json")
            if prior_ref != sha256_file(prior_artifact):
                lineage_errors.append("prior_artifact_sha256 does not match arm_b CQS file hash")
                prior_ok = False
        if sha256_text(json.dumps(revised, sort_keys=True)) == sha256_text(
                json.dumps(cqs_b, sort_keys=True)):
            lineage_errors.append("revised CQS is byte-identical to prior: retry mislabeled as re-digestion")
        if not vr["ok"]:
            lineage_errors.append(f"revised CQS invalid: {vr['errors'][:3]}")
        res["checks"]["arm_c_lineage_valid"] = not lineage_errors
        if lineage_errors:
            errors.append(f"{case_dir.name}: arm_c lineage errors: {lineage_errors[:4]}")
            res["ok"] = False
        res["checks"]["arm_c_render_reproducible"] = (
            (arm_c_dir / "human_render.md").read_text(encoding="utf-8") == render(revised))
        if not res["checks"]["arm_c_render_reproducible"]:
            errors.append(f"{case_dir.name}: arm_c human_render.md not reproducible")
            res["ok"] = False
    else:
        res["checks"]["arm_c_triggered"] = False

    case_results.append(res)
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="CQC-P1 benchmark package validator (deterministic facts only)")
    ap.add_argument("--json", action="store_true", dest="machine")
    ap.add_argument("--hygiene", action="store_true", help="also check for committed bytecode")
    args = ap.parse_args(argv)

    if not BENCH.is_dir():
        print("NO_P1_BENCHMARK: benchmarks/p1 not present (pre-P1 branch); nothing to validate.")
        return 0

    errors: list[str] = []
    case_results: list[dict] = []
    cases = sorted([d for d in BENCH.iterdir() if d.is_dir() and d.name.startswith("case_")])
    if not cases:
        print("NO_CASES: benchmarks/p1 exists but contains no case_* directories.")
        return 1
    for c in cases:
        validate_case(c, errors, case_results)

    hygiene = None
    if args.hygiene:
        tracked = subprocess.run(["git", "ls-files"], cwd=PKG,
                                 capture_output=True, text=True, timeout=15).stdout.splitlines()
        pycs = [t for t in tracked if t.endswith(".pyc") or "__pycache__" in t]
        hygiene = {"committed_bytecode": pycs, "scope": "git-tracked files only"}
        if pycs:
            errors.append(f"repository hygiene: bytecode committed: {pycs[:5]}")

    report = {"benchmark_dir": str(BENCH), "case_count": len(cases), "cases": case_results,
              "all_ok": not errors, "errors": errors[:30], "hygiene": hygiene}
    if args.machine:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for c in case_results:
            print(("PASS" if c["ok"] else "FAIL"), c["case_id"])
        for e in errors:
            print(f"      - {e}")
        print(f"cases={len(cases)} all_ok={report['all_ok']}")
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
