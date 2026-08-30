# CQC-P0 — Human Summary

First reading entry point for HO + ChatGPT. Machine truth lives in
`docs/CQC_P0_METRICS.json` and `docs/CQC_P0_SHA256_MANIFEST.txt`; this
document interprets and never overwrites them.

## 1. Contract and status

- Contract: `CQC-P0-MINIMAL-DIGESTION-SURFACE-v0.1` (parent: `CQC-MASTER-v0.1-DIGESTION-AS-ARTIFACT`)
- Status: **READY_FOR_REVIEW**
- Repository: `mo21cn/mafs-cqc` (independent new line; independent CI)
- Branch: `dev/cqc-p0`

## 2. What was built

The minimal digestion surface per contract §4-§12:

- `schemas/candidate_question_set.v0.1.schema.json` — frozen CandidateQuestionSet v0.1 contract
- `instructions/cqc_p0_digest.md` — model-facing digestion instruction (short, per §7)
- `scripts/validate_cqs.py` — deterministic validator, all 13 machine checks of §11, zero-dependency (bundled mini JSON-Schema validator)
- `scripts/render_cqs.py` — deterministic human-readable renderer (§12), byte-stable, no timestamps
- `scripts/build_p0.py` — machine metrics + SHA-256 manifest builder
- `examples/` — 3 real heterogeneous narratives (inputs) + 3 digested CandidateQuestionSets (outputs) + 3 renderings
- `tests/` — 22 tests: every §11 rule, renderer determinism, committed-artifact reproducibility
- `.github/workflows/cqc-p0.yml` — single minimal CI workflow (§17)

No LLM runtime, no framework, no service layer (§8, §13 respected).

## 3. Final field set

Set envelope: `artifact_id, schema_version, source_narrative_sha256, source_narrative, questions[]`.
Per question (exactly the seven contract fields): `question_id, statement,
source_trace[{exact_quote}], question_type, dependencies[], resolution_condition, uncertainty`.

**Nothing was removed; nothing was added.** All seven fields earned their keep
across the three dry runs.

## 4. Three narratives used (heterogeneous, real domains)

| Tag | Domain | Semantic shape |
|---|---|---|
| A_gf_em | GF / EM identity-lineage (real Replay B task, oracle-verified facts) | entity resolution + terminology/lineage + negative branch |
| B_virtual_cell | Virtual Cell novelty-framing | prior-art boundary + generalization + fast-moving claims |
| C_hbot_ovary | HBOT ↔ ovarian reserve (real MAFS v0.x replay domain) | mechanism + intervention controls + measurement + causal claim + translation |

Narrative A facts are anchored in the independently verified scholarly oracle of
`mafs-v3-p0` (von Reyn 2014 `10.1038/nn.3741`; Namiki 2018 `10.7554/eLife.34272`;
Scheffer 2020; FlyWire root IDs recorded as unverified, not fabricated).
Narratives B and C are real research-domain narratives written for this dry run
from the operator-side perspective; no citations are fabricated inside them.

## 5. Mechanical validation results

All numbers from `docs/CQC_P0_METRICS.json` (machine-generated):

- example_count: 3 — schema_valid 3/3; source_hash 3/3; exact source trace 3/3;
  dependency DAG 3/3; narrative-input byte match 3/3; deterministic render 3/3.
- test_count: 22 (all passing locally and in CI).

## 6. Observed semantic tensions (recorded, NOT fixed — §15)

1. **Verbatim trace vs markdown hard-wrapping.** The first digestion run failed
   12/14 trace checks because narrative paragraphs were hard-wrapped across
   lines while quotes were single-line. Fixed by re-authoring narratives with
   one sentence per line (byte-exact quotes). Pressure for P1: if narratives
   come as flowing documents, either an ingestion convention (sentence-per-line)
   or an explicitly-defined whitespace-normalized *secondary* check will be
   needed; P0 kept the validator strictly verbatim per contract.
2. **Sentence-level anchoring is the minimum unit.** One trace (A CQ-02) needed
   a 50+-word sentence because the semantic anchor is the full conflation
   statement; fine-grained anchoring would require offset machinery, which P0
   correctly forbids.
3. **Question-type vocabulary sufficed.** All 14 questions across three
   heterogeneous domains mapped into the provisional vocabulary; no coercion
   was needed, and the free-string rule was exercised in tests.
4. **Uncertainty stayed explicit.** 5/14 questions carry non-null free-text
   uncertainty (A: 3, B: 1, C: 1). The strongest pressure was on C CQ-04
   (animal-IRI protection result must not silently generalize to healthy
   ovaries) and B CQ-03 (fast-moving claims force time-bound conclusions).
   No ambiguity was "cleaned away".
5. **resolution_condition vs search-plan boundary.** While authoring, the
   wording repeatedly drifted toward retrieval planning ("query Crossref for...")
   and had to be pulled back to "what evidence would resolve this". P1 should
   watch this boundary; it is a model-discipline issue, not a validator issue.
6. **Dependencies were sparse by design.** 4 dependency edges across 14 questions,
   only where search order/interpretation materially depends (e.g. C CQ-02→CQ-01,
   C CQ-04→CQ-01+CQ-02, A CQ-05→CQ-03, B CQ-02→CQ-01). The validator checked
   structure only, never scientific truth of the edge.
7. **Mechanical assembler need.** Model-produced question fragments + narrative
   byte injection were combined by a one-shot script kept OUT of the repository
   (assembly is substrate work, not question intelligence). If P1 digests many
   narratives, a small deterministic assembler earns a place in `scripts/`.
   Recorded as evidence, not implemented now.

## 7. Cognition boundary honesty

- Decomposition, granularity, typing, dependency and uncertainty judgments were
  produced by the model (Local Claw) and are visible in the committed artifacts.
- Deterministic code only validates structure, identity, trace verbatim-ness,
  DAG integrity, and renders. **No deterministic question intelligence was added.**
- CI validates committed artifacts; it never regenerates cognition (§8).

## 8. Execution record

- Meaningful push/CI cycles: see `docs/CQC_P0_METRICS.json` (`meaningful_push_ci_cycles`).
- CI run: see `docs/CQC_P0_METRICS.json` (`ci_run_id`) — pinned workflow `cqc-p0`.
- Pinned commit for the verified artifact set: see `commit_sha` in METRICS.
- Local pre-push checks: pytest (22), validator on all 3 artifacts with input
  cross-check, renderer reproducibility on all 3.

## 9. Bounded recommendation for P1

Proceed to **CQC-P1 — Real-Task Digestion Replay**, with the baseline-protocol
question resolved first in the P1 phase contract: who defines the evaluation
protocol (HO + ChatGPT recommended, so that the executor is never the scorer),
and what the narrative-only baseline receives (same downstream task, same
budget). Also carry in: the sentence-per-line ingestion convention question
(tension 1) and the deterministic assembler need (tension 7) as P1 design inputs.
