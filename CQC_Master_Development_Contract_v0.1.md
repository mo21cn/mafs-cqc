# Candidate Question Compiler (CQC)
## Master Development Contract v0.1
### Digestion-as-Artifact Upstream Module for MAFS

**Contract ID:** `CQC-MASTER-v0.1-DIGESTION-AS-ARTIFACT`  
**Module:** Candidate Question Compiler (CQC)  
**Development Mode:** Independent line → empirical validation → bounded integration into MAFS  
**Primary Work Actor:** Local Claw  
**Planning / Acceptance Authority:** HO + ChatGPT  
**Execution Source of Truth:** Git repository + GitHub Actions  
**Status:** Master contract / phase contracts required before implementation of each step  
**Development Principle:** Thin architecture, model-owned cognition, artifact-owned continuity

---

# 0. Purpose

The Candidate Question Compiler exists to solve one narrow but fundamental problem:

```text
Research Narrative
        ↓
implicit model understanding
        ↓
CandidateQuestion Artifact Set
```

MAFS should not assume that a Human Operator has already transformed an ambiguous research narrative into perfectly scoped, independently searchable scientific questions.

CQC therefore provides the semantic entry point to MAFS.

However, CQC is **not** a software system that attempts to reproduce scientific intelligence in deterministic code.

Its role is:

> **Make the model's first research-intent digestion explicit, inspectable, reusable, and downstream-operable as an artifact.**

The model performs the cognition.

CQC defines and preserves the artifact boundary.

---

# 1. Governing Thesis

This module is developed under the working hypothesis:

> **Digestion is artifact.**

For engineering purposes:

```text
Reasoning
= latent cognition may change

Digestion
= cognition becomes durable
  through a changed, usable artifact
```

Therefore the primary engineering target is not:

```text
"How do we code an intelligent question generator?"
```

It is:

```text
"What artifact must exist after the model has digested
a research narrative?"
```

The first CQC artifact is:

```text
CandidateQuestionSet
```

This contract does not claim a complete Digestion Theory.

CQC is the first bounded implementation used to test whether artifact-mediated digestion improves a real research workflow.

---

# 2. Architectural Position

The intended upstream chain is:

```text
Research Narrative
        ↓
Candidate Question Compiler
        ↓
CandidateQuestionSet
        ↓
Search Requirement Profile
        ↓
Budget Envelope
        ↓
MAFS Multi-Axis Evidence Search
        ↓
EvidenceLandscapePackage
```

CQC is developed independently first.

It is merged into the MAFS upstream path only after its artifact contract and empirical value are demonstrated.

The development line must not depend on a full MAFS rewrite.

---

# 3. Core Boundary

## 3.1 CQC owns

CQC owns the externalization boundary for:

- research-intent decomposition;
- question identity;
- source traceability;
- question dependencies;
- resolution conditions;
- explicit uncertainty;
- artifact validation;
- downstream handoff.

## 3.2 The model owns

The model owns:

- semantic understanding;
- decomposition judgment;
- granularity judgment;
- interpretation of ambiguous research intent;
- recognition of prerequisite questions;
- assignment of provisional question type;
- reformulation necessary to make a question searchable.

## 3.3 CQC does not own

CQC must not become:

- a deterministic QuestionSplitter;
- a GranularityScorer;
- a QuestionRanker;
- a semantic relevance solver;
- a research-priority engine;
- a hypothesis-generation engine;
- a theory-construction engine;
- a general AI scientist;
- a universal ontology compiler.

The architecture must not duplicate model cognition merely because traditional software would encode that cognition as a subsystem.

---

# 4. Compile, Do Not Freely Generate

The Candidate Question Compiler is not a creativity engine.

Its job is:

> Convert the supplied research narrative into the smallest useful set of independently searchable scientific question artifacts while preserving the original research intent.

Preferred behavior:

```text
semantic decomposition
+
normalization
+
dependency exposure
+
uncertainty preservation
```

Not:

```text
open-ended research ideation
```

A scientifically interesting question that cannot be traced to the source intent should not silently enter the CandidateQuestionSet.

If additional questions are useful but not entailed by the source narrative, they must be explicitly marked as an expansion rather than silently merged into the compiled output.

---

# 5. CandidateQuestionSet Is the Primary Artifact

The first implementation target is the artifact contract, not the compiler algorithm.

A provisional minimal form is:

```yaml
CandidateQuestionSet:
  source_intent:
  questions:
    - question_id:
      statement:
      source_trace:
      question_type:
      dependencies:
      resolution_condition:
      uncertainty:
```

The exact schema is not frozen by this master contract.

Phase G0 will decide the smallest sufficient representation.

The first version should prefer **5–7 meaningful fields** over a large schema.

---

# 6. Required Artifact Properties

Every CandidateQuestion artifact should eventually satisfy the following semantic properties.

## 6.1 Traceability

The question must remain traceable to the source narrative.

The system should be able to answer:

```text
Where did this question come from?
```

## 6.2 Atomicity

A CandidateQuestion should be:

> the smallest unit for which a distinct evidence landscape could meaningfully change the research framing.

Too coarse:

```text
"Does oxygen affect ovarian aging?"
```

Too fine:

```text
many lexical fragments that are individually searchable
but scientifically meaningless
```

## 6.3 Searchability

A CandidateQuestion must be specific enough to support a downstream search requirement.

## 6.4 Dependency

Prerequisite relationships should be explicit when they materially affect search order.

Example:

```text
Q1 — Is paper X correctly identified?
        ↓
Q2 — Does paper X establish naming relation Y?
        ↓
Q3 — Can Y be mapped to dataset entity Z?
```

## 6.5 Resolution condition

The artifact should state what evidence would materially resolve or change the state of the question.

## 6.6 Uncertainty

The compiler must preserve ambiguity rather than convert uncertainty into false certainty.

---

# 7. Question Types

A provisional vocabulary may include:

```text
ENTITY_RESOLUTION
SOURCE_CONTENT
TERMINOLOGY_OR_NAMING
HISTORICAL_LINEAGE
MECHANISM
CAUSAL_CLAIM
NOVELTY_OR_PRIOR_ART
MEASUREMENT_OR_OBSERVABILITY
INTERVENTION_OR_CONTROL
GENERALIZATION
TRANSLATION
TOOL_OR_METHOD
```

This taxonomy is **not frozen**.

It exists only to support early real-task testing.

A future phase may collapse, rename, or split types based on empirical evidence.

The system must not force all questions through one search template.

---

# 8. Development Line

The CQC line consists of six bounded phases.

Each phase requires its own implementation contract before execution.

---

# 8.1 CQC-G0 — Artifact Contract Freeze

**Question:**

> What must the first digestion leave behind?

Primary output:

```text
CandidateQuestionSet Artifact Contract
```

G0 should define:

- minimal required fields;
- optional fields;
- traceability semantics;
- dependency semantics;
- uncertainty semantics;
- artifact identity/versioning;
- validation rules;
- human-readable rendering.

G0 must not implement a decomposition algorithm.

G0 success means:

> a model can produce a CandidateQuestionSet that another process can inspect and consume without reconstructing the original latent reasoning.

---

# 8.2 CQC-P0 — Minimal Digestion Surface

**Target:**

```text
Research Narrative
→ CandidateQuestionSet
```

P0 should remain extremely thin.

Expected ingredients:

```text
artifact contract
+
model invocation instruction
+
artifact validator
+
human-readable output
```

P0 must not implement:

```text
SRP
BudgetEnvelope
MAFS integration
question ranking
scientific importance scoring
```

Primary empirical question:

> Can the implicit decomposition behavior already observed in strong models be made explicit without damaging it?

---

# 8.3 CQC-P1 — Real-Task Digestion Replay

P1 is primarily an empirical validation phase.

Use heterogeneous real tasks rather than synthetic NLP examples.

Preferred benchmark families include:

```text
1. entity / identity resolution
   e.g. GF / EM neuron-ID task

2. novelty / prior-art audit

3. mechanism question

4. source-content verification

5. mixed narrative containing
   entities + tools + mechanisms + claims
```

Where possible compare:

```text
Narrative-only baseline
vs
Narrative → CQC Artifact → downstream task
```

Primary evaluation dimensions:

```text
intent preservation
critical-question recall
unnecessary-question rate
granularity consistency
dependency correctness
question-type usefulness
searchability
missed-critical-question rate
downstream usability
```

Generic NLP similarity is not a primary metric.

---

# 8.4 CQC-P2 — Granularity & Dependency Closure

P2 is authorized only by failures observed in P1.

Potential failure families:

```text
too coarse
too fine
duplicate questions
false dependency
missing prerequisite
intent drift
unsearchable question
uncertainty collapsed into certainty
```

P2 should repair artifact constraints and invocation discipline before adding algorithms.

Do not add a `GranularityScorer`, `DependencySolver`, or equivalent subsystem unless a real measured failure cannot be solved by a thinner artifact rule.

Primary target:

> Make CandidateQuestionSet reliable enough to serve as the semantic input to search planning.

---

# 8.5 CQC-P3 — Search Requirement Profile

P3 introduces the second digestion artifact:

```text
CandidateQuestionSet
        ↓
SearchRequirementProfile
```

A provisional form may include:

```yaml
SearchRequirementProfile:
  question_id:
  required_axes:
  optional_axes:
  irrelevant_axes:
  evidence_types:
  source_classes:
  depth:
  stopping_requirements:
```

Core rule:

> **Multi-Axis does not mean All Axes Every Time.**

MAFS should receive an adaptive search topology.

The model determines the topology.

The artifact makes that topology explicit and executable.

P3 must not become a deterministic scientific search planner.

---

# 8.6 CQC-P4 — BudgetEnvelope

P4 adds a lightweight resource envelope to the Search Requirement Profile.

The interface should remain minimal:

```yaml
budget: STANDARD
```

Possible profiles:

```text
LIGHT
STANDARD
DEEP
AUTO
```

AUTO is optional and should only be implemented if prior phases demonstrate real value.

Required budget semantics:

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

Budget may cover:

```text
wall time
model/token consumption
external retrieval calls
expensive evidence escalation
```

Do not build a general Cost Manager unless real failures later justify it.

---

# 8.7 CQC-P5 — MAFS Integration & Freeze

P5 integrates the independently validated CQC line into MAFS.

Target artifact chain:

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

The integration test should verify:

```text
traceability
artifact identity
lineage
state continuity
authority boundaries
downstream usability
```

P5 is not a MAFS rewrite.

Integration should be the smallest adapter necessary to allow MAFS to consume the upstream artifacts.

CQC may be frozen only after the merged path demonstrates value on real tasks.

---

# 9. Search Requirement Profile Principles

The Search Requirement Profile should answer:

```text
Which search axes matter?
Which axes do not matter?
Which evidence types can resolve the question?
Which source classes are required or preferred?
How deep should the search go?
What constitutes sufficient coverage?
What resource envelope applies?
```

It must remain a model-produced artifact.

Do not encode scientific search intelligence as a fixed decision tree unless a future benchmark proves such a rule necessary.

---

# 10. Budget Principles

Budget is question-dependent.

Conceptually:

```text
Question Type
→ Search Topology
→ Cost Shape
```

A simple identity-resolution question may require:

```text
few axes
low depth
small budget
```

A mechanism or novelty audit may require:

```text
multiple structural axes
historical terminology
adjacent disciplines
selective deep evidence review
larger budget
```

Budget limits execution.

Budget does not define scientific truth.

---

# 11. Validation Philosophy

The CQC line is benchmark-driven.

Use real failures to justify new architecture.

Standing rule:

> **Measured failure justifies architecture. Architecture does not justify itself.**

And:

> **No measured failure → no new architecture.**

Each real failure may earn:

```text
an artifact invariant
a validation rule
a regression benchmark
a small implementation constraint
```

It does not automatically earn:

```text
a new engine
a new ranker
a new solver
a new framework
```

---

# 12. Digestion-as-Artifact Research Value

CQC also serves as the first bounded empirical implementation of the working Digestion hypothesis.

The first testable transition is:

```text
Research Narrative
        ↓ model digestion
CandidateQuestionSet
```

The research question is not:

```text
"Can an LLM generate questions?"
```

It is:

> **Does making the model's first research-intent digestion explicit as a durable artifact improve downstream scientific search behavior compared with answer-centric or implicit workflows?**

Possible downstream indicators include:

```text
reduced framing drift
higher critical-question recall
better dependency handling
better axis allocation
lower repeated-reasoning cost
greater cross-stage consistency
better provenance / traceability
```

This contract does not require publication work.

It only preserves the implementation structure necessary for future empirical analysis.

---

# 13. Artifact-Centric Development Principle

For every meaningful cognitive transition in the CQC line, ask:

```text
What durable artifact changed?
```

If the answer is only:

```text
"the model understood it better"
```

the capability has not yet been engineered.

However:

> Artifact-centric does not mean artifact proliferation.

Each new artifact type must earn its existence by enabling a real downstream transition.

The initial line should remain centered on only:

```text
CandidateQuestionSet
SearchRequirementProfile
BudgetEnvelope
```

No broad Artifact Framework is authorized.

---

# 14. Human-Readable Summary — Standing Convention

Every CQC development phase must return one concise human-readable summary for HO + ChatGPT.

The summary should include:

```text
phase / contract
what changed
what artifact changed
benchmark or validation result
files changed
cost / CI cycles
unresolved failures
one bounded next step
```

Machine facts must come from machine artifacts.

The human summary is a digestion/acceptance surface, not a competing source of truth.

---

# 15. Cost Discipline

CQC should remain lighter than the MAFS execution spine.

The module exists to expose model cognition, not replace it.

Default development discipline:

```text
local dry-run
→ affected tests
→ affected deterministic entrypoints
→ one meaningful push
→ GitHub Actions independent verification
```

CI should not become the primary debugging loop.

Every phase contract should define a bounded development envelope appropriate to that phase.

---

# 16. Independent-Line Rule

CQC should be developed independently from the frozen/stable MAFS retrieval line until P5.

Reasons:

```text
avoid destabilizing proven retrieval behavior
allow artifact design to evolve
permit clean A/B testing
separate semantic-entry failures from retrieval failures
prevent premature coupling
```

P5 is the only phase authorized to merge the validated CQC path into the main MAFS flow.

---

# 17. MAFS Boundary After Integration

After P5, the intended MAFS boundary becomes:

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
evidence density
coverage
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

# 18. Explicit Scientific-Line Exclusion

The CQC development line does **not** implement or model:

```text
phenomenon
→ empirical law
→ constructive theory
→ principle theory
```

That hierarchy belongs to a separate scientific/research line.

It must not become a CQC feature, taxonomy, ontology, or development milestone.

---

# 19. Freeze Criteria

The CQC module may be considered ready for integration/freeze only when:

```yaml
artifact:
  candidate_question_set_is_stable: true
  source_traceability: demonstrated
  uncertainty_preservation: demonstrated
  dependency_representation: useful
  downstream_searchability: demonstrated

empirical:
  heterogeneous_real_tasks_run: true
  critical_question_failures_measured: true
  major_granularity_failures_closed: true
  narrative_to_artifact_value_demonstrated: true

architecture:
  model_owns_cognition: true
  deterministic_question_intelligence_added: false
  unnecessary_ranker_or_solver_added: false
  artifact_count_bounded: true

integration:
  srp_consumable_by_mafs: true
  budget_envelope_consumable_by_mafs: true
  artifact_lineage_preserved: true
```

No single scalar CQC quality score is required.

---

# 20. Phase Authorization Rule

This master contract authorizes the **development line**, not automatic execution of all phases.

Before each phase:

```text
HO + ChatGPT
→ review previous evidence
→ issue bounded phase contract
→ Local Claw executes
→ GitHub Actions verifies
→ HO + ChatGPT digest / accept
```

A later phase may be narrowed, postponed, merged, or removed if earlier empirical evidence changes the architecture.

The roadmap is not a feature checklist.

---

# 21. Final Architecture Statement

The CQC line is based on the following distinction:

```text
The model performs digestion.

The artifact makes digestion durable.

The architecture validates, preserves,
and hands off the artifact.

MAFS consumes the artifact.
```

Therefore:

> **CQC is not software that knows how to invent scientific questions. It is the explicit artifact interface through which a model's implicit research-intent digestion becomes usable scientific state.**

---

# 22. Development Sequence

```text
CQC-G0
Artifact Contract Freeze
        ↓
CQC-P0
Minimal Digestion Surface
        ↓
CQC-P1
Real-Task Digestion Replay
        ↓
CQC-P2
Granularity & Dependency Closure
        ↓
CQC-P3
Search Requirement Profile
        ↓
CQC-P4
BudgetEnvelope
        ↓
CQC-P5
MAFS Integration & Freeze
```

This sequence is the current master plan.

It may evolve only from empirical evidence, not from feature-completeness pressure.

---

# 23. First Next Step

The next authorized planning target after this master contract is reviewed is:

```text
CQC-G0 — CandidateQuestion Artifact Contract Freeze
```

G0 should answer only:

> **What is the minimum durable artifact that must exist after the first research-intent digestion?**

No compiler implementation should begin before that artifact boundary is frozen.
