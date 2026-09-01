#!/usr/bin/env python
"""Generate docs/CQC_P5_SHA256_MANIFEST.txt using canonical Git bytes
(per CQC-P5-RA1 contract §18).

For each listed file:
  - resolve the Git blob hash via `git ls-files -s <path>` (the index hash
    is the canonical blob hash after `.gitattributes` eol=lf normalization);
  - read the canonical bytes via `git cat-file blob <hash>`;
  - compute SHA-256 over the canonical bytes;
  - emit `<sha256>  <path>`.

The manifest deliberately omits its own path (no self-hash loop) and
omits any file the contract does not require. Coverage enforcement is
done in validate_p5 via a "mandatory closure surface" check.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
OUT = PKG / "docs" / "CQC_P5_SHA256_MANIFEST.txt"


def git_blob_hash(p: Path) -> str:
    """Return the Git blob hash (SHA-1) for the file at path p."""
    out = subprocess.run(
        ["git", "ls-files", "-s", "--", str(p)],
        cwd=str(PKG), capture_output=True, text=True, check=True,
    ).stdout.strip()
    # format: "<mode> <hash> <stage>\t<path>"
    return out.split()[1]


def git_blob_bytes(blob_sha: str) -> bytes:
    out = subprocess.run(
        ["git", "cat-file", "blob", blob_sha],
        cwd=str(PKG), capture_output=True, check=True,
    )
    return out.stdout


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main(argv=None) -> int:
    files: list[str] = [
        ".github/workflows/cqc-p5.yml",
        "integration/mafs_v3/adapter.py",
        "integration/mafs_v3/validator.py",
        "integration/mafs_v3/render.py",
        "schemas/cqc_mafs_integration_binding.v0.1.schema.json",
        "scripts/validate_p5.py",
        "scripts/derive_integration_review.py",
        "scripts/generate_p5_manifest.py",
        "tests/test_p5.py",
        "docs/CQC_P5_SUMMARY.md",
        "docs/CQC_P5_METRICS.json",
    ]
    # 6 contextual × 5 files
    for case in ("s1_vms_cellular_mechanism", "s2_vcell_paradigm", "s3_antagonist_domains",
                 "s4_avca_donor_data", "s5_mixed_commitment", "s6_narrow_source_check"):
        for f in ("integration_binding.json", "source_cqs.json", "source_srp.json",
                  "budget_envelope.json", "evaluation/integration_review.json"):
            files.append(f"benchmarks/p5/contextual/{case}/{f}")
    # 3 mafs_planning × 6 files
    for case in ("m1_s4_shared", "m2_s6_instability", "m3_s5_standard"):
        for f in ("integration_binding.json", "source_cqs.json", "source_srp.json",
                  "budget_envelope.json", "mafs_planning.json",
                  "evaluation/integration_review.json"):
            files.append(f"benchmarks/p5/mafs_planning/{case}/{f}")
    # 2 budget_perturbation
    for case in ("quick_negative_s5", "stale_binding_s5"):
        for f in ("integration_binding.json", "source_cqs.json", "source_srp.json",
                  "budget_envelope.json"):
            files.append(f"benchmarks/p5/budget_perturbation/{case}/{f}")
    # stale fixture includes a tampered envelope
    files.append("benchmarks/p5/budget_perturbation/stale_binding_s5/budget_envelope.tampered.json")

    # Compute the SHA-256 of the canonical Git bytes for each file.
    entries: list[tuple[str, str]] = []
    for rel in files:
        p = PKG / rel
        if not p.exists():
            print(f"  MISSING: {rel}", file=sys.stderr)
            return 1
        blob_sha = git_blob_hash(p)
        canonical = git_blob_bytes(blob_sha)
        sha = sha256_bytes(canonical)
        entries.append((sha, rel))

    # Header
    head_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(PKG), capture_output=True, text=True, check=True,
    ).stdout.strip() or "unknown"
    lines = [
        "# CQC_P5_SHA256_MANIFEST.txt - canonical Git-byte SHA-256 of P5 closure surface",
        "# contract: CQC-P5-RA1-CROSS-REPO-CI-INTEGRATION-TRUTH-FINAL-CLOSURE-v0.1 §18",
        f"# package: {PKG.name}",
        f"# generated from HEAD: {head_sha}",
        f"# pinned MAFS baseline: cd09699fc8cc160ab5cfff00a41e714961dd2109",
        f"# P4 source baseline: 8028e17a6eaab364c744cfa72b714f0f0bd6cf01",
        f"# total entries: {len(entries)}",
        "#",
        "# This manifest is pinned to the canonical Git object bytes (post-",
        "# eol=lf normalization via .gitattributes). Re-running this script on a",
        "# clean working tree of the same commit will reproduce identical",
        "# SHA-256 entries.",
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
