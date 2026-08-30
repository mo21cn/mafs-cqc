#!/usr/bin/env python
"""CQC-P0 deterministic human-readable renderer.

Contract CQC-P0-MINIMAL-DIGESTION-SURFACE-v0.1 section 12.
Renders a CandidateQuestionSet from JSON only. Adds structural labels,
never model interpretation. Output is byte-deterministic (no timestamps).
JSON remains the machine source of truth.

Usage:
  python scripts/render_cqs.py <artifact.json> [-o out.md]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def render(artifact: dict) -> str:
    lines: list[str] = []
    lines.append(f"# CandidateQuestionSet: {artifact['artifact_id']}")
    lines.append("")
    lines.append(f"- schema_version: {artifact['schema_version']}")
    lines.append(f"- source_narrative_sha256: {artifact['source_narrative_sha256']}")
    lines.append(f"- questions: {len(artifact['questions'])}")
    lines.append("")
    lines.append("## Source Narrative (verbatim)")
    lines.append("")
    lines.append(artifact["source_narrative"].rstrip("\n"))
    lines.append("")
    lines.append("## Questions")
    lines.append("")
    for q in artifact["questions"]:
        lines.append(f"### {q['question_id']}")
        lines.append("")
        lines.append(f"- type: {q['question_type']}")
        lines.append(f"- statement: {q['statement']}")
        lines.append("- source trace:")
        for tr in q["source_trace"]:
            lines.append(f'  - "{tr["exact_quote"]}"')
        deps = q.get("dependencies") or []
        lines.append(f"- dependencies: {', '.join(deps) if deps else '(none)'}")
        lines.append(f"- resolution condition: {q['resolution_condition']}")
        unc = q.get("uncertainty")
        lines.append(f"- uncertainty: {unc if unc else '(none)'}")
        lines.append("")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Deterministic human-readable rendering of a CandidateQuestionSet")
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
        args.output.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
