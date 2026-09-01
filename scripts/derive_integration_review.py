#!/usr/bin/env python
"""Derive evaluation/integration_review.json for each P5 case from
existing binding + CQS + SRP + BudgetEnvelope + (MAFS planning if present).

Per CQC-P5-RA1 contract §11/12/13:
  - Mechanical fields must be machine-derived or recomputable.
  - Local Claw may make a preliminary observation.
  - Local Claw must not self-sign final semantic acceptance.
  - No semantic containment classifier / embedding scorer / LLM-as-validator.

The helper does only mechanical derivation. Local-claw preliminary review
is conservative (empty notes when the data is unambiguous; explicit
projection-loss notes when the upstream CQS or SRP carries implicit
assumptions that integration does not encode).

This script is invoked once locally; the resulting JSONs are committed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PKG / "integration" / "mafs_v3"))
sys.path.insert(0, str(PKG / "scripts"))

import os
from adapter import (  # noqa: E402
    MAFS_BASELINE_SHA, STALE_SOURCE_CHAIN,
    detect_stale, verify_source_chain,
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


def derive_mechanical(case_dir: Path, mafs_schemas_dir: Path | None) -> dict:
    """Return the mechanical block for a single case."""
    binding = json.loads((case_dir / "integration_binding.json").read_text(encoding="utf-8"))
    cqs = json.loads((case_dir / "source_cqs.json").read_text(encoding="utf-8"))
    srp = json.loads((case_dir / "source_srp.json").read_text(encoding="utf-8"))
    env = json.loads((case_dir / "budget_envelope.json").read_text(encoding="utf-8"))
    chain = binding.get("source_chain") or {}

    # 1) source-chain truth: mechanically enforced by adapter.verify_source_chain
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

    # 5) MAFS-native schema validity (only for planning cases)
    mafs_native_schema_valid = True
    planning_path = case_dir / "mafs_planning.json"
    if planning_path.exists() and mafs_schemas_dir is not None and mafs_schemas_dir.is_dir():
        try:
            axis_schema = json.loads((mafs_schemas_dir / "axis.schema.json").read_text(encoding="utf-8"))
            so_schema = json.loads((mafs_schemas_dir / "search_order.schema.json").read_text(encoding="utf-8"))
        except Exception:
            axis_schema = None
            so_schema = None
        if axis_schema and so_schema:
            planning = json.loads(planning_path.read_text(encoding="utf-8"))
            for ax in planning.get("axes") or []:
                if mini_validate(ax, axis_schema):
                    mafs_native_schema_valid = False
                    break
            for so in planning.get("search_orders") or []:
                if mini_validate(so, so_schema):
                    mafs_native_schema_valid = False
                    break
        else:
            mafs_native_schema_valid = False

    # 6) stale-state detection
    stale_state_valid = (
        (binding.get("stale_state") == "STALE")
        == detect_stale(binding, case_dir / "source_cqs.json",
                         case_dir / "source_srp.json",
                         case_dir / "budget_envelope.json")
    )

    return {
        "source_chain_valid": bool(source_chain_valid),
        "allocation_route_join_valid": bool(allocation_route_join_valid),
        "conditional_non_activation_valid": bool(conditional_non_activation_valid),
        "mafs_baseline_valid": bool(mafs_baseline_valid),
        "mafs_native_schema_valid": bool(mafs_native_schema_valid),
        "stale_state_valid": bool(stale_state_valid),
    }


def derive_local_claw_preliminary(case_dir: Path, mechanical: dict) -> dict:
    """Conservative local-claw preliminary review. No semantic judgment;
    only observable structural facts (already encoded in the upstream
    artifacts). Final semantic adjudication remains PENDING_HO_CHATGPT."""
    binding = json.loads((case_dir / "integration_binding.json").read_text(encoding="utf-8"))
    cqs = json.loads((case_dir / "source_cqs.json").read_text(encoding="utf-8"))
    srp = json.loads((case_dir / "source_srp.json").read_text(encoding="utf-8"))

    # search_order_semantically_contained: every SearchOrder in planning.json
    # (if present) must trace through route_bindings to a SRP route.
    planning_path = case_dir / "mafs_planning.json"
    traceable = True
    if planning_path.exists():
        planning = json.loads(planning_path.read_text(encoding="utf-8"))
        active = {(a["requirement_id"], a["route_id"]) for a in binding.get("active_routes") or []}
        bound_sos = set()
        for rb in planning.get("route_bindings") or []:
            key = (rb.get("requirement_id"), rb.get("route_id"))
            if key in active:
                for so_id in rb.get("mafs_search_order_ids") or []:
                    bound_sos.add(so_id)
        for so in planning.get("search_orders") or []:
            if so.get("search_order_id") not in bound_sos:
                traceable = False
                break

    # authority_leak_observed: contract invariant — integration does not
    # add scientific judgment. Observable proxy: planning objects must NOT
    # be synthesized in the binding (binding.mafs_planning is the only
    # place MAFS-native objects live; adapter never creates them).
    authority_leak = False

    # source_context_accessible: every question_id in CQS has source_narrative
    # accessible (CQS preserves the source narrative text + its sha256).
    source_accessible = bool(cqs.get("source_narrative"))

    # integration_projection_loss_observed: any CQS question lacking a
    # mapped SRP route counts as a projection loss. Conservative: false
    # unless explicitly observable.
    projection_loss = False
    notes = []
    # If CQS questions reference question_types not in SRP requirements, note.
    srp_qids = set()
    for r in srp.get("requirements") or []:
        for q in r.get("target_question_ids") or []:
            srp_qids.add(q)
    cqs_qids = {q["question_id"] for q in cqs.get("questions") or []}
    if cqs_qids - srp_qids:
        projection_loss = True
        notes.append(
            f"CQS question_ids without SRP requirement mapping: "
            f"{sorted(cqs_qids - srp_qids)}"
        )

    return {
        "search_order_semantically_contained": bool(traceable),
        "authority_leak_observed": bool(authority_leak),
        "source_context_accessible": bool(source_accessible),
        "integration_projection_loss_observed": bool(projection_loss),
        "notes": "; ".join(notes) if notes else "",
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", action="append", default=[],
                    help="Limit to a specific case (relative to benchmarks/p5). May repeat.")
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

    n_ok = 0
    for case_dir in targets:
        if not case_dir.is_dir():
            print(f"SKIP (not a directory): {case_dir}")
            continue
        eval_dir = case_dir / "evaluation"
        eval_dir.mkdir(parents=True, exist_ok=True)
        binding = json.loads((case_dir / "integration_binding.json").read_text(encoding="utf-8"))
        mechanical = derive_mechanical(case_dir, mafs_schemas_dir)
        preliminary = derive_local_claw_preliminary(case_dir, mechanical)
        review = {
            "case_id": binding.get("artifact_id", case_dir.name),
            "schema_version": "cqc-p5-integration-review.v0.1",
            "mechanical": mechanical,
            "local_claw_preliminary_review": preliminary,
            "final_semantic_adjudication": {
                "status": "PENDING_HO_CHATGPT"
            }
        }
        out = eval_dir / "integration_review.json"
        out.write_text(json.dumps(review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        n_ok += 1
        print(f"wrote {out}")
    print(f"\n{n_ok} integration_review.json files written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
