# RA1 Re-adjudication — case_vcell_scope

## Reference-set separation (contract §5)

```yaml
substantive_targets:
  - Virtual Cell 学术研究方向的饱和盘点
interpretive_constraints:
  - "Virtual Cel" 拼写歧义（实体风险注记：领域概念 vs VCell 软件 vs 其他）
  - 相邻术语边界（whole-cell / digital cell 等）作为盘点检索面的界定
noncritical_input_noise: []
```

## Re-adjudicated substantive coverage

- Arm A: 1/1 (QA-01..05 inventory across lines; typo normalized silently — an interpretive-constraint handling, not a substantive miss).
- Arm B initial: 1/1 (CQ-01) — **substantive parity**.
- Arm B dependency failure (measured, contract §7.1): edge CQ-01→CQ-02 was a **false prerequisite** — the inventory is searchable from Virtual Cell reviews/programs without the adjacent-term boundary.

## Arm C re-digestion result

- Prior: CQS-CQC-P1-02 (unchanged, preserved).
- Revised: CQS-CQC-P1-02-RC1 — CQ-01.dependencies = [] (false edge removed).
- Repair effect: CQ-01 now independently searchable; CQ-02 remains a real constraint question (still valuable for coverage improvement, no longer a blocker).
- New failures introduced: none (validator: revised schema-valid, DAG valid, differs from prior, render reproducible).

## Reframed comparison

Arm A's typo normalization was an unrecorded interpretation inside its **direct downstream artifact**; Arm B's typo handling is question-addressable state (CQ-03 with the VCell-software alternative reading). P1's "Arm A interpretation choices are inherently unrecoverable" is **withdrawn/narrowed**: they are recorded in Arm A's prep JSON (`missing_information_before_search`, `natural_reasoning_notes`), just in free-form, downstream-specific form rather than typed per-question form.
