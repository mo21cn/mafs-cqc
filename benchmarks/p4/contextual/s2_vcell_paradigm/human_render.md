# BudgetEnvelope: BE-CQC-P4-S2

- schema_version: 0.1
- source_srp_id: SRP-CQC-P3-02-R1
- source_srp_sha256: 67036a5c48d02608a25ba00c85260162dc6bce74a78ba4079f0c12f18e6cf1a0
- budget mode: STANDARD (normal research pass)
- wall_clock target/ceiling: 25 / 40 minutes
- model_tokens target/ceiling: 300000 / 500000

## Allocations

### AL01

- requirement_id: R01
- route_id: historical_lineage [COMMITTED]
- wall_clock_target_minutes: 10
- model_token_target: 120000
- rationale: 候选范式盘点是 S2 最大义务：宽收由证据生成，类别饱和为停机条件。

### AL02

- requirement_id: R02
- route_id: terminology_boundary [COMMITTED]
- wall_clock_target_minutes: 6
- model_token_target: 60000
- rationale: 判定基准显式确立是 CQ-01 候选筛选的前提义务。

### AL03

- requirement_id: R03
- route_id: historical_lineage [COMMITTED]
- wall_clock_target_minutes: 6
- model_token_target: 60000
- rationale: 谱系映射依赖 R01 清单，规模可控。

## Escalation Policy

- trigger: a REQUIRED route remains unresolved at target budget -> action: REALLOCATE_WITHIN_CEILING
- trigger: a CONDITIONAL route becomes epistemically activated -> action: REALLOCATE_WITHIN_CEILING
- trigger: the hard ceiling would be exceeded -> action: REQUEST_ENVELOPE_EXPANSION

## Feasibility

- status: FEASIBLE
- unfunded: (none)
- constraint_note: STANDARD envelope: all 3 REQUIRED routes funded; no conditional routes exist in this SRP.

