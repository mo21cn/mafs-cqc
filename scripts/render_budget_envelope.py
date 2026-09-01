#!/usr/bin/env python
"""CQC-P4 deterministic human-readable renderer for BudgetEnvelope v0.1.
Structural labels only; byte-deterministic (binary write).
Usage: python scripts/render_budget_envelope.py <envelope.json> [-o out.md]"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def render(artifact: dict) -> str:
    lines: list[str] = []
    lines.append(f"# BudgetEnvelope: {artifact['artifact_id']}")
    lines.append("")
    lines.append(f"- schema_version: {artifact['schema_version']}")
    lines.append(f"- source_srp_id: {artifact['source_srp_id']}")
    lines.append(f"- source_srp_sha256: {artifact['source_srp_sha256']}")
    bi = artifact["budget_intent"]
    lines.append(f"- budget mode: {bi['mode']} ({bi['operator_goal']})")
    te = artifact["total_envelope"]
    wc, mt = te["wall_clock"], te["model_tokens"]
    lines.append(f"- wall_clock target/ceiling: {wc['target_minutes']} / {wc['hard_ceiling_minutes']} minutes")
    lines.append(f"- model_tokens target/ceiling: {mt['target_tokens']} / {mt['hard_ceiling_tokens']}")
    lines.append("")
    lines.append("## Allocations")
    lines.append("")
    for a in artifact["allocations"]:
        lines.append(f"### {a['allocation_id']}")
        lines.append("")
        lines.append(f"- requirement_id: {a['requirement_id']}")
        lines.append(f"- route_id: {a['route_id']} [{a['activation']}]")
        lines.append(f"- wall_clock_target_minutes: {a['wall_clock_target_minutes']}")
        lines.append(f"- model_token_target: {a['model_token_target']}")
        lines.append(f"- rationale: {a['rationale']}")
        lines.append("")
    lines.append("## Escalation Policy")
    lines.append("")
    for t in artifact["escalation_policy"]["triggers"]:
        lines.append(f"- trigger: {t['trigger']} -> action: {t['action']}")
    lines.append("")
    lines.append("## Feasibility")
    lines.append("")
    f = artifact["feasibility"]
    lines.append(f"- status: {f['status']}")
    if f["unfunded_obligations"]:
        for u in f["unfunded_obligations"]:
            lines.append(f"- unfunded: {u['requirement_id']} / {u['route_id']} — {u['reason']}")
    else:
        lines.append("- unfunded: (none)")
    lines.append(f"- constraint_note: {f['constraint_note']}")
    lines.append("")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Deterministic human-readable rendering of a BudgetEnvelope")
    ap.add_argument("artifact", type=Path)
    ap.add_argument("-o", "--output", type=Path, default=None)
    args = ap.parse_args(argv)

    if not args.artifact.is_file():
        print(f"MISSING_FILE: {args.artifact}", file=sys.stderr)
        return 1
    try:
        artifact = json.loads(args.artifact.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"INVALID_JSON: {args.artifact}: {e}", file=sys.stderr)
        return 1

    text = render(artifact)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(text.encode("utf-8"))
    else:
        sys.stdout.buffer.write(text.encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
