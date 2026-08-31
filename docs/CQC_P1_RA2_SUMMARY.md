# CQC-P1-RA2 — Structured Summary

Human interpretation layer for HO + ChatGPT. Machine truth: `docs/CQC_P1_RA2_METRICS.json`,
`docs/CQC_P1_RA2_SHA256_MANIFEST.txt`; per-case current ledger = `evaluation/comparison.json`.

## A — Acceptance Header

```yaml
contract_id: CQC-P1-RA2-ARTIFACT-RECURSIVE-DIGESTION-DOWNSTREAM-STATE-PROPAGATION-CLOSURE-v0.1
status: READY_FOR_REVIEW
repository: mo21cn/mafs-cqc
branch: dev/cqc-p1
verified_commit_sha: (pinned in docs/CQC_P1_RA2_METRICS.json)
ci_run_id: (pinned in docs/CQC_P1_RA2_METRICS.json)
meaningful_push_ci_cycles: (see METRICS; >= 2 corrected per contract section 13)
```

## B — Artifact Recursion Ledger

| Case | Prior CQS | Revised CQS | Old Downstream State (stale) | New Downstream State | Stale State Removed |
|---|---|---|---|---|---|
| case_vcell_scope | CQS-CQC-P1-02 | CQS-CQC-P1-02-RC1 | "CQ-01 blocked by CQ-02"; CQ-02 listed as prerequisite ordering | all three questions independently searchable; ordering = heuristic/coverage preference (explicitly labeled, not blocking); blocked list empty | ✅ |
| case_antagonist_domains | CQS-CQC-P1-04 | CQS-CQC-P1-04-RC1 | CQ-03 described as an independent tool-use branch (no declared prerequisite) | blocked list: {CQ-02←[CQ-01], CQ-03←[CQ-01]}; independent list: [CQ-01, CQ-04]; reason_for_order matches revised graph | ✅ |
| case_avca_donor_data | CQS-CQC-P1-05 | CQS-CQC-P1-05-RC1 | CQ-02 blocked only by CQ-01; prep text claimed CQ-03 binds the answer (contradiction) | blocked list: {CQ-02←[CQ-01, CQ-03]}; independent list: [CQ-01, CQ-03]; contradiction closed in both artifact and prep | ✅ |

## C — Dependency Propagation Ledger

```yaml
case_vcell_scope:
  revised_dependencies: {CQ-01: [], CQ-02: [], CQ-03: []}
  blocked_questions: []
  independent_questions: [CQ-01, CQ-02, CQ-03]
  consistency_status: PASS
case_antagonist_domains:
  revised_dependencies: {CQ-01: [], CQ-02: [CQ-01], CQ-03: [CQ-01], CQ-04: []}
  blocked_questions: [{CQ-02 ← CQ-01}, {CQ-03 ← CQ-01}]
  independent_questions: [CQ-01, CQ-04]
  consistency_status: PASS
case_avca_donor_data:
  revised_dependencies: {CQ-01: [], CQ-02: [CQ-01, CQ-03], CQ-03: []}
  blocked_questions: [{CQ-02 ← CQ-01, CQ-03}]
  independent_questions: [CQ-01, CQ-03]
  consistency_status: PASS
```

## D — Source Binding Ledger

```yaml
case_vcell_scope:
  revised_artifact_id: CQS-CQC-P1-02-RC1
  revised_artifact_sha256: 5767b005…
  downstream_source_artifact_id: CQS-CQC-P1-02-RC1
  downstream_source_artifact_sha256: 5767b005…
  binding_status: PASS
case_antagonist_domains:
  revised_artifact_id: CQS-CQC-P1-04-RC1
  revised_artifact_sha256: 3a6fff27…
  downstream_source_artifact_id: CQS-CQC-P1-04-RC1
  downstream_source_artifact_sha256: 3a6fff27…
  binding_status: PASS
case_avca_donor_data:
  revised_artifact_id: CQS-CQC-P1-05-RC1
  revised_artifact_sha256: 2d5c90f6…
  downstream_source_artifact_id: CQS-CQC-P1-05-RC1
  downstream_source_artifact_sha256: 2d5c90f6…
  binding_status: PASS
```

## E — Evaluation Truth Closure

- **Current comparison source** per case: `evaluation/comparison.json` (updated to the RA2 final ledger: RA1 reference-set separation, final Arm C state, direct-vs-typed framing, current dependency truth, current lineage truth). Count: 5/5.
- **Historical / superseded** (retained, header-marked): `evaluation/adjudication.md` (P1 initial) and `evaluation/ra1_adjudication.md` (RA1) — 10 files, all labeled `HISTORICAL / SUPERSEDED` pointing to `comparison.json`.
- **Claims withdrawn or narrowed** (carried from RA1, now final): Arm A mislabeled as "no artifact" — withdrawn; typo/repetition counted as scientific coverage — withdrawn; "Arm A inherently unrecoverable" — narrowed to document-level addressability.
- **Final comparison interpretation**: substantive coverage parity 5/5; the honest differentiator is interpretive-state capture (free-form vs question-addressable), addressability, lineage, dependency truth, and local repairability.

## F — Machine Validation

```yaml
raw_hash_linkage:                    PASS (A 5/5, B 5/5, C 3/3)
prior_artifact_hash_binding:         PASS (3/3)
revised_artifact_hash_binding:       PASS (3/3 — RA2 Closure E: failure_diagnosis.revised_artifact_sha256 == file hash)
downstream_source_binding:           PASS (3/3 — RA2 Closure C: id + sha bound to revised CQS; STALE fail-tested)
dependency_state_consistency:        PASS (3/3 — RA2 Closure D: no-dep not blocked, dep-bearing not independent, prerequisites fully propagated)
render_reproducibility:              PASS (arm_b 5/5, arm_c 3/3)
test_result:                         28 PASS
repository_hygiene:                  PASS (0 committed bytecode)
```

## G — Architecture Delta

```yaml
candidate_question_schema_changed: false
new_production_artifact_types: 0
new_semantic_scorers: 0
new_solvers: 0
new_propagation_frameworks: 0
new_llm_runtime_frameworks: 0
live_retrieval_added: false
mafs_integration_performed: false
```

Implementation delta: 3 Arm C downstream preparations regenerated (benchmark fields, not production artifacts); `validate_p1.py` gained three mechanical invariants (Closure C/D/E); 5 comparison.json ledgers updated; 10 historical files header-marked; RA1 cycle-count truth corrected; RA2 docs. No propagation engine, no build framework, no new artifact family.

## H — Digestion Finding

RA2 demonstrated the difference between a re-digested artifact and a re-digested artifact chain. All three revised CQS objects were semantically correct after RA1, yet every derived downstream preparation still carried the old dependency state — the revision had not propagated. The failure was not scientific judgment but artifact plumbing: nothing mechanically connected the revised source to its derived state, so the derived state silently kept telling the old story. The repair needed no new intelligence and no new system: three structured fields in the preparation (`source_artifact_id`, `source_artifact_sha256`, structured blocked list) plus three mechanical validator invariants now make the chain self-checking. The lesson generalizes: in an artifact-mediated pipeline, *any* upstream revision invalidates derived state until regeneration, and the binding that proves regeneration must be verified by the substrate, never assumed. Model decides what the dependency means; the substrate verifies that downstream state actually reflects the model's revised artifact.

## I — Next Step

**CQC-P2** — the P1 line is now truthful end-to-end (raw lineage, re-digestion lineage, downstream propagation, single evaluation truth per case). The only unmeasured claim left is behavioral (does typed digestion improve real retrieval), which belongs to P2's own bounded scope; preparation-level evidence is exhausted.
