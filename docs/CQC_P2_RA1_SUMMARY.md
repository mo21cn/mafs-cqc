# CQC-P2-RA1 — Structured Summary

Human interpretation layer for HO + ChatGPT. Machine truth: `docs/CQC_P2_RA1_METRICS.json`,
`docs/CQC_P2_RA1_SHA256_MANIFEST.txt`, per-case `evaluation/{redigestion_record.json,
admission_rationales.json, projection_review.json}`.

## A — Acceptance Header

```yaml
contract_id: CQC-P2-RA1-COMMITMENT-ADJUDICATION-PRODUCTIVE-INSTABILITY-SEVEN-FIELD-REPAIR-v0.1
status: READY_FOR_REVIEW
repository: mo21cn/mafs-cqc
branch: dev/cqc-p2
evidence_commit_sha: (pinned in docs/CQC_P2_RA1_METRICS.json)
evidence_ci_run_id: (pinned in docs/CQC_P2_RA1_METRICS.json)
metrics_pin_commit_sha: (pinned in docs/CQC_P2_RA1_METRICS.json)
meaningful_push_ci_cycles: (see METRICS)
```

## B — Initial P2 Adjudication Matrix

| Case | Initial Finding | Destructive Overcommitment | Productive Instability | Repair Required |
|---|---|---|---|---|
| s1_vms_cellular_mechanism | Mechanism anchors (KNDy/kisspeptin/NK; endothelium/smooth muscle; hypothalamic nuclei) committed without source authorization | YES | none observed | YES |
| s2_vcell_paradigm | Candidate paradigm families + comparison baselines pre-populated | YES | criterion ambiguity (preserved) | YES |
| s3_antagonist_domains | CQ-04 = answer-organization artifact; CQ-01 RC search-procedure leak | YES | type ambiguity TERMINOLOGY vs ENTITY_RESOLUTION (preserved) | YES |
| s4_avca_donor_data | Structure acceptable; dual-gate reflects session-memory absorption of P1-RA lesson | NO | — | NO (PASS_WITH_CAVEAT) |
| s5_mixed_commitment | CQ-04 = downstream consequence turned into upstream question | YES | mixed-type dispersion (preserved) | YES |
| s6_narrow_source_check | RC procedural sequencing; identity-boundary unresolved | NO (no overcommitment) | identity granularity context-dependent (preserved) | bounded RC repair only |

## C — Re-digestion Delta

| Case | Prior Artifact | Measured Failure | Fields Changed | What Was Removed/Narrowed | What Instability Was Preserved |
|---|---|---|---|---|---|
| s1 | CQS-CQC-P2-01 | Mechanism anchors beyond source | CQ-01 statement/RC/uncertainty | KNDy/NK/endothelium/nuclei commitments removed from statements and conditions | population + resolution ambiguities |
| s2 | CQS-CQC-P2-02 | Pre-populated paradigm candidates + baselines | CQ-01 statement/RC | baseline bracket and candidate-family examples removed; evidence generates the candidate space | criterion ambiguity (CQ-02), entity ambiguity (uncertainty) |
| s3 | CQS-CQC-P2-03 | CQ-04 organization artifact; CQ-01 RC procedure leak; ATC example beyond source | removed CQ-04; CQ-01/CQ-02 RC | answer-organization question deleted; procedure and ATC examples de-proceduralized/de-sourced | type ambiguity retained in uncertainty (no multi-label added) |
| s5 | CQS-CQC-P2-05 | CQ-04 downstream-consequence-as-question | removed CQ-04; CQ-03 RC context note | consequence demoted to context | mixed-type dispersion (MECHANISM/NOVELTY/MEASUREMENT) |
| s6 | CQS-CQC-P2-06 | RC procedural sequencing | CQ-01 RC/uncertainty | step sequencing replaced by evidence states | 1-CQ no-decomposition structure; identity-boundary left unresolved by use |

S4: intentionally preserved (no record required by §4).

## D — Final Semantic State

```yaml
s1_vms_cellular_mechanism:
  initial_adjudication: FAIL_REPAIR_REQUIRED
  repair_performed: re-digested CQS-CQC-P2-01-R1
  final_state: PASS
  productive_instability_preserved: population/resolution ambiguities (uncertainty)
  remaining_boundary: none recorded
s2_vcell_paradigm:
  initial_adjudication: FAIL_REPAIR_REQUIRED
  repair_performed: re-digested CQS-CQC-P2-02-R1
  final_state: PASS
  productive_instability_preserved: criterion ambiguity; entity (software) ambiguity
  remaining_boundary: none recorded
s3_antagonist_domains:
  initial_adjudication: FAIL_REPAIR_REQUIRED
  repair_performed: re-digested CQS-CQC-P2-03-R1 (CQ-04 removed; RCs de-proceduralized)
  final_state: PRODUCTIVE_INSTABILITY_PRESERVED
  productive_instability_preserved: type ambiguity TERMINOLOGY vs ENTITY_RESOLUTION
  remaining_boundary: 研究 dual sense folded into inventory scope (noted, not branched)
s4_avca_donor_data:
  initial_adjudication: PASS_WITH_CAVEAT
  repair_performed: none (preserved)
  final_state: PASS_WITH_CAVEAT
  productive_instability_preserved: n/a
  remaining_boundary: contamination caveat (session memory) explicitly retained
s5_mixed_commitment:
  initial_adjudication: FAIL_REPAIR_REQUIRED
  repair_performed: re-digested CQS-CQC-P2-05-R1 (CQ-04 removed)
  final_state: PRODUCTIVE_INSTABILITY_PRESERVED
  productive_instability_preserved: mixed epistemic dimensions without privileged type
  remaining_boundary: metabolite species left unspecified (operator's term retained)
s6_narrow_source_check:
  initial_adjudication: BOUNDARY_UNRESOLVED_PRESERVED
  repair_performed: bounded RC repair CQS-CQC-P2-06-R1
  final_state: BOUNDARY_UNRESOLVED_PRESERVED
  productive_instability_preserved: 1-CQ no-decomposition structure
  remaining_boundary: identity as evidence-object vs execution-prerequisite (use-dependent)
```

## E — Seven-Field Repair Result

```yaml
all_measured_failures_repairable_without_schema_change: true
schema_pressure_observed: false
missing_representation_if_any: none — every repair used statement/uncertainty/resolution_condition edits plus question removal; dependencies and source_trace untouched
```

**SEVEN_FIELD_REPAIR_SUCCEEDED.** Do not read this as universality: the boundary
cases that remain (s3 type duality, s6 identity granularity) were representable
because the source genuinely supports the instability, not because the schema
absorbs all future cases.

## F — Resolution-Condition Regression

```yaml
s1: leakage_before: 0 (statements carried the overcommitment, not RC) · after: 0
s2: leakage_before: 0 · after: 0
s3: leakage_before: 1 (CQ-01 '以原词检索得到的') · after: 0 (evidence-state wording)
s4: leakage_before: 0 · after: 0
s5: leakage_before: 0 · after: 0
s6: leakage_before: 1 (CQ-01 '先…再…' sequencing) · after: 0 (evidence-state branches)
```

Machine regression scan across all revised CQS: 0 leaks (pattern set: 先以/先查/逐篇/以原词检索/再核对/检索得到的/检索顺序).

## G — CandidateQuestion Admission Review

Every final CQ carries an evidence-landscape rationale in
`evaluation/admission_rationales.json` (16 rationales across 5 final artifacts +
s4's 3). CQs removed at RA1 failed the admission test: s3 CQ-04 organized the
answer; s5 CQ-04 was a downstream consequence. Both deletions are recorded with
their rationale; neither left a hole in substantive coverage (verified against the
RA1 reference-set separation).

## H — P2-B Freeze

```text
R1 diamond: PASS / unchanged
R2 sequential: PASS / unchanged
No graph framework added
No propagation engine added
```

## I — MAFS Deferred Note

Design debt observed (record-only, ≤150 words): MAFS's current skill boundary mixes
evidence-state characterization with downstream value/action language in places
(e.g. framing-advice style guidance near its gates). CQC's commitment/adjudication
discipline — evidence states separated from value decisions, admission rationales
for each item entering the chain — is a candidate methodology MAFS may import later.
No MAFS file, skill, or contract was touched in this round.

## J — Architecture Delta

```yaml
candidate_question_schema_changed: false
new_production_artifact_types: 0
new_confidence_fields: 0
new_semantic_scorers: 0
new_dependency_solvers: 0
new_graph_frameworks: 0
live_retrieval_added: false
mafs_modified: false
```

## K — P2 Finding

RA1's five repairs share one signature: the first-pass artifact committed something
the source did not authorize — and in every case the seven fields were sufficient to
*withdraw* the commitment without losing anything the source actually supported.
The productive-instability side is equally important: s3's type duality and s6's
identity-granularity boundary were left standing, each recorded in uncertainty,
each explicitly use-dependent. The distinction that made this possible is the
admission test ("what independent evidence landscape does this question own?") —
it is a model-side judgment, stored only in evaluation records, and it cleanly
separated the two failures that looked similar at first pass (s3 CQ-04 vs s3 CQ-01:
one organizes answers, one disambiguates referents — only the first is an
overcommitment). The contamination caveat on s4 stays: a model that has internalized
a lesson cannot demonstrate it would rediscover it. Seven-field repair succeeded
without schema pressure; the schema earned another round of trust by *not* growing.

## L — Next Step

**CQC-P3** — commitment boundary adjudicated, productive instability preserved,
seven-field repair proven; the next digestion transition (CQS + source context →
SRP) is the master v0.2 sequence's next bounded phase.
