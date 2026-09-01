"""CQC→MAFS integration adapter (contract CQC-P5 section 6).

Owns ONLY: identity/hash continuity, allocation→SRP route join, COMMITTED vs
RESERVE accounting, unfunded-REQUIRED detection, MAFS baseline pin, caller-supplied
Axis/SearchOrder shape validation, route→MAFS-object lineage, stale detection.

Owns NOT: scientific relevance, query concepts, axis family by heuristic,
operation type from question_type, provider selection from route label, candidate
selection, resolution. No auto-selection, no resolve() invocation.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

MAFS_BASELINE_REPO = "mo21cn/mafs-v3-p0"
MAFS_BASELINE_SHA = "cd09699fc8cc160ab5cfff00a41e714961dd2109"
MAFS_BASELINE_INTERFACE = "MAFS v3.0-P1.5-RA3 closed execution-boundary state"

CQC_SOURCE_CHAIN_MISMATCH = "CQC_SOURCE_CHAIN_MISMATCH"
P5_CONDITIONAL_ROUTE_PREACTIVATION = "P5_CONDITIONAL_ROUTE_PREACTIVATION"
P5_REQUIRED_ROUTE_UNBOUND = "P5_REQUIRED_ROUTE_UNBOUND"
P5_DUPLICATE_ROUTE_BINDING = "P5_DUPLICATE_ROUTE_BINDING"
MAFS_BASELINE_MISMATCH = "MAFS_BASELINE_MISMATCH"
STALE_SOURCE_CHAIN = "STALE_SOURCE_CHAIN"
INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT = "INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


class P5Error(Exception):
    """Fail-closed integration error carrying a stable code."""

    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


@dataclass
class IntegrationResult:
    binding: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)
    code: str = "OK"


def verify_source_chain(cqs_path: Path, srp_path: Path, envelope_path: Path) -> None:
    """Contract section 11: full upstream continuity, mechanically verified."""
    cqs = json.loads(cqs_path.read_text(encoding="utf-8"))
    srp = json.loads(srp_path.read_text(encoding="utf-8"))
    env = json.loads(envelope_path.read_text(encoding="utf-8"))
    cqs_sha = sha256_file(cqs_path)
    srp_sha = sha256_file(srp_path)
    env_sha = sha256_file(envelope_path)

    checks = [
        (srp.get("source_cqs_id") == cqs.get("artifact_id"),
         "SRP.source_cqs_id != CQS.artifact_id"),
        (srp.get("source_cqs_sha256") == cqs_sha,
         "SRP.source_cqs_sha256 != SHA256(CQS)"),
        (env.get("source_srp_id") == srp.get("artifact_id"),
         "BudgetEnvelope.source_srp_id != SRP.artifact_id"),
        (env.get("source_srp_sha256") == srp_sha,
         "BudgetEnvelope.source_srp_sha256 != SHA256(SRP)"),
        (srp.get("source_narrative_sha256") == cqs.get("source_narrative_sha256"),
         "source narrative hash discontinuity between CQS and SRP"),
    ]
    failed = [d for ok, d in checks if not ok]
    if failed:
        raise P5Error(CQC_SOURCE_CHAIN_MISMATCH, "; ".join(failed))


def _route_status_map(srp: dict) -> dict:
    m = {}
    for r in srp["requirements"]:
        for rt in r["epistemic_routes"]:
            m[(r["requirement_id"], rt["route_id"])] = rt["status"]
    return m


def build_binding(*, case_id: str, cqs_path: Path, srp_path: Path, envelope_path: Path,
                  mafs_baseline_sha: str = MAFS_BASELINE_SHA,
                  caller_planning: dict | None = None) -> IntegrationResult:
    """Contract sections 11-15: bind the chain, classify routes, validate caller planning."""
    res = IntegrationResult()
    try:
        verify_source_chain(cqs_path, srp_path, envelope_path)
    except P5Error as e:
        res.code = e.code
        res.errors.append(e.detail)
        return res

    srp = json.loads(srp_path.read_text(encoding="utf-8"))
    env = json.loads(envelope_path.read_text(encoding="utf-8"))
    cqs = json.loads(cqs_path.read_text(encoding="utf-8"))

    if mafs_baseline_sha != MAFS_BASELINE_SHA:
        res.code = MAFS_BASELINE_MISMATCH
        res.errors.append(f"pinned baseline {MAFS_BASELINE_SHA}, got {mafs_baseline_sha}")
        return res

    route_status = _route_status_map(srp)
    unfunded = []
    for u in env["feasibility"].get("unfunded_obligations") or []:
        unfunded.append({"requirement_id": u["requirement_id"],
                         "route_id": u["route_id"], "reason": u["reason"]})

    # classify allocations
    active, held = [], []
    for a in env["allocations"]:
        key = (a["requirement_id"], a["route_id"])
        st = route_status.get(key)
        if st is None:
            res.code = CQC_SOURCE_CHAIN_MISMATCH
            res.errors.append(f"allocation {a['allocation_id']} references non-SRP route {key}")
            return res
        if a["activation"] == "COMMITTED":
            if st != "REQUIRED":
                res.code = P5_CONDITIONAL_ROUTE_PREACTIVATION
                res.errors.append(f"{a['allocation_id']}: COMMITTED on CONDITIONAL route {key}")
                return res
            active.append({"requirement_id": a["requirement_id"], "route_id": a["route_id"],
                           "allocation_id": a["allocation_id"], "allocation_activation": "COMMITTED",
                           "mafs_axis_id": None, "mafs_search_order_ids": []})
        elif a["activation"] == "RESERVE_CONDITIONAL":
            if st != "CONDITIONAL":
                res.code = CQC_SOURCE_CHAIN_MISMATCH
                res.errors.append(f"{a['allocation_id']}: RESERVE on non-CONDITIONAL route {key}")
                return res
            held.append({"requirement_id": a["requirement_id"], "route_id": a["route_id"],
                         "allocation_id": a["allocation_id"], "activation": "RESERVE_CONDITIONAL"})

    # REQUIRED routes must be active (unless explicitly unfunded in an INSUFFICIENT envelope)
    declared_unfunded = {(u["requirement_id"], u["route_id"]) for u in unfunded}
    active_keys = {(r["requirement_id"], r["route_id"]) for r in active}
    for (rid, route), st in route_status.items():
        if st == "REQUIRED" and (rid, route) not in active_keys and (rid, route) not in declared_unfunded:
            res.code = P5_REQUIRED_ROUTE_UNBOUND
            res.errors.append(f"REQUIRED route {rid}/{route} has no COMMITTED allocation and is not declared unfunded")
            return res

    # duplicate route binding detection
    if len(active_keys) != len(active):
        res.code = P5_DUPLICATE_ROUTE_BINDING
        res.errors.append("duplicate (requirement_id, route_id) in active routes")
        return res

    # caller planning: validate lineage refs (contract sections 15-17)
    planning = caller_planning or {"axes": [], "search_orders": [], "route_bindings": []}
    route_to_axis = {}
    for rb in planning.get("route_bindings", []):
        key = (rb.get("requirement_id"), rb.get("route_id"))
        if key not in active_keys:
            res.code = CQC_SOURCE_CHAIN_MISMATCH
            res.errors.append(f"caller planning references non-active route {key}")
            return res
        if key in route_to_axis:
            res.code = P5_DUPLICATE_ROUTE_BINDING
            res.errors.append(f"caller planning duplicates route {key}")
            return res
        route_to_axis[key] = rb

    for r in active:
        rb = route_to_axis.get((r["requirement_id"], r["route_id"]))
        if rb:
            r["mafs_axis_id"] = rb.get("mafs_axis_id")
            r["mafs_search_order_ids"] = rb.get("mafs_search_order_ids", [])

    # held conditional routes must never claim MAFS executable lineage (contract section 13)
    held_ids = {(h["requirement_id"], h["route_id"]) for h in held}
    for so in planning.get("search_orders", []):
        src_route = (so.get("source_requirement_id"), so.get("source_route_id"))
        if src_route in held_ids:
            res.code = P5_CONDITIONAL_ROUTE_PREACTIVATION
            res.errors.append(f"SearchOrder {so.get('search_order_id')} claims lineage to held conditional route {src_route}")
            return res

    status = READY if env["feasibility"]["status"] == "FEASIBLE" else INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT
    binding = {
        "artifact_id": f"BIND-{case_id}",
        "schema_version": "0.1",
        "source_chain": {
            "cqs_id": cqs["artifact_id"], "cqs_sha256": sha256_file(cqs_path),
            "srp_id": srp["artifact_id"], "srp_sha256": sha256_file(srp_path),
            "budget_envelope_id": env["artifact_id"], "budget_envelope_sha256": sha256_file(envelope_path),
        },
        "mafs_baseline": {"repository": MAFS_BASELINE_REPO, "commit_sha": mafs_baseline_sha,
                          "interface_state": MAFS_BASELINE_INTERFACE},
        "active_routes": active,
        "held_conditional_routes": held,
        "unfunded_required_routes": unfunded,
        "status": status,
        "stale_state": "CURRENT",
    }
    res.binding = binding
    res.code = "OK" if status != INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT else INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT
    return res


READY = "READY_FOR_MAFS_PREFLIGHT"


def detect_stale(binding: dict, cqs_path: Path, srp_path: Path, envelope_path: Path) -> bool:
    """Contract section 22: any upstream source change makes dependent binding stale."""
    try:
        chain = binding["source_chain"]
        if sha256_file(cqs_path) != chain["cqs_sha256"]:
            return True
        if sha256_file(srp_path) != chain["srp_sha256"]:
            return True
        if sha256_file(envelope_path) != chain["budget_envelope_sha256"]:
            return True
    except (KeyError, FileNotFoundError):
        return True
    return False


def mark_stale(binding: dict) -> dict:
    b = json.loads(json.dumps(binding))
    b["status"] = STALE_SOURCE_CHAIN
    b["stale_state"] = "STALE"
    return b


# ---- MAFS-native schema/construct compatibility (contract section 24) ----
def validate_mafs_native(planning: dict, mafs_schemas_dir: Path) -> list:
    """Validate caller-authored MAFS Axis/SearchOrder objects against the pinned
    MAFS schemas. Returns list of errors (empty == valid)."""
    from mini_jsonschema import validate as mini_validate

    errors = []
    axis_schema = json.loads((mafs_schemas_dir / "axis.schema.json").read_text(encoding="utf-8"))
    so_schema = json.loads((mafs_schemas_dir / "search_order.schema.json").read_text(encoding="utf-8"))
    for ax in planning.get("axes", []):
        errs = mini_validate(ax, axis_schema)
        if errs:
            errors.append(f"Axis {ax.get('axis_id')}: {errs[:3]}")
    for so in planning.get("search_orders", []):
        errs = mini_validate(so, so_schema)
        if errs:
            errors.append(f"SearchOrder {so.get('search_order_id')}: {errs[:3]}")
    return errors
