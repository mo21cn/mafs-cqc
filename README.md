# mafs-cqc

**Candidate Question Compiler (CQC)** — Digestion-as-Artifact upstream module for MAFS.

CQC makes a model's first research-intent digestion explicit, inspectable, reusable, and
downstream-operable as a durable artifact (`CandidateQuestionSet`), without encoding
scientific question intelligence into deterministic software.

```text
The model performs digestion.
The artifact makes digestion durable.
The architecture validates, preserves, and hands off the artifact.
MAFS consumes the artifact.
```

## Status

- Master contract: `CQC-MASTER-v0.1-DIGESTION-AS-ARTIFACT` (this repository, root)
- Current phase: **CQC-P0 — Minimal Digestion Surface + Artifact Freeze** on branch `dev/cqc-p0`
- Independent line: merged into MAFS only at CQC-P5, via a minimal adapter

## Layout (P0)

```text
schemas/candidate_question_set.v0.1.schema.json
instructions/cqc_p0_digest.md
scripts/validate_cqs.py, render_cqs.py, build_p0.py
examples/inputs/ outputs/ rendered/
tests/
docs/
```

## Verification

```text
python -m pytest -q
python scripts/validate_cqs.py examples/outputs/*.json
python scripts/render_cqs.py examples/outputs/<x>.json   # deterministic
```

GitHub Actions independently verifies committed artifacts; CI never regenerates model cognition.
