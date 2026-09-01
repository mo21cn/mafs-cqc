"""CQC→MAFS integration binding renderer (contract CQC-P5 section 30).
Identity/hashes/routes/stale-state only; no scientific summary generation."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def render(b: dict) -> str:
    L = []
    L.append(f"# CQC→MAFS Integration Binding: {b['artifact_id']}")
    L.append("")
    L.append(f"- schema_version: {b['schema_version']}")
    L.append(f"- status: {b['status']}")
    L.append(f"- stale_state: {b['stale_state']}")
    sc = b["source_chain"]
    L.append(f"- CQS: {sc['cqs_id']} ({sc['cqs_sha256'][:12]}…)")
    L.append(f"- SRP: {sc['srp_id']} ({sc['srp_sha256'][:12]}…)")
    L.append(f"- BudgetEnvelope: {sc['budget_envelope_id']} ({sc['budget_envelope_sha256'][:12]}…)")
    mb = b["mafs_baseline"]
    L.append(f"- MAFS baseline: {mb['repository']} @ {mb['commit_sha'][:12]}… ({mb['interface_state']})")
    L.append("")
    L.append("## Active Route Bindings")
    L.append("")
    for a in b["active_routes"]:
        axis = a.get("mafs_axis_id") or "(no MAFS Axis bound)"
        sos = ", ".join(a.get("mafs_search_order_ids") or []) or "(no SearchOrder)"
        L.append(f"- {a['requirement_id']}/{a['route_id']} ← {a['allocation_id']} [COMMITTED] → Axis {axis}, SearchOrders: {sos}")
    if not b["active_routes"]:
        L.append("- (none)")
    L.append("")
    L.append("## Held Conditional Routes")
    L.append("")
    for h in b["held_conditional_routes"]:
        L.append(f"- {h['requirement_id']}/{h['route_id']} ← {h['allocation_id']} [RESERVE_CONDITIONAL — held, not executable]")
    if not b["held_conditional_routes"]:
        L.append("- (none)")
    L.append("")
    L.append("## Unfunded Required Routes")
    L.append("")
    for u in b["unfunded_required_routes"]:
        L.append(f"- {u['requirement_id']}/{u['route_id']} — {u['reason']}")
    if not b["unfunded_required_routes"]:
        L.append("- (none)")
    L.append("")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: render.py <binding.json>", file=sys.stderr)
        sys.exit(1)
    b = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    sys.stdout.buffer.write(render(b).encode("utf-8"))
