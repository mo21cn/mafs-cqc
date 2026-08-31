# Candidate Question Compiler (CQC)
## Master Development Contract v0.2
### Post-P1 Roadmap Rebaseline — Digestion-as-Artifact Upstream Module for MAFS

**Contract ID:** `CQC-MASTER-v0.2-POST-P1-REBASELINE`  
**Supersedes:** `CQC_Master_Development_Contract_v0.1.md`  
**Module:** Candidate Question Compiler (CQC)  
**Development Mode:** Independent line → empirical validation → contextual search-requirement digestion → bounded integration into MAFS  
**Primary Work Actor:** Local Claw  
**Planning / Acceptance Pair:** HO + ChatGPT  
**Execution Source of Truth:** Git repository + GitHub Actions  
**Repository:** `mo21cn/mafs-cqc`  
**Status:** Post-P1 master rebaseline / P0 and P1 closed / P2 onward revised  
**Development Principle:** Thin architecture, model-owned cognition, artifact-owned continuity, evidence-earned structure

---

# 0. Why v0.2 Exists

v0.1 was written before CQC-P0 and CQC-P1 had produced real empirical evidence.

That evidence changed the roadmap.

P0 and P1 demonstrated that the original direction was broadly correct:

```text
Research Narrative
→ model digestion
→ CandidateQuestionSet
```

but they also showed that several assumptions in the original roadmap were too simple.

The most important findings were:

```text
schema-valid artifact
!=
semantically digested artifact

semantic relation
!=
true prerequisite

artifact exists
!=
artifact comparison is valid

revised artifact
!=
revised artifact chain

direct downstream artifact
!=
typed intermediate artifact
```

Most importantly, five heterogeneous P1 cases did **not** demonstrate that a CandidateQuestionSet necessarily produces more substantive scientific coverage than a strong narrative-only path.

The observed value of the typed intermediate artifact was instead concentrated in:

```text
question identity
source traceability
explicit uncertainty
prerequisite semantics
addressability
lineage
local repairability
cross-stage consistency
stale-state detection
```

Therefore v0.2 does not continue mechanically into the original:

```text
P2 = Granularity & Dependency Closure
```

roadmap.

The post-P1 roadmap is rebaselined around a more precise question:

> **What should an artifact commit to, what should it refuse to collapse, and how reliably can that commitment be revised and consumed downstream?**

---

# 1. Governing Thesis v0.2

The working thesis remains:

> **Digestion is artifact.**

But v0.2 narrows what this means.

It does **not** mean:

```text
artifact = transparent readout of latent cognition
```

It means:

> **Digestion becomes engineering-relevant when contextual cognition is externalized into a durable, addressable, revisable commitment that downstream work can inspect and consume.**

For engineering purposes:

```text
Reasoning
= model cognition may change

Digestion
= cognition crosses an artifact boundary
  and becomes durable enough to be addressed,
  inspected, revised, validated, and reused
```

A stronger v0.2 formulation is:

> **An artifact is a durable, discrete, revisable commitment projected from richer contextual cognition.**

This formulation carries both benefit and risk.

Benefits:

```text
addressability
traceability
handoff
validation
local repair
lineage
downstream reuse
```

Risks:

```text
projection loss
false precision
context loss
category overcommitment
semantic mis-anchoring
incorrect dependency commitment
error propagation
```

The purpose of the architecture is not to pretend these risks disappear.

The purpose is to make them visible and governable.

---

# 2. Evidence Boundary

CQC v0.2 distinguishes between:

```text
what has been empirically earned
what remains a design hypothesis
what remains explicitly unproven
```

## 2.1 Earned by P0 / P1

The following are supported by the completed development line:

```text
a small CandidateQuestionSet can externalize model digestion;

mechanical validity does not guarantee semantic fidelity;

dependency edges require prerequisite truth, not mere usefulness;

explicit conflict can target local re-digestion;

a revised upstream artifact can invalidate derived downstream state;

content-addressed source binding can mechanically detect stale derived state;

typed intermediate artifacts can make interpretive state more
addressable and locally repairable than direct downstream preparation.
```

## 2.2 Not earned

CQC has **not** yet established that:

```text
typed CQS always improves scientific correctness;
typed CQS always improves critical-question recall;
typed CQS always reduces total cost;
question types have clean natural boundaries;
a stable universal decomposition taxonomy exists;
CQS fields transparently expose internal model variables;
Digestion Theory is proven;
CQC makes the model intrinsically more intelligent.
```

These claims must not enter contracts as assumptions.

---

# 3. Architectural Position

The intended long-term chain remains:

```text
Research Narrative
        ↓
CandidateQuestionSet
        ↓
SearchRequirementProfile
        ↓
BudgetEnvelope
        ↓
MAFS
        ↓
EvidenceLandscapePackage
```

But v0.2 adds a critical context rule:

> **Typed digestion never supersedes source context.**

The source narrative is not disposable input.

It remains the context reservoir against which later artifacts may be re-interpreted.

Therefore the effective chain is:

```text
Research Narrative ───────────────────────────────┐
        ↓                                         │
CandidateQuestionSet                              │
        ↓                                         │
SearchRequirementProfile  ← consumes context ─────┤
        ↓                                         │
BudgetEnvelope                                    │
        ↓                                         │
MAFS                                              │
        ↓                                         │
EvidenceLandscapePackage                         │
                                                  │
re-digestion may return to source context ─────────┘
```

CQC remains independently developed until P5 integration.

---

# 4. Core Authority Boundary

## 4.1 The model owns

The model owns:

```text
semantic understanding
decomposition judgment
granularity judgment
ambiguity recognition
question reformulation
semantic trace judgment
prerequisite judgment
question-type description
contextual search-requirement reasoning
re-digestion after explicit conflict
```

## 4.2 Deterministic substrate owns

The deterministic substrate may own:

```text
schema validity
artifact identity
hash binding
source-trace exactness
dependency DAG integrity
artifact lineage
derived-from binding
stale-state detection
render reproducibility
budget ceilings
machine acceptance facts
```

## 4.3 Deterministic substrate must not own

It must not decide:

```text
which scientific question is correct
which interpretation is scientifically preferable
whether a semantic dependency is true
which question type "really" applies
how important a question is
whether novelty exists
which search route is scientifically best
```

Standing rule:

> **The model decides what a semantic commitment means. The substrate verifies that the system faithfully preserves and consumes that commitment.**

---

# 5. Compile, Do Not Freely Generate

CQC remains a compiler in the bounded sense:

```text
semantic decomposition
+
normalization
+
dependency exposure
+
uncertainty preservation
+
artifact commitment
```

It is not:

```text
open-ended ideation
research-priority generation
hypothesis invention without source trace
```

A scientifically interesting question that is not grounded in the source narrative must not silently enter the primary CandidateQuestionSet.

The architecture should prefer:

```text
preserve ambiguity
```

over:

```text
complete the operator's intent on the model's behalf
```

when the source is genuinely underspecified.

---

# 6. CandidateQuestionSet v0.1 — Frozen Core

The P0/P1 development line successfully used the following per-question fields:

```yaml
question_id:
statement:
source_trace:
question_type:
dependencies:
resolution_condition:
uncertainty:
```

Set-level envelope:

```yaml
artifact_id:
schema_version:
source_narrative_sha256:
source_narrative:
questions:
```

This seven-field CandidateQuestion core is **frozen through the start of P2**.

P2 is a stress test of this representation before extension.

Standing rule:

> **Stress before extension.**

No new field is authorized merely because a richer representation can be imagined.

---

# 7. Artifact Semantics v0.2

## 7.1 `statement`

A useful scientific question with a distinct enough evidence landscape to support downstream work.

Do not assume one universal granularity rule exists.

Granularity is a model judgment subject to empirical stress testing.

## 7.2 `source_trace`

A commitment that the CandidateQuestion is grounded in the source narrative.

Exact trace validation proves only:

```text
quote exists
```

It does not prove:

```text
quote semantically entails the question
```

Semantic fidelity remains model/reviewer judgment.

## 7.3 `question_type`

`question_type` remains:

```text
provisional
non-exhaustive
free-string
descriptive
```

It is **not**:

```text
a natural ontology
a hard router
a universal taxonomy
an authoritative semantic state variable
```

A mixed or boundary case is not automatically a taxonomy failure.

v0.2 explicitly allows the possibility that some question-type boundaries are structurally fuzzy.

Do not add confidence scores or boundary-distance fields without measured failure.

## 7.4 `dependencies`

Dependencies encode **true prerequisites**, not:

```text
usefulness
thematic similarity
preferred order
possible reuse
coverage convenience
```

Standing test:

> **If removing the edge leaves the downstream question correctly interpretable and searchable, the edge is not a prerequisite.**

## 7.5 `resolution_condition`

This states:

```text
what evidence state would materially resolve,
falsify, narrow, or change the question
```

not:

```text
how to search for it
which provider to use
which query to issue
```

## 7.6 `uncertainty`

`uncertainty` is an explicit commitment about unresolved ambiguity.

It must not be interpreted as a transparent readout of an internal scalar uncertainty variable.

Do not manufacture numerical confidence unless a future failure justifies it.

---

# 8. Artifact Commitment Principle

v0.2 introduces an explicit distinction:

```text
model cognition
→ rich, contextual, distributed internal processing

artifact
→ discrete commitment made for downstream work
```

Therefore the main P2 question is no longer:

```text
How do we make the categories cleaner?
```

It is:

> **When is a discrete artifact commitment useful, and when does it create false precision or destructive context loss?**

Standing principle:

> **Artifact does not eliminate semantic uncertainty; it relocates it to an explicit boundary.**

This boundary is where errors become inspectable.

---

# 9. Re-digestion and Revision Terminology

v0.2 removes `recursion` as a formal architecture claim.

Use precise terminology.

## 9.1 Semantic revision / re-digestion

```text
Artifact A_t
+
explicit conflict Δ_t
→ model re-digestion
→ Artifact A_t+1
```

This is an artifact state transition.

A simple retry of the original narrative is not re-digestion.

## 9.2 Derived-state invalidation

If:

```text
B_t derived_from A_t
```

and:

```text
A_t → A_t+1
```

then:

```text
B_t becomes stale
```

until it is regenerated from the revised source.

This is:

```text
dependency invalidation
content-addressed stale-state detection
incremental recomputation
```

not a new AI reasoning primitive.

Do not build a `PropagationEngine` merely to implement this.

Use mature software-engineering patterns when topology becomes more complex.

---

# 10. P0 / P1 Historical Closure

## 10.1 CQC-P0 — CLOSED / ACCEPTED

P0 established:

```text
Research Narrative
→ CandidateQuestionSet
```

with thin deterministic validation.

P0/RA1/RA2 earned:

```text
schema validity != semantic digestion
semantic relation != prerequisite
re-digestion should repair artifact meaning, not add semantic software
```

## 10.2 CQC-P1 — CLOSED / ACCEPTED

P1 used five RAW real-task cases and compared:

```text
Arm A:
Raw Narrative
→ direct downstream artifact

Arm B:
Raw Narrative
→ typed CandidateQuestionSet
→ downstream artifact
```

The result did not establish superior substantive coverage for Arm B.

The primary observed value of the typed intermediate artifact was:

```text
addressability
explicit question identity
source trace
uncertainty
prerequisite representation
lineage
local repair
cross-stage consistency
```

Three measured failures earned Arm C re-digestion.

RA2 then closed stale downstream state using:

```text
source artifact identity
source artifact hash
dependency-state consistency
```

without creating a propagation framework.

---

# 11. Development Philosophy v0.2

Standing rules:

> **Measured failure justifies architecture. Architecture does not justify itself.**

> **No measured failure → no new architecture.**

And symmetrically:

> **Single-case success earns an observation; repeated heterogeneous success may earn an invariant.**

Also:

> **A concept that helps find a solution is not automatically the mechanism implemented by the system.**

This rule is added after the useful-but-overextended `recursion` interpretation.

Contracts must use the most mature existing technical vocabulary available.

Do not coin a new architectural subsystem where a known software-engineering pattern already solves the measured problem.

---

# 12. CQC Research Value — Rebased

The original v0.1 question emphasized whether explicit digestion improves downstream scientific search behavior.

v0.2 narrows the empirical value claim.

Current earned proposition:

> **A typed intermediate CandidateQuestion artifact can make model interpretation more addressable, auditable, lineage-bound, and locally repairable than direct downstream preparation alone.**

Not yet earned:

> CQC necessarily increases substantive scientific coverage.

Future evaluation may still test:

```text
critical-question recall
search quality
cost
framing stability
```

but those are open empirical questions.

The immediate research focus becomes:

```text
artifact commitment quality
projection loss
context preservation
repair locality
lineage reliability
downstream composability
```

---

# 13. CQC-P2 — Artifact Commitment Boundary & Projection-Loss Stress Test

**Status:** Rebaselined / next major phase.

Original P2 `Granularity & Dependency Closure` is retired as the primary roadmap definition.

Granularity and dependency become regression dimensions inside a broader P2.

P2 contains two orthogonal workstreams.

---

## 13.1 P2-A — Semantic Commitment Boundary

Primary question:

> **Where does converting contextual model understanding into a discrete CandidateQuestion artifact begin to distort the research intent?**

Stress families should include:

```text
high ambiguity
underspecified entities
mixed epistemic types
mechanism + novelty mixtures
source-content + interpretation mixtures
granularity boundary cases
context-dependent questions
false precision traps
questions where "no decomposition" may be the correct output
```

P2-A should measure:

```text
intent preservation
projection loss
unsupported commitment
ambiguity preservation
context loss
over-decomposition
under-decomposition
false prerequisite
missing prerequisite
```

P2-A must not aim to eliminate every boundary case.

Success means:

> the artifact can remain honest at the boundary without requiring deterministic semantic intelligence.

---

## 13.2 P2-B — Artifact Revision Robustness

Primary question:

> **When a discrete commitment is revised, does the existing lightweight lineage model remain trustworthy under harder dependency topologies?**

Stress cases may include:

```text
fan-out:
A → B
A → C

diamond:
A → B
A → C
B,C → D

sequential revision:
A_t → A_t+1 → A_t+2

partial regeneration:
one dependent artifact refreshed,
another remains stale

multiple downstream consumers
sharing one upstream CandidateQuestionSet
```

These are stress cases, not authorization for an ArtifactGraph framework.

Use current minimal:

```text
artifact identity
content hash
derived-from binding
stale detection
regeneration
```

first.

If the lightweight model fails, inspect mature build-system / incremental-computation patterns before inventing architecture.

---

# 14. P2 Anti-Goals

P2 must not become:

```text
QuestionType Ontology Project
GranularityScorer Project
DependencySolver Project
Confidence Calibration Engine
ArtifactGraph Framework
PropagationEngine
Reflection Manager
Universal Digestion Runtime
```

Do not add:

```text
question_type_confidence
boundary_distance
semantic probability
```

without measured evidence that the existing representation cannot preserve the required state.

---

# 15. P2 Exit Criteria

P2 may close when:

```yaml
semantic_commitment:
  heterogeneous_boundary_cases_run: true
  ambiguity_preservation_tested: true
  mixed_type_cases_tested: true
  false_precision_failures_measured: true
  major_context-loss failures characterized: true

artifact_contract:
  seven_field_cqs_still_sufficient_or_failure_proven: true
  question_type_not_used_as_hard_router: true
  source_narrative_retained_as_context: true

revision_robustness:
  fan_out_or_diamond_case_tested: true
  repeated_revision_case_tested: true
  stale_state_detectable: true
  no_unearned_graph_framework_added: true

architecture:
  deterministic_semantic_intelligence_added: false
  new_schema_fields_added_only_if_failure_earned: true
```

P2 does not need to eliminate ambiguity.

It needs to prove that ambiguity can remain visible without breaking the artifact chain.

---

# 16. CQC-P3 — Contextual Search Requirement Digestion

**Status:** Rebaselined future phase.

P3 remains the second major digestion transition:

```text
CandidateQuestionSet
+
source narrative context
+
explicit uncertainty
+
dependencies
→ model digestion
→ SearchRequirementProfile
```

This is a crucial v0.2 change.

P3 must **not** reduce to:

```text
question_type
→ fixed search template
```

or:

```text
question_type
→ hard-coded axis routing table
```

`question_type` may be a cue.

It may not become the controlling semantic variable.

---

# 17. SearchRequirementProfile v0.2 Principles

The exact SRP schema is **not frozen** by this master contract.

The original provisional fields:

```text
required_axes
optional_axes
irrelevant_axes
evidence_types
source_classes
depth
stopping_requirements
```

remain historical placeholders only.

Before P3 freezes a schema, it must re-examine whether:

```text
axis
route
falsification path
evidence requirement
source requirement
```

is the right vocabulary.

The lesson from MAFS remains:

> **Multi-Axis does not mean All Axes Every Time.**

But v0.2 adds:

> **Search topology must be digested from the full contextual artifact state, not looked up from a discrete question label.**

---

# 18. P3 Core Boundary

The model owns:

```text
which epistemic routes matter
which evidence types are sufficient
which sources are appropriate
how deep a branch deserves to go
which uncertainties require parallel search routes
```

The substrate may own:

```text
schema validity
route identity
declared bounds
stopping-state representation
artifact lineage
```

P3 must not become a deterministic scientific search planner.

---

# 19. CQC-P4 — BudgetEnvelope

**Status:** Retained with minor rebaseline.

P4 remains a lightweight execution-boundary phase.

Budget is an external resource constraint, not a symbolic representation of scientific truth.

Possible profiles remain:

```text
LIGHT
STANDARD
DEEP
AUTO
```

AUTO remains optional.

Required semantics remain:

```text
Soft Target reached
→ reduce expansion / expensive escalation

Hard Ceiling reached
→ stop new branches
→ preserve current state
→ return partial
```

Permanent invariant:

```text
BUDGET_EXHAUSTED
!=
EVIDENCE_EXHAUSTED
```

v0.2 changes the cost-shape model from:

```text
Question Type
→ Search Topology
→ Cost Shape
```

to:

```text
CandidateQuestionSet + source context
→ SearchRequirementProfile
→ Cost Shape
```

Do not let `question_type` determine budget directly.

---

# 20. CQC-P5 — MAFS Integration & Artifact-Lineage Closure

**Status:** Retained, strengthened.

P5 integrates the independently validated CQC line into MAFS.

Target chain:

```text
A0 ResearchNarrative
        ↓
A1 CandidateQuestionSet
        ↓
A2 SearchRequirementProfile
        ↓
A3 BudgetEnvelope
        ↓
MAFS
        ↓
A4 EvidenceLandscapePackage
```

v0.2 requires every derived artifact boundary to preserve enough lineage to determine:

```text
what source artifact was consumed
which source version/hash was consumed
whether the source has since changed
whether the derived artifact is current or stale
```

P5 must not build a general artifact-graph runtime unless measured integration failures require it.

Prefer minimal content-addressed bindings and known incremental-computation patterns.

---

# 21. Integration Invariants

P5 must verify:

```text
traceability
artifact identity
source context accessibility
lineage
state continuity
stale-state detection
revision propagation
authority boundaries
downstream usability
```

Standing rule earned from P1:

> **Re-digestion is incomplete while dependent artifacts still encode the superseded state.**

This is an artifact-chain invariant.

It is not a claim about recursion.

---

# 22. Artifact-Centric Development Principle v0.2

For every meaningful cognitive transition ask:

```text
What durable commitment changed?
```

Then ask:

```text
What context was compressed or lost?
What downstream state depends on that commitment?
Can the commitment be locally revised?
Can stale derived state be detected?
```

If the answer to the first question is only:

```text
"the model understood it better"
```

the capability has not yet been engineered.

But:

> **Artifact-centric does not mean artifact proliferation.**

Each artifact type must earn its existence.

---

# 23. No Transparent-Readout Assumption

CQC must not assume that fields such as:

```text
question_type
uncertainty
resolution_condition
failure diagnosis
```

are transparent probes into a pre-existing latent variable.

They are generated commitments made under an artifact contract.

Therefore:

```text
field present
!=
internal state transparently decoded

field confident
!=
internal representation has a matching scalar confidence

field schema-valid
!=
field semantically correct
```

This design caution should remain active throughout P2/P3.

---

# 24. Human-Readable Summary — Standing Requirement

Every development phase and remediation phase must return a structured human-readable Summary.

The Summary is a required acceptance surface.

At minimum:

```text
phase / contract
artifact changes
semantic changes
machine facts
benchmark evidence
failure ledger
architecture delta
cost / CI cycles
unresolved conflicts
one bounded next step
```

Machine facts come from machine artifacts.

Interpretive claims must be visibly separated from machine truth.

A Summary is itself an artifact and is therefore subject to the same rule:

```text
well-structured
!=
empirically supported
```

---

# 25. HO + LLM Interpretation Discipline

HO + ChatGPT interpretations are not exempt from artifact evidence.

Standing rule:

> **System explanations generated during review are themselves generated artifacts and must not be promoted into architecture merely because they are coherent.**

Examples:

```text
a metaphor that helped solve one failure
→ useful heuristic

the same metaphor generalized into architecture
→ requires independent evidence
```

This rule was earned after the `recursion` interpretation helped locate a simple solution but did not accurately name the implemented mechanism.

---

# 26. Cost Discipline

Default development loop:

```text
bounded contract
→ Local Claw local feedback loop
→ affected tests
→ affected deterministic entrypoints
→ meaningful push
→ GitHub Actions independent verification
→ structured Summary
→ HO + ChatGPT digestion / acceptance
```

CI is an independent verifier.

It must not become the primary debugger.

Every phase contract should define a bounded iteration budget.

---

# 27. Independent-Line Rule

CQC remains independent from the stable MAFS retrieval line until P5.

This rule has now received practical support from P0/P1:

```text
semantic artifact experimentation
did not contaminate retrieval truth
```

Reasons remain:

```text
independent artifact evolution
independent CI
clean acceptance lineage
clean benchmark comparison
separation of semantic-entry failures from retrieval failures
prevention of premature coupling
```

---

# 28. MAFS Boundary After Integration

After P5:

```text
Research Narrative
→ CandidateQuestionSet
→ SearchRequirementProfile
→ BudgetEnvelope
→ MAFS
→ EvidenceLandscapePackage
→ Evidence State
→ STOP
```

MAFS may characterize:

```text
coverage
evidence density
convergence
historical lineage
prior-art collision
known unknowns
```

CQC/MAFS must not decide:

```text
laboratory leverage
research priority
experimental tractability
ATTACK / PROBE / PARK / DROP
```

Those belong to a separate downstream capability.

---

# 29. Explicit Scientific-Line Exclusion

CQC does **not** implement:

```text
phenomenon
→ empirical law
→ constructive theory
→ principle theory
```

This hierarchy belongs to a scientific/research line.

It must not become a CQC taxonomy, ontology, or phase target.

---

# 30. Freeze Criteria v0.2

The CQC upstream module may be considered ready for final integration/freeze only when:

```yaml
candidate_question_artifact:
  seven_field_core_stable_or_evidence_based_revision_complete: true
  source_traceability_demonstrated: true
  ambiguity_preservation_demonstrated: true
  dependency_prerequisite_semantics_demonstrated: true
  source_context_retained: true

empirical:
  heterogeneous_real_tasks_run: true
  typed_vs_direct_artifact_value_characterized: true
  artifact_commitment_boundary_stress_tested: true
  projection_loss_failures_characterized: true
  revision_robustness_stress_tested: true

architecture:
  model_owns_semantic_cognition: true
  deterministic_semantic_intelligence_added: false
  question_type_not_authoritative_router: true
  unnecessary_ranker_or_solver_added: false
  artifact_count_bounded: true
  no_unearned_artifact_graph_framework: true

search_requirements:
  srp_is_contextually_digested: true
  source_narrative_context_available: true
  hard_type_routing_absent: true

integration:
  srp_consumable_by_mafs: true
  budget_envelope_consumable_by_mafs: true
  artifact_lineage_preserved: true
  stale_derived_state_detectable: true
```

No scalar CQC quality score is required.

---

# 31. Phase Authorization Rule

This master contract authorizes the development line, not automatic execution.

Before each phase:

```text
HO + ChatGPT
→ review evidence
→ issue bounded contract
→ Local Claw executes
→ GitHub Actions verifies
→ structured Summary
→ HO + ChatGPT accept / narrow / remediate
```

A phase may be:

```text
narrowed
rebaselined
merged
postponed
removed
```

when empirical evidence changes the architecture.

The roadmap is not a feature checklist.

---

# 32. Post-P1 Development Sequence

```text
CQC-P0
Minimal Digestion Surface
CLOSED / ACCEPTED
        ↓

CQC-P1
Real-Task Digestion Replay
+ Re-digestion Lineage
+ Artifact-Chain Consistency
CLOSED / ACCEPTED
        ↓

CQC-P2
Artifact Commitment Boundary
& Projection-Loss Stress Test
        │
        ├─ Semantic Commitment Boundary
        │
        └─ Artifact Revision Robustness
        ↓

CQC-P3
Contextual Search Requirement Digestion
CQS + source context → SRP
        ↓

CQC-P4
BudgetEnvelope
        ↓

CQC-P5
MAFS Integration
& Artifact-Lineage Closure
```

---

# 33. Immediate Next Step

The next authorized planning target is:

# **CQC-P2 — Artifact Commitment Boundary & Projection-Loss Stress Test**

P2 should begin by designing stress cases, not new schema.

Priority test families:

```text
1. ambiguous / underspecified research intent
2. mixed epistemic-type questions
3. granularity boundary cases
4. context-loss traps
5. false-precision traps
6. fan-out or diamond artifact dependencies
7. sequential revisions
8. partial stale regeneration
```

The first P2 contract must explicitly preserve:

```text
the seven-field CQS
source narrative as context reservoir
question_type as non-authoritative hint
no confidence field
no semantic scorer
no graph framework
```

unless a measured P2 failure earns a change.

---

# 34. Final Architecture Statement v0.2

The CQC line now rests on the following distinctions:

```text
The model performs contextual cognition.

Digestion creates a durable commitment.

The artifact does not perfectly reproduce cognition.

The artifact makes part of cognition addressable.

Semantic errors are repaired by model re-digestion.

Structural consistency is enforced by deterministic substrate.

A revised source invalidates stale derived state.

Source context remains available because typed artifacts are projections,
not replacements for the original narrative.

MAFS consumes the resulting contextual artifact chain.
```

Therefore:

> **CQC is not software that knows how to invent scientific questions, nor a symbolic model of how the LLM internally thinks. It is a thin artifact interface that makes selected research-intent commitments durable enough to inspect, revise, bind, and hand off — while preserving the richer source context from which those commitments were projected.**

---

# 35. Post-P1 Rebaseline Basis

This v0.2 rebaseline is grounded in two classes of evidence.

## 35.1 Internal development evidence

P0/P1 empirical work demonstrated:

```text
mechanical validity / semantic validity separation
true-prerequisite discipline
direct vs typed artifact distinction
earned re-digestion
content-addressed source binding
stale derived-state detection
local repairability
```

## 35.2 External design caution

Recent work on neural population codes and LLM language representation provides a useful design prior:

```text
LLM representations are distributed, contextual, graded, and high-dimensional;
clean symbolic boundaries should not be assumed;
decodable constructs should not be equated with the model's actual computation.
```

For CQC this evidence is used as a **design caution**, not as proof that scientific-question representations behave identically to linguistic representations.

The practical consequence is conservative:

```text
do not overinterpret schema fields as transparent latent variables;
do not assume category boundaries will become perfectly clean;
do not force hard routing from provisional labels;
stress artifact commitments before extending the schema.
```

---

# 36. Supersession Note

`CQC_Master_Development_Contract_v0.1.md` remains historically useful for understanding the original development intent.

For future development decisions, this v0.2 document is the current master roadmap.

Where v0.1 and v0.2 differ:

```text
v0.2 governs.
```
