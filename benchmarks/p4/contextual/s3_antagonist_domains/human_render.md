# BudgetEnvelope: BE-CQC-P4-S3

- schema_version: 0.1
- source_srp_id: SRP-CQC-P3-03
- source_srp_sha256: c0ef444b0f5786cbf1b94638ee997e3bf3f8d96ceb7f3928fc73d220cf07d295
- budget mode: STANDARD (normal research pass)
- wall_clock target/ceiling: 20 / 40 minutes
- model_tokens target/ceiling: 250000 / 400000

## Allocations

### AL01

- requirement_id: R01
- route_id: entity_resource_identity [COMMITTED]
- wall_clock_target_minutes: 6
- model_token_target: 60000
- rationale: 指称消歧是 S3 唯一的 REQUIRED 义务，也是 R02/R03 的证据边界前提。

### AL02

- requirement_id: R01
- route_id: terminology_boundary [RESERVE_CONDITIONAL]
- wall_clock_target_minutes: 4
- model_token_target: 40000
- rationale: 竞争解读识别仅在实体类型分布显示显著竞争时激活。

### AL03

- requirement_id: R02
- route_id: domain_coverage_inventory [RESERVE_CONDITIONAL]
- wall_clock_target_minutes: 8
- model_token_target: 80000
- rationale: 领域盘点矩阵 gated on R01 消歧；药理解读确认前不预激活。

### AL04

- requirement_id: R03
- route_id: domain_coverage_inventory [RESERVE_CONDITIONAL]
- wall_clock_target_minutes: 6
- model_token_target: 60000
- rationale: 工具用途盘点 gated on R01；同上不预激活。

## Escalation Policy

- trigger: a REQUIRED route remains unresolved at target budget -> action: REALLOCATE_WITHIN_CEILING
- trigger: a CONDITIONAL route becomes epistemically activated -> action: REALLOCATE_WITHIN_CEILING
- trigger: the hard ceiling would be exceeded -> action: REQUEST_ENVELOPE_EXPANSION

## Feasibility

- status: FEASIBLE
- unfunded: (none)
- constraint_note: STANDARD envelope: 1 REQUIRED route (referent disambiguation) funded; 3 CONDITIONAL routes hold reserve only - no pre-activation.

