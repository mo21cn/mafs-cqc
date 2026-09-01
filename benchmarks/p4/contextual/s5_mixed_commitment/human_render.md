# BudgetEnvelope: BE-CQC-P4-S5-R2

- schema_version: 0.1
- source_srp_id: SRP-CQC-P3-05-R1
- source_srp_sha256: be9c573eb78bb32deaf6fae1b73fcee009245ec1554d33f424a199a749674d35
- budget mode: STANDARD (normal research pass)
- wall_clock target/ceiling: 25 / 40 minutes
- model_tokens target/ceiling: 300000 / 500000

## Allocations

### AL01

- requirement_id: R01
- route_id: mechanism_evidence [COMMITTED]
- wall_clock_target_minutes: 8
- model_token_target: 90000
- rationale: 机制连锁效应证据是 S5 三维度之一（mechanism）。

### AL02

- requirement_id: R02
- route_id: historical_lineage [COMMITTED]
- wall_clock_target_minutes: 8
- model_token_target: 90000
- rationale: 既有直接靶向策略盘点是范式新意判定的对照集（novelty 维度）。

### AL03

- requirement_id: R03
- route_id: measurement_observability [COMMITTED]
- wall_clock_target_minutes: 7
- model_token_target: 80000
- rationale: R03 获得 committed 资源是因为已接纳的测量/观测义务需要对检出限、代谢物覆盖面、通量与单细胞/近单细胞可行性边界的刻画。

### AL04

- requirement_id: R02
- route_id: counterexample_negative_evidence [RESERVE_CONDITIONAL]
- wall_clock_target_minutes: 3
- model_token_target: 30000
- rationale: 上游抑制思路已被尝试/放弃的记录检索仅在宽泛盘点暗示该可能时激活。

## Escalation Policy

- trigger: a REQUIRED route remains unresolved at target budget -> action: REALLOCATE_WITHIN_CEILING
- trigger: a CONDITIONAL route becomes epistemically activated -> action: REALLOCATE_WITHIN_CEILING
- trigger: the hard ceiling would be exceeded -> action: REQUEST_ENVELOPE_EXPANSION

## Feasibility

- status: FEASIBLE
- unfunded: (none)
- constraint_note: STANDARD envelope: all 3 mixed-dimension REQUIRED routes funded; 1 conditional reserve for counterexample retrieval.

