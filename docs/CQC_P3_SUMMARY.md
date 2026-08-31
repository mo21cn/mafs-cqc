# CQC-P3 — Canonical Summary (Final)

Human-readable canonical summary of final P3 state. Counts source from
`docs/CQC_P3_METRICS.json` (machine-derived from final artifacts by CQC-P3-RA3).
Integrity: `docs/CQC_P3_RA3_SHA256_MANIFEST.txt` (validator-enforced).

## A — Acceptance Header

```yaml
contract_id: CQC-P3-CONTEXTUAL-SEARCH-REQUIREMENT-DIGESTION-v0.1
current_phase_state: CQC-P3-RA3-CLOSED
repository: mo21cn/mafs-cqc
branch: dev/cqc-p3
contextual_case_count: 6
type_perturbation_case_count: 2
meaningful_push_ci_cycles_current_step: 1 (RA3 finalization)
```

The actual evidence commit SHA and CI run are reported externally in the Local Claw
return note (self-pinning retired per P2-RA2 §7).

## B — SRP v0.1 Frozen Shape

Final per-requirement fields: `requirement_id`, `target_question_ids`,
`evidence_need`, `epistemic_routes[{route_id, purpose, status, condition}]`,
`source_requirements`, `stopping_condition`, `uncertainty_binding`. Set envelope binds
the source CQS by id+SHA and the source narrative verbatim by SHA. Schema unchanged
since P3 freeze; no pressure earned a new field across 6 cases + 2 perturbations.

## C — Final Contextual Case Matrix

| Case | Final State | Conditional Routes | Key Boundary |
|---|---|---:|---|
| S1 | PASS | 2 | containment holds (population/resolution ambiguities stay conditional) |
| S2 | REPAIRED | 0 | evidence-state semantics, not search strategy |
| S3 | PRODUCTIVE_INSTABILITY_PRESERVED | 3 | terminology/entity ambiguity preserved |
| S4 | PASS | 1 | shared requirement retained (identity serves CQ-01+CQ-02) |
| S5 | REPAIRED | 1 | context resurrection closed |
| S6 | BOUNDARY_UNRESOLVED_PRESERVED | 1 | identity granularity preserved |

Counts are machine-derived from final artifacts (`docs/CQC_P3_METRICS.json`).

## D — Productive Instability

S3 and S6 show productive instability can survive downstream as conditional routes:
S3's referent ambiguity gates two inventory routes; S6's fuzzy reference keeps the
identity route conditional on ambiguity materiality. Neither collapsed into a silent
choice, and neither was a representation failure.

## E — Context Authority

Source context may interpret / qualify / condition admitted commitments. It may not
mint or resurrect obligations beyond the CQS admission boundary (S5's resurrected
animal-experiment-design obligation was removed and placed as importance context in
uncertainty_binding; admission synchronized).

## F — Type Perturbation

```yaml
T1 (s3 CQ-01 TERMINOLOGY_OR_NAMING -> ENTITY_RESOLUTION): VALID_PASS
T2 (s5 CQ-01 MECHANISM -> CAUSAL_CLAIM): INVALID_CONTROL_DESIGN
mechanical_identity_valid: 2
valid_experimental_controls: 1
invalid_experimental_controls: 1
second_valid_perturbation: NOT_AVAILABLE
```

At least one valid perturbation (T1) supports the claim that `question_type` did not
act as a hard router in that tested case. T2 is historical evidence of an invalid
control design, not evidence of type invariance.

## G — Canonical Machine Counts

```yaml
requirement_count_total: 16
route_count_total: 20
required_route_count: 12
conditional_route_count: 8
distinct_route_id_count: 8
shared_requirement_count: 1
orphan_requirement_count: 0
type_perturbation_mechanical_identity_valid_count: 2
type_perturbation_valid_control_count: 1
type_perturbation_invalid_control_count: 1
```

## H — Review / Integrity Truth

```yaml
contextual_review_source_cqs_sha256_verified: 6/6
contextual_review_srp_sha256_verified: 6/6
contextual_review_mechanical_fields_recomputed: 6/6
contextual_review_identity_fields_verified: 6/6
final_integrity_manifest: docs/CQC_P3_RA3_SHA256_MANIFEST.txt (validator-enforced)
```

## I — Architecture Delta

```yaml
cqs_schema_changed: false
srp_schema_changed: false
new_semantic_scorers: 0
new_hard_routers: 0
new_provider_routers: 0
new_query_generators: 0
new_budget_systems: 0
mafs_integrated: false
live_retrieval_added: false
```

## J — What P3 Earned / Did Not Earn

**Earned:**
- SRP v0.1 is a viable second digestion artifact.
- CQS remains the admission boundary.
- Source context may interpret / qualify / condition admitted commitments.
- Source context may not mint or resurrect obligations beyond CQS admission.
- S3 and S6 show productive instability can survive downstream as conditional routes.
- T1 is valid evidence that question_type is not acting as a hard router in that tested case.
- Review artifacts can be mechanically bound to the artifacts they evaluate.
- Source context was preserved in 6/6 cases.

**Not earned:**
- universal question_type invariance
- source-context incremental causal necessity beyond accepted CQS (NOT_ISOLATED)
- live retrieval improvement
- search-quality improvement
- budget efficiency

No broad Digestion Theory claim.

## K — Next Step

**CQC-P4** — the CQS→SRP chain is frozen with machine-enforced review truth and
integrity manifest; BudgetEnvelope can now be designed against the real
CQS+context→SRP→cost-shape chain.

---

# Historical Notes (superseded)

> **SUPERSEDED — P2-RA1 CORRECTION (retained for history)**: the original claim
> "material in 6/6 cases" conflated preserved availability with isolated incremental
> necessity. Final statement: source context was preserved and available in 6/6
> cases; incremental causal necessity beyond the accepted CQS was NOT_ISOLATED in P3.
>
> **SUPERSEDED — P3 pre-RA2 counts (retained for history)**: early P3 route and
> perturbation accounting was corrected in P3-RA2; the final canonical counts live in
> `docs/CQC_P3_METRICS.json` (16 requirements / 20 routes / 8 CONDITIONAL / 8
> distinct route IDs / 1 valid + 1 invalid perturbation control).
