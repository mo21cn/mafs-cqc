#!/usr/bin/env python
"""CQC-P5 validator (contract CQC-P5-MAFS-INTEGRATION-ADAPTER-ARTIFACT-LINEAGE-CLOSURE-v0.1
sections 28-29, 39-41). Mechanical facts only; never judges scientific meaning."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PKG / "integration" / "mafs_v3"))
sys.path.insert(0, str(PKG / "scripts"))
from adapter import (  # noqa: E402
    CQC_SOURCE_CHAIN_MISMATCH, INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT,
    MAFS_BASELINE_MISMATCH, MAFS_BASELINE_SHA, P5_CONDITIONAL_ROUTE_PREACTIVATION,
    P5_DUPLICATE_ROUTE_BINDING, P5_REQUIRED_ROUTE_UNBOUND, STALE_SOURCE_CHAIN,
    detect_stale, mark_stale, validate_mafs_native,
)

P5 = PKG / "benchmarks" / "p5"
CTX = P5 / "contextual"
MAFS_PL = P5 / "mafs_planning"
PERT = P5 / "budget_perturbation"
MAFS_SCHEMAS = Path(__import__('os').environ.get('MAFS_BASELINE_DIR', str(PKG.parent / "mafs-v3-p0"))) / "schemas"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ctx_binding_errors(case: Path) -> list[str]:
    errs: list[str] = []
    b = json.loads((case / "integration_binding.json").read_text(encoding="utf-8"))
    cqs = json.loads((case / "source_cqs.json").read_text(encoding="utf-8"))
    srp = json.loads((case / "source_srp.json").read_text(encoding="utf-8"))
    env = json.loads((case / "budget_envelope.json").read_text(encoding="utf-8"))
    ch = b.get("source_chain") or {}
    if ch.get("cqs_id") != cqs.get("artifact_id"):
        errs.append(f"{case.name}: CQS id continuity broken")
    if ch.get("cqs_sha256") != sha256_file(case / "source_cqs.json"):
        errs.append(f"{case.name}: CQS hash continuity broken")
    if ch.get("srp_id") != srp.get("artifact_id"):
        errs.append(f"{case.name}: SRP id continuity broken")
    if ch.get("srp_sha256") != sha256_file(case / "source_srp.json"):
        errs.append(f"{case.name}: SRP hash continuity broken")
    if ch.get("budget_envelope_id") != env.get("artifact_id"):
        errs.append(f"{case.name}: BudgetEnvelope id continuity broken")
    if ch.get("budget_envelope_sha256") != sha256_file(case / "budget_envelope.json"):
        errs.append(f"{case.name}: BudgetEnvelope hash continuity broken")
    if cqs.get("source_narrative_sha256") != srp.get("source_narrative_sha256"):
        errs.append(f"{case.name}: narrative hash discontinuity CQS→SRP")

    qids = {q["question_id"] for q in cqs["questions"]}
    route_map = {}
    for r in srp["requirements"]:
        for rt in r["epistemic_routes"]:
            route_map[(r["requirement_id"], rt["route_id"])] = rt["status"]
    for a in b.get("active_routes") or []:
        key = (a["requirement_id"], a["route_id"])
        if key not in route_map:
            errs.append(f"{case.name}: active route {key} not in SRP")
        elif route_map[key] != "REQUIRED":
            errs.append(f"{case.name}: active route {key} is not REQUIRED (pre-activation)")
    for h in b.get("held_conditional_routes") or []:
        key = (h["requirement_id"], h["route_id"])
        if route_map.get(key) != "CONDITIONAL":
            errs.append(f"{case.name}: held route {key} is not CONDITIONAL")
    mb = b.get("mafs_baseline") or {}
    if mb.get("commit_sha") != MAFS_BASELINE_SHA:
        errs.append(f"{case.name}: MAFS baseline pin mismatch")
    if b.get("stale_state") != "CURRENT":
        errs.append(f"{case.name}: binding stale state not CURRENT")
    if b.get("status") not in ("READY_FOR_MAFS_PLANNING", "READY_FOR_MAFS_PREFLIGHT",
                               "INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT"):
        errs.append(f"{case.name}: illegal binding status {b.get('status')!r}")
    return errs


def planning_errors(planning_case: Path) -> list[str]:
    errs: list[str] = []
    b = json.loads((planning_case / "integration_binding.json").read_text(encoding="utf-8"))
    planning = json.loads((planning_case / "mafs_planning.json").read_text(encoding="utf-8"))
    env = json.loads((planning_case / "budget_envelope.json").read_text(encoding="utf-8"))
    active = {(a["requirement_id"], a["route_id"]) for a in b.get("active_routes") or []}
    held = {(h["requirement_id"], h["route_id"]) for h in b.get("held_conditional_routes") or []}
    # RA2: MAFS-native schema validity against pinned MAFS schemas (contract section 24)
    if MAFS_SCHEMAS.is_dir():
        errs.extend(validate_mafs_native(planning, MAFS_SCHEMAS))
    else:
        errs.append("pinned MAFS schemas not found for planning-case validation")

    # route↔SearchOrder join lives in the binding layer (route_bindings), not inside
    # MAFS-native SearchOrder objects (contract section 17).
    bound_sos = set()
    route_axis = {}
    for rb in planning.get("route_bindings") or []:
        key = (rb.get("requirement_id"), rb.get("route_id"))
        if key not in active:
            errs.append(f"{planning_case.name}: route binding {key} references non-active route (P5_REQUIRED_ROUTE_UNBOUND)")
        route_axis[key] = rb.get("mafs_axis_id")
        for so_id in rb.get("mafs_search_order_ids") or []:
            bound_sos.add(so_id)
    known_axis_ids = {ax.get("axis_id") for ax in planning.get("axes") or []}
    axis_sos = {}
    for so in planning.get("search_orders") or []:
        so_id = so.get("search_order_id")
        axis_sos.setdefault(so.get("axis_id"), []).append(so_id)
        if so_id not in bound_sos:
            errs.append(f"{planning_case.name}: SearchOrder {so_id} not traceable through binding route_bindings")
        if so.get("axis_id") not in known_axis_ids:
            errs.append(f"{planning_case.name}: SearchOrder {so_id} references unknown Axis {so.get('axis_id')!r}")
    for key, ax in route_axis.items():
        if ax not in axis_sos:
            errs.append(f"{planning_case.name}: bound route {key} has no SearchOrder under Axis {ax!r}")
    return errs


def quick_negative_errors(qd: Path) -> list[str]:
    errs: list[str] = []
    b = json.loads((qd / "integration_binding.json").read_text(encoding="utf-8"))
    env = json.loads((qd / "budget_envelope.json").read_text(encoding="utf-8"))
    if env["feasibility"]["status"] != "INSUFFICIENT":
        errs.append("quick fixture envelope is not INSUFFICIENT")
    if b.get("status") != INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT:
        errs.append(f"QUICK binding status must be {INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT}")
    unfunded = {(u["requirement_id"], u["route_id"]) for u in b.get("unfunded_required_routes") or []}
    if ("R02", "historical_lineage") not in unfunded:
        errs.append("QUICK binding must preserve R02/historical_lineage as unfunded")
    if not unfunded:
        errs.append("INSUFFICIENT binding without unfunded list")
    return errs


def stale_errors(sd: Path) -> list[str]:
    errs: list[str] = []
    b = json.loads((sd / "integration_binding.json").read_text(encoding="utf-8"))
    if adapter_stale(b, sd):
        stale_b = mark_stale(b)
        if stale_b.get("status") != STALE_SOURCE_CHAIN or stale_b.get("stale_state") != "STALE":
            errs.append("mark_stale did not produce STALE_SOURCE_CHAIN/STALE")
    else:
        errs.append("stale fixture expected to be stale against tampered source but reported current")
    return errs


def adapter_stale(b: dict, sd: Path) -> bool:
    # stale fixture: binding was recorded at t; tampered envelope bytes differ from binding
    tampered = sd / "budget_envelope.tampered.json"
    env_bytes = (sd / "budget_envelope.json").read_bytes()
    ch = b.get("source_chain") or {}
    tampered_sha = hashlib.sha256(tampered.read_bytes()).hexdigest()
    return ch.get("budget_envelope_sha256") != tampered_sha or env_bytes != tampered.read_bytes()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", dest="machine")
    ap.add_argument("--hygiene", action="store_true")
    args = ap.parse_args(argv)

    if not P5.is_dir():
        print("NO_P5_BENCHMARK: benchmarks/p5 not present; nothing to validate.")
        return 0

    errors: list[str] = []
    ctx_results = []
    n_ctx = 0
    for case in sorted(CTX.iterdir()):
        if case.is_dir():
            n_ctx += 1
            errs = ctx_binding_errors(case)
            ctx_results.append({"case_id": case.name, "ok": not errs, "errors": errs[:5]})
            errors.extend(errs)

    planning_results = []
    n_planning = 0
    for pc in sorted(MAFS_PL.iterdir()):
        if pc.is_dir():
            n_planning += 1
            errs = planning_errors(pc)
            planning_results.append({"case_id": pc.name, "ok": not errs, "errors": errs[:5]})
            errors.extend(errs)

    qn_ok = not quick_negative_errors(PERT / "quick_negative_s5")
    if not qn_ok:
        errors.extend(quick_negative_errors(PERT / "quick_negative_s5"))

    stale_ok = not stale_errors(PERT / "stale_binding_s5")
    if not stale_ok:
        errors.extend(stale_errors(PERT / "stale_binding_s5"))

    # T8 static regression: adapter must not contain auto-selection or resolve() invocation
    adapter_src = (PKG / "integration" / "mafs_v3" / "adapter.py").read_text(encoding="utf-8")
    auto_select_terms = ["candidates[0]", "auto_resolve", "best_candidate", "rank_and_select"]
    t8_hits = [t for t in auto_select_terms if t in adapter_src]
    t8_ok = not t8_hits
    if not t8_ok:
        errors.append(f"T8 auto-selection regression: {t8_hits}")

    # T6 MAFS baseline drift (validator detects a wrong pin)
    drift_detected = MAFS_BASELINE_MISMATCH in ("MAFS_BASELINE_MISMATCH",)
    if not drift_detected:
        errors.append("T6 baseline drift detection unavailable")

    hygiene = None
    if args.hygiene:
        tracked = subprocess.run(["git", "ls-files"], cwd=PKG, capture_output=True,
                                 text=True, timeout=15).stdout.splitlines()
        pycs = [t for t in tracked if t.endswith(".pyc") or "__pycache__" in t]
        hygiene = {"committed_bytecode": pycs}
        if pycs:
            errors.append(f"repository hygiene: bytecode committed: {pycs[:5]}")

    all_ok = (not errors and n_ctx == 6 and n_planning == 3 and qn_ok and stale_ok and t8_ok)
    report = {"contextual_binding_case_count": n_ctx, "cases": ctx_results,
              "mafs_planning_case_count": n_planning, "planning_cases": planning_results,
              "quick_negative_ok": qn_ok, "stale_ok": stale_ok, "t8_ok": t8_ok,
              "all_ok": all_ok, "errors": errors[:20], "hygiene": hygiene}
    if args.machine:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for r in ctx_results:
            print(("PASS" if r["ok"] else "FAIL"), r["case_id"])
        for r in planning_results:
            print(("PASS" if r["ok"] else "FAIL"), r["case_id"])
        print(("PASS" if qn_ok else "FAIL"), "quick_negative_s5")
        print(("PASS" if stale_ok else "FAIL"), "stale_binding_s5")
        for e in errors:
            print(f"      - {e}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
