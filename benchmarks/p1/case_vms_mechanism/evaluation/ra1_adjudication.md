> **HISTORICAL / SUPERSEDED** — Current machine-readable comparison source: \evaluation/comparison.json\ (CQC-P1-RA2). This file is retained as development history.

# RA1 Re-adjudication — case_vms_mechanism

## Reference-set separation (contract §5)

```yaml
substantive_targets:
  - 血管舒缩症状的细胞分辨率机制解释（中枢 KNDy 线 + 血管线）
interpretive_constraints:
  - 『女性』人群范围未指定（围绝经期 vs 治疗诱导等）
  - 『细胞分辨率』指组学还是成像未指定
noncritical_input_noise: []
```

## Re-adjudicated substantive coverage

- Arm A: recovered 1/1 substantive target (QA-01..04 cover both mechanism lines at cell resolution).
- Arm B (final, unchanged — no Arm C): recovered 1/1 (CQ-01). **Substantive parity.**
- Interpretive constraints: both arms captured both constraints; Arm B as durable per-question uncertainty (CQ-02/CQ-03), Arm A as inline notes in its preparation document.

## Reframed comparison (contract §4 vocabulary)

Arm A holds a **direct downstream artifact** (downstream_preparation.json with question order, missing-information and reasoning notes — free-form, downstream-specific interpretive state). Arm B holds a **typed intermediate CQS + downstream artifact** whose interpretive state is question-addressable and source-traced. P1's original claim "Arm A has no artifact / traceability none" is **withdrawn**.

## Failure ledger (Arm B)

```yaml
dependency_failures: []
missing_prerequisites: []
other_semantic_failures: []
```

No Arm C trigger (confirmed by RA1 re-adjudication).
