#!/usr/bin/env python
"""Derive evaluation/integration_review.json for each P5 case.

Per CQC-P5-RA1-CI1 contract (semantic-review provenance):

  - mechanical block: machine-derived facts (source-chain / route-join /
    conditional-non-activation / MAFS baseline / MAFS-native schema /
    stale-state / search-order-lineage-traceability).
  - local_claw_preliminary_review: Local Claw must read the actual
    artifacts and fill in. The script may generate the BLOCK with
    PENDING_LOCAL_CLAW placeholders but never auto-fill semantic
    verdicts.
  - final_semantic_adjudication: PENDING_HO_CHATGPT (CI1 must never
    self-sign PASS).

For planning cases (have mafs_planning.json), the script populates:
  - mechanical block (including search_order_lineage_traceable)
  - local_claw_preliminary_review with authored_by=LOCAL_CLAW,
    review_basis=[5 artifact paths], and the 5 semantic fields as
    PENDING_LOCAL_CLAW.
  - final_semantic_adjudication.status = PENDING_HO_CHATGPT
Local Claw must then read M1/M2/M3 and overwrite the PENDING values.

For contextual cases (no mafs_planning.json), the script populates:
  - mechanical block
  - local_claw_preliminary_review with planning-specific semantic
    fields = NOT_APPLICABLE.
  - final_semantic_adjudication.status = PENDING_HO_CHATGPT

No semantic classifier, embedding scorer, or LLM-as-validator runtime.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PKG / "integration" / "mafs_v3"))
sys.path.insert(0, str(PKG / "scripts"))

from adapter import (  # noqa: E402
    MAFS_BASELINE_SHA, detect_stale, verify_source_chain,
)
from mini_jsonschema import validate as mini_validate  # noqa: E402


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _route_status_map(srp: dict) -> dict:
    m = {}
    for r in srp["requirements"]:
        for rt in r["epistemic_routes"]:
            m[(r["requirement_id"], rt["route_id"])] = rt["status"]
    return m


def derive_mechanical(case_dir: Path, mafs_schemas_dir: Path | None,
                       has_planning: bool) -> dict:
    """Return the mechanical block for a single case.

    `has_planning` controls mafs_native_schema_valid: True only if the
    case carries mafs_planning.json. Contextual cases that lack
    mafs_planning.json still get a mechanical block but with
    mafs_native_schema_valid = False (the assertion "schema validity
    against the pinned MAFS schemas" is meaningless without a planning
    object to validate).
    """
    binding = json.loads((case_dir / "integration_binding.json").read_text(encoding="utf-8"))
    cqs = json.loads((case_dir / "source_cqs.json").read_text(encoding="utf-8"))
    srp = json.loads((case_dir / "source_srp.json").read_text(encoding="utf-8"))
    env = json.loads((case_dir / "budget_envelope.json").read_text(encoding="utf-8"))
    chain = binding.get("source_chain") or {}

    # 1) source-chain truth
    try:
        verify_source_chain(case_dir / "source_cqs.json",
                            case_dir / "source_srp.json",
                            case_dir / "budget_envelope.json")
        source_chain_valid = True
    except Exception:
        source_chain_valid = False

    # 2) allocation↔route join against SRP
    route_status = _route_status_map(srp)
    active = binding.get("active_routes") or []
    join_ok = True
    for a in active:
        key = (a["requirement_id"], a["route_id"])
        st = route_status.get(key)
        if st != "REQUIRED" or a.get("allocation_activation") != "COMMITTED":
            join_ok = False
            break
    allocation_route_join_valid = join_ok

    # 3) COMMITTED eligibility + CONDITIONAL non-activation
    held = binding.get("held_conditional_routes") or []
    conditional_non_activation_valid = all(
        a.get("allocation_activation") == "COMMITTED" for a in active
    ) and all(h.get("activation") == "RESERVE_CONDITIONAL" for h in held)

    # 4) MAFS baseline pin
    mb = binding.get("mafs_baseline") or {}
    mafs_baseline_valid = (
        mb.get("commit_sha") == MAFS_BASELINE_SHA
        and mb.get("repository") == "mo21cn/mafs-v3-p0"
    )

    # 5) MAFS-native schema validity (only meaningful for planning cases)
    if has_planning and mafs_schemas_dir is not None and mafs_schemas_dir.is_dir():
        try:
            axis_schema = json.loads((mafs_schemas_dir / "axis.schema.json").read_text(encoding="utf-8"))
            so_schema = json.loads((mafs_schemas_dir / "search_order.schema.json").read_text(encoding="utf-8"))
        except Exception:
            axis_schema = None
            so_schema = None
        mafs_native_schema_valid = False
        if axis_schema and so_schema:
            planning = json.loads((case_dir / "mafs_planning.json").read_text(encoding="utf-8"))
            for ax in planning.get("axes") or []:
                if mini_validate(ax, axis_schema):
                    mafs_native_schema_valid = False
                    break
            else:
                for so in planning.get("search_orders") or []:
                    if mini_validate(so, so_schema):
                        mafs_native_schema_valid = False
                        break
                else:
                    mafs_native_schema_valid = True
    else:
        # Contextual cases: no MAFS planning object exists; the
        # "validity against MAFS schemas" assertion does not apply.
        mafs_native_schema_valid = False

    # 6) stale-state detection
    stale_state_valid = (
        (binding.get("stale_state") == "STALE")
        == detect_stale(binding, case_dir / "source_cqs.json",
                         case_dir / "source_srp.json",
                         case_dir / "budget_envelope.json")
    )

    # 7) search-order lineage traceability (planning-only; for contextual
    #    cases it is a structural predicate, not a semantic one — it
    #    simply reports whether the binding has route_bindings that
    #    resolve to SRP routes).  If the case has no mafs_planning.json,
    #    the predicate is N/A structurally (no SearchOrder to trace).
    if has_planning:
        planning = json.loads((case_dir / "mafs_planning.json").read_text(encoding="utf-8"))
        active_keys = {(a["requirement_id"], a["route_id"]) for a in active}
        bound_sos = set()
        so_traced = True
        for rb in planning.get("route_bindings") or []:
            key = (rb.get("requirement_id"), rb.get("route_id"))
            if key not in active_keys:
                so_traced = False
                break
            for so_id in rb.get("mafs_search_order_ids") or []:
                bound_sos.add(so_id)
        for so in planning.get("search_orders") or []:
            if so.get("search_order_id") not in bound_sos:
                so_traced = False
                break
        search_order_lineage_traceable = so_traced
    else:
        search_order_lineage_traceable = False  # structurally N/A (no SO)

    return {
        "source_chain_valid": bool(source_chain_valid),
        "allocation_route_join_valid": bool(allocation_route_join_valid),
        "conditional_non_activation_valid": bool(conditional_non_activation_valid),
        "mafs_baseline_valid": bool(mafs_baseline_valid),
        "mafs_native_schema_valid": bool(mafs_native_schema_valid),
        "stale_state_valid": bool(stale_state_valid),
        "search_order_lineage_traceable": bool(search_order_lineage_traceable),
    }


def _build_planning_template(case_dir: Path) -> dict:
    """Local Claw preliminary review block for a PLANNING case, with
    semantic verdicts as PENDING_LOCAL_CLAW. Local Claw must fill after
    reading source_cqs.json / source_srp.json / budget_envelope.json /
    integration_binding.json / mafs_planning.json."""
    return {
        "authored_by": "LOCAL_CLAW",
        "review_basis": [
            "source_cqs.json",
            "source_srp.json",
            "budget_envelope.json",
            "integration_binding.json",
            "mafs_planning.json",
        ],
        "search_order_semantically_contained": "PENDING_LOCAL_CLAW",
        "authority_leak_observed": "PENDING_LOCAL_CLAW",
        "integration_projection_loss_observed": "PENDING_LOCAL_CLAW",
        "conditional_preactivation_observed": "PENDING_LOCAL_CLAW",
        "source_context_promoted_to_obligation": "PENDING_LOCAL_CLAW",
        "notes": "Local Claw must inspect M1/M2/M3 artifacts and replace the 5 PENDING_LOCAL_CLAW fields above with observed conclusions; final_semantic_adjudication must remain PENDING_HO_CHATGPT.",
    }


def _build_contextual_template(case_dir: Path) -> dict:
    """Local Claw preliminary review block for a CONTEXTUAL case. The
    planning-specific semantic fields are NOT_APPLICABLE (no MAFS
    planning object). Non-planning structural fields (e.g. source
    context accessibility) are machine-derivable; see mechanical block
    for the structural facts."""
    return {
        "authored_by": "MACHINE_DERIVED",
        "review_basis": [
            "source_cqs.json",
            "source_srp.json",
            "budget_envelope.json",
            "integration_binding.json",
        ],
        "search_order_semantically_contained": "NOT_APPLICABLE",
        "authority_leak_observed": "NOT_APPLICABLE",
        "integration_projection_loss_observed": "NOT_APPLICABLE",
        "conditional_preactivation_observed": "NOT_APPLICABLE",
        "source_context_promoted_to_obligation": "NOT_APPLICABLE",
        "notes": "Contextual case carries no MAFS-native planning object; planning-specific semantic fields are NOT_APPLICABLE. Source-chain identity, allocation-route join, and conditional non-activation are verified by the mechanical block.",
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", action="append", default=[])
    args = ap.parse_args(argv)

    p5 = PKG / "benchmarks" / "p5"
    mafs_schemas_dir = Path(os.environ.get(
        "MAFS_BASELINE_DIR", str(PKG.parent / "mafs-v3-p0"))) / "schemas"

    targets: list[Path] = []
    if args.case:
        for c in args.case:
            targets.append(p5 / c)
    else:
        for sub in (p5 / "mafs_planning", p5 / "contextual"):
            if sub.is_dir():
                for d in sorted(sub.iterdir()):
                    if d.is_dir():
                        targets.append(d)

    n_planning = 0
    n_contextual = 0
    for case_dir in targets:
        if not case_dir.is_dir():
            print(f"SKIP (not a directory): {case_dir}")
            continue
        eval_dir = case_dir / "evaluation"
        eval_dir.mkdir(parents=True, exist_ok=True)
        binding = json.loads((case_dir / "integration_binding.json").read_text(encoding="utf-8"))
        has_planning = (case_dir / "mafs_planning.json").is_file()
        mechanical = derive_mechanical(case_dir, mafs_schemas_dir, has_planning)
        if has_planning:
            preliminary = _build_planning_template(case_dir)
            n_planning += 1
        else:
            preliminary = _build_contextual_template(case_dir)
            n_contextual += 1
        review = {
            "case_id": binding.get("artifact_id", case_dir.name),
            "schema_version": "cqc-p5-integration-review.v0.2",
            "mechanical": mechanical,
            "local_claw_preliminary_review": preliminary,
            "final_semantic_adjudication": {
                "status": "PENDING_HO_CHATGPT"
            }
        }
        out = eval_dir / "integration_review.json"
        out.write_text(json.dumps(review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {out}")
    print(f"\n{n_planning} planning + {n_contextual} contextual = {n_planning + n_contextual} review files written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
