# Local Claw Contract
## CQC-P0 — Minimal Digestion Surface + CandidateQuestionSet Artifact Freeze

**Contract ID:** `CQC-P0-MINIMAL-DIGESTION-SURFACE-v0.1`  
**Parent Contract:** `CQC_Master_Development_Contract_v0.1.md`  
**Work Actor:** **Local Claw**  
**Planning / Acceptance Authority:** **HO + ChatGPT**  
**Development Mode:** **Independent new repository / independent line**  
**Recommended Repository:** `mafs-cqc`  
**Working Branch:** `dev/cqc-p0`  
**Execution Truth Plane:** Git repository + GitHub Actions  
**Completion State:** `RETURN_FOR_HO_PLUS_CHATGPT_ACCEPTANCE`

---

# 0. Decision

CQC starts now as a new independent development line.

A separate G0 implementation round is not required. The minimum artifact freeze and the minimum working surface are combined into P0.

P0 has only two goals:

1. freeze the first minimal `CandidateQuestionSet` contract;
2. prove that a strong model can produce valid instances from real research narratives without adding deterministic “question intelligence”.

P0 does **not** authorize SRP, BudgetEnvelope, MAFS integration, ranking, scoring, or research-priority logic.

---

# 1. Repository bootstrap

Create a new repository:

```text
mafs-cqc
```

Preferred flow:

```text
create minimal main
→ create dev/cqc-p0
→ perform P0 only on dev/cqc-p0
```

If remote creation is unavailable:

```text
REPOSITORY_BOOTSTRAP_BLOCKED
→ STOP
```

Do not place CQC inside the existing MAFS repository as a fallback.

If `mafs-cqc` already exists with unrelated or ambiguous content:

```text
REPOSITORY_IDENTITY_CONFLICT
→ STOP
```

---

# 2. Governing boundary

## Model owns

```text
semantic understanding
question decomposition
granularity judgment
ambiguity recognition
dependency recognition
provisional question typing
searchable reformulation
```

## Deterministic substrate owns

```text
artifact schema
artifact identity
source-trace validation
dependency integrity validation
source-narrative hash verification
deterministic human-readable rendering
machine acceptance facts
```

The deterministic substrate must not decide which scientific questions are correct.

---

# 3. P0 cognitive transition

The only authorized transition is:

```text
ResearchNarrative
        ↓ model digestion
CandidateQuestionSet
```

P0 succeeds if another process can inspect, validate, render, and later consume the resulting artifact without reconstructing latent reasoning.

---

# 4. CandidateQuestionSet v0.1

## Set-level envelope

```yaml
CandidateQuestionSet:
  artifact_id:
  schema_version:
  source_narrative_sha256:
  source_narrative:
  questions:
```

## CandidateQuestion

Start from exactly these seven fields:

```yaml
CandidateQuestion:
  question_id:
  statement:
  source_trace:
  question_type:
  dependencies:
  resolution_condition:
  uncertainty:
```

Fields may be removed if proven redundant.

Do not add fields unless a real P0 dry-run cannot be represented honestly without them.

---

# 5. Field semantics

### `question_id`
Local stable identifier such as `CQ-01`. No semantic meaning encoded in the ID.

### `statement`
The smallest useful scientific question for which a distinct evidence landscape could materially change the research framing.

It must be independently searchable and scientifically meaningful, not a lexical fragment.

### `source_trace`
Primary anti-drift field.

Use the minimum exact-source representation:

```yaml
source_trace:
  - exact_quote: "..."
```

The validator must confirm that every `exact_quote` occurs verbatim in `source_narrative`.

Do not build line-offset, token-offset, embedding, or semantic-span provenance machinery in P0.

Questions not traceable to source intent must not silently enter `questions[]`. If the model notices an interesting but unentailed expansion, it may mention it only in a separate non-binding human note.

### `question_type`
Use the master contract’s provisional vocabulary as guidance, but do **not** freeze it as an exhaustive ontology.

The schema should accept any non-empty string.

If a real task requires a new type, preserve it honestly and report it; do not coerce it into the wrong class.

### `dependencies`
List prerequisite `question_id` values only when they materially affect search order or interpretation.

Machine checks:

```text
target exists
no self-dependency
DAG is acyclic
```

The validator does not judge scientific correctness of the dependency.

### `resolution_condition`
Concise statement of what evidence would materially resolve, falsify, narrow, or otherwise change the state of the question.

This is not a search plan.

### `uncertainty`
Use only:

```yaml
uncertainty: null
```

or free text.

Do not introduce an uncertainty enum in P0.

Preserve ambiguity; do not “clean up” an ambiguous narrative into false certainty.

---

# 6. Narrative identity

Store each source narrative verbatim.

Compute:

```text
source_narrative_sha256
```

from the exact UTF-8 bytes used for digestion.

This is only an identity/lineage anchor. Do not build a general provenance framework.

---

# 7. Model-facing instruction

Create one concise instruction artifact, recommended:

```text
instructions/cqc_p0_digest.md
```

It should tell the model to:

```text
preserve source intent
decompose only where a distinct evidence landscape exists
preserve ambiguity
expose prerequisites
produce CandidateQuestionSet v0.1
avoid open-ended ideation
avoid answering the questions
avoid search planning
avoid literature retrieval
```

Keep it short. Do not encode decomposition intelligence as a large procedural prompt.

---

# 8. No automated LLM runtime

P0 does **not** require:

```text
LLM API integration
model router
agent framework
prompt orchestration framework
MCP server
web service
database
queue
workflow engine
```

Local Claw may act as the model executor during development and commit the resulting example artifacts.

GitHub Actions validates committed artifacts; CI does not regenerate model cognition.

---

# 9. Minimal implementation surface

Preferred structure:

```text
schemas/
  candidate_question_set.v0.1.schema.json

instructions/
  cqc_p0_digest.md

scripts/
  validate_cqs.py
  render_cqs.py        # optional

examples/
  inputs/
  outputs/
  rendered/

tests/
docs/
```

Prefer plain functions, dicts, JSON, Markdown, and JSON Schema.

No service layer, class hierarchy, database, or framework is authorized.

---

# 10. Real-narrative dry runs

Use three heterogeneous real research narratives:

```text
A. GF / EM identity-lineage narrative
B. Virtual Cell / novelty-framing narrative
C. one mechanism or mixed narrative already used in prior MAFS work
```

For each, produce:

```text
source narrative
source SHA256
CandidateQuestionSet JSON
deterministic human-readable rendering
validation result
```

P0 does not retrieve literature, run MAFS, or score scientific quality.

The goal is to pressure-test the artifact contract across different semantic shapes.

---

# 11. Deterministic validation

Required machine checks:

```text
schema valid
artifact_id present
schema_version present
source hash matches
question_id unique
statement non-empty
every source_trace exact quote exists in narrative
dependency target exists
no self-dependency
dependency DAG acyclic
resolution_condition non-empty
uncertainty is null or text
questions[] non-empty
```

Must **not** machine-score:

```text
scientific importance
semantic correctness
granularity quality
scientific dependency truth
novelty
research usefulness
```

---

# 12. Human-readable rendering

Render each CandidateQuestion deterministically from JSON, showing:

```text
question_id
statement
source trace
type
dependencies
resolution condition
uncertainty
```

The renderer must not add new model interpretation.

JSON is the machine source of truth.

---

# 13. Explicit P0 non-goals

Do not implement:

```text
Search Requirement Profile
BudgetEnvelope
MAFS adapter
MAFS search
query generation
axis assignment
provider selection
question ranking
importance score
granularity score
dependency solver
novelty score
research-opportunity generation
ATTACK / PROBE / PARK / DROP
artifact framework
agent framework
ontology system
memory system
database
API service
UI
```

Also exclude the scientific line:

```text
phenomenon
→ empirical law
→ constructive theory
→ principle theory
```

---

# 14. P0 empirical claim boundary

P0 asks only:

> Can a strong model’s implicit research-intent digestion be made explicit as a small CandidateQuestionSet artifact without forcing that cognition into deterministic software?

P0 must **not** claim:

```text
CQC improves search quality
CQC beats narrative-only baseline
CQC improves scientific correctness
```

Those are P1 questions.

---

# 15. What P0 must report, not automatically fix

Record any observed pressure such as:

```text
field redundancy
missing representational need
source-trace difficulty
uncertainty collapse
too-coarse questions
too-fine questions
dependency ambiguity
question-type mismatch
```

Observed failure is evidence for later design.

It is not automatic authorization to add architecture during P0.

---

# 16. Development discipline

Before first meaningful push, locally pass:

```text
affected tests
validator on all three examples
renderer on all three examples
source-hash checks
dependency checks
```

GitHub Actions is an independent verifier, not the primary debugger.

Maximum:

```text
3 meaningful code-changing push → CI → diagnose cycles
```

If still not acceptance-green after the third:

```text
ITERATION_BUDGET_EXHAUSTED
→ STOP
```

Infrastructure-only reruns with no code change do not count.

---

# 17. CI minimum

Use one minimal CI workflow validating:

```text
tests
schema
all committed example CQS artifacts
source hashes
source traces
dependency DAG integrity
deterministic rendering reproducibility
```

Do not create multi-workflow governance machinery in P0.

---

# 18. Required artifacts

At minimum:

```text
CQC_Master_Development_Contract_v0.1.md
schemas/candidate_question_set.v0.1.schema.json
instructions/cqc_p0_digest.md
scripts/validate_cqs.py
examples/inputs/<3 narratives>
examples/outputs/<3 CQS json artifacts>
examples/rendered/<3 human-readable artifacts>
tests/
docs/CQC_P0_SUMMARY.md
docs/CQC_P0_METRICS.json
docs/CQC_P0_SHA256_MANIFEST.txt
```

If a separate renderer script is used, include it.

---

# 19. Machine metrics

`docs/CQC_P0_METRICS.json` should contain only factual machine outputs:

```yaml
contract_id:
commit_sha:
ci_run_id:
artifact_schema_version:
example_count:
schema_valid_count:
source_hash_valid_count:
source_trace_valid_count:
dependency_graph_valid_count:
deterministic_render_valid_count:
meaningful_push_ci_cycles:
production_file_count:
test_count:
```

No synthetic scalar “CQC quality score”.

---

# 20. Human summary

`docs/CQC_P0_SUMMARY.md` is the first HO + ChatGPT review surface.

It must state:

```text
what was built
final field set
what was removed, if anything
three narratives used
mechanical validation results
observed semantic tensions
whether uncertainty remained explicit
whether any new architecture was added and why
CI run / commit
meaningful CI cycles
bounded recommendation for P1
```

Machine facts come from pinned CI / committed artifacts.

---

# 21. Stop conditions

STOP and return `ARCHITECTURE_EXPANSION_BLOCKED` if P0 appears to require:

```text
deterministic semantic question selection
granularity scoring engine
question ranking engine
dependency solver
semantic similarity subsystem
LLM orchestration framework
MAFS integration
SRP generation
BudgetEnvelope generation
large ontology
database/service layer
```

Return the measured failure instead of implementing first and justifying later.

---

# 22. Acceptance standard

CQC-P0 is accepted only when:

```yaml
repository:
  independent_new_line: true
  ci_is_independent: true

artifact:
  candidate_question_set_contract_frozen: true
  artifact_small_and_inspectable: true
  source_narrative_identity_preserved: true
  exact_source_trace_machine_validated: true
  dependency_integrity_machine_validated: true
  uncertainty_can_remain_explicit: true

cognition_boundary:
  model_owns_decomposition: true
  model_owns_granularity_judgment: true
  deterministic_question_intelligence_added: false

examples:
  heterogeneous_real_narratives: 3
  all_structurally_valid: true
  all_human_readable: true

scope:
  srp_implemented: false
  budget_implemented: false
  mafs_integration_performed: false
  llm_runtime_framework_added: false
  ranking_or_scoring_engine_added: false

execution:
  local_pre_push_check_passed: true
  meaningful_push_ci_cycles_lte_3: true
  final_ci_passed: true
```

Semantic quality is reviewed by HO + ChatGPT after return.

P0 structural acceptance must not pretend to be a scientific-quality verdict.

---

# 23. Required return note

```text
CQC-P0 Status:
READY_FOR_REVIEW
| REPOSITORY_BOOTSTRAP_BLOCKED
| REPOSITORY_IDENTITY_CONFLICT
| ARCHITECTURE_EXPANSION_BLOCKED
| ITERATION_BUDGET_EXHAUSTED
| BLOCKED

Repository:
<repo>

Branch:
<branch>

Commit SHA:
<sha>

CI Run ID:
<id>

CandidateQuestionSet Schema:
<path>

Final Per-Question Fields:
<fields>

Real Narrative Examples:
<n>

Schema Validation:
PASS | FAIL

Source Narrative Hash Validation:
PASS | FAIL

Exact Source Trace Validation:
PASS | FAIL

Dependency DAG Validation:
PASS | FAIL

Deterministic Rendering:
PASS | FAIL

Uncertainty Preserved:
YES | NO | MIXED

Deterministic Question Intelligence Added:
NO | YES

SRP Implemented:
NO | YES

Budget Implemented:
NO | YES

MAFS Integration Performed:
NO | YES

Meaningful Push/CI Cycles:
<n>

Human Summary:
<path>

Observed Contract Pressure:
<brief list>

Recommended Next Step:
CQC-P1 | P0-RA | STOP_AND_REVIEW
```

---

# 24. Final instruction

Do not write software that knows how to invent the questions.

Let the model digest the narrative.

Make the result durable.

Validate only what software can honestly validate.

Preserve ambiguity instead of cleaning it away.

Return the artifact to HO + ChatGPT for digestion.

The success of P0 is not a clever compiler.

The success of P0 is that the first digestion becomes visible without architecture pretending to be the intelligence.
