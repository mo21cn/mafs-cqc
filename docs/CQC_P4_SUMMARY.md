# CQC-P4 — Canonical Summary (Final)

Human-readable canonical summary of final P4 state. Counts source from
`docs/CQC_P4_METRICS.json` (machine-derived from final artifacts). Integrity:
`docs/CQC_P4_SHA256_MANIFEST.txt` (validator-enforced, mandatory-coverage checked).

## A — Acceptance Header

```yaml
contract_id: CQC-P4-BUDGET-ENVELOPE-v0.1
current_phase_state: CQC-P4-RA2-CLOSED
repository: mo21cn/mafs-cqc
branch: dev/cqc-p4
contextual_case_count: 6
budget_perturbation_case_count: 2
meaningful_push_ci_cycles_current_step: (RA2 = 1; see docs/CQC_P4_METRICS.json)
p4_ra1_meaningful_push_ci_cycles: 2
```

The actual evidence commit SHA and CI run are reported externally in the Local Claw
return note (self-pinning retired per P2-RA2 §7).

## B — BudgetEnvelope v0.1 Frozen Shape

Set envelope: `artifact_id`, `schema_version`, `source_srp_id` + `source_srp_sha256`
(byte-bound to the accepted P3 SRP), `budget_intent{mode, operator_goal}`,
`total_envelope{wall_clock{target, hard_ceiling}, model_tokens{target, hard_ceiling}}`,
`allocations[]`, `escalation_policy{triggers[]}`, `feasibility{status,
unfunded_obligations, constraint_note}`. Per allocation: `allocation_id`,
`requirement_id`, `route_id`, `activation[COMMITTED|RESERVE_CONDITIONAL]`,
`wall_clock_target_minutes`, `model_token_target`, `rationale`.

Schema unchanged since P4 freeze; no pressure earned a new field across 6 cases +
2 perturbations + 2 repair rounds.

## C — Final Contextual Budget Matrix

| Case | Mode | Requirements | Routes | COMMITTED | RESERVE_CONDITIONAL | Feasibility |
|---|---|---:|---:|---:|---:|---|
| s1_vms_cellular_mechanism | STANDARD | 3 | 4 | 2 | 2 | FEASIBLE |
| s2_vcell_paradigm | STANDARD | 3 | 3 | 3 | 0 | FEASIBLE |
| s3_antagonist_domains | STANDARD | 3 | 4 | 1 | 3 | FEASIBLE |
| s4_avca_donor_data | STANDARD | 3 | 3 | 2 | 1 | FEASIBLE |
| s5_mixed_commitment | STANDARD | 3 | 4 | 3 | 1 | FEASIBLE |
| s6_narrow_source_check | STANDARD | 1 | 2 | 1 | 1 | FEASIBLE |

Counts are machine-derived from final artifacts (`docs/CQC_P4_METRICS.json`).

## D — Budget Authority

BudgetEnvelope controls resource only: it allocates, reserves, caps, defers,
declares insufficiency, and requests escalation. It never deletes a requirement,
changes a stopping_condition, promotes a CONDITIONAL route to COMMITTED, rewrites
source requirements, or carries context-only downstream meaning.

## E — QUICK / STANDARD / DEEP Stress (S5, same accepted SRP)

```yaml
QUICK S5 = INSUFFICIENT
unfunded = R02 / historical_lineage

STANDARD S5 = FEASIBLE

DEEP S5 = FEASIBLE
3 COMMITTED + 1 RESERVE_CONDITIONAL
```

source_srp_sha256 identical across all three (byte-identical source_srp.json);
requirements/routes/stopping_conditions/source_requirements unchanged. Only resource
commitments differ. QUICK's INSUFFICIENT reports the exact unfunded obligation
(R02/historical_lineage) rather than weakening the SRP.

## F — Productive Instability Budgeting

S3: 3 CONDITIONAL routes hold RESERVE_CONDITIONAL capacity (disambiguation-gated
inventories); none pre-activated. S6: identity route kept as conditional reserve,
activated only if reference ambiguity becomes material. Productive instability
survives as reserve, not as premature certainty.

## G — Shared Requirement

S4's R01 (Atlas identity, targets CQ-01+CQ-02) is budgeted **once** — one
allocation. Deduplication is route-based: same (requirement_id, route_id) cannot be
duplicated; question cardinality does not multiply allocations (validator-enforced).

## H — Review Truth

```yaml
contextual_review_source_srp_binding: 6/6
contextual_review_budget_envelope_binding: 6/6
contextual_review_machine_truth: 6/6
```

Validator enforces review truth (P4_REVIEW_BINDING_MISMATCH /
P4_REVIEW_MACHINE_TRUTH_MISMATCH → FAIL).

## I — Under-Budget Truth

QUICK constraint (S5): status INSUFFICIENT; unfunded obligation
`R02/historical_lineage` explicitly listed with reason. The SRP was not weakened,
trimmed, or re-scoped to force FEASIBLE.

## J — Architecture Delta

```yaml
cqs_schema_changed: false
srp_schema_changed: false
budget_envelope_schema_changed: false
new_cost_scorers: 0
new_question_type_budget_routers: 0
new_optimizers: 0
new_provider_routers: 0
new_query_generators: 0
mafs_integrated: false
live_retrieval_added: false
```

## K — P4 Finding

**Earned:** an accepted SRP can be converted into an explicit bounded resource
artifact without changing scientific obligations, prematurely activating uncertainty,
or hiding insufficient budget. Required routes receive committed resource exactly
once; conditional routes receive reserve while staying conditional; under-funded
states surface as typed feasibility statuses with requirement/route-granular
references; QUICK→STANDARD→DEEP changes only resource commitments.
**Not earned:** wall-clock/token accuracy, optimality, search-quality improvement,
runtime completion — no live retrieval exists in P3/P4 by contract.

## L — P4-RA1/RA2 Final Closure

```yaml
resource_authority: >
  Budget rationale explains resource shape only. It cannot reintroduce scientific
  substructure, search strategy, or context-only downstream meaning beyond SRP.
s1:
  unadmitted central/vascular mechanism substructure removed
  repair-history prose removed from final BudgetEnvelope
  history preserved in budget_envelope.initial.json + evaluation/redigestion_record.json
s2:
  wide-net/search-strategy language removed
  evidence-saturation language retained
s5:
  animal-design importance context removed from AL03 resource rationale
  measurement/observability resource rationale retained
review_truth:
  6/6 source bindings valid
  6/6 budget-envelope bindings valid
  6/6 contextual review machine truth valid
shared_requirement:
  deduplication is route-based: same (requirement_id, route_id) cannot be duplicated;
  question cardinality does not multiply allocations
canonical_integrity: >
  Summary, Metrics, Reviews, Validator, and Manifest describe the same final state.
p4_ra1_meaningful_push_ci_cycles: 2
p4_ra2_meaningful_push_ci_cycles_current_step: 1
historical_note: >
  RA1 cycle 1 exposed stale canonical metrics after review-truth semantics changed;
  the validator correctly rejected the stale machine artifact.
```

## M — Next Step

**CQC-P5** — the CQC artifact chain is complete (CQS → SRP → BudgetEnvelope, all
frozen and machine-guarded); the next bounded phase is the MAFS integration adapter
(minimal, per master v0.2 §16), pending HO + ChatGPT authorization.
