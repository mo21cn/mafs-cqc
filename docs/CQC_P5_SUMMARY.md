# CQC-P5 — Structured Summary

## A — Acceptance Header

```yaml
contract_id: CQC-P5-MAFS-INTEGRATION-ADAPTER-ARTIFACT-LINEAGE-CLOSURE-v0.1
status: READY_FOR_REVIEW
repository: mo21cn/mafs-cqc
branch: dev/cqc-p5
cqc_p4_source_commit: (see docs/CQC_P4_METRICS.json evidence chain)
mafs_baseline_commit: cd09699fc8cc160ab5cfff00a41e714961dd2109
meaningful_push_ci_cycles_current_step: (see docs/CQC_P5_METRICS.json)
```

## B — Frozen Artifact Chain

```text
CQS      → admission commitment
SRP      → evidence-obligation commitment
BudgetEnvelope → resource-authority commitment
```

The validated chain Research Narrative → CQS → SRP → BudgetEnvelope is bound to
MAFS-native planning artifacts through the integration sidecar. A downstream layer
may consume an upstream commitment; it may not silently rewrite it.

## C — P5 Boundary

```text
P5 adds no fourth CQC cognitive artifact.
CQCMAFSIntegrationBinding is lineage-only:
identity, hash binding, route/allocation join, activation state,
stale-state detection, MAFS baseline pin, MAFS-native artifact references.
It records what was handed across the boundary; it does not decide what the
science means.
```

## D — Six-Case Lineage Matrix

| Case | CQS→SRP | SRP→Budget | Active Routes | Held Conditional | Source Context | Status |
|---|---:|---:|---:|---:|---|---|
| S1 | ✓ | ✓ | 2 | 2 | accessible | READY_FOR_MAFS_PREFLIGHT |
| S2 | ✓ | ✓ | 3 | 0 | accessible | READY_FOR_MAFS_PREFLIGHT |
| S3 | ✓ | ✓ | 1 | 3 | accessible | READY_FOR_MAFS_PREFLIGHT |
| S4 | ✓ | ✓ | 2 | 1 | accessible | READY_FOR_MAFS_PREFLIGHT |
| S5 | ✓ | ✓ | 3 | 1 | accessible | READY_FOR_MAFS_PREFLIGHT |
| S6 | ✓ | ✓ | 1 | 1 | accessible | READY_FOR_MAFS_PREFLIGHT |

## E — Three MAFS Planning Cases

Model-authored MAFS-native Axis/SearchOrder objects; deterministic layer validates
shape + lineage only.

| Case | CQC Route | MAFS Axis | MAFS SearchOrder | MAFS Preflight |
|---|---|---|---|---|
| M1 (S4 shared) | R01/entity_resource_identity (shared, CQ-01+CQ-02) | A1 resource-identity-confirmation | SO-A1-1 lookup_by_id | schema-valid, route-level single binding |
| M1 | R02/measurement_observability | A2 metadata-decidability | SO-A2-1 lookup_by_id | schema-valid |
| M2 (S6 instability) | R01/source_content_verification | A1 supplementary-material-content-verification | SO-A1-1 lookup_by_id | schema-valid |
| M3 (S5 STANDARD) | R01/mechanism_evidence | A1 mechanism-cascade-evidence | SO-A1-1 discovery_search | schema-valid |
| M3 | R02/historical_lineage | A2 prior-art-strategy-inventory | SO-A2-1 discovery_search | schema-valid |
| M3 | R03/measurement_observability | A3 single-cell-metabolomics-capability | SO-A3-1 discovery_search | schema-valid |

Model judgment: axis families, propositions, operation types, query representations.
Deterministic validation: schema conformance (pinned MAFS schemas), route binding
uniqueness, held-route non-activation, baseline pin. No deterministic route→axis
lookup table exists.

## F — S5 QUICK Negative Case

```text
INSUFFICIENT
R02/historical_lineage unfunded
integration blocked (INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT)
requirement preserved (unfunded list, not deleted, not downgraded)
```

## G — Stale-State Closure

Stale fixture: binding recorded at source state t; tampered upstream envelope
staged. `detect_stale()` returns stale; `mark_stale()` yields
STALE_SOURCE_CHAIN / STALE. Regeneration is required; the validator never
auto-regenerates. Re-digestion is incomplete while dependent integration state
still encodes the superseded source.

## H — Cognitive Checkpoint Preservation

```text
planning → discover() → STOP → explicit CandidatePointer selection → resolve()
```

The adapter contains no auto-selection (T8 AST scan: no candidates[0], no
auto_resolve/best_candidate/rank_and_select/select_candidate, no mafs_p0 import).
No end-to-end one-shot helper exists.

## I — MAFS Baseline

```yaml
pinned: cd09699fc8cc160ab5cfff00a41e714961dd2109
interface_state: MAFS v3.0-P1.5-RA3 closed execution-boundary state
modified: false
```

## J — Architecture Delta

```yaml
cqs_schema_changed: false
srp_schema_changed: false
budget_envelope_schema_changed: false
mafs_schema_changed: false
new_cqc_cognitive_artifact_types: 0
integration_binding_sidecar_added: true
new_semantic_scorers: 0
new_rankers: 0
new_solvers: 0
new_query_planners: 0
general_artifact_graph_added: false
candidate_auto_selection_added: false
mafs_production_modified: false
```

## K — Earned / Not Earned

**Earned:** CQS→SRP→BudgetEnvelope is consumable as a lineage-bound MAFS input
chain; resource authority survives integration; productive instability survives
(held, not pre-activated); shared requirements do not multiply execution by CQ
cardinality; budget insufficiency blocks execution without deleting epistemic
obligations; source revisions make dependent integration state stale; MAFS-native
planning objects can be authored from CQC commitments; MAFS's
discover→cognitive-checkpoint→resolve boundary survives integration (untouched).

**Not earned:** search recall improvement, scientific correctness, actual cost
prediction, completion within CQC ceilings, provider optimality, SearchOrder
optimality, automated candidate selection, EvidenceLandscapePackage completeness,
production merge. These require later evidence.

## L — Next Step

```text
CQC-UPSTREAM-FREEZE
```

(condition: P5 acceptance confirmed by HO + ChatGPT; any actual repository-side
merge into MAFS requires a separate bounded integration authorization)
