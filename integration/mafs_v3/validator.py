"""CQC→MAFS integration binding validator (contract CQC-P5 sections 28-29).
Mechanical facts only. Never judges scientific meaning."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

sys_dir = Path(__file__).resolve().parent
if str(sys_dir) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(sys_dir))

from adapter import (  # noqa: E402
    MAFS_BASELINE_SHA, detect_stale,
)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_binding(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def validate_binding_file(binding_path: Path, cqs_path: Path, srp_path: Path,
                          envelope_path: Path, mafs_schemas_dir: Path | None = None) -> tuple[dict, list[str]]:
    """Mechanically validate a binding against its upstream sources.

    Returns (report, errors). Never judges scientific meaning.
    """
    errors: list[str] = []
    b = json.loads(binding_path.read_text(encoding="utf-8"))
    report = {"binding_id": b.get("artifact_id"), "checks": {}, "ok": True}

    def chk(key: str, val: bool):
        report["checks"][key] = bool(val)
        if not val:
            errors.append(f"{binding_path.parent.parent.name}: {key} FAILED")
        return val

    # schema shape: minimal structural validation (avoid schema lib dependency here)
    required_top = {"artifact_id", "schema_version", "source_chain", "mafs_baseline",
                    "active_routes", "held_conditional_routes", "unfunded_required_routes",
                    "status", "stale_state"}
    chk("top_level_shape", required_top.issubset(set(b.keys())))

    chain = b.get("source_chain") or {}
    cqs = json.loads(cqs_path.read_text(encoding="utf-8"))
    srp = json.loads(srp_path.read_text(encoding="utf-8"))
    env = json.loads(envelope_path.read_text(encoding="utf-8"))

    chk("cqs_id_continuity", chain.get("cqs_id") == cqs.get("artifact_id"))
    chk("cqs_hash_continuity", chain.get("cqs_sha256") == sha256_file(cqs_path))
    chk("srp_id_continuity", chain.get("srp_id") == srp.get("artifact_id"))
    chk("srp_hash_continuity", chain.get("srp_sha256") == sha256_file(srp_path))
    chk("budget_id_continuity", chain.get("budget_envelope_id") == env.get("artifact_id"))
    chk("budget_hash_continuity", chain.get("budget_envelope_sha256") == sha256_file(envelope_path))
    chk("narrative_hash_continuity",
        chain.get("cqs_sha256") == cqs.get("source_narrative_sha256")
        and cqs.get("source_narrative_sha256") == srp.get("source_narrative_sha256"))

    # allocation→route join against the SRP
    route_status = {}
    for r in srp["requirements"]:
        for rt in r["epistemic_routes"]:
            route_status[(r["requirement_id"], rt["route_id"])] = rt["status"]
    join_ok = True
    for a in active_routes_items(b):
        key = (a["requirement_id"], a["route_id"])
        st = route_status.get(key)
        if st != "REQUIRED" or a.get("allocation_activation") != "COMMITTED":
            join_ok = False
    chk("allocation_route_join_valid", join_ok)

    # COMMITTED eligibility + CONDITIONAL non-activation
    chk("only_committed_routes_active",
        all(a.get("allocation_activation") == "COMMITTED" for a in active_routes_items(b)))
    held = held_routes_items(b)
    chk("conditional_non_activation_valid",
        all(h.get("activation") == "RESERVE_CONDITIONAL" for h in held))

    # unfunded REQUIRED truth
    unfunded = unfunded_items(b)
    insuff = b.get("status") == "INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT"
    unfunded_keys = {(u["requirement_id"], u["route_id"]) for u in unfunded}
    unfunded_required_in_srp = {(rid, rt) for (rid, rt), st in route_status.items()
                                if st == "REQUIRED"} - {
        (a["requirement_id"], a["route_id"]) for a in active_routes_items(b)}
    chk("budget_insufficiency_truth_valid",
        (not insuff) or (bool(unfunded_keys) and unfunded_keys <= unfunded_required_in_srp))

    # MAFS baseline pin
    mb = b.get("mafs_baseline") or {}
    chk("mafs_baseline_valid", mb.get("commit_sha") == MAFS_BASELINE_SHA
        and mb.get("repository") == "mo21cn/mafs-v3-p0")

    # stale detection against actual bytes
    chk("stale_detection_valid",
        (b.get("stale_state") == "STALE") == detect_stale(b, cqs_path, srp_path, envelope_path))

    # Axis/SearchOrder schema validity (if caller planning artifacts are referenced)
    if mafs_schemas_dir is not None:
        axis_schema = json.loads((mafs_schemas_dir / "axis.schema.json").read_text(encoding="utf-8"))
        so_schema = json.loads((mafs_schemas_dir / "search_order.schema.json").read_text(encoding="utf-8"))
        from mini_jsonschema import validate as mv
        schema_ok = True
        for ax in mafs_planning_items(b).get("axes", []):
            if mv(ax, axis_schema):
                schema_ok = False
        for so in mafs_planning_items(b).get("search_orders", []):
            if mv(so, so_schema):
                schema_ok = False
        chk("mafs_native_schema_valid", schema_ok)

    report["ok"] = not errors
    return report, errors


def active_routes_items(b: dict) -> list:
    return b.get("active_routes") or []


def held_routes_items(b: dict) -> list:
    return b.get("held_conditional_routes") or []


def unfunded_items(b: dict) -> list:
    return b.get("unfunded_required_routes") or []


def mafs_planning_items(b: dict) -> dict:
    return b.get("mafs_planning") or {}
