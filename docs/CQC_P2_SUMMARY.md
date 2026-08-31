# CQC-P2 — Structured Summary

Human interpretation layer for HO + ChatGPT. Machine truth: `docs/CQC_P2_METRICS.json`,
`docs/CQC_P2_SHA256_MANIFEST.txt`, `benchmarks/p2/**`.

## A — Acceptance Header

```yaml
contract_id: CQC-P2-ARTIFACT-COMMITMENT-BOUNDARY-PROJECTION-LOSS-STRESS-v0.1
status: READY_FOR_REVIEW
repository: mo21cn/mafs-cqc
branch: dev/cqc-p2
verified_commit_sha: (pinned in docs/CQC_P2_METRICS.json)
ci_run_id: (pinned in docs/CQC_P2_METRICS.json)
semantic_case_count: 6
revision_topology_case_count: 2
meaningful_push_ci_cycles: 1
```

## B — Master Contract Alignment

v0.2 retired the v0.1 "Granularity & Dependency Closure" P2 after P1 showed that
mechanical validity ≠ semantic digestion and that substantive coverage is at
parity between direct and typed paths. The rebaselined P2 tests two different
things: (A) where converting contextual cognition into a discrete CandidateQuestionSet
starts to distort intent (projection loss, false precision, context collapse), and
(B) whether the lightweight identity/hash/derived-from discipline survives harder
revision topologies (fan-out diamond, sequential revision, partial regeneration)
without a graph framework. The seven-field schema was stress-tested, not extended.
"Recursion" was retired as an architecture claim; state-transition vocabulary is used.

## C — Semantic Stress Matrix

Columns C-J are Local Claw preliminary observations only; **final status PENDING_HO_CHATGPT**.

| Case | Input Type | CQ Count | Ambiguity Visible | Possible Projection Loss | Possible False Precision | Over/Under Decomp | Type Boundary Note | HO+ChatGPT Status |
|---|---|---:|---|---|---|---|---|---|
| s1_vms_cellular_mechanism | RAW | 3 | yes (population, omics-vs-imaging) | "请搜索" action intent projected out by design; 潮热/盗汗 concretization recorded | none | none | types clean | PENDING_HO_CHATGPT |
| s2_vcell_paradigm | RAW | 3 | yes (criterion, typo) | implicit time-window of "产生了" has no field | none | none | NOVELTY/TERMINOLOGY/LINEAGE split cleanly | PENDING_HO_CHATGPT |
| s3_antagonist_domains | RAW | 4 | yes (referent, dimension) | 研究 dual sense folded into inventory scope | none | none (heavy-ambiguity 4-way split judged faithful; HO to confirm) | CQ-01 dual-plausible TERMINOLOGY vs ENTITY_RESOLUTION — recorded in uncertainty, descriptive choice | PENDING_HO_CHATGPT |
| s4_avca_donor_data | RAW | 3 | yes (thresholds, repetition) | none | none | none | types clean; session-memory asymmetry recorded (dual-gate produced directly, RA1 prior absorbed) | PENDING_HO_CHATGPT |
| s5_mixed_commitment | SYNTHETIC_STRESS | 4 | yes (primary dimension absent by design; metabolite species unspecified) | 具体表型 ("代谢影像变化") not invented | none (oncometabolite naming deliberately withheld) | none | **core finding: 4 types across one case — no single type summarizes it; honest iff type is not a hard router** | PENDING_HO_CHATGPT |
| s6_narrow_source_check | SYNTHETIC_STRESS | 1 | yes (author+year fuzzy reference) | identity-resolution path kept inside resolution_condition by design | none | none — 1-CQ output is the faithful digestion; over-decomposition would be the failure | SOURCE_CONTENT clean | PENDING_HO_CHATGPT |

## D — Seven-Field Contract Pressure

```yaml
cases_requiring_no_new_field: 6
cases_with_possible_schema_pressure: 0
possible_missing_representation: none required by the executed cases; nearest candidate was a "time-window" qualifier for s2 (handled by source_narrative context reservoir) and an "interpretation-basis" note for s3 (handled by uncertainty)
schema_changed: false
```

## E — Question-Type Boundary Findings

- Clean single-type: s1 (3 types), s4, s5 (4 distinct types), s6 (1 type).
- Multiple plausible types on one question: s3 CQ-01 (TERMINOLOGY_OR_NAMING vs
  ENTITY_RESOLUTION) — resolved descriptively, tension preserved in uncertainty;
  not scored, not routed on.
- Type seemed immaterial to interpretation: none observed in this set.
- No confidence/boundary-distance field proposed: no measured failure requires it.

## F — Revision Robustness

```yaml
R1_diamond:
  scenario: A0 → {B0, C0} → D0 (multi-source); revise A0→A1; regenerate B1, C1, D1
  initial_state: all current
  revision: A0 superseded; B0/C0 stale; D0 transitively stale (validator-proven)
  regeneration: B1/C1/D1 current
  status: PASS (expected_state.json fully matched; no propagation engine)
R2_sequential:
  scenario: A0 → {B0, C0}; A0→A1; regenerate B1 only; then A1→A2 with nothing regenerated
  states: after-partial → B1 current, C0 stale; after-A2 → B1 stale, C0 stale
  status: PASS (partial stale detection and repeated-revision detection both proven)
```

Multi-source binding for D0/D1 is benchmark-only (list of {artifact_id, revision,
content_sha256}); no production artifact family and no graph framework were created.

## G — Architecture Delta

```yaml
candidate_question_schema_changed: false
new_production_artifact_types: 0
new_semantic_scorers: 0
new_dependency_solvers: 0
new_graph_frameworks: 0
new_propagation_engines: 0
new_llm_runtime_frameworks: 0
live_retrieval_added: false
mafs_integration_performed: false
```

Implementation delta: `scripts/validate_p2.py`; `benchmarks/p2/**`; `tests/test_p2.py`
(P2 invariants); CI step; Master v0.2 unchanged copy in repo root. No production
logic changes to the P0 surface.

## H — Machine Validation

```yaml
semantic_packages_complete: 6/6
cqs_schema_validation: 6/6
source_hash_validation: 6/6
source_trace_exact_validation: 6/6
dependency_dag_validation: 6/6
render_reproducibility: 6/6
projection_review_records: 6/6
r1_stale_detection: PASS (incl. transitive stale through the diamond)
r2_partial_and_repeated_stale_detection: PASS
test_result: 28 PASS
repository_hygiene: PASS
```

## I — P2 Finding

The boundary between useful commitment and destructive overcommitment turned out to
be governed by two existing fields, not by new ones. Wherever the source narrative
genuinely under-specified intent (populations, thresholds, criteria, referents), the
uncertainty field carried the ambiguity forward without breaking any downstream
check — s4 and s5 are the clearest cases, where an existence claim and a four-way
mixed commitment respectively remained fully schema-valid while visibly unresolved.
Where the model added specificity the source did not contain (s1's "潮热/盗汗"), the
projection was conservative and recorded. False precision never had to be invented:
the only near-miss was s3's dual-plausible type on CQ-01, which the descriptive
type vocabulary absorbed without becoming a router. On the revision side, the
lightweight identity/hash/derived-from model survived both hard topologies: the
diamond's transitive staleness and R2's partial regeneration were both provable
from content hashes alone, with the one real engineering fault (EOL drift breaking
byte-level binding) already fixed at RA1. The honest limit of this evidence: all
semantic observations are Local Claw preliminary — HO + ChatGPT own the projection-
loss verdicts; and the seven-field contract has now been stressed across 11 cases
(5 P1 + 6 P2) without a failure that earns a new field.

## J — Next-Step Recommendation

**CQC-P3** — the commitment boundary held under stress and the lineage model held
under harder topologies, so the next valuable digestion transition is the one the
master v0.2 sequence names: contextual Search Requirement digestion (CQS + source
context → SRP), under the rule that question_type may cue but never route.
