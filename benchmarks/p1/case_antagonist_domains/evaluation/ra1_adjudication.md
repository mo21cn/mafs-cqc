> **HISTORICAL / SUPERSEDED** — Current machine-readable comparison source: \evaluation/comparison.json\ (CQC-P1-RA2). This file is retained as development history.

# RA1 Re-adjudication — case_antagonist_domains

## Reference-set separation (contract §5)

```yaml
substantive_targets:
  - 拮抗剂研究的应用领域盘点
  - 拮抗剂作为研究工具的非治疗用途
interpretive_constraints:
  - 『拮抗剂』指称范围（药理分子 vs 拮抗肌 vs 其他）未指定
  - 『应用领域』的盘点维度（疾病/靶点/模态）未指定
noncritical_input_noise: []
```

## Re-adjudicated substantive coverage

- Arm A: 2/2 (QA-01..03; dimension choice implicit).
- Arm B initial: 2/2 (CQ-02 inventory; CQ-03 tools) — **substantive parity**.
- Interpretive constraints: Arm A defaulted to the pharmacological reading silently; Arm B made it CQ-01 and the dimension choice CQ-04.

## Arm B failure ledger (measured, contract §8.1)

```yaml
dependency_failures:
  - "CQ-02→CQ-01 confirmed valid (RA2 test: inventory surface definition)"
missing_prerequisites:
  - "CQ-03 (research-tool usage) assumed the pharmacological-molecule reading while marked independent of CQ-01 — if disambiguation leaves the pharmacological reading, CQ-03 is no longer valid"
other_semantic_failures: []
```

## Arm C re-digestion result

- Prior: CQS-CQC-P1-04 (unchanged, preserved).
- Revised: CQS-CQC-P1-04-RC1 — CQ-03.dependencies = [CQ-01]; CQ-03.uncertainty now states the assumed pharmacological reading explicitly.
- Repair effect: the premature semantic branch is now declared and gated; if CQ-01 resolves away from pharmacological reading, CQ-03 is flagged for re-formulation instead of silently surviving.
- New failures introduced: none (validator PASS: schema, DAG, differs-from-prior, render reproducible).
