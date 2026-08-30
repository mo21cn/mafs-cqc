# CQC-P1 — Structured Summary

Human interpretation layer for HO + ChatGPT. Machine truth: `docs/CQC_P1_METRICS.json`,
`docs/CQC_P1_SHA256_MANIFEST.txt`; per-case machine facts + preliminary adjudication in
`benchmarks/p1/<case>/evaluation/`.

## A — Acceptance Header

```yaml
contract_id: CQC-P1-REAL-TASK-DIGESTION-REPLAY-REDIGESTION-LINEAGE-v0.1
status: READY_FOR_REVIEW
repository: mo21cn/mafs-cqc
branch: dev/cqc-p1
verified_commit_sha: (pinned in docs/CQC_P1_METRICS.json)
ci_run_id: (pinned in docs/CQC_P1_METRICS.json)
benchmark_case_count: 5
raw_or_verbatim_case_count: 5
reconstructed_case_count: 0
meaningful_push_ci_cycles: 1
```

## B — Benchmark Matrix

| Case | Family | Input Status | Arm A | Arm B | Arm C Triggered | Primary Observation |
|---|---|---|---|---|---|---|
| case_vms_mechanism | C (mechanism/causal) | RAW | 5 lines | 3 questions / 0 edges | No | Ambiguities durable in B vs inline in A; coverage parity |
| case_vcell_scope | A (entity/identity) | RAW | 5 lines | 3 questions / 1 edge | No | Typo surfaced as explicit question (CQ-03) in B, silent in A |
| case_vcell_paradigm | B (novelty/prior-art) | RAW | 4 lines | 3 questions / 1 edge | No | Undefined paradigm-criterion → operable question (CQ-02) in B |
| case_antagonist_domains | E (mixed) | RAW | 4 lines | 4 questions / 1 edge | No | Heaviest ambiguity: disambiguation gated the inventory in B (blocking edge) |
| case_avca_donor_data | D (source-content) | RAW | 4 lines | 3 questions / 1 edge | No | Threshold provenance: CQ-03 three-state decidability binds the existence answer |

## C — Arm A vs Arm B Results

Per case, full detail in `benchmarks/p1/<case>/evaluation/comparison.json`.
Machine facts (validate_p1): 5/5 CQS schema-valid, source-hash valid, exact-trace
valid, DAG valid, render reproducible; 22 tests pass. All semantic fields below are
**manual-adjudication facts (Local Claw preliminary, pending HO + ChatGPT final)**.

| Case | Critical coverage A | Critical coverage B | Intent preservation | Granularity failures | Dependency failures | Cross-stage drift | Traceability |
|---|---|---|---|---|---|---|---|
| vms | full (inline) | full (durable) | A: silent, B: durable | none / none | A: n/a, B: 0 edges pass | none | A: none, B: full |
| vcell_scope | full; typo unauditable | full; typo explicit (CQ-03) | B keeps VCell-software reading | none / none | A: n/a, B: 1 edge passes RA2 test | none | A: none, B: full |
| vcell_paradigm | full; criterion proxy silent | full; criterion explicit (CQ-02) | B converts gap to question | none / none | A: n/a, B: 1 edge passes RA2 test | none | A: none, B: full |
| antagonist | full; interpretation defaulted | full; interpretation gated (CQ-01→CQ-02) | B surfaces dimension choice (CQ-04) | none / none | A: n/a, B: 1 edge passes RA2 test | none | A: none, B: full |
| avca | full; thresholds borrowed silently | full; thresholds three-state (CQ-03) | B preserves 有没有有没有 in uncertainty | none / none | A: n/a, B: 1 edge passes RA2 test | none | A: none, B: full |

Repeated-reasoning cost: 1 model generation pass per arm per case (observable);
token/wall-time not measurable in this environment (null); manual intervention 0.

## D — Re-digestion Lineage

**No measured artifact failure earned re-digestion in P1.**

Arm C was not triggered in any of the five cases: every Arm B artifact passed the
P0 schema, preserved all ambiguities explicitly, recovered the expected critical
set, and its four dependency edges all survived the RA2 prerequisite test. Per
contract §15, no Arm C run was manufactured.

Note on H2: the re-digestion mechanism itself (prior artifact + explicit conflict
→ diagnosis → revised artifact) was exercised for real during the accepted P0-RA1
(20 field repairs) and P0-RA2 (4 field repairs) closures on this same line; P1
records no *new* lineage events.

## E — Success Symmetry Ledger

- **Occurred once (observation)**: vcell_scope's typo→question conversion.
- **Repeated across heterogeneous cases (candidate capability)**: in all five
  cases, Arm A's interpretation choices were behaviorally sound but structurally
  unauditable (typo normalization, threshold borrowing, criterion proxying,
  disambiguation defaulting), while Arm B rendered the same choices as durable,
  inspectable, reversible artifact state. This repeats across 5/5 heterogeneous
  families — candidate capability level, not yet an invariant.
- **Not yet strong enough to freeze**: any claim that Arm B *improves retrieval
  outcomes* — P1 measured search *preparation* only (no live retrieval by
  contract); the coverage parity observed (B never missed a critical question A
  found, and A never found one B missed) is a structural parity result that must
  not be over-read.

## F — Failure Ledger

- Repeated failure family in **Arm A (structural, not per-case)**: interpretation
  choices are unrecorded across all five cases — no artifact, no audit trail, no
  targeted repair possible. This is the baseline's defining weakness, as designed.
- No repeated failure family observed in Arm B artifacts.
- Environmental asymmetry (recorded per §10): the model executing both arms holds
  session memory of the CQC line (Virtual Cell context from P0), an unavoidable
  asymmetry for a single-model experiment; it equally benefits both arms.

## G — Architecture Delta

```yaml
candidate_question_schema_changed: false
new_artifact_types: 0
new_semantic_scorers: 0
new_rankers: 0
new_solvers: 0
new_llm_runtime_frameworks: 0
mafs_integration_performed: false
srp_implemented: false
budget_implemented: false
```

Implementation delta: `scripts/validate_p1.py` (benchmark-package validator,
deterministic facts only) + `benchmarks/p1/**` + docs. No production logic added
to the P0 surface.

## H — Digestion Finding

P1's five raw cases show the artifact's value is not "better questions" — Arm B's
questions are structurally the same ones Arm A generates inline. The measurable
difference is **interpretation provenance**: every case contained at least one
decision the model had to make that the operator did not specify (a typo, a
threshold, a criterion, a domain default, a population scope). In Arm A those
decisions are executed silently and are unrecoverable from the output; in Arm B
each becomes inspectable artifact state — a question (CQ-xx), an uncertainty
field, or a blocking dependency edge — that can be confirmed, amended, or
reversed without re-reading the whole preparation. The blocking edges Arm B
produced (4 total, all surviving the RA2 test) are the same "search-surface"
judgments Arm A makes implicitly. Coverage was at parity; no re-digestion was
earned. The honest claim P1 supports: explicit digestion converts *silent
interpretive defaults* into *auditable interpretive state* at zero coverage cost
across all five heterogeneous families.

## I — Next-Step Recommendation

**CQC-P1-RA** — one bounded remediation round to close the single measurable
gap before P2: the missing live-downstream leg. P1 compared search *preparation*
only; the claim that auditable state improves actual search behavior requires a
P1-RA that (a) pins a downstream retrieval task (bounded, per-contract §8 proxy
extended with an execution leg), (b) re-runs Arms A/B on the same five frozen
cases, and (c) measures whether Arm B's durable state reduces repeated-reasoning
cost and improves target recall vs Arm A. Until that leg exists, P2's
granularity/dependency closure would be built on preparation-only evidence.
