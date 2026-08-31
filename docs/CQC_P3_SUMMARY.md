# CQC-P3 — Structured Summary

Human interpretation layer for HO + ChatGPT. Machine truth: `docs/CQC_P3_METRICS.json`,
`docs/CQC_P3_SHA256_MANIFEST.txt`, per-case `evaluation/*`.

## A — Acceptance Header

```yaml
contract_id: CQC-P3-CONTEXTUAL-SEARCH-REQUIREMENT-DIGESTION-v0.1
status: READY_FOR_REVIEW
repository: mo21cn/mafs-cqc
branch: dev/cqc-p3
contextual_case_count: 6
type_perturbation_case_count: 2
meaningful_push_ci_cycles: (see docs/CQC_P3_METRICS.json)
```

The actual evidence commit SHA and CI run are reported externally in the Local Claw
return note (self-pinning retired per P2-RA2 §7).

## B — SRP v0.1 Schema Decision

Final per-requirement fields: `requirement_id`, `target_question_ids`,
`evidence_need`, `epistemic_routes[{route_id, purpose, status, condition}]`,
`source_requirements`, `stopping_condition`, `uncertainty_binding`. Set envelope binds
the source CQS by id+SHA and the source narrative verbatim by SHA.

- `target_question_ids` (1..n) exists so one obligation can serve several CQs (S4's
  shared identity requirement) without duplicating requirements.
- `epistemic_routes.status` carries exactly REQUIRED/CONDITIONAL — CONDITIONAL is the
  mechanism that consumes uncertainty without collapsing it (P3-C).
- `stopping_condition` is epistemic (what evidence state suffices), never budgetary.
- `uncertainty_binding` is free text carrying forward what would change routes/sources.
- **Rejected imagined fields**: route priority, route confidence, provider hints,
  query templates, cost fields, a closed route ontology (six cases needed 6 distinct
  descriptive route_ids across cases — open vocabulary sufficed), per-requirement
  dependency edges between requirements (the CQS dependency edges already carry the
  ordering information).
- **Schema pressure observed**: none — all six cases represented honestly in the
  provisional shape with zero structural deviations.

## C — Contextual SRP Matrix

All final semantic statuses: **PENDING_HO_CHATGPT** (Local Claw preliminary only).

| Case | CQs | SRP Requirements | Conditional Routes | Source Context Contribution | Preliminary Concern | HO+ChatGPT Status |
|---|---:|---:|---:|---|---|---|
| s1_vms_cellular_mechanism | 3 | 3 | 2 | material (search-request intent + population scope justify R02) | none observed | FINALIZED (P3-RA2) |
| s2_vcell_paradigm | 3 | 3 | 0 (1 gated by CQS dep) | material (narrative brevity justifies wide-net-then-filter) | none | FINALIZED (P3-RA2) |
| s3_antagonist_domains | 3 | 3 | 4 | material (10-char narrative makes disambiguation the gate) | none | FINALIZED (P3-RA2) |
| s4_avca_donor_data | 3 | 3 | 1 | material (named resource + undefined thresholds exist only in source) | none | FINALIZED (P3-RA2) |
| s5_mixed_commitment | 3 | 3 | 1 | material (design-constraint linkage exists only in source) | none | FINALIZED (P3-RA2) |
| s6_narrow_source_check | 1 | 1 | 1 | material (fuzzy reference style makes identity route conditional) | none | FINALIZED (P3-RA2) |

## D — Productive Instability Consumption

```yaml
s3_antagonist_domains:
  uncertainty: 拮抗剂 referent range (pharmacological vs muscle vs other) + inventory dimension
  conditional_route: domain_coverage_inventory [CONDITIONAL] gated on R01 disambiguation;
    terminology_boundary [CONDITIONAL] on competing readings
  silent_collapse_observed: false
s6_narrow_source_check:
  uncertainty: fuzzy author+year reference; identity granularity use-dependent
  conditional_route: entity_resource_identity [CONDITIONAL] — activates only when
    reference ambiguity becomes material; otherwise embedded in source-content verification
  silent_collapse_observed: false
```

## E — Question-Type Non-Authority Stress

| Case | Original Type | Perturbed Type | Non-type Fields Identical | SRP Structural Diff | Hard-Routing Leak | Status |
|---|---|---|---|---|---|---|
| T1 (s3 CQ-01) | TERMINOLOGY_OR_NAMING | ENTITY_RESOLUTION | yes (all five non-type fields) | none — identical requirement set/routes | none observed | FINALIZED (P3-RA2) |
| T2 (s5 CQ-01) | MECHANISM | CAUSAL_CLAIM | yes | none — mechanism_evidence route unchanged | none observed | FINALIZED (P3-RA2) |

T2 honesty caveat: CAUSAL_CLAIM's plausibility was not pre-registered in the P2
record; the stress simultaneously probed whether an unregistered plausible relabeling
changes SRP behavior — it did not.

## F — Source Context Findings

> **P2-RA1 CORRECTION**: the original claim "material in 6/6 cases" conflated preserved availability with isolated incremental necessity. Corrected statement: **source context was preserved and available in 6/6 cases; the present P3 design did not isolate its incremental causal contribution beyond the accepted CQS.** Per-case observations below are interpretive observations on how context was used, not isolated causal evidence.

Per-case `source_context_contribution`: **preserved-and-available in 6/6 cases** (recorded in contextual_review.json with the specific justification; `incremental_necessity_tested: false`, `conclusion: NOT_ISOLATED`). Summarized: the
source narrative materially shaped the SRP in every case — through the
search-request phrasing (s1), brevity-driven strategy (s2), ambiguity weight (s3), named-object + threshold gaps (s4), design-linkage statement (s5), and reference
fuzziness (s6). No case reported `none`; no value was manufactured. The causal-isolation claim is retired.

## G — Requirement Admission

Final requirement count: **16** across 6 SRPs (3/3/3/3/3/1). Requirements removed
before freeze: **0** (first-pass admission held). Shared requirements observed: **1**
(s4 R01 — Atlas identity serves CQ-01 and supplies CQ-02's inventory source).
Orphan requirements: **0** (validator-enforced).

## H — Execution Leakage Audit

```yaml
provider_names_added: 0
exact_queries_added: 0
budget_fields_added: 0
execution_order_fields_added: 0
```

Named source objects inherited from narratives and reported separately: Arc Virtual
Cell Atlas (s4, target evidence object), Gould 2022 Cell Reports paper (s6, target
evidence object). Both are the §14 exception (named evidence object ≠ search
provider); the leakage scanner (Crossref/PubMed/Google Scholar/top-k/API endpoint/
HTTP/token budget/query string/provider fallback/resolver call) reports 0 hits.

## I — Architecture Delta

```yaml
candidate_question_schema_changed: false
srp_artifact_type_added: true
new_semantic_scorers: 0
new_hard_routers: 0
new_provider_routers: 0
new_query_generators: 0
new_budget_systems: 0
mafs_integrated: false
live_retrieval_added: false
```

SRP v0.1 is the second artifact type earned by the development line (per master
v0.2 §16: each artifact must earn its existence — P3's six cases are that evidence).

## J — P3 Finding

P3's central result is that the second digestion transition worked **by consuming,
not collapsing**: every SRP was digested from the full contextual state (CQS +
verbatim narrative), and every unresolved ambiguity in the CQS re-appeared in the
SRP as a CONDITIONAL route or an uncertainty binding rather than a silent choice.
The strongest evidence is structural: 8 of 20 routes are CONDITIONAL (16 requirements across 6 cases), and the
two cases designed around productive instability (s3, s6) produced exactly the
gated topologies the P2 findings predicted. The type-perturbation stress showed the
one valid perturbation (T1, pre-registered plausible) supports that the type label did not act as a hard router; the second perturbation was an invalid control (unregistered plausibility) and is not counted —
including an unregistered relabeling (T2) — meaning `question_type` currently has
no hidden routing power. Source-context retention: **preserved and available in 6/6 cases; incremental
causal necessity beyond the accepted CQS was not isolated in P3** - in each case,
at least one SRP feature (a conditional route, a shared obligation, or a
named-object exception) drew on content present only in the narrative, which is
preserved-and-available evidence, not isolated causal proof.
The honest limit: SRP quality itself (are these the right evidence obligations?) is
a semantic judgment that remains with HO + ChatGPT, and no live retrieval has
tested whether these obligations improve downstream search.

## K — Next Step Recommendation

**CQC-P4** — with SRP v0.1 frozen and P2/P3 semantics stable, the lightweight
BudgetEnvelope phase (master v0.2 §19) can now be designed against a real artifact
chain (CQS+context→SRP→cost shape) instead of the retired question-type→cost-shape
model.
