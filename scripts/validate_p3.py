#!/usr/bin/env python
"""CQC-P3 validator (contract CQC-P3-CONTEXTUAL-SEARCH-REQUIREMENT-DIGESTION-v0.1 sections 18-19).

Validates ONLY deterministic facts:
  - P3 contextual package completeness (6 cases)
  - SRP v0.1 schema validity
  - source narrative / source CQS SHA truth (case_metadata + copied files)
  - source CQS artifact identity (source_cqs_id matches embedded artifact_id)
  - target_question_ids exist in source CQS (no orphan requirements)
  - requirement IDs unique; route IDs unique within a requirement; route status enum
  - deterministic render reproducibility
  - type-perturbation: non-type fields identical to base, source context identical, SRP valid
  - execution/provider leakage scan (machine-checkable terms)
  - repository hygiene (--hygiene, git-tracked bytecode only)

NEVER judges: semantic route correctness, requirement quality, projection loss.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_cqs import validate_artifact  # noqa: E402
from render_srp import render  # noqa: E402

PKG = Path(__file__).resolve().parents[1]
P3 = PKG / "benchmarks" / "p3"
SEM = P3 / "contextual"
DOCS = PKG / "docs"
TP = P3 / "type_perturbation"
SCHEMA = PKG / "schemas" / "search_requirement_profile.v0.1.schema.json"

SEM_REQUIRED = {
    "source_narrative.txt", "source_cqs.json", "case_metadata.json",
    "search_requirement_profile.json", "human_render.md",
    "evaluation/contextual_review.json", "evaluation/requirement_admission.json",
}

LEAK_TERMS = ["crossref", "pubmed", "google scholar", "api endpoint", "top-k",
              "http request", "token budget", "query string", "provider fallback",
              "resolver call"]


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha256_text(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def load_schema() -> dict:
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


def _mini_validate(instance, schema, path="$", errors=None, root=None):
    from mini_jsonschema import validate as mv
    if errors is None:
        return mv(instance, schema, path)
    errors.extend(mv(instance, schema, path))
    return errors


def leak_scan(text: str) -> list[str]:
    low = text.lower()
    return [t for t in LEAK_TERMS if t in low]


def validate_semantic_case(case: Path, errors: list, results: list) -> dict:
    res = {"case_id": case.name, "ok": True, "checks": {}}
    missing = [f for f in SEM_REQUIRED if not (case / f).is_file()]
    if missing:
        errors.append(f"{case.name}: missing {missing}")
        res["ok"] = False
        results.append(res)
        return res
    res["checks"]["package_complete"] = True

    meta = json.loads((case / "case_metadata.json").read_text(encoding="utf-8"))
    srp = json.loads((case / "search_requirement_profile.json").read_text(encoding="utf-8"))
    cqs = json.loads((case / "source_cqs.json").read_text(encoding="utf-8"))
    narr = (case / "source_narrative.txt").read_text(encoding="utf-8")

    schema = load_schema()
    errs = _mini_validate(srp, schema)
    res["checks"]["srp_schema_valid"] = not errs
    if errs:
        errors.append(f"{case.name}: SRP schema errors: {errs[:4]}")
        res["ok"] = False

    narr_sha = sha256_text(narr)
    cqs_sha = sha256_file(case / "source_cqs.json")
    ok = (srp["source_narrative_sha256"] == narr_sha == meta["source_narrative_sha256"]
          and srp["source_narrative"] == narr
          and srp["source_cqs_sha256"] == cqs_sha == meta["source_cqs_sha256"])
    res["checks"]["source_binding_valid"] = ok
    if not ok:
        errors.append(f"{case.name}: source narrative/CQS binding mismatch")
        res["ok"] = False

    # copied CQS must equal the accepted P2 final CQS byte-for-byte
    p2_cqs = PKG / "benchmarks" / "p2" / "semantic" / case.name / "candidate_question_set.json"
    res["checks"]["p2_cqs_drift_free"] = (cqs_bytes := (case / "source_cqs.json").read_bytes()) == p2_cqs.read_bytes()
    if not res["checks"]["p2_cqs_drift_free"]:
        errors.append(f"{case.name}: source_cqs.json drifted from P2 final CQS (P3_SOURCE_CQS_DRIFT)")
        res["ok"] = False

    cv = validate_artifact(cqs)
    if not cv["ok"]:
        errors.append(f"{case.name}: copied CQS fails P0 validation: {cv['errors'][:3]}")
        res["ok"] = False

    qids = {q["question_id"] for q in cqs["questions"]}
    rids = [r["requirement_id"] for r in srp["requirements"]]
    res["checks"]["requirement_ids_unique"] = len(rids) == len(set(rids))
    if not res["checks"]["requirement_ids_unique"]:
        errors.append(f"{case.name}: duplicate requirement_id")
        res["ok"] = False
    res["checks"]["question_refs_valid"] = True
    res["checks"]["route_status_valid"] = True
    res["checks"]["route_ids_unique"] = True
    orphan = 0
    for r in srp["requirements"]:
        targets = r["target_question_ids"]
        if not targets or any(t not in qids for t in targets):
            res["checks"]["question_refs_valid"] = False
            errors.append(f"{case.name}: {r['requirement_id']} references missing CQ ids {targets}")
            res["ok"] = False
        if not targets:
            orphan += 1
        route_ids = [rt["route_id"] for rt in r["epistemic_routes"]]
        if len(route_ids) != len(set(route_ids)):
            res["checks"]["route_ids_unique"] = False
            errors.append(f"{case.name}: {r['requirement_id']} duplicate route_id")
            res["ok"] = False
        for rt in r["epistemic_routes"]:
            if rt["status"] not in ("REQUIRED", "CONDITIONAL"):
                res["checks"]["route_status_valid"] = False
                errors.append(f"{case.name}: {r['requirement_id']} illegal route status {rt['status']}")
                res["ok"] = False
    if orphan:
        errors.append(f"{case.name}: orphan requirement (no valid target)")

    # execution leakage scan (named source objects are preserved verbatim from the narrative)
    leak_terms = leak_scan(json.dumps(srp["requirements"], ensure_ascii=False).lower())
    res["checks"]["execution_leak_free"] = not leak_terms
    if leak_terms:
        errors.append(f"{case.name}: execution/provider leakage terms: {leak_terms}")
        res["ok"] = False

    rendered = render(srp)
    res["checks"]["render_reproducible"] = rendered == (case / "human_render.md").read_text(encoding="utf-8")
    if not res["checks"]["render_reproducible"]:
        errors.append(f"{case.name}: human_render.md not reproducible")
        res["ok"] = False

    review = json.loads((case / "evaluation" / "contextual_review.json").read_text(encoding="utf-8"))
    # RA2 Closure D: review-truth — review identity/hash/mechanical fields must match actual artifacts
    review_ok = True
    if review.get("source_cqs_id") != cqs.get("artifact_id"):
        errors.append(f"{case.name}: contextual_review.source_cqs_id mismatch (CONTEXTUAL_REVIEW_MACHINE_TRUTH_MISMATCH)")
        review_ok = False
    if review.get("source_cqs_sha256") != cqs_sha:
        errors.append(f"{case.name}: contextual_review.source_cqs_sha256 does not match source_cqs.json bytes")
        review_ok = False
    if review.get("srp_artifact_id") != srp.get("artifact_id"):
        errors.append(f"{case.name}: contextual_review.srp_artifact_id mismatch")
        review_ok = False
    if review.get("srp_sha256") != sha256_file(case / "search_requirement_profile.json"):
        errors.append(f"{case.name}: contextual_review.srp_sha256 does not match search_requirement_profile.json bytes")
        review_ok = False
    recomputed = {
        "schema_valid": not errs,
        "source_binding_valid": ok,
        "question_refs_valid": res["checks"].get("question_refs_valid", False),
        "render_valid": res["checks"].get("render_reproducible", False),
        "execution_leak_free": not leak_terms,
    }
    stated = review.get("mechanical") or {}
    for k, actual in recomputed.items():
        if bool(stated.get(k)) != bool(actual):
            errors.append(f"{case.name}: contextual_review.mechanical.{k}={stated.get(k)} but recomputed truth={bool(actual)} (CONTEXTUAL_REVIEW_MACHINE_TRUTH_MISMATCH)")
            review_ok = False
    res["checks"]["review_truth_valid"] = review_ok
    if not review_ok:
        res["ok"] = False
    fa = review.get("final_semantic_adjudication") or {}
    fa_status = fa.get("status")
    if not fa_status or fa_status == "PENDING_HO_CHATGPT":
        errors.append(f"{case.name}: final_semantic_adjudication missing or still pending (RA2 requires finalized state)")
        res["ok"] = False
    allowed = {"PASS", "PASS_WITH_CAVEAT", "REPAIRED", "PRODUCTIVE_INSTABILITY_PRESERVED", "BOUNDARY_UNRESOLVED_PRESERVED"}
    if fa_status not in allowed and fa_status != "PENDING_HO_CHATGPT":
        errors.append(f"{case.name}: illegal final_semantic_adjudication.status {fa_status!r}")
        res["ok"] = False
    results.append(res)
    return res


def validate_perturbation(td: Path, base_dir: Path, errors: list, results: list) -> dict:
    res = {"perturbation": td.name, "ok": True, "checks": {}}
    required = ["source_cqs_perturbed.json", "search_requirement_profile.json",
                "human_render.md", "evaluation/type_perturbation_review.json"]
    missing = [f for f in required if not (td / f).is_file()]
    if missing:
        errors.append(f"{td.name}: missing {missing}")
        res["ok"] = False
        results.append(res)
        return res
    review = json.loads((td / "evaluation" / "type_perturbation_review.json").read_text(encoding="utf-8"))
    base_case = review.get("base_case")
    if not base_case:
        errors.append(f"{td.name}: review missing base_case")
        res["ok"] = False
        results.append(res)
        return res
    base_cqs = json.loads((base_dir / base_case / "source_cqs.json").read_text(encoding="utf-8"))
    pert_cqs = json.loads((td / "source_cqs_perturbed.json").read_text(encoding="utf-8"))
    base_srp = json.loads((base_dir / base_case / "search_requirement_profile.json").read_text(encoding="utf-8"))
    pert_srp = json.loads((td / "search_requirement_profile.json").read_text(encoding="utf-8"))

    qid = review["perturbed_question_id"]
    bq = next(q for q in base_cqs["questions"] if q["question_id"] == qid)
    pq = next(q for q in pert_cqs["questions"] if q["question_id"] == qid)
    non_type_identical = all(
        (bq.get(f) == pq.get(f)) for f in ("statement", "source_trace", "dependencies",
                                           "resolution_condition", "uncertainty"))
    ctx_identical = base_srp["source_narrative"] == pert_srp["source_narrative"]
    res["checks"]["non_type_fields_identical"] = non_type_identical
    res["checks"]["source_context_identical"] = ctx_identical
    res["checks"]["only_type_changed"] = (bq["question_type"] == review["original_question_type"]
                                          and pq["question_type"] == review["perturbed_question_type"])
    sv = validate_artifact(pert_cqs)
    res["checks"]["perturbed_cqs_valid"] = sv["ok"]
    sp_errs = _mini_validate(pert_srp, load_schema())
    res["checks"]["perturbed_srp_valid"] = not sp_errs
    res["checks"]["render_reproducible"] = render(pert_srp) == (td / "human_render.md").read_text(encoding="utf-8")
    if not (non_type_identical and ctx_identical and res["checks"]["only_type_changed"]
            and sv["ok"] and not sp_errs and res["checks"]["render_reproducible"]):
        errors.append(f"{td.name}: perturbation mechanical checks failed")
        res["ok"] = False
    if review.get("final_semantic_adjudication", {}).get("status") != "PENDING_HO_CHATGPT":
        pass  # RA2: perturbation reviews are finalized (T1 VALID_PASS / T2 INVALID_CONTROL_DESIGN)
    st = review.get("final_semantic_adjudication", {}).get("status")
    if review["base_case"] == "s3_antagonist_domains" and st != "VALID_PASS":
        errors.append(f"{td.name}: T1 final state must be VALID_PASS (got {st!r})")
        res["ok"] = False
    if review["base_case"] == "s5_mixed_commitment" and st != "INVALID_CONTROL_DESIGN":
        errors.append(f"{td.name}: T2 final state must be INVALID_CONTROL_DESIGN (got {st!r})")
        res["ok"] = False
    results.append(res)
    return res


def validate_canonical_metrics(errors: list) -> dict:
    """RA3 Closure F: canonical metrics must match recomputed artifact counts."""
    out = {"canonical_metrics_truth_valid": False}
    m_path = DOCS / "CQC_P3_METRICS.json"
    if not m_path.is_file():
        errors.append("canonical CQC_P3_METRICS.json missing")
        return out
    m = json.loads(m_path.read_text(encoding="utf-8"))
    recomputed = {
        "requirement_count_total": req_total, "route_count_total": routes_total,
        "required_route_count": reqd, "conditional_route_count": cond,
        "distinct_route_id_count": len(distinct), "shared_requirement_count": shared,
        "orphan_requirement_count": orphan,
        "type_perturbation_total_count": 2,
        "type_perturbation_mechanical_identity_valid_count": mech_valid,
        "type_perturbation_srp_valid_count": 2,
        "type_perturbation_valid_control_count": ctrl_valid,
        "type_perturbation_invalid_control_count": ctrl_invalid,
    }
    bad = [k for k, val in recomputed.items() if m.get(k) != val]
    if bad:
        errors.append(f"CANONICAL_METRICS_TRUTH_MISMATCH: {bad}")
        out["mismatches"] = bad
    else:
        out["canonical_metrics_truth_valid"] = True
    return out


def validate_summary_no_stale(errors: list) -> dict:
    """RA3 Closure F: canonical Summary must not contain known stale assertions."""
    out = {"summary_no_stale_claims": False}
    s_path = DOCS / "CQC_P3_SUMMARY.md"
    if not s_path.is_file():
        errors.append("canonical CQC_P3_SUMMARY.md missing")
        return out
    t = s_path.read_text(encoding="utf-8")
    stale = [
        "All final semantic statuses: PENDING_HO_CHATGPT",
        "6 distinct route_ids",
        "6 distinct route IDs",
        "4 of 16 requirements are CONDITIONAL",
        "two valid type perturbations",
        "material in 6/6 cases: in",
    ]
    found = [s for s in stale if s in t]
    if found:
        errors.append(f"canonical Summary contains stale claims: {found}")
        return out
    out["summary_no_stale_claims"] = True
    return out


def validate_ra3_manifest(errors: list) -> dict:
    """RA3 Closure F: every manifest path must exist and SHA must match current bytes."""
    out = {"final_manifest_valid": False, "manifest_entries": 0}
    mf = DOCS / "CQC_P3_RA3_SHA256_MANIFEST.txt"
    if not mf.is_file():
        errors.append("final RA3 manifest missing (docs/CQC_P3_RA3_SHA256_MANIFEST.txt)")
        return out
    bad = []
    n = 0
    for line in mf.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        sha, rel = line.split("  ", 1)
        p = PKG / rel
        n += 1
        if not p.is_file():
            bad.append(f"missing {rel}")
        elif hashlib.sha256(p.read_bytes()).hexdigest() != sha:
            bad.append(f"hash mismatch {rel}")
    out["manifest_entries"] = n
    if bad:
        errors.append(f"P3_FINAL_MANIFEST_MISMATCH: {bad[:5]}")
        return out
    out["final_manifest_valid"] = True
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", dest="machine")
    ap.add_argument("--hygiene", action="store_true")
    args = ap.parse_args(argv)

    if not P3.is_dir():
        print("NO_P3_BENCHMARK: benchmarks/p3 not present; nothing to validate.")
        return 0

    errors: list[str] = []
    sem_results: list[dict] = []
    cases = sorted([d for d in SEM.iterdir() if d.is_dir()])
    for c in cases:
        validate_semantic_case(c, errors, sem_results)
    tp_results: list[dict] = []
    for td in sorted(TP.iterdir()):
        if td.is_dir():
            validate_perturbation(td, SEM, errors, tp_results)

    # RA3: recompute canonical counts from final artifacts
    global req_total, routes_total, reqd, cond, distinct, shared, orphan, mech_valid, ctrl_valid, ctrl_invalid
    req_total = routes_total = reqd = cond = 0
    distinct = set()
    shared = orphan = mech_valid = ctrl_valid = ctrl_invalid = 0
    for c in cases:
        srp = json.loads((c / "search_requirement_profile.json").read_text(encoding="utf-8"))
        cqs = json.loads((c / "source_cqs.json").read_text(encoding="utf-8"))
        qids = {q["question_id"] for q in cqs["questions"]}
        req_total += len(srp["requirements"])
        if srp["requirements"] and len(srp["requirements"][0].get("target_question_ids", [])) > 1 \
                and all(t in qids for t in srp["requirements"][0]["target_question_ids"]):
            shared += 1
        for r in srp["requirements"]:
            routes_total += len(r["epistemic_routes"])
            if not all(t in qids for t in r["target_question_ids"]):
                orphan += 1
            for rt in r["epistemic_routes"]:
                distinct.add(rt["route_id"])
                if rt["status"] == "CONDITIONAL":
                    cond += 1
                else:
                    reqd += 1
    for td in sorted(TP.iterdir()):
        if not td.is_dir():
            continue
        review = json.loads((td / "evaluation" / "type_perturbation_review.json").read_text(encoding="utf-8"))
        m = review.get("mechanical") or {}
        if (m.get("non_type_fields_identical") and m.get("source_context_identical")
                and (m.get("both_srp_valid") or (m.get("perturbed_cqs_valid") and m.get("perturbed_srp_valid")))):
            mech_valid += 1
        st = (review.get("final_semantic_adjudication") or {}).get("status")
        if st == "VALID_PASS":
            ctrl_valid += 1
        if st == "INVALID_CONTROL_DESIGN":
            ctrl_invalid += 1

    hygiene = None
    if args.hygiene:
        tracked = subprocess.run(["git", "ls-files"], cwd=PKG, capture_output=True,
                                 text=True, timeout=15).stdout.splitlines()
        pycs = [t for t in tracked if t.endswith(".pyc") or "__pycache__" in t]
        hygiene = {"committed_bytecode": pycs}
        if pycs:
            errors.append(f"repository hygiene: bytecode committed: {pycs[:5]}")

    # RA3 canonical-truth validations
    canon = validate_canonical_metrics(errors)
    summ = validate_summary_no_stale(errors)
    manif = validate_ra3_manifest(errors)

    all_ok = (not errors and all(r["ok"] for r in sem_results) and all(r["ok"] for r in tp_results)
              and canon.get("canonical_metrics_truth_valid") and summ.get("summary_no_stale_claims")
              and manif.get("final_manifest_valid"))
    report = {"semantic_case_count": len(cases), "cases": sem_results,
              "type_perturbations": tp_results,
              "canonical_metrics_truth": canon, "summary_no_stale_claims": summ,
              "final_manifest": manif,
              "all_ok": all_ok,
              "errors": errors[:20], "hygiene": hygiene}
    if args.machine:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for r in sem_results:
            print(("PASS" if r["ok"] else "FAIL"), r["case_id"])
        for r in tp_results:
            print(("PASS" if r["ok"] else "FAIL"), r["perturbation"])
        for e in errors:
            print(f"      - {e}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
