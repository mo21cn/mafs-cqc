# CQC-P4 — Structured Summary

Human-readable canonical summary of final P4 state. Counts source from
`docs/CQC_P4_METRICS.json` (machine-derived from final artifacts). Integrity:
`docs/CQC_P4_SHA256_MANIFEST.txt`.

## A — Acceptance Header

```yaml
contract_id: CQC-P4-BUDGET-ENVELOPE-v0.1
status: READY_FOR_REVIEW
repository: mo21cn/mafs-cqc
branch: dev/cqc-p4
contextual_case_count: 6
budget_perturbation_case_count: 2 (+1 intent-invariance comparison)
meaningful_push_ci_cycles_current_step: 1
```

## B — BudgetEnvelope v0.1 Schema Decision

Set envelope: `artifact_id`, `schema_version`, `source_srp_id` + `source_srp_sha256`
(byte-bound to the accepted P3 SRP), `budget_intent{mode, operator_goal}`,
`total_envelope{wall_clock{target, hard_ceiling}, model_tokens{target, hard_ceiling}}`,
`allocations[]`, `escalation_policy{triggers[]}`, `feasibility{status,
unfunded_obligations, constraint_note}`. Per allocation: `allocation_id`,
`requirement_id`, `route_id`, `activation[COMMITTED|RESERVE_CONDITIONAL]`,
`wall_clock_target_minutes`, `model_token_target`, `rationale`.

Each field earns its place: `target/ceiling` split separates intent from
authorization; `activation` carries the REQUIRED-vs-CONDITIONAL distinction without
a third invented state; `unfunded_obligations` makes under-budget truth explicit at
requirement/route granularity. **Rejected imagined fields**: provider/API quota
fields, per-question_type cost multipliers, route confidence/priority scores, a
requirement-level dependency graph (SRP/CQS bindings already carry it), and any
"activation_likelihood" probability — none was earned by a measured failure.
Schema pressure observed: none.

## C — Contextual Budget Matrix

Final semantic status: **PENDING_HO_CHATGPT** (Local Claw preliminary only).

| Case | Mode | Requirements | Routes | COMMITTED | RESERVE_CONDITIONAL | Feasibility | HO+ChatGPT Status |
|---|---|---:|---:|---:|---:|---|---|
| s1_vms_cellular_mechanism | STANDARD | 3 | 4 | 2 | 2 | FEASIBLE | PENDING_HO_CHATGPT |
| s2_vcell_paradigm | STANDARD | 3 | 3 | 3 | 0 | FEASIBLE | PENDING_HO_CHATGPT |
| s3_antagonist_domains | STANDARD | 3 | 4 | 1 | 3 | FEASIBLE | PENDING_HO_CHATGPT |
| s4_avca_donor_data | STANDARD | 3 | 3 | 2 | 1 | FEASIBLE | PENDING_HO_CHATGPT |
| s5_mixed_commitment | STANDARD | 3 | 4 | 3 | 1 | FEASIBLE | PENDING_HO_CHATGPT |
| s6_narrow_source_check | STANDARD | 1 | 2 | 1 | 1 | FEASIBLE | PENDING_HO_CHATGPT |

All counts machine-derived from final artifacts (`docs/CQC_P4_METRICS.json`).

## D — Budget Authority

SRP obligations unchanged across every envelope. BudgetEnvelope controls resource
only: it allocates, reserves, caps, defers, declares insufficiency, and requests
escalation — it never deletes a requirement, changes a stopping_condition, promotes
a CONDITIONAL route to COMMITTED, or rewrites source requirements.

## E — QUICK / STANDARD / DEEP Stress (S5, same accepted SRP)

```yaml
source_srp_sha256: identical across all three (byte-identical source_srp.json)
requirements/routes/stopping_conditions/source_requirements: unchanged
QUICK (8/12 min, 120k/180k tok):  2 COMMITTED, 0 reserve, INSUFFICIENT
STANDARD (25/40 min, 300k/500k): 3 COMMITTED, 1 reserve, FEASIBLE
DEEP (45/60 min, 500k/700k tok):  4 COMMITTED(3+1 reserve), FEASIBLE
```

Only resource commitments differ. QUICK's INSUFFICIENT is reported with the exact
unfunded obligation (R02/historical_lineage) rather than weakening the SRP.

## F — Productive Instability Budgeting

S3: 3 CONDITIONAL routes hold RESERVE_CONDITIONAL capacity (disambiguation-gated
inventories); none pre-activated. S6: identity route kept as conditional reserve,
activated only if reference ambiguity becomes material. Productive instability
survives as reserve, not as premature certainty.

## G — Shared Requirement

S4's R01 (Atlas identity, targets CQ-01+CQ-02) is budgeted **once** — one
allocation, no duplication from question cardinality (validator-enforced).

## H — Under-Budget Truth

QUICK constraint (S5): status INSUFFICIENT; unfunded obligation
`R02/historical_lineage` explicitly listed with reason (minimum honest cost of the
lineage sweep exceeds remaining ceiling after R01/R03). The SRP was not weakened,
trimmed, or re-scoped to force FEASIBLE.

## I — Architecture Delta

```yaml
cqs_schema_changed: false
srp_schema_changed: false
budget_envelope_artifact_added: true
new_cost_scorers: 0
new_question_type_budget_routers: 0
new_optimizers: 0
new_provider_routers: 0
new_query_generators: 0
mafs_integrated: false
live_retrieval_added: false
```

## J — P4 Finding

**Earned:** an accepted SRP can be converted into an explicit bounded time/token
resource artifact without changing scientific obligations, prematurely activating
uncertainty, or hiding insufficient budget. Required routes receive committed
resource exactly once (shared requirements included); conditional routes receive
reserve capacity while staying honestly conditional; under-funded states surface as
typed feasibility statuses with requirement/route-granular unfunded references; and
QUICK→STANDARD→DEEP changes only time/token/reserve/feasibility — never the science.
**Not earned:** any claim about real wall-clock or token accuracy, optimality,
search-quality improvement, or runtime completion — no live retrieval exists in P3/P4
by contract; actual cost calibration belongs to later integration/runtime evidence.

## K — Next Step

**CQC-P5** — the CQC artifact chain is complete (CQS → SRP → BudgetEnvelope, all
frozen and machine-guarded); the next bounded phase is the MAFS integration
adapter (minimal, per master v0.2 §16), pending HO + ChatGPT authorization.
