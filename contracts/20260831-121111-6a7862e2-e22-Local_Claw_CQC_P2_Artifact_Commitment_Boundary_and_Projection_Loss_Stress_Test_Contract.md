# Local Claw Contract
## CQC-P2 — Artifact Commitment Boundary & Projection-Loss Stress Test

**Contract ID:** `CQC-P2-ARTIFACT-COMMITMENT-BOUNDARY-PROJECTION-LOSS-STRESS-v0.1`  
**Module:** Candidate Question Compiler (CQC)  
**Master Contract:** `CQC_Master_Development_Contract_v0.2_Post_P1_Roadmap_Rebaseline.md`  
**Parent Closure:** `CQC-P1 → RA1 → RA2 — CLOSED / ACCEPTED`  
**Work Actor:** **Local Claw**  
**Planning / Acceptance Pair:** **HO + ChatGPT**  
**Repository:** `mo21cn/mafs-cqc`  
**Working Branch:** `dev/cqc-p2`  
**Execution Truth Plane:** Git repository + GitHub Actions  
**Task Type:** **Semantic commitment stress test + revision-topology robustness test**  
**Live Retrieval:** **Forbidden**  
**MAFS Integration:** **Forbidden**  
**Schema Expansion:** **Forbidden during first-pass P2 execution**  
**Architecture Expansion:** **Forbidden unless separately authorized after measured failure**  
**Completion State:** `RETURN_FOR_HO_PLUS_CHATGPT_ACCEPTANCE`

---

# 0. Mandatory Pre-read, Then Execute

Before changing the repository, Local Claw must read:

```text
CQC_Master_Development_Contract_v0.2_Post_P1_Roadmap_Rebaseline.md
docs/CQC_P1_RA2_SUMMARY.md
```

If the v0.2 master contract supplied by HO is not yet in the repository, place an unchanged copy in the repository root before execution.

Do **not** draft a replacement P2 contract.

Do **not** stop to ask HO to approve an implementation plan.

After the pre-read, execute this contract directly.

The pre-read is a boundary check, not a new planning phase.

---

# 1. Mission

P0 established that research-intent digestion can be externalized as a small typed `CandidateQuestionSet`.

P1 established that the observed value of the typed intermediate artifact is not superior substantive coverage, but:

```text
addressability
source traceability
explicit uncertainty
prerequisite semantics
lineage
local repairability
cross-stage consistency
```

P1 also established that a revised upstream artifact can invalidate derived state and that stale derived state can be detected with minimal content-addressed binding.

P2 now asks two new questions:

## P2-A — Semantic Commitment Boundary

> **Where does converting richer contextual understanding into a discrete CandidateQuestion artifact begin to create projection loss, false precision, or destructive context collapse?**

## P2-B — Artifact Revision Robustness

> **Does the current lightweight identity/hash/derived-from discipline remain reliable under harder revision topologies without requiring a new ArtifactGraph or propagation framework?**

P2 is a **stress test**, not a feature-completion phase.

---

# 2. Governing Principles

P2 must preserve the following v0.2 principles:

> **Artifact is a durable, discrete, revisable commitment projected from richer contextual cognition.**

> **Typed digestion never supersedes source context.**

> **Artifact does not eliminate semantic uncertainty; it relocates it to an explicit boundary.**

> **Stress before extension.**

> **Measured failure justifies architecture. Architecture does not justify itself.**

> **A concept that helped find a solution is not automatically the mechanism implemented by the system.**

Do not use `recursion` as the formal name for dependency invalidation or revision propagation.

Use mature terms:

```text
artifact state transition / re-digestion
content-addressed source binding
dependency invalidation
stale derived state
incremental regeneration
```

---

# 3. Frozen CQS Contract

The accepted CandidateQuestionSet remains frozen during P2 first-pass execution.

Set-level:

```yaml
artifact_id:
schema_version:
source_narrative_sha256:
source_narrative:
questions:
```

Per-question:

```yaml
question_id:
statement:
source_trace:
question_type:
dependencies:
resolution_condition:
uncertainty:
```

Do not add:

```text
question_type_confidence
boundary_distance
semantic_probability
granularity_score
dependency_score
projection_loss_score
```

A P2 failure may **recommend** a future schema change.

It does not authorize Local Claw to implement that change.

---

# 4. `question_type` Boundary

P2 must treat `question_type` as:

```text
provisional
descriptive
non-exhaustive
non-authoritative
```

It must not become:

```text
hard router
search-template key
ontology truth
latent-state probe
```

A mixed-type question is not automatically a failure.

The failure of interest is **forced false precision**.

If the model cannot honestly choose one label, preserve that tension in the existing artifact fields rather than inventing a new taxonomy during P2.

---

# 5. P2-A — Semantic Commitment Boundary Test Set

P2-A must use **six cases**.

Four must be the existing raw P1 operator cases below, reused **verbatim**:

```text
S1 — case_vms_cellular_mechanism
     "请搜索女性血管舒缩症状在细胞分辨率层面的机制解释"

S2 — case_vcell_paradigm
     "“Virtual Cel”产生了哪些新的研究范式？"

S3 — case_antagonist_domains
     "拮抗剂研究的应用领域有哪些"

S4 — case_avca_donor_data
     "\"Arc Virtual Cell Atlas\"数据集资源里有没有有没有年轻健康血管/心脏原代供体数据"
```

Use the exact committed raw narrative bytes from P1.

Do not rewrite them.

Add two **benchmark-only synthetic stress cases**:

```text
S5 — Mixed commitment case
A short research narrative that genuinely combines:
mechanism + novelty/prior-art + measurement,
without telling the model which dimension is primary.

S6 — Minimal / no-decomposition case
A deliberately narrow source-content question where
one CandidateQuestion may be sufficient and over-decomposition
would itself be the failure.
```

Rules for S5/S6:

```text
benchmark-only
clearly labeled SYNTHETIC_STRESS
no hidden answer
no literature facts inserted as oracle
no pre-labeled CandidateQuestion decomposition
no search axes
```

Local Claw may author S5/S6 only as benchmark stimuli.

Their exact text must be preserved and SHA256-bound.

---

# 6. P2-A Execution

For each of the six cases:

```text
source narrative
→ model digestion
→ CandidateQuestionSet using frozen P0 instruction/schema
→ deterministic render
→ mechanical validation
→ projection-loss review record
```

Do not perform live search.

Do not produce SRP.

Do not produce BudgetEnvelope.

Do not automatically re-digest semantic failures during the first pass.

The initial artifact must remain preserved for HO + ChatGPT adjudication.

---

# 7. Projection-Loss Review Record

For each semantic stress case create:

```text
benchmarks/p2/semantic/<case_id>/evaluation/projection_review.json
```

This is a **benchmark record**, not a new production artifact family.

Required structure:

```yaml
case_id:
input_status:
source_sha256:
cqs_artifact_id:
cqs_sha256:

mechanical:
  schema_valid:
  source_hash_valid:
  source_trace_exact_valid:
  dependency_dag_valid:
  deterministic_render_valid:

local_claw_preliminary_review:
  source_intent_elements:
  preserved_elements:
  possibly_lost_elements:
  possible_unsupported_commitments:
  ambiguity_preserved:
  possible_false_precision:
  possible_over_decomposition:
  possible_under_decomposition:
  possible_context_loss:
  possible_dependency_issue:
  possible_question_type_overcommitment:

final_semantic_adjudication:
  status: PENDING_HO_CHATGPT
```

Important:

Local Claw's preliminary review is **not** the final semantic verdict.

Do not convert preliminary semantic judgments into machine metrics.

---

# 8. P2-A Evaluation Questions

HO + ChatGPT acceptance must be able to answer, from the delivered artifacts:

### 8.1 Ambiguity Preservation

Did the CQS preserve genuine ambiguity, or silently choose an interpretation?

### 8.2 Projection Loss

Did an important source-context relation disappear when converted into fields/questions?

### 8.3 False Precision

Did the artifact make a cleaner categorical claim than the source supports?

### 8.4 Granularity Boundary

Did the model split the narrative into independently meaningful evidence units, or merely into convenient lexical parts?

### 8.5 No-decomposition Capacity

Can the CQC leave a narrow task narrow?

P2 must allow:

```text
1 CandidateQuestion
```

when that is the most faithful digestion.

### 8.6 Mixed-Type Honesty

Can a mixed epistemic case remain honest without turning `question_type` into a false ontology?

### 8.7 Context Reservoir

Could a later model recover necessary context from:

```text
CandidateQuestionSet + preserved source_narrative
```

without inventing missing information?

---

# 9. P2-A Success Does Not Mean "No Ambiguity"

P2-A passes conceptually when ambiguity is **visible and governable**.

It does not require every ambiguity to be resolved.

Do not treat:

```text
uncertainty remains
```

as failure.

Treat:

```text
uncertainty silently collapsed
```

as candidate failure.

---

# 10. P2-B — Revision Robustness Stress Tests

P2-B is deterministic and must use the current lightweight lineage model first.

Do not build a graph framework.

Create benchmark-only fixtures under:

```text
benchmarks/p2/revision_topology/
```

Two mandatory scenarios:

```text
R1 — fan-out / diamond dependency
R2 — sequential revision + partial regeneration
```

---

# 11. R1 — Fan-out / Diamond Dependency

Construct a benchmark-only artifact topology:

```text
        A0
       /  \
     B0    C0
       \  /
        D0
```

Where:

```text
B0 derived_from A0
C0 derived_from A0
D0 derived_from B0 + C0
```

Use content hashes and explicit source bindings.

Then revise:

```text
A0 → A1
```

Expected truth:

```text
B0 = stale
C0 = stale
D0 = transitively stale
```

Regenerate:

```text
A1 → B1
A1 → C1
B1 + C1 → D1
```

Final state must be current.

The validator must prove this benchmark truth without scheduling or repairing automatically.

Do not build a propagation engine.

---

# 12. R2 — Sequential Revision + Partial Regeneration

Construct:

```text
A0 → B0
A0 → C0
```

Then:

```text
A0 → A1
```

Regenerate only:

```text
B0 → B1 from A1
```

Leave:

```text
C0
```

unchanged.

Expected:

```text
B1 = current
C0 = stale
```

Then revise again:

```text
A1 → A2
```

Expected before regeneration:

```text
B1 = stale
C0 = stale
```

The validator must distinguish:

```text
current
stale
```

from actual content binding.

It must not infer semantic correctness.

---

# 13. P2-B Implementation Boundary

Preferred implementation:

```text
simple benchmark fixtures
+
small deterministic validator extension
+
small tests
```

Allowed:

```text
artifact_id
artifact_sha256
source_artifact_id / source_artifact_sha256
multiple source bindings for D0/D1 benchmark fixture
```

Benchmark-only multi-source binding is allowed if required by the diamond case.

Not allowed:

```text
ArtifactGraph class hierarchy
scheduler
propagation engine
rebuild daemon
generic incremental computation framework
database graph
queue
event bus
```

If the current lightweight model cannot represent R1/R2 honestly without such machinery:

```text
LIGHTWEIGHT_LINEAGE_LIMIT_REACHED
→ STOP
→ report measured failure
```

Do not solve it by expanding architecture during P2.

---

# 14. Deterministic Validator Scope

Create or minimally extend:

```text
scripts/validate_p2.py
```

It may validate only:

```text
P2 package completeness
CQS schema compatibility
raw/source SHA truth
source_trace exactness
dependency DAG integrity
render reproducibility
artifact/source hash binding
derived-from source existence
current vs stale truth in R1/R2
transitive stale truth in the benchmark diamond
repository hygiene
```

It must not validate:

```text
projection loss
semantic fidelity
false precision
granularity quality
question-type correctness
scientific dependency truth
```

---

# 15. No Automatic Semantic Repair in P2 First Pass

P2-A first-pass semantic failures must remain visible.

Do not automatically:

```text
change schema
change prompt architecture
add fields
repair all CQS
```

before HO + ChatGPT review.

Reason:

> P2 exists to characterize the boundary before changing the boundary.

If Local Claw believes a failure requires a schema change, record:

```text
SCHEMA_PRESSURE_OBSERVED
```

with the exact case and missing representational need.

Do not implement it.

---

# 16. Required P2 Repository Structure

Recommended:

```text
benchmarks/p2/
  semantic/
    <6 case directories>/
      source_narrative.txt
      case_metadata.json
      candidate_question_set.json
      human_render.md
      evaluation/
        projection_review.json

  revision_topology/
    r1_diamond/
      fixtures/
      expected_state.json
      validation_report.json

    r2_sequential/
      fixtures/
      expected_state.json
      validation_report.json

scripts/
  validate_p2.py

tests/
  # minimal P2 additions only

docs/
  CQC_P2_SUMMARY.md
  CQC_P2_METRICS.json
  CQC_P2_SHA256_MANIFEST.txt
```

Reuse existing P0/P1 schema, renderer, and validation helpers where practical.

Do not duplicate them.

---

# 17. Structured Summary — Mandatory

Create:

```text
docs/CQC_P2_SUMMARY.md
```

Required sections:

## A — Acceptance Header

```yaml
contract_id:
status:
repository:
branch:
verified_commit_sha:
ci_run_id:
semantic_case_count:
revision_topology_case_count:
meaningful_push_ci_cycles:
```

## B — Master Contract Alignment

Briefly state:

```text
what changed after v0.1
why P2 is no longer "Granularity & Dependency Closure"
what P2 is testing instead
```

Maximum 250 words.

## C — Semantic Stress Matrix

| Case | Input Type | CQ Count | Ambiguity Visible | Possible Projection Loss | Possible False Precision | Possible Over/Under Decomposition | HO+ChatGPT Status |
|---|---|---:|---|---|---|---|---|

The semantic columns are Local Claw preliminary observations only.

Mark final status:

```text
PENDING_HO_CHATGPT
```

## D — Seven-Field Contract Pressure

Report:

```yaml
cases_requiring_no_new_field:
cases_with_possible_schema_pressure:
possible_missing_representation:
schema_changed: false
```

Do not claim the schema is insufficient until HO + ChatGPT confirms.

## E — Question-Type Boundary Findings

Report observed cases where:

```text
one type fit cleanly
multiple plausible types existed
type seemed unimportant to downstream interpretation
```

Do not propose a confidence field unless a measured failure specifically requires it.

## F — Revision Robustness

For R1/R2 report:

```yaml
scenario:
initial_state:
revision:
expected_stale_state:
validator_observed_state:
regeneration_state:
status:
```

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

## H — Machine Validation

```yaml
semantic_packages_complete:
cqs_schema_validation:
source_hash_validation:
source_trace_exact_validation:
dependency_dag_validation:
render_reproducibility:
r1_stale_detection:
r2_stale_detection:
test_result:
repository_hygiene:
```

## I — P2 Finding

Maximum 500 words.

Answer only:

> What did P2 reveal about the boundary between useful artifact commitment and destructive overcommitment, and about the limits of the current lightweight revision-lineage model?

Do not write a broad Digestion Theory manifesto.

## J — Next-Step Recommendation

Exactly one:

```text
CQC-P3
CQC-P2-RA
MASTER_REBASELINE_REQUIRED
STOP_AND_REVIEW
```

---

# 18. Machine Metrics

Create:

```text
docs/CQC_P2_METRICS.json
```

Minimum machine-derived fields:

```yaml
contract_id:
verified_commit_sha:
ci_run_id:

semantic_case_count:
raw_reused_case_count:
synthetic_stress_case_count:
cqs_schema_valid_count:
source_hash_valid_count:
source_trace_exact_valid_count:
dependency_dag_valid_count:
deterministic_render_valid_count:

revision_topology_case_count:
r1_binding_valid:
r1_stale_detection_valid:
r1_final_regeneration_valid:
r2_binding_valid:
r2_partial_stale_detection_valid:
r2_second_revision_stale_detection_valid:

test_count:
meaningful_push_ci_cycles:
```

Manual semantic observations must not be stored as machine truth.

No synthetic scalar P2 score.

---

# 19. SHA Manifest

Create:

```text
docs/CQC_P2_SHA256_MANIFEST.txt
```

Cover:

```text
master contract v0.2 copy
all six semantic source narratives
all six CQS artifacts
all six renders
all six projection-review records
all R1/R2 fixtures
validator
tests
summary
metrics
```

Do not include generated bytecode.

---

# 20. Local Feedback Loop

Before first meaningful push:

```text
validate all six CQS packages
validate all source hashes
validate all exact source traces
validate all DAGs
reproduce all renders
run R1 stale-state test
run R2 stale-state test
run affected tests
scan repository hygiene
```

must pass locally.

CI remains independent verification.

---

# 21. Development Budget

Maximum:

```text
3 meaningful code-changing push → CI cycles
```

P2 is primarily benchmark/stress execution.

If more than three code-changing cycles appear necessary:

```text
ITERATION_BUDGET_EXHAUSTED
→ STOP
```

Benchmark-artifact commits without code changes remain traceable but are not architecture-development cycles.

---

# 22. Stop Conditions

Stop and return if any of the following appears necessary:

```text
CandidateQuestion schema change
new production artifact type
semantic scorer
confidence engine
granularity scorer
dependency solver
ArtifactGraph framework
PropagationEngine
scheduler
live retrieval
MAFS integration
SRP implementation
BudgetEnvelope implementation
```

Use:

```text
SCHEMA_PRESSURE_OBSERVED
LIGHTWEIGHT_LINEAGE_LIMIT_REACHED
ARCHITECTURE_EXPANSION_BLOCKED
```

as appropriate.

The measured failure is the deliverable.

Do not implement the architecture before authorization.

---

# 23. Acceptance Standard

CQC-P2 is eligible for acceptance when:

```yaml
semantic_commitment:
  semantic_cases_completed: 6
  existing_raw_cases_reused_verbatim: true
  synthetic_cases_labeled: true
  seven_field_schema_unchanged: true
  ambiguity_boundary_exposed_for_review: true
  projection_loss_review_records_present: true
  final_semantic_status_left_to_ho_chatgpt: true

revision_robustness:
  diamond_case_executed: true
  sequential_revision_case_executed: true
  partial_stale_state_detected: true
  repeated_revision_stale_state_detected: true
  final_regeneration_truth_verified: true

architecture:
  deterministic_semantic_intelligence_added: false
  new_graph_framework_added: false
  propagation_engine_added: false
  confidence_field_added: false
  live_retrieval_added: false
  mafs_integration_performed: false

execution:
  structured_summary_present: true
  machine_metrics_present: true
  sha_manifest_present: true
  final_ci_passed: true
```

P2 acceptance does **not** require:

```text
zero ambiguity
zero projection loss
perfect question-type boundaries
proof that the seven-field schema is universal
```

An honest boundary failure is a valid P2 result.

---

# 24. Required Return Note

```text
CQC-P2 Status:
READY_FOR_REVIEW
| SCHEMA_PRESSURE_OBSERVED
| LIGHTWEIGHT_LINEAGE_LIMIT_REACHED
| ARCHITECTURE_EXPANSION_BLOCKED
| ITERATION_BUDGET_EXHAUSTED
| BLOCKED

Repository:
<repo>

Branch:
<branch>

Verified Commit SHA:
<sha>

CI Run ID:
<id>

Semantic Stress Cases:
<n>/6

Raw Reused Cases:
<n>/4

Synthetic Stress Cases:
<n>/2

CandidateQuestion Schema Changed:
NO | YES

Possible Schema Pressure:
NONE | OBSERVED

R1 Diamond:
PASS | FAIL

R2 Sequential Revision:
PASS | FAIL

New ArtifactGraph Framework:
NO | YES

New Propagation Engine:
NO | YES

Live Retrieval Added:
NO | YES

MAFS Integration Performed:
NO | YES

Tests:
<n> PASS | FAIL

Meaningful Push/CI Cycles:
<n>

Structured Summary:
docs/CQC_P2_SUMMARY.md

Machine Metrics:
docs/CQC_P2_METRICS.json

SHA Manifest:
docs/CQC_P2_SHA256_MANIFEST.txt

Recommended Next Step:
CQC-P3 | CQC-P2-RA | MASTER_REBASELINE_REQUIRED | STOP_AND_REVIEW
```

---

# 25. Final Instruction to Local Claw

Read v0.2 first.

Then stress the commitment boundary.

Do not improve the schema before it fails.

Do not force ambiguity to disappear.

Do not treat `question_type` as a hidden truth variable.

Do not build an ArtifactGraph because a diamond exists.

Use content hashes and source bindings first.

If the lightweight lineage model fails, report the failure.

If the seven-field CQS fails, report the exact missing representation.

P2 succeeds when it tells HO + ChatGPT where the current artifact contract is genuinely strong, where it distorts cognition, and whether the existing revision-lineage discipline survives harder topologies without another wheel being invented.
