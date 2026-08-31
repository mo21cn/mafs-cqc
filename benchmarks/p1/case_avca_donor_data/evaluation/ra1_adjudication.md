> **HISTORICAL / SUPERSEDED** — Current machine-readable comparison source: \evaluation/comparison.json\ (CQC-P1-RA2). This file is retained as development history.

# RA1 Re-adjudication — case_avca_donor_data

## Reference-set separation (contract §5)

```yaml
substantive_targets:
  - Arc Virtual Cell Atlas 中年轻健康血管/心脏原代供体数据的存在性判定
interpretive_constraints:
  - 『年轻』『健康』『原代』三个判定词的阈值与元数据可判定性（实质性约束：直接决定存在性主张如何成立）
  - Atlas 实体身份/收录范围确认（存在性判定的证据来源前提）
noncritical_input_noise:
  - "有没有有没有" 文本重复（按单一疑问理解；记录于 uncertainty，不计为科学覆盖项）
```

## Re-adjudicated substantive coverage

- Arm A: 1/1 (QA-01..03; threshold conventions borrowed silently).
- Arm B initial: 1/1 (CQ-02) — **substantive parity**.
- Interpretive constraints: Arm A's threshold borrowing was silent; Arm B's CQ-03 (three-state decidability mapping) is the **interpretive-constraint capture** — per contract §5.1 it materially binds the final existence claim, but it is not itself a substantive target.

## Arm B failure ledger (measured, contract §9.1)

```yaml
dependency_failures:
  - "CQ-02→CQ-01 confirmed valid (RA2 test)"
missing_prerequisites:
  - "CQ-02 did not depend on CQ-03 (threshold decidability) although the downstream preparation itself states CQ-03's output binds whether/how CQ-02 can be answered — a stage-referential contradiction"
other_semantic_failures: []
```

## Arm C re-digestion result

- Prior: CQS-CQC-P1-05 (unchanged, preserved).
- Revised: CQS-CQC-P1-05-RC1 — CQ-02.dependencies = [CQ-01, CQ-03].
- Repair effect: the existence answer is now structurally gated on both the Atlas identity AND the decidability verdict; the contradiction between artifact and preparation is closed.
- New failures introduced: none (validator PASS).
