# CQC-P1-RA1 — Structured Summary

Human interpretation layer for HO + ChatGPT. Machine truth: `docs/CQC_P1_RA1_METRICS.json`,
`docs/CQC_P1_RA1_SHA256_MANIFEST.txt`, per-case `evaluation/ra1_adjudication.md`.

## A — Acceptance Header

```yaml
contract_id: CQC-P1-RA1-EXPERIMENTAL-TRUTH-LINEAGE-EARNED-REDIGESTION-CLOSURE-v0.1
status: READY_FOR_REVIEW
repository: mo21cn/mafs-cqc
branch: dev/cqc-p1
verified_commit_sha: (pinned in docs/CQC_P1_RA1_METRICS.json)
ci_run_id: (pinned in docs/CQC_P1_RA1_METRICS.json)
benchmark_case_count: 5
arm_c_triggered_count: 3
meaningful_push_ci_cycles: 1
```

## B — Machine Lineage Closure

| Case | Raw SHA | Arm A SHA Match | Arm B SHA Match | Arm C SHA Match |
|---|---|---|---|---|
| case_vms_mechanism | c0600db6… | ✅ (fixed) | ✅ (fixed) | n/a |
| case_vcell_scope | aac9f8ba… | ✅ (fixed) | ✅ (fixed) | ✅ |
| case_vcell_paradigm | 37f34e94… | ✅ (fixed) | ✅ (fixed) | n/a |
| case_antagonist_domains | 5975fee3… | ✅ (fixed) | ✅ (fixed) | ✅ |
| case_avca_donor_data | 7b136c4d… | ✅ (fixed) | ✅ (fixed) | ✅ |

All 10 downstream preparations carried hand-copied incorrect hashes at P1 (first
12 hex chars correct, tails wrong); repaired mechanically without regenerating any
model content. `validate_p1.py` now enforces the invariant (metadata == every
present arm's `raw_input_sha256`) and fails on mismatch — verified by 6 new tests.

## C — Baseline Reinterpretation

```text
Arm A = direct downstream artifact (downstream_preparation.json: questions, order,
        missing-information, reasoning notes — free-form, downstream-specific
        interpretive state)
Arm B = typed intermediate CandidateQuestionSet + downstream artifact
        (question-addressable, source-traced, dependency-structured interpretive state)
```

P1 claims **withdrawn or narrowed** (from `docs/CQC_P1_SUMMARY.md` and per-case
adjudications):

1. "Arm A: no artifact / traceability none" — **withdrawn**. Arm A writes a durable
   downstream JSON; its interpretive state is free-form but present and recorded.
2. "Arm A interpretation choices are inherently unrecoverable" — **narrowed** to:
   they are recoverable from Arm A's prep document by reading it, but are not
   question-addressable, not source-traced, and not structurally gating.
3. "Arm B recovered the typo/repetition as coverage" — **withdrawn**. Per §5 the
   typo and the 有没有有没有 repetition are interpretive constraints / input noise;
   they earn interpretive-state-capture credit, not substantive coverage credit.
4. "Arm B dependency edges all survive the RA2 test" — **narrowed**: 4 edges were
   declared passing; HO acceptance found 1 false prerequisite and 2 missing
   prerequisites among them (all repaired via earned Arm C this round).
5. "Substantive coverage parity" — **retained** after reference-set separation
   (all 5 cases: Arm A and final explicit-digestion artifact both 100% on
   substantive targets).

## D — Reference-Set Re-adjudication

Per-case three-way separation (full detail in each `ra1_adjudication.md`):

```yaml
case_vms_mechanism:
  substantive_targets: [cell-resolution mechanism landscape (central + vascular)]
  interpretive_constraints: [population scope, omics-vs-imaging]
  noncritical_input_noise: []
case_vcell_scope:
  substantive_targets: [direction inventory]
  interpretive_constraints: [typo disposition, adjacent-term boundary]
  noncritical_input_noise: []
case_vcell_paradigm:
  substantive_targets: [candidate paradigms, lineage]
  interpretive_constraints: [paradigm-judgment criterion undefined]
  noncritical_input_noise: [Virtual Cel spelling (same-origin as scope case)]
case_antagonist_domains:
  substantive_targets: [application-domain inventory, research-tool usage]
  interpretive_constraints: [antagonist referent range, inventory dimension]
  noncritical_input_noise: []
case_avca_donor_data:
  substantive_targets: [donor-data existence in Atlas]
  interpretive_constraints: [young/healthy/primary thresholds (materially binds the existence claim), atlas identity]
  noncritical_input_noise: [有没有有没有 repetition]
```

Substantive coverage after re-adjudication: Arm A 5/5 cases full; final
explicit-digestion artifact (B or C) 5/5 cases full. Parity holds on the
**substantive** dimension; the differentiators live in interpretive-state capture,
addressability, lineage, and dependency truth.

## E — Initial Arm B Failure Ledger

```yaml
case_vms_mechanism:
  dependency_failures: []
  missing_prerequisites: []
  other_semantic_failures: []
case_vcell_scope:
  dependency_failures: [CQ-01→CQ-02 false prerequisite]
  missing_prerequisites: []
  other_semantic_failures: []
case_vcell_paradigm:
  dependency_failures: []
  missing_prerequisites: []
  other_semantic_failures: []
case_antagonist_domains:
  dependency_failures: [CQ-02→CQ-01 confirmed valid]
  missing_prerequisites: [CQ-03 assumed pharmacological reading while independent of CQ-01]
  other_semantic_failures: []
case_avca_donor_data:
  dependency_failures: [CQ-02→CQ-01 confirmed valid]
  missing_prerequisites: [CQ-02 not gated on CQ-03 despite prep stating CQ-03 binds the answer]
  other_semantic_failures: []
```

Three mandatory triggers (contract §1.3) all present: vcell_scope, antagonist_domains, avca_donor_data.

## F — Arm C Re-digestion Ledger

```yaml
case_vcell_scope:
  prior_artifact: CQS-CQC-P1-02 (preserved, untouched)
  conflict: CQ-01→CQ-02 false prerequisite
  diagnosis: RA2 rule — inventory searchable without adjacent-term boundary
  repair: CQ-01.dependencies = []
  revised_artifact: CQS-CQC-P1-02-RC1
  repair_effect: inventory independently searchable; CQ-02 remains as constraint question
  new_failure_introduced: none
case_antagonist_domains:
  prior_artifact: CQS-CQC-P1-04 (preserved, untouched)
  conflict: CQ-03 assumed pharmacological reading while independent
  diagnosis: missing prerequisite / premature semantic branch
  repair: CQ-03.dependencies=[CQ-01]; assumption made explicit in uncertainty
  revised_artifact: CQS-CQC-P1-04-RC1
  repair_effect: premature branch declared and gated
  new_failure_introduced: none
case_avca_donor_data:
  prior_artifact: CQS-CQC-P1-05 (preserved, untouched)
  conflict: CQ-02 not gated on CQ-03 despite prep stating CQ-03 binds the answer
  diagnosis: missing prerequisite / stage-referential contradiction
  repair: CQ-02.dependencies=[CQ-01, CQ-03]
  revised_artifact: CQS-CQC-P1-05-RC1
  repair_effect: existence answer structurally bound to standards decidability
  new_failure_introduced: none
```

Lineage mechanically verified: prior hash binds the untouched Arm B file; revised
differs from prior; revised passes P0 schema/DAG; Arm C raw hash binds case input;
render reproducible.

## G — Final A vs Explicit-Digestion Comparison

- **Substantive coverage**: parity 5/5 both arms (after noise/constraint separation).
- **Intent preservation**: both arms preserve intent; Arm B's preservation is
  question-addressable and source-traced.
- **Interpretive-state capture**: Arm A captures it free-form inside the prep
  document; Arm B captures it as typed per-question fields. Same information,
  different addressability.
- **Addressability**: Arm B's state is addressable per question (amend CQ-02's
  uncertainty without touching the artifact's other content); Arm A's is
  document-addressable only.
- **Lineage**: both arms now bind the raw input hash mechanically; Arm B/C
  additionally chain CQS → revision lineage (prior hash, conflict, diagnosis).
- **Dependency truth**: after earned re-digestion, final explicit-digestion
  artifacts carry 2 edges total (case_vcell_scope: 0; case_antagonist_domains: 2 —
  CQ-02→CQ-01, CQ-03→CQ-01; case_avca_donor_data: 2 — CQ-02→CQ-01, CQ-02→CQ-03;
  case_vms/paradigm: 0/1), every edge with a stated prerequisite rationale.
- **Cross-stage consistency**: the one observed stage-referential contradiction
  (avca CQ-02/CQ-03) existed in the *typed* artifact and was caught — typedness
  made the contradiction checkable.
- **Local repairability**: demonstrated by three minimal re-digestions (1–2 field
  edits each) with zero regeneration of unrelated content.
- **Repeated-reasoning cost**: unchanged from P1 (1 generation pass per arm;
  assembly/render are mechanical).

## H — Success Symmetry Ledger

- Single-case observation: typedness exposing a stage-referential contradiction
  (avca) — occurred once.
- Repeated heterogeneous observation: interpretation-choice externalization in
  explicit-digestion artifacts (5/5 cases, now including the corrected view that
  Arm A externalizes too — the difference is typedness/addressability, not
  existence).
- Candidate capability: local, targeted re-digestion from explicit conflict
  (demonstrated 3/3 with zero new failures).
- Not yet earned invariant: that typed intermediates improve *retrieval outcomes*
  — still unmeasured (no live retrieval in this line by contract).

## I — Architecture Delta

```yaml
candidate_question_schema_changed: false
new_production_artifact_types: 0
new_semantic_scorers: 0
new_rankers: 0
new_solvers: 0
new_llm_runtime_frameworks: 0
live_retrieval_added: false
mafs_integration_performed: false
srp_implemented: false
budget_implemented: false
```

Implementation delta: `validate_p1.py` downstream-hash invariant + arm_c path fix;
`tests/test_p1_ra1.py` (6 tests); 3 Arm C packages; 5 re-adjudication files; RA1
docs. Zero production-logic changes to the P0 surface.

## J — Digestion Finding

RA1's central lesson is that the experiment was wrong before its conclusions were:
all ten downstream artifacts bound hand-copied hashes while every validator passed
— provenance must be enforced, not self-attested. The reframed comparison also
changed what the artifact debate is about: both arms write durable artifacts, so
the real question is whether a typed intermediate makes interpretive state more
addressable and locally repairable. The three earned re-digestions show it does in
one specific way: a typed artifact lets a semantic error be *located* (which
question, which field), *gated* (blocking edge), and *repaired locally* (1–2 field
edits) without touching anything else — while the failed prior artifact stays on
record. Just as important is what RA1 refused: P1 had counted typo and repetition
handling as scientific coverage; separating substantive targets from interpretive
constraints showed that "coverage" was parity all along, and the honest claim is
narrower than the original but now stands on clean evidence.

## K — Next-Step Recommendation

**CQC-P2** — with the P1 experiment now truthful (lineage enforced, reference
sets separated, earned re-digestions closed), the next measured-failure driver for
granularity/dependency closure can only come from running the prepared questions
against real retrieval (P2's own bounded scope per the master contract), since P1
and RA1 have exhausted preparation-level evidence.
