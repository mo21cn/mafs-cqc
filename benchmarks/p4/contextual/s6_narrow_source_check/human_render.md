# BudgetEnvelope: BE-CQC-P4-S6

- schema_version: 0.1
- source_srp_id: SRP-CQC-P3-06-R1
- source_srp_sha256: ffdf4d673069fe28784135af9d54734934134a41fb88619db9bcef796fd10032
- budget mode: STANDARD (normal research pass)
- wall_clock target/ceiling: 8 / 15 minutes
- model_tokens target/ceiling: 80000 / 120000

## Allocations

### AL01

- requirement_id: R01
- route_id: source_content_verification [COMMITTED]
- wall_clock_target_minutes: 5
- model_token_target: 40000
- rationale: 存在性三态核查是 S6 唯一 REQUIRED 义务；窄任务保持窄预算。

### AL02

- requirement_id: R01
- route_id: entity_resource_identity [RESERVE_CONDITIONAL]
- wall_clock_target_minutes: 3
- model_token_target: 25000
- rationale: 指称消歧仅在歧义实质化（无法唯一确定论文）时升级为显式路线。

## Escalation Policy

- trigger: a REQUIRED route remains unresolved at target budget -> action: REALLOCATE_WITHIN_CEILING
- trigger: a CONDITIONAL route becomes epistemically activated -> action: REALLOCATE_WITHIN_CEILING
- trigger: the hard ceiling would be exceeded -> action: REQUEST_ENVELOPE_EXPANSION

## Feasibility

- status: FEASIBLE
- unfunded: (none)
- constraint_note: STANDARD envelope: single REQUIRED existence check funded; identity route kept as conditional reserve.

