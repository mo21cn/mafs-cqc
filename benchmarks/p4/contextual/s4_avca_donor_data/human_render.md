# BudgetEnvelope: BE-CQC-P4-S4

- schema_version: 0.1
- source_srp_id: SRP-CQC-P3-04
- source_srp_sha256: 03355816136dd52e66e70f7c92125386bf62c5ee1d57bd2e9a30f0ecad0cad31
- budget mode: STANDARD (normal research pass)
- wall_clock target/ceiling: 20 / 40 minutes
- model_tokens target/ceiling: 250000 / 400000

## Allocations

### AL01

- requirement_id: R01
- route_id: entity_resource_identity [COMMITTED]
- wall_clock_target_minutes: 8
- model_token_target: 80000
- rationale: 共享义务（服务 CQ-01 与 CQ-02）：Atlas 身份/范围/访问确认只预算一次，不因 target_question_ids 复制。

### AL02

- requirement_id: R02
- route_id: measurement_observability [COMMITTED]
- wall_clock_target_minutes: 7
- model_token_target: 70000
- rationale: 三判定词的可判定性三态映射是 CQ-02 回答的前提义务。

### AL03

- requirement_id: R03
- route_id: source_content_verification [RESERVE_CONDITIONAL]
- wall_clock_target_minutes: 6
- model_token_target: 60000
- rationale: 存在性核查 gated on R01（清单源）与 R02（判定标准）；激活前仅保留预备容量。

## Escalation Policy

- trigger: a REQUIRED route remains unresolved at target budget -> action: REALLOCATE_WITHIN_CEILING
- trigger: a CONDITIONAL route becomes epistemically activated -> action: REALLOCATE_WITHIN_CEILING
- trigger: the hard ceiling would be exceeded -> action: REQUEST_ENVELOPE_EXPANSION

## Feasibility

- status: FEASIBLE
- unfunded: (none)
- constraint_note: STANDARD envelope: shared identity requirement budgeted once; 2 REQUIRED routes funded; 1 conditional reserve for the gated existence check.

