# BudgetEnvelope: BE-CQC-P4-S1-R1

- schema_version: 0.1
- source_srp_id: SRP-CQC-P3-01
- source_srp_sha256: 67755617b29aef2f3d80f53b20fb9fb2434fe8512a4dae5472fe9263e83380ea
- budget mode: STANDARD (normal research pass)
- wall_clock target/ceiling: 25 / 40 minutes
- model_tokens target/ceiling: 300000 / 500000

## Allocations

### AL01

- requirement_id: R01
- route_id: mechanism_evidence [COMMITTED]
- wall_clock_target_minutes: 10
- model_token_target: 120000
- rationale: R01/mechanism_evidence is the largest evidence obligation in S1 and therefore receives the largest committed allocation. ( formerly named specific unadmitted mechanism lines )

### AL02

- requirement_id: R03
- route_id: measurement_observability [COMMITTED]
- wall_clock_target_minutes: 8
- model_token_target: 90000
- rationale: 观测技术边界决定 CQ-01 证据的可靠性与缺口，属必答题。

### AL03

- requirement_id: R02
- route_id: mechanism_evidence [RESERVE_CONDITIONAL]
- wall_clock_target_minutes: 5
- model_token_target: 50000
- rationale: 人群比较仅在 R01 证据暗示人群间差异时激活。

### AL04

- requirement_id: R02
- route_id: counterexample_negative_evidence [RESERVE_CONDITIONAL]
- wall_clock_target_minutes: 3
- model_token_target: 30000
- rationale: 反例检索仅在跨人群外推主张出现时激活。

## Escalation Policy

- trigger: a REQUIRED route remains unresolved at target budget -> action: REALLOCATE_WITHIN_CEILING
- trigger: a CONDITIONAL route becomes epistemically activated -> action: REALLOCATE_WITHIN_CEILING
- trigger: the hard ceiling would be exceeded -> action: REQUEST_ENVELOPE_EXPANSION

## Feasibility

- status: FEASIBLE
- unfunded: (none)
- constraint_note: STANDARD envelope: 2 REQUIRED routes funded (mechanism core + observability); 2 conditional reserves held for population comparison and counterexample retrieval.

