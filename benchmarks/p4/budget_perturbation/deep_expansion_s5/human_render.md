# BudgetEnvelope: BE-CQC-P4-S5-DEEP

- schema_version: 0.1
- source_srp_id: SRP-CQC-P3-05-R1
- source_srp_sha256: be9c573eb78bb32deaf6fae1b73fcee009245ec1554d33f424a199a749674d35
- budget mode: DEEP (expanded prior-art stress)
- wall_clock target/ceiling: 45 / 60 minutes
- model_tokens target/ceiling: 500000 / 700000

## Allocations

### AL01

- requirement_id: R01
- route_id: mechanism_evidence [COMMITTED]
- wall_clock_target_minutes: 12
- model_token_target: 150000
- rationale: DEEP 模式扩大机制证据覆盖（人群/细胞类型细分）。

### AL02

- requirement_id: R02
- route_id: historical_lineage [COMMITTED]
- wall_clock_target_minutes: 12
- model_token_target: 150000
- rationale: DEEP 模式扩大既有策略盘点的深度与回溯年限。

### AL03

- requirement_id: R03
- route_id: measurement_observability [COMMITTED]
- wall_clock_target_minutes: 10
- model_token_target: 120000
- rationale: DEEP 模式扩大观测技术边界调查。

### AL04

- requirement_id: R02
- route_id: counterexample_negative_evidence [RESERVE_CONDITIONAL]
- wall_clock_target_minutes: 5
- model_token_target: 60000
- rationale: DEEP 模式为反例检索保留更大预备容量。

## Escalation Policy

- trigger: a REQUIRED route remains unresolved at target budget -> action: REALLOCATE_WITHIN_CEILING
- trigger: a CONDITIONAL route becomes epistemically activated -> action: REALLOCATE_WITHIN_CEILING
- trigger: the hard ceiling would be exceeded -> action: REQUEST_ENVELOPE_EXPANSION

## Feasibility

- status: FEASIBLE
- unfunded: (none)
- constraint_note: DEEP envelope funds all 3 REQUIRED routes with expanded capacity; 1 conditional reserve retained. Scientific obligations and route states identical to STANDARD.

