#!/usr/bin/env python
"""Generate docs/CQC_UPSTREAM_FREEZE_SHA256_MANIFEST.txt using canonical
Git bytes (per CQC-UPSTREAM-FREEZE-v0.1 §14).

Frozen CQC producer surface; no `generated from HEAD` field; no
self-hash loop (this manifest is intentionally not listed).
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
OUT = PKG / "docs" / "CQC_UPSTREAM_FREEZE_SHA256_MANIFEST.txt"


def git_blob_bytes(rel: str) -> bytes:
    blob_sha = subprocess.run(
        ["git", "ls-files", "-s", "--", rel],
        cwd=str(PKG), capture_output=True, text=True, check=True,
    ).stdout.strip().split()[1]
    return subprocess.run(
        ["git", "cat-file", "blob", blob_sha],
        cwd=str(PKG), capture_output=True, check=True,
    ).stdout


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main(argv=None) -> int:
    files: list[str] = [
        # Master contract (the artifact-protocol architecture source)
        "CQC_Master_Development_Contract_v0.1.md",
        "CQC_Master_Development_Contract_v0.2_Post_P1_Roadmap_Rebaseline.md",
        # P0..P5 canonical summaries
        "docs/CQC_P0_SUMMARY.md",
        "docs/CQC_P1_SUMMARY.md",
        "docs/CQC_P2_SUMMARY.md",
        "docs/CQC_P3_SUMMARY.md",
        "docs/CQC_P4_SUMMARY.md",
        "docs/CQC_P5_SUMMARY.md",
        # P0..P5 canonical metrics
        "docs/CQC_P0_METRICS.json",
        "docs/CQC_P1_METRICS.json",
        "docs/CQC_P2_METRICS.json",
        "docs/CQC_P3_METRICS.json",
        "docs/CQC_P4_METRICS.json",
        "docs/CQC_P5_METRICS.json",
        # P0..P5 canonical SHA256 manifests
        "docs/CQC_P0_SHA256_MANIFEST.txt",
        "docs/CQC_P1_SHA256_MANIFEST.txt",
        "docs/CQC_P2_SHA256_MANIFEST.txt",
        "docs/CQC_P3_SHA256_MANIFEST.txt",
        "docs/CQC_P4_SHA256_MANIFEST.txt",
        "docs/CQC_P5_SHA256_MANIFEST.txt",
        # Frozen artifact schemas
        "schemas/candidate_question_set.v0.1.schema.json",
        "schemas/search_requirement_profile.v0.1.schema.json",
        "schemas/budget_envelope.v0.1.schema.json",
        "schemas/cqc_mafs_integration_binding.v0.1.schema.json",
        # P5 adapter / validator / renderer
        "integration/mafs_v3/adapter.py",
        "integration/mafs_v3/validator.py",
        "integration/mafs_v3/render.py",
        # Upstream freeze artifacts (this script's own output excluded)
        "docs/CQC_UPSTREAM_FREEZE_SUMMARY.md",
        "docs/CQC_UPSTREAM_FREEZE_METRICS.json",
    ]

    entries: list[tuple[str, str]] = []
    for rel in files:
        p = PKG / rel
        if not p.exists():
            print(f"  MISSING: {rel}", file=sys.stderr)
            return 1
        canonical = git_blob_bytes(rel)
        entries.append((sha256_bytes(canonical), rel))

    lines = [
        "# CQC_UPSTREAM_FREEZE_SHA256_MANIFEST.txt - canonical Git-byte SHA-256",
        "# contract: CQC-UPSTREAM-FREEZE-v0.1 §14",
        "#",
        "# Stable inner provenance only:",
        "#   P4 source baseline: 8028e17a6eaab364c744cfa72b714f0f0bd6cf01",
        "#   pinned MAFS baseline: cd09699fc8cc160ab5cfff00a41e714961dd2109",
        "#",
        "# Git owns outer identity; this manifest does not encode HEAD.",
        "# Entries are SHA-256 over post-eol=lf-normalized Git blobs.",
        f"# total entries: {len(entries)}",
        "#",
    ]
    for sha, rel in entries:
        lines.append(f"{sha}  {rel}")
    # No self-hash loop: this file is intentionally not listed.
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(entries)} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
