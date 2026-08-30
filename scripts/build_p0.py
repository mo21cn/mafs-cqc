#!/usr/bin/env python
"""CQC-P0 metrics + SHA-256 manifest builder (deterministic, machine facts only).

Contract CQC-P0-MINIMAL-DIGESTION-SURFACE-v0.1 sections 18-19.

Usage:
  python scripts/build_p0.py [--cycles N] [--ci-run-id ID]

Writes docs/CQC_P0_METRICS.json and docs/CQC_P0_SHA256_MANIFEST.txt.
Unknown values stay null (never zero-filled).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]

MANIFEST_GLOBS = [
    "schemas/*.json",
    "instructions/*.md",
    "scripts/*.py",
    "examples/inputs/*",
    "examples/outputs/*.json",
    "examples/rendered/*.md",
    "tests/*.py",
    ".github/workflows/*.yml",
    "contracts/*.md",
    "CQC_Master_Development_Contract_v0.1.md",
]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git_sha() -> str | None:
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=PKG,
                           capture_output=True, text=True, timeout=10)
        return r.stdout.strip() or None
    except Exception:
        return None


def count_tests() -> int | None:
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q"],
                           cwd=PKG, capture_output=True, text=True, timeout=120)
        for line in r.stdout.splitlines()[::-1]:
            line = line.strip()
            if "tests collected" in line or "test selected" in line:
                return int(line.split()[0])
    except Exception:
        pass
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycles", type=int, default=None,
                    help="meaningful push/CI cycles so far")
    ap.add_argument("--ci-run-id", type=str, default=None)
    args = ap.parse_args()

    outputs = sorted((PKG / "examples" / "outputs").glob("*.json"))
    inputs = PKG / "examples" / "inputs"

    # validator (machine mode)
    r = subprocess.run(
        [sys.executable, str(PKG / "scripts" / "validate_cqs.py")]
        + [str(p) for p in outputs] + ["--check-inputs", str(inputs), "--json"],
        capture_output=True, text=True, timeout=120)
    validation = json.loads(r.stdout)

    # renderer reproducibility
    sys.path.insert(0, str(PKG / "scripts"))
    from render_cqs import render
    render_ok = 0
    for out in outputs:
        committed = PKG / "examples" / "rendered" / (out.stem + ".md")
        if committed.is_file():
            art = json.loads(out.read_text(encoding="utf-8"))
            if render(art) == committed.read_text(encoding="utf-8"):
                render_ok += 1

    production_file_count = sum(
        len(list(PKG.glob(g))) for g in ["schemas/*.json", "instructions/*.md", "scripts/*.py"])

    metrics = {
        "contract_id": "CQC-P0-MINIMAL-DIGESTION-SURFACE-v0.1",
        "commit_sha": git_sha(),
        "ci_run_id": args.ci_run_id,
        "artifact_schema_version": "0.1",
        "example_count": len(outputs),
        "schema_valid_count": sum(1 for a in validation["artifacts"] if a.get("schema_valid")),
        "source_hash_valid_count": sum(1 for a in validation["artifacts"] if a.get("source_hash_valid")),
        "source_trace_valid_count": sum(1 for a in validation["artifacts"] if a.get("exact_trace_valid")),
        "dependency_graph_valid_count": sum(1 for a in validation["artifacts"] if a.get("dependency_dag_valid")),
        "narrative_input_match_count": sum(
            1 for a in validation["artifacts"] if a.get("narrative_file_match") is True),
        "deterministic_render_valid_count": render_ok,
        "meaningful_push_ci_cycles": args.cycles,
        "production_file_count": production_file_count,
        "test_count": count_tests(),
    }

    docs = PKG / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "CQC_P0_METRICS.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = []
    for pattern in MANIFEST_GLOBS:
        for p in sorted(PKG.glob(pattern)):
            if p.is_file() and "docs" not in p.relative_to(PKG).parts:
                lines.append(f"{sha256_file(p)}  {p.relative_to(PKG).as_posix()}")
    (docs / "CQC_P0_SHA256_MANIFEST.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
