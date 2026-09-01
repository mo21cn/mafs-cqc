# CQC-P5 — Structured Summary

## A — Acceptance Header

```yaml
contract_id: CQC-P5-MAFS-INTEGRATION-ADAPTER-ARTIFACT-LINEAGE-CLOSURE-v0.1
current_phase_state: READY_FOR_REVIEW
repository: mo21cn/mafs-cqc
branch: dev/cqc-p5
cqc_p4_source_commit: 8028e17a6eaab364c744cfa72b714f0f0bd6cf01
mafs_baseline_commit: cd09699fc8cc160ab5cfff00a41e714961dd2109
meaningful_push_ci_cycles_current_step: 1
```

`cqc_p4_source_commit` is the exact 40-char SHA of the P4-RA2 final-gate
acceptance commit (`CQC-P4-RA2-FINAL-GATE: coverage fixture uses Path object for
PKG monkeypatch + manifest entry rebound for tests/test_p4_ra2.py`)
on `dev/cqc-p4`, frozen into this summary per Closure H. No indirect
`see other artifact` reference; the SHA itself is pinned.

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

## E — Three MAFS Planning Cases (schema-validated, not preflight-executed)

Model-authored MAFS-native Axis/SearchOrder objects; deterministic layer validates
shape + lineage only.

| Case | CQC Route | MAFS Axis | MAFS SearchOrder | MAFS Native Planning Schema Validation |
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

**Full MAFS preflight was not executed in P5 and remains a repository-side
integration concern.** The validation performed here is shape + lineage only;
`MAFS.run_preflight()` would also require `CompiledTarget`, `ProviderManifest`,
`NegotiationResult`, compiled queries, `GateDependencyGraph`, runtime
fingerprint, `BudgetState`, and the target-freeze path. None of these MAFS-native
context objects are fabricated in P5; producing them would be repository-side
work outside the CQC line.

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
chain; resource authority survives integration (FEASIBLE / CONSTRAINED /
INSUFFICIENT preserved as three distinct resource states); productive
instability survives (held, not pre-activated); shared requirements do not
multiply execution by CQ cardinality; budget insufficiency blocks execution
without deleting epistemic obligations; source revisions make dependent
integration state stale; MAFS-native planning objects can be authored from CQC
commitments and their shape is schema-validated against the pinned MAFS
schemas; MAFS's discover→cognitive-checkpoint→resolve boundary survives
integration (untouched).

**Not earned:** full MAFS `run_preflight()` execution (NOT_EVALUATED — out of
scope for P5); search recall improvement, scientific correctness, actual cost
prediction, completion within CQC ceilings, provider optimality, SearchOrder
optimality, automated candidate selection, EvidenceLandscapePackage completeness,
production merge. These require later evidence or out-of-scope work.

## L — Next Step

```text
Immediate next step: CQC-UPSTREAM-FREEZE
Post-freeze integration path: MAFS-REPOSITORY-SIDE-INTEGRATION / Path C
```

Per CQC-P5-RA1-CI1 §15, the immediate next step after P5 final acceptance
is **CQC-UPSTREAM-FREEZE** (P5 closure acceptance → CQC upstream line
freeze). Only after that freeze may a separate bounded contract authorize
**MAFS-REPOSITORY-SIDE-INTEGRATION** (the thin MAFS-side consumer adapter
against the pinned/versioned CQC artifact protocol) per CQC-P5-RA1
Amendment A — Path C.

The freeze sequence:

```text
CQC-P5 acceptance (CI1)
  ↓
CQC-UPSTREAM-FREEZE            (P5 closure final; CQC upstream line frozen)
  ↓
separate bounded authorization
  ↓
MAFS-REPOSITORY-SIDE-INTEGRATION / Path C   (thin MAFS-side consumer adapter)
```

# `P5-RA1 Final Closure`

## A. Cross-Repo CI Isolation

CQC pytest collection is scoped to `./tests`. External MAFS tests under
`external/mafs-v3-p0/tests/` are not collected as CQC tests. The CI step that
previously ran `python -m pytest -q` from the repository root (which caused
duplicate `test_p1_ra1` module basename collision with the CQC-owned test of
the same name) now runs `python -m pytest -q tests`.

## B. MAFS Test Schema Path

`MAFS_BASELINE_DIR` is the single path contract for the validator and the
tests. The previous hardcoded sibling path `PKG.parent / "mafs-v3-p0" /
"schemas"` in `tests/test_p5.py` is replaced with
`Path(os.environ.get("MAFS_BASELINE_DIR", <local default>)) / "schemas"`. CI
sets `MAFS_BASELINE_DIR=${{ github.workspace }}/external/mafs-v3-p0` for both
the validator and the test step. In CI, `pinned_mafs_schema_tests_execute_in_ci: true`.

## C. Resource-State Truth

```text
FEASIBLE ≠ CONSTRAINED ≠ INSUFFICIENT
CONSTRAINED is no longer collapsed into INSUFFICIENT.
```

The adapter's binding-status branch now preserves CONSTRAINED as a distinct
upstream envelope state and maps it to `READY_FOR_MAFS_PREFLIGHT` (with the
resource constraint recorded in the upstream BudgetEnvelope, not in the
binding-status field). A regression test exercises a constructed CONSTRAINED
envelope with `unfunded_obligations=[]` and asserts the binding is not
`INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT`.

## D. Full Source-Chain Truth

The canonical P5 validator (`scripts/validate_p5.py::ctx_binding_errors`)
imports and calls `adapter.verify_source_chain()` rather than re-implementing
the CQS↔SRP↔BudgetEnvelope hash and id checks. There is one source-chain truth
implementation with multiple consumers (adapter + validator). On any source-
chain mismatch the canonical validator fails with the adapter's existing
stable failure semantics (`CQC_SOURCE_CHAIN_MISMATCH`).

A negative regression test (`test_p5.py::TestT1bSourceChainNegative::test_wrong_srp_source_cqs_sha256`)
mutates `srp.source_cqs_sha256` to a wrong value while leaving the binding
internally self-consistent, and asserts P5 validation fails with
`CQC_SOURCE_CHAIN_MISMATCH`. This proves the canonical validator no longer
validates only the sidecar's local copies.

## E. MAFS Compatibility Claim

```text
3/3 MAFS-native planning packages schema-validated.
Full MAFS preflight NOT_EVALUATED.
```

The previous overclaimed `mafs_preflight_evaluated_count: 3` (which implied
`MAFS.run_preflight()` was executed) is replaced with
`mafs_native_planning_schema_evaluated_count: 3` + `mafs_full_preflight_evaluated_count: 0`
+ `mafs_full_preflight_status: "NOT_EVALUATED"`. No fake MAFS preflight
objects are fabricated; the claim is narrowed to the evidence actually
earned.

## F. Integration Review

Per-case `evaluation/integration_review.json` artifacts are present for
**6 contextual + 3 MAFS-planning = 9 total** (per CQC-P5-RA1-CI1 Closure C).

The review inventory distinguishes three layers:

```text
mechanical review truth
  machine-derived: source-chain, route-join, conditional non-activation,
  MAFS baseline pin, MAFS-native schema validity, stale-state, search-
  order lineage traceability. 9/9 PASS.

Local Claw preliminary semantic review
  authored_by: LOCAL_CLAW (planning) | MACHINE_DERIVED (contextual).
  3/3 planning cases completed by Local Claw after reading M1/M2/M3
  artifacts (source_cqs.json, source_srp.json, budget_envelope.json,
  integration_binding.json, mafs_planning.json).
  6/6 contextual cases set planning-specific fields to NOT_APPLICABLE
  (no MAFS-native planning object exists for contextual cases).

HO+ChatGPT final semantic adjudication
  3/3 PENDING_HO_CHATGPT (CI1 must not self-sign PASS).
```

The P5-RA1 contract's "structural traceability != semantic containment"
rule (Closure A) is enforced by separating `mechanical` (machine-derived
from structural artifacts) from `local_claw_preliminary_review` (Local
Claw inspects M1/M2/M3 and records observed conclusions) and
`final_semantic_adjudication` (PENDING_HO_CHATGPT).

## G. Canonical State

Machine artifacts do not claim `CQC-P5-CLOSED` before independent CI proves
closure. The previous premature `current_phase_state: "CQC-P5-CLOSED"` (in
the metrics file while cross-repo CI was red) is replaced with
`current_phase_state: "READY_FOR_REVIEW"`. The final closure script / workflow
would update to CLOSED only after a green CI run; the metrics file does not
encode CLOSED as a machine field that pre-empts the CI verdict.

## H. P4 Source Baseline

```text
cqc_p4_source_commit: 8028e17a6eaab364c744cfa72b714f0f0bd6cf01
```

The exact 40-char SHA of the P4-RA2 final-gate acceptance commit
(`CQC-P4-RA2-FINAL-GATE: coverage fixture uses Path object for PKG
monkeypatch + manifest entry rebound for tests/test_p4_ra2.py`) is
written directly into this summary and into `docs/CQC_P5_METRICS.json`. No
indirect "see docs/CQC_P4_METRICS.json" reference; no use of the current
P5 HEAD as a substitute for the P4 source baseline.

## I. Canonical Integrity

```text
Summary
Metrics
Reviews
Validator
Manifest
```

all describe the same final P5 state.

- Summary: this document.
- Metrics: `docs/CQC_P5_METRICS.json`.
- Reviews: `benchmarks/p5/**/evaluation/integration_review.json` (9 files).
- Validator: `scripts/validate_p5.py` and `integration/mafs_v3/{adapter,validator}.py`.
- Manifest: `docs/CQC_P5_SHA256_MANIFEST.txt`.

## J. Next Step

`CQC-UPSTREAM-FREEZE` (immediate); `MAFS-REPOSITORY-SIDE-INTEGRATION` /
Path C (post-freeze; per CQC-P5-RA1-CI1 §15).
