#!/usr/bin/env python
"""CQC-P3 deterministic human-readable renderer for SearchRequirementProfile v0.1.

Structural labels only; no model interpretation. Byte-deterministic (binary write).
Usage: python scripts/render_srp.py <srp.json> [-o out.md]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def render(artifact: dict) -> str:
    lines: list[str] = []
    lines.append(f"# SearchRequirementProfile: {artifact['artifact_id']}")
    lines.append("")
    lines.append(f"- schema_version: {artifact['schema_version']}")
    lines.append(f"- source_cqs_id: {artifact['source_cqs_id']}")
    lines.append(f"- source_cqs_sha256: {artifact['source_cqs_sha256']}")
    lines.append(f"- source_narrative_sha256: {artifact['source_narrative_sha256']}")
    lines.append(f"- requirements: {len(artifact['requirements'])}")
    lines.append("")
    lines.append("## Source Narrative (verbatim)")
    lines.append("")
    lines.append(artifact["source_narrative"].rstrip("\n"))
    lines.append("")
    lines.append("## Requirements")
    lines.append("")
    for r in artifact["requirements"]:
        lines.append(f"### {r['requirement_id']}")
        lines.append("")
        lines.append(f"- target_question_ids: {', '.join(r['target_question_ids'])}")
        lines.append(f"- evidence_need: {r['evidence_need']}")
        lines.append("- epistemic routes:")
        for route in r["epistemic_routes"]:
            lines.append(f"  - {route['route_id']} [{route['status']}] — {route['purpose']}")
            lines.append(f"    condition: {route['condition']}")
        lines.append(f"- source_requirements: {', '.join(r['source_requirements'])}")
        lines.append(f"- stopping_condition: {r['stopping_condition']}")
        lines.append(f"- uncertainty_binding: {r['uncertainty_binding']}")
        lines.append("")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Deterministic human-readable rendering of an SRP")
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
