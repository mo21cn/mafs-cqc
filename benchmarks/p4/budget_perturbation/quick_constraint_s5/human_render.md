# BudgetEnvelope: BE-CQC-P4-S5-QUICK

- schema_version: 0.1
- source_srp_id: SRP-CQC-P3-05-R1
- source_srp_sha256: be9c573eb78bb32deaf6fae1b73fcee009245ec1554d33f424a199a749674d35
- budget mode: QUICK (fast triage)
- wall_clock target/ceiling: 8 / 12 minutes
- model_tokens target/ceiling: 120000 / 180000

## Allocations

### AL01

- requirement_id: R01
- route_id: mechanism_evidence [COMMITTED]
- wall_clock_target_minutes: 4
- model_token_target: 50000
- rationale: QUICK 模式下机制维度压缩为核心检索。

### AL02

- requirement_id: R03
- route_id: measurement_observability [COMMITTED]
- wall_clock_target_minutes: 4
- model_token_target: 50000
- rationale: QUICK 模式下观测维度压缩为能力边界速查。

## Escalation Policy

- trigger: a REQUIRED route remains unresolved at target budget -> action: REALLOCATE_WITHIN_CEILING
- trigger: a CONDITIONAL route becomes epistemically activated -> action: REALLOCATE_WITHIN_CEILING
- trigger: the hard ceiling would be exceeded -> action: RETURN_INSUFFICIENT

## Feasibility

- status: INSUFFICIENT
- unfunded: R02 / historical_lineage — 在 QUICK 硬上限 12 分钟内，R01/R03 已占 8 分钟；既有策略谱系盘点的最小诚实成本（约 6 分钟）无法在此剩余容量内资助。该 REQUIRED 义务保持 unfunded 并显式记录，不以降低证据标准的方式修复。
- constraint_note: QUICK 紧缩上限无法诚实资助全部 3 个 REQUIRED 义务；SRP 义务未被删减或弱化——缺口如实上报。

