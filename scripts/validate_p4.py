#!/usr/bin/env python
"""CQC-P4 validator (contract CQC-P4-BUDGET-ENVELOPE-v0.1 sections 30-31).

Validates ONLY deterministic facts. Never judges semantic optimality.
Exit 0 iff all checks pass; 1 otherwise. Failure codes:
  P4_SOURCE_SRP_DRIFT          copied SRP != accepted P3 SRP bytes
  CANONICAL_METRICS_TRUTH_MISMATCH (inherited from validate_p3 when run there)
  BUDGET_ENVELOPE_INVALID      schema/accounting/reference failures
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_budget_envelope import render  # noqa: E402
from mini_jsonschema import validate as mini_validate  # noqa: E402

PKG = Path(__file__).resolve().parents[1]
P4 = PKG / "benchmarks" / "p4"
CTX = P4 / "contextual"
DOCS = PKG / "docs"
PERT = P4 / "budget_perturbation"
SCHEMA = PKG / "schemas" / "budget_envelope.v0.1.schema.json"
SRP_SCHEMA = PKG / "schemas" / "search_requirement_profile.v0.1.schema.json"

PKG_REQUIRED = {
    "source_srp.json", "budget_intent.json", "budget_envelope.json",
    "human_render.md", "evaluation/budget_review.json",
    "evaluation/allocation_admission.json",
}
_counts: dict = {}

LEAK_TERMS = ["crossref", "pubmed", "google scholar", "api endpoint", "top-k",
              "http request", "query string", "provider fallback", "resolver call"]


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha256_text(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def load_schema(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def accounting(envelope: dict, srp: dict) -> list[str]:
    errs: list[str] = []
    te = envelope["total_envelope"]
    wc_t, wc_c = te["wall_clock"]["target_minutes"], te["wall_clock"]["hard_ceiling_minutes"]
    mt_t, mt_c = te["model_tokens"]["target_tokens"], te["model_tokens"]["hard_ceiling_tokens"]
    if not wc_c >= wc_t:
        errs.append(f"hard_ceiling_minutes {wc_c} < target {wc_t}")
    if not mt_c >= mt_t:
        errs.append(f"hard_ceiling_tokens {mt_c} < target {mt_t}")

    req_routes = {}  # requirement_id -> {route_id: (activation | None, srp_status)}
    for r in srp["requirements"]:
        for rt in r["epistemic_routes"]:
            req_routes.setdefault(r["requirement_id"], {})[rt["route_id"]] = rt["status"]

    committed_wc = committed_tok = total_wc = total_tok = 0
    funded_required = set()
    seen_alloc_ids = set()
    seen_routes = set()
    for a in envelope["allocations"]:
        aid, rid, route = a["allocation_id"], a["requirement_id"], a["route_id"]
        if aid in seen_alloc_ids:
            errs.append(f"duplicate allocation_id {aid}")
        seen_alloc_ids.add(aid)
        if rid not in req_routes:
            errs.append(f"{aid}: requirement_id {rid} does not exist in source SRP")
            continue
        if route not in req_routes[rid]:
            errs.append(f"{aid}: route {route} does not belong to requirement {rid}")
            continue
        key = (rid, route)
        if key in seen_routes:
            errs.append(f"{aid}: duplicate allocation for route {rid}/{route}")
        seen_routes.add(key)
        act = a["activation"]
        srp_status = req_routes[rid][route]
        if act == "COMMITTED":
            committed_wc += a["wall_clock_target_minutes"]
            committed_tok += a["model_token_target"]
            total_wc += a["wall_clock_target_minutes"]
            total_tok += a["model_token_target"]
            if srp_status != "REQUIRED":
                errs.append(f"{aid}: COMMITTED allocation on non-REQUIRED route {rid}/{route} (SRP status {srp_status}) — CONDITIONAL routes may not be pre-activated")
            else:
                funded_required.add(key)
                if key in funded_required and sum(1 for x in envelope["allocations"]
                                                  if x["requirement_id"] == rid and x["route_id"] == route) > 1:
                    pass
        elif act == "RESERVE_CONDITIONAL":
            total_wc += a["wall_clock_target_minutes"]
            total_tok += a["model_token_target"]
            if srp_status != "CONDITIONAL":
                errs.append(f"{aid}: RESERVE_CONDITIONAL allocation on non-CONDITIONAL route {rid}/{route} (SRP status {srp_status})")
        else:
            errs.append(f"{aid}: illegal activation {act}")

    # REQUIRED routes fully funded exactly once; REQUIRED routes explicitly listed as
    # unfunded in an INSUFFICIENT envelope are exempt (contract section 31).
    declared_unfunded = {(u["requirement_id"], u["route_id"])
                         for u in (envelope.get("feasibility") or {}).get("unfunded_obligations") or []}
    for rid, routes in req_routes.items():
        for route, status in routes.items():
            if status == "REQUIRED" and (rid, route) not in funded_required \
                    and (rid, route) not in declared_unfunded:
                errs.append(f"REQUIRED route {rid}/{route} has no COMMITTED allocation (silently omitted)")

    if committed_wc > wc_t:
        errs.append(f"COMMITTED wall-clock sum {committed_wc} > target {wc_t}")
    if committed_tok > mt_t:
        errs.append(f"COMMITTED token sum {committed_tok} > target {mt_t}")
    if total_wc > wc_c:
        errs.append(f"total wall-clock sum {total_wc} > hard ceiling {wc_c}")
    if total_tok > mt_c:
        errs.append(f"total token sum {total_tok} > hard ceiling {mt_c}")
    return errs


def feasibility_consistency(envelope: dict, srp: dict) -> list[str]:
    errs: list[str] = []
    f = envelope["feasibility"]
    status = f["status"]
    te = envelope["total_envelope"]
    wc_c = te["wall_clock"]["hard_ceiling_minutes"]
    mt_c = te["model_tokens"]["hard_ceiling_tokens"]
    req_routes = set()
    for r in srp["requirements"]:
        for rt in r["epistemic_routes"]:
            if rt["status"] == "REQUIRED":
                req_routes.add((r["requirement_id"], rt["route_id"]))
    funded = {(a["requirement_id"], a["route_id"]) for a in envelope["allocations"]
              if a["activation"] == "COMMITTED"}
    unfunded_required = req_routes - funded
    listed = {(u["requirement_id"], u["route_id"]) for u in f["unfunded_obligations"]}

    if status == "FEASIBLE":
        if unfunded_required:
            errs.append(f"FEASIBLE but unfunded REQUIRED routes exist: {sorted(unfunded_required)}")
        if f["unfunded_obligations"]:
            errs.append("FEASIBLE but unfunded_obligations list is non-empty")
    elif status == "INSUFFICIENT":
        if not listed:
            errs.append("INSUFFICIENT without identifiable unfunded REQUIRED obligation")
        for u in list(f["unfunded_obligations"]):
            key = (u["requirement_id"], u["route_id"])
            if key not in req_routes:
                errs.append(f"unfunded obligation {key} is not a REQUIRED route of this SRP")
        missing_listing = unfunded_required - listed
        if missing_listing:
            errs.append(f"INSUFFICIENT but unlisted unfunded REQUIRED routes: {sorted(missing_listing)}")
    if status == "CONSTRAINED":
        if unfunded_required:
            errs.append(f"CONSTRAINED but unfunded REQUIRED routes exist: {sorted(unfunded_required)}")
    # ceiling sanity for INSUFFICIENT: deficit must be plausible (committed <= ceiling)
    committed = sum(a["wall_clock_target_minutes"] for a in envelope["allocations"]
                    if a["activation"] == "COMMITTED")
    if committed > wc_c and status != "INSUFFICIENT":
        errs.append(f"COMMITTED exceeds hard ceiling but status is {status}")
    return errs


def shared_requirement_check(envelope: dict, srp: dict) -> list[str]:
    """RA1 subtractive fix (contract section 12): dedup is route-based.
    A shared requirement (target_question_ids > 1) may legitimately carry multiple
    allocations IF they target different epistemic routes. The only forbidden thing
    is duplicating the same (requirement_id, route_id) merely because question
    cardinality multiplied. Same-(req,route) dedup is already enforced in accounting()."""
    errs: list[str] = []
    for r in srp["requirements"]:
        if len(r["target_question_ids"]) > 1:
            allocs = [a for a in envelope["allocations"] if a["requirement_id"] == r["requirement_id"]]
            route_ids = [a["route_id"] for a in allocs]
            if len(route_ids) != len(set(route_ids)):
                errs.append(f"shared requirement {r['requirement_id']} has duplicate allocations for the same route (question-cardinality duplication)")
    return errs


def validate_package(case: Path, base_srp_bytes: bytes, errors: list, results: list) -> dict:
    res = {"case_id": case.name, "ok": True, "checks": {}}
    missing = [f for f in PKG_REQUIRED if not (case / f).is_file()]
    if missing:
        errors.append(f"{case.name}: missing {missing}")
        res["ok"] = False
        results.append(res)
        return res
    res["checks"]["package_complete"] = True

    meta = json.loads((case / "budget_intent.json").read_text(encoding="utf-8"))
    srp_bytes = (case / "source_srp.json").read_bytes()
    srp = json.loads(srp_bytes.decode("utf-8"))
    env = json.loads((case / "budget_envelope.json").read_text(encoding="utf-8"))
    intent = meta

    # P4_SOURCE_SRP_DRIFT
    res["checks"]["source_srp_binding_valid"] = (
        srp_bytes == base_srp_bytes
        and srp.get("artifact_id") == env.get("source_srp_id")
        and sha256_file(case / "source_srp.json") == env.get("source_srp_sha256") == env.get("source_srp_sha256")
        and env.get("source_srp_id") == srp.get("artifact_id"))
    if not res["checks"]["source_srp_binding_valid"]:
        errors.append(f"{case.name}: P4_SOURCE_SRP_DRIFT or binding mismatch")
        res["ok"] = False

    sp_errs = mini_validate(srp, load_schema(SRP_SCHEMA))
    res["checks"]["srp_schema_valid"] = not sp_errs
    if sp_errs:
        errors.append(f"{case.name}: source SRP schema errors: {sp_errs[:3]}")
        res["ok"] = False

    be_errs = mini_validate(env, load_schema(SCHEMA))
    res["checks"]["budget_envelope_schema_valid"] = not be_errs
    if be_errs:
        errors.append(f"{case.name}: BudgetEnvelope schema errors: {be_errs[:4]}")
        res["ok"] = False

    res["checks"]["budget_intent_valid"] = (
        intent.get("mode") == env["budget_intent"]["mode"]
        and intent.get("operator_goal") == env["budget_intent"]["operator_goal"])

    acc_errs = accounting(env, srp)
    res["checks"]["allocation_refs_valid"] = not any("does not exist" in e or "does not belong" in e for e in acc_errs)
    res["checks"]["required_routes_funded"] = not any("no COMMITTED allocation" in e for e in acc_errs)
    res["checks"]["conditional_routes_not_preactivated"] = not any("pre-activated" in e or "non-REQUIRED route" in e for e in acc_errs)
    res["checks"]["target_accounting_valid"] = not any("target" in e and "ceiling" not in e for e in acc_errs)
    res["checks"]["ceiling_accounting_valid"] = not any("hard ceiling" in e for e in acc_errs)
    if acc_errs:
        errors.append(f"{case.name}: accounting errors: {acc_errs[:5]}")
        res["ok"] = False

    dup = shared_requirement_check(env, srp)
    res["checks"]["shared_requirement_not_duplicated"] = not dup
    if dup:
        errors.append(f"{case.name}: shared requirement double-budgeted: {dup[:3]}")
        res["ok"] = False

    feas_errs = feasibility_consistency(env, srp)
    res["checks"]["feasibility_structural_consistency"] = not feas_errs
    if feas_errs:
        errors.append(f"{case.name}: feasibility inconsistency: {feas_errs[:3]}")
        res["ok"] = False

    blob = json.dumps(env["allocations"], ensure_ascii=False).lower()
    leak = [t for t in LEAK_TERMS if t in blob]
    res["checks"]["no_provider_query_fields"] = not leak
    if leak:
        errors.append(f"{case.name}: provider/query leakage: {leak}")
        res["ok"] = False

    res["checks"]["render_reproducible"] = render(env) == (case / "human_render.md").read_text(encoding="utf-8")
    if not res["checks"]["render_reproducible"]:
        errors.append(f"{case.name}: human_render.md not reproducible")
        res["ok"] = False

    # RA1: review-truth enforcement — review identity/hash/mechanical fields must match actual artifacts
    review_ok = True
    srp_sha_actual = hashlib.sha256(srp_bytes).hexdigest()
    env_sha_actual = hashlib.sha256((case / "budget_envelope.json").read_bytes()).hexdigest()
    br = json.loads((case / "evaluation" / "budget_review.json").read_text(encoding="utf-8"))
    if br.get("source_srp_id") != srp.get("artifact_id") or br.get("source_srp_sha256") != srp_sha_actual:
        errors.append(f"{case.name}: P4_REVIEW_BINDING_MISMATCH (source_srp identity/sha)")
        review_ok = False
    if br.get("budget_envelope_id") != env.get("artifact_id") or br.get("budget_envelope_sha256") != env_sha_actual:
        errors.append(f"{case.name}: P4_REVIEW_BINDING_MISMATCH (budget_envelope identity/sha)")
        review_ok = False
    recomputed_mech = {
        "schema_valid": res["checks"].get("budget_envelope_schema_valid", False),
        "source_binding_valid": res["checks"].get("source_srp_binding_valid", False),
        "allocation_refs_valid": res["checks"].get("allocation_refs_valid", False),
        "required_routes_funded": res["checks"].get("required_routes_funded", False),
        "conditional_routes_not_preactivated": res["checks"].get("conditional_routes_not_preactivated", False),
        "target_accounting_valid": res["checks"].get("target_accounting_valid", False),
        "ceiling_accounting_valid": res["checks"].get("ceiling_accounting_valid", False),
        "shared_requirement_not_duplicated": res["checks"].get("shared_requirement_not_duplicated", False),
        "render_valid": res["checks"].get("render_reproducible", False),
    }
    stated = br.get("mechanical") or {}
    for k, actual in recomputed_mech.items():
        if bool(stated.get(k)) != bool(actual):
            errors.append(f"{case.name}: budget_review.mechanical.{k}={stated.get(k)} but recomputed truth={bool(actual)} (P4_REVIEW_MACHINE_TRUTH_MISMATCH)")
            review_ok = False
    hash_binding_ok = (br.get("source_srp_sha256") == hashlib.sha256((case / "source_srp.json").read_bytes()).hexdigest()
                       and br.get("budget_envelope_sha256") == env_sha_actual)
    res["checks"]["review_hash_valid"] = hash_binding_ok
    res["checks"]["review_machine_truth_valid"] = all(
        bool(stated.get(k)) == bool(actual) for k, actual in recomputed_mech.items())
    res["checks"]["review_truth_valid"] = review_ok
    if not review_ok:
        res["ok"] = False

    fa = (br.get("final_semantic_adjudication") or {}).get("status")
    if fa != "PENDING_HO_CHATGPT":
        errors.append(f"{case.name}: budget_review final status must remain PENDING_HO_CHATGPT at P4-RA1")
        res["ok"] = False

    results.append(res)
    return res


def validate_perturbation(td: Path, base_case: str, base_srp_bytes: bytes, expected_mode: str,
                          expected_feasibility: set, errors: list, results: list) -> dict:
    res = {"perturbation": td.name, "ok": True, "checks": {}}
    required = ["source_srp.json", "budget_intent.json", "budget_envelope.json",
                "human_render.md", "evaluation/budget_review.json"]
    missing = [f for f in required if not (td / f).is_file()]
    if missing:
        errors.append(f"{td.name}: missing {missing}")
        res["ok"] = False
        results.append(res)
        return res
    srp_bytes = (td / "source_srp.json").read_bytes()
    env = json.loads((td / "budget_envelope.json").read_text(encoding="utf-8"))
    intent = json.loads((td / "budget_intent.json").read_text(encoding="utf-8"))
    srp = json.loads(srp_bytes.decode("utf-8"))

    res["checks"]["source_srp_identity_valid"] = (
        srp_bytes == base_srp_bytes and env.get("source_srp_sha256") == hashlib.sha256(srp_bytes).hexdigest())
    if not res["checks"]["source_srp_identity_valid"]:
        errors.append(f"{td.name}: source SRP identity drift from P3 accepted bytes")
        res["ok"] = False
    res["checks"]["intent_mode"] = intent.get("mode")
    if intent.get("mode") != expected_mode:
        errors.append(f"{td.name}: expected mode {expected_mode}, got {intent.get('mode')}")
        res["ok"] = False
    res["checks"]["feasibility_status"] = env["feasibility"]["status"]
    if env["feasibility"]["status"] not in expected_feasibility:
        errors.append(f"{td.name}: feasibility {env['feasibility']['status']} not in expected {expected_feasibility}")
        res["ok"] = False
    acc_errs = accounting(env, srp)
    res["checks"]["accounting_valid"] = not acc_errs
    if acc_errs:
        errors.append(f"{td.name}: accounting errors: {acc_errs[:5]}")
        res["ok"] = False
    res["checks"]["render_reproducible"] = render(env) == (td / "human_render.md").read_text(encoding="utf-8")
    if not res["checks"]["render_reproducible"]:
        errors.append(f"{td.name}: human_render.md not reproducible")
        res["ok"] = False
    br = json.loads((td / "evaluation" / "budget_review.json").read_text(encoding="utf-8"))
    if (br.get("final_semantic_adjudication") or {}).get("status") != "PENDING_HO_CHATGPT":
        errors.append(f"{td.name}: budget_review final status must remain PENDING_HO_CHATGPT at P4")
        res["ok"] = False
    results.append(res)
    return res


def validate_canonical_metrics(errors: list) -> dict:
    """RA1 section 19: canonical metrics must match recomputed truth."""
    out = {"canonical_metrics_truth_valid": False}
    m_path = DOCS / "CQC_P4_METRICS.json"
    if not m_path.is_file():
        errors.append("canonical CQC_P4_METRICS.json missing")
        return out
    m = json.loads(m_path.read_text(encoding="utf-8"))
    recomputed = {
        "contextual_case_count": 6,
        "budget_envelope_schema_valid_count": _counts.get("budget_envelope_schema_valid"),
        "source_srp_binding_valid_count": _counts.get("source_srp_binding_valid"),
        "allocation_ref_valid_count": _counts.get("allocation_refs_valid"),
        "required_route_funding_valid_count": _counts.get("required_routes_funded"),
        "conditional_non_preactivation_valid_count": _counts.get("conditional_routes_not_preactivated"),
        "target_accounting_valid_count": _counts.get("target_accounting_valid"),
        "ceiling_accounting_valid_count": _counts.get("ceiling_accounting_valid"),
        "shared_requirement_dedup_valid_count": _counts.get("shared_requirement_not_duplicated"),
        "deterministic_render_valid_count": _counts.get("render_reproducible"),
        "contextual_review_hash_valid_count": _counts.get("review_hash_valid"),
        "contextual_review_machine_truth_valid_count": _counts.get("review_machine_truth_valid"),
        "total_allocation_count": _counts.get("total_allocation_count"),
        "committed_allocation_count": _counts.get("committed_allocation_count"),
        "conditional_reserve_allocation_count": _counts.get("conditional_reserve_allocation_count"),
        "feasible_case_count": _counts.get("feasible_case_count"),
        "constrained_case_count": _counts.get("constrained_case_count"),
        "insufficient_case_count": _counts.get("insufficient_case_count"),
    }
    bad = [k for k, val in recomputed.items() if m.get(k) != val]
    if bad:
        errors.append(f"P4_CANONICAL_METRICS_TRUTH_MISMATCH: {bad}")
        out["mismatches"] = bad
    else:
        out["canonical_metrics_truth_valid"] = True
    return out


def validate_final_manifest(errors: list) -> dict:
    """RA1 section 18: every manifest entry path must exist and SHA must match current bytes."""
    out = {"final_manifest_valid": False, "manifest_entries": 0}
    mf = DOCS / "CQC_P4_SHA256_MANIFEST.txt"
    if not mf.is_file():
        errors.append("final P4 manifest missing (docs/CQC_P4_SHA256_MANIFEST.txt)")
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
        errors.append(f"P4_FINAL_MANIFEST_MISMATCH: {bad[:5]}")
        return out
    out["final_manifest_valid"] = True
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", dest="machine")
    ap.add_argument("--hygiene", action="store_true")
    args = ap.parse_args(argv)

    if not P4.is_dir():
        print("NO_P4_BENCHMARK: benchmarks/p4 not present; nothing to validate.")
        return 0

    errors: list[str] = []
    results: list[dict] = []
    cases = sorted([d for d in CTX.iterdir() if d.is_dir()])
    for c in cases:
        validate_package(c, (PKG / "benchmarks" / "p3" / "contextual" / c.name / "search_requirement_profile.json").read_bytes(),
                         errors, results)

    pert_results: list[dict] = []
    pert_specs = [
        ("quick_constraint_s5", "s5_mixed_commitment", "QUICK", {"INSUFFICIENT", "CONSTRAINED"}),
        ("deep_expansion_s5", "s5_mixed_commitment", "DEEP", {"FEASIBLE"}),
    ]
    for td_name, base, mode, feas in pert_specs:
        td = PERT / td_name
        if td.is_dir():
            validate_perturbation(td, base, (PKG / "benchmarks" / "p3" / "contextual" / base / "search_requirement_profile.json").read_bytes(),
                                  mode, feas, errors, pert_results)

    # intent invariance
    inv = PERT / "intent_invariance_s5" / "comparison.json"
    inv_ok = False
    if inv.is_file():
        d = json.loads(inv.read_text(encoding="utf-8"))
        inv_ok = (len(d["compared_envelopes"]) == 3
                  and len({e["source_srp_sha256"] for e in d["compared_envelopes"]}) == 1
                  and len({e["mode"] for e in d["compared_envelopes"]}) == 3)
        if not inv_ok:
            errors.append("intent invariance comparison invalid")
    else:
        errors.append("intent_invariance_s5/comparison.json missing")

    hygiene = None
    if args.hygiene:
        tracked = subprocess.run(["git", "ls-files"], cwd=PKG, capture_output=True,
                                 text=True, timeout=15).stdout.splitlines()
        pycs = [t for t in tracked if t.endswith(".pyc") or "__pycache__" in t]
        hygiene = {"committed_bytecode": pycs}
        if pycs:
            errors.append(f"repository hygiene: bytecode committed: {pycs[:5]}")

    def count(key: str) -> int:
        return sum(1 for r in results + pert_results if r["checks"].get(key))

    # RA1: allocation/feasibility counts from final envelopes
    total_alloc = committed_alloc = reserve_alloc = 0
    feas = {"FEASIBLE": 0, "CONSTRAINED": 0, "INSUFFICIENT": 0}
    for c in cases:
        env = json.loads((c / "budget_envelope.json").read_text(encoding="utf-8"))
        for a in env["allocations"]:
            total_alloc += 1
            if a["activation"] == "COMMITTED":
                committed_alloc += 1
            else:
                reserve_alloc += 1
        feas[env["feasibility"]["status"]] += 1
    for td in sorted(PERT.iterdir()):
        if td.is_dir() and (td / "budget_envelope.json").is_file():
            env = json.loads((td / "budget_envelope.json").read_text(encoding="utf-8"))
            feas[env["feasibility"]["status"]] += 1

    # RA1 canonical-truth validations
    global _counts
    _counts = {
        "budget_envelope_schema_valid": count("budget_envelope_schema_valid"),
        "source_srp_binding_valid": count("source_srp_binding_valid"),
        "allocation_refs_valid": count("allocation_refs_valid"),
        "required_routes_funded": count("required_routes_funded"),
        "conditional_routes_not_preactivated": count("conditional_routes_not_preactivated"),
        "target_accounting_valid": count("target_accounting_valid"),
        "ceiling_accounting_valid": count("ceiling_accounting_valid"),
        "shared_requirement_not_duplicated": count("shared_requirement_not_duplicated"),
        "render_reproducible": sum(1 for r in results if r["checks"].get("render_reproducible")),
        "review_hash_valid": sum(1 for r in results if r["checks"].get("review_hash_valid")),
        "review_machine_truth_valid": sum(1 for r in results if r["checks"].get("review_machine_truth_valid")),
        "total_allocation_count": total_alloc,
        "committed_allocation_count": committed_alloc,
        "conditional_reserve_allocation_count": reserve_alloc,
        "feasible_case_count": feas["FEASIBLE"],
        "constrained_case_count": feas["CONSTRAINED"],
        "insufficient_case_count": feas["INSUFFICIENT"],
    }
    canon = validate_canonical_metrics(errors)
    manif = validate_final_manifest(errors)

    all_ok = (not errors and all(r["ok"] for r in results) and all(r["ok"] for r in pert_results) and inv_ok
              and canon.get("canonical_metrics_truth_valid") and manif.get("final_manifest_valid"))
    report = {"contextual_case_count": len(cases), "cases": results,
              "type_perturbations": pert_results, "intent_invariance_valid": inv_ok,
              "canonical_metrics_truth": canon, "final_manifest": manif,
              "all_ok": all_ok, "errors": errors[:20], "hygiene": hygiene}
    if args.machine:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for r in results:
            print(("PASS" if r["ok"] else "FAIL"), r["case_id"])
        for r in pert_results:
            print(("PASS" if r["ok"] else "FAIL"), r["perturbation"])
        print("intent invariance:", "PASS" if inv_ok else "FAIL")
        for e in errors:
            print(f"      - {e}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
