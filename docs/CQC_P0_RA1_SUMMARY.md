# CQC-P0-RA1 — Structured Summary

Human interpretation layer for HO + ChatGPT. Machine truth: `docs/CQC_P0_RA1_METRICS.json`
and `docs/CQC_P0_RA1_SHA256_MANIFEST.txt`.

## A — Acceptance Header

```yaml
contract_id: CQC-P0-RA1-SEMANTIC-FIDELITY-STRUCTURED-DIGESTION-CLOSURE-v0.1
status: READY_FOR_REVIEW
repository: mo21cn/mafs-cqc
branch: dev/cqc-p0
verified_commit_sha: (see docs/CQC_P0_RA1_METRICS.json — pinned after CI, docs-only commit follows)
ci_run_id: (see docs/CQC_P0_RA1_METRICS.json)
meaningful_push_ci_cycles: 1
```

## B — Artifact Delta Table

All semantic field changes across the three artifacts (20 field edits; statements unchanged).
`RC` = resolution_condition, `ST` = source_trace, `DEP` = dependencies.

| Artifact | Question | Field | Before Problem | After Meaning | Why This Is a Digestion Fix |
|---|---|---|---|---|---|
| A_gf_em | CQ-01 | RC | "直接获取…并逐项检查…则提取并记录" — retrieval procedure | Evidence = supplementary-materials content; exists(+coverage) / confirmed-absent | Search verbs removed; epistemic condition kept |
| A_gf_em | CQ-02 | RC | "在 PubMed/Crossref 以 … 组合检索" — provider names + query plan | Evidence = existence/absence of a verifiable 2020 von-Reyn GF bibliographic record | Provider names and query syntax deleted; only the record-state condition remains |
| A_gf_em | CQ-03 | RC | "以…为准，确认…一致则视为确立" — procedural "confirm" | Establishment condition: Namiki 2018 text + VFB FBbt:00004020 records agree | Sources kept as evidence types, procedure wording removed |
| A_gf_em | CQ-04 | RC | "明确确立同义则更新映射" — downstream action leaked | State semantics: synonymy established / distinct / default DISTINCT stance | "Update mapping" is an action, not an evidence state |
| A_gf_em | CQ-05 | RC | "以…资源确认…比对并记录" — inspection procedure | Evidence = dataset annotation records of DNp01 root IDs; agreement/mismatch = solution state | Inspection verbs removed; version binding kept |
| B_virtual_cell | CQ-01 | RC | "系统性检索…统计哪些…" — systematic-search plan | Evidence = public, verifiable evaluation evidence forming a coverage map by setting type | "Systematically search" prohibited phrase removed |
| B_virtual_cell | CQ-02 | RC | "在 CQ-01 的文献覆盖图基础上，检索社区基准…" — retrieval procedure | Evidence = public benchmark records (split/metrics/SOTA); absence = solution state | Procedure removed; dependency on CQ-01 also removed (see DEP) |
| B_virtual_cell | CQ-03 | RC | "检索各团队的论文…形成主张-团队对照表" — workflow | Evidence = public claims classified into representation/prediction/causal, time-bound | "Retrieve… build table" replaced by the evidence-state mapping |
| B_virtual_cell | CQ-04 | RC | "基于…确认是否存在…存在则评估…不存在则记录" | Evidence = protocols containing combination settings + held-out class splits; reusability dims | Confirmed existence/absence as states, not steps |
| C_hbot_ovary | CQ-01 | RC | "检索…定量研究，按…归纳效应方向" — search + aggregation procedure | Evidence = quantitative redox measurements stratified by protocol parameters | Search/aggregation verbs removed; direction-switch condition retained |
| C_hbot_ovary | CQ-02 | RC | "对 CQ-01 收录的动物研究逐篇核对…输出按证据等级分组的研究清单" — audit workflow | Evidence = control setup (sham/normobaric O2/normoxia), randomization, blinding per effect claim; stratification = solution state | "Check paper by paper / output list" deleted |
| C_hbot_ovary | CQ-03 | RC | "检索方法学文献…输出各测量适用场景" | Evidence = reliability/validity/bias records for AMH, AFC, histological counts + comparability evidence | Retrieval + output verbs removed |
| C_hbot_ovary | CQ-04 | RC | "在 CQ-01/CQ-02 的证据清单上，检索…分级记录" | Evidence = studies with primordial-follicle activation/loss endpoints, graded by control quality; absence = evidence gap, NOT negative finding | Retrieval removed; "absence ≠ negative" kept as state semantics |
| C_hbot_ovary | CQ-05 | RC | "将…逐项对照，量化暴露差距并评估外推风险等级" — comparison procedure | Evidence = the gap itself between animal exposure parameters and clinical regimens | Procedure removed; the measured gap IS the evidence state |
| C_hbot_ovary | CQ-02 | ST | Quote was "Clinical HBOT protocols differ widely…" — supports dose/translation, NOT control quality (semantic misanchor) | Quote: "the quality of the interventional controls in the animal literature" | Trace now anchors the reason this question exists |
| C_hbot_ovary | CQ-05 | ST | Quote was "Human evidence … thin and mostly indirect" — supports a general gap, NOT animal→clinic extrapolation (semantic misanchor) | Quote: "Clinical HBOT protocols differ widely in pressure, session count, and duration, and the animal dosing rarely matches clinical exposure." | Trace now anchors the extrapolation question |
| B_virtual_cell | CQ-02 | DEP | Edge CQ-02→CQ-01 was "later analysis benefits" — benchmark existence is independently decidable | (edge removed) | Sparse graph preferred; no prerequisite rationale could be stated firmly |
| B_virtual_cell | CQ-04 | DEP | Edges {CQ-01, CQ-02}; CQ-01 was contextual only | [CQ-02] — reusability evidence IS the benchmark record set | Retained edge has a firm prerequisite rationale |
| C_hbot_ovary | CQ-02 | DEP | Edge CQ-02→CQ-01 — control quality is independently assessable | (edge removed) | No firm "cannot interpret without" statement available |
| C_hbot_ovary | CQ-04 | DEP | Edges {CQ-01, CQ-02}; CQ-01 mechanism direction is contextual | [CQ-02] — direct-evidence grading requires the control-quality stratification | Retained edge has a firm prerequisite rationale |

Dependency edges after re-digestion (all with stated prerequisite rationales):

- A: CQ-05→CQ-03 — "CQ-05 queries entities under the canonical label DNp01; that label's authority is exactly what CQ-03 establishes. Without it, entity-query results are uninterpretable."
- B: CQ-04→CQ-02 — "The reusability evidence for a protocol IS the benchmark record set (splits, metrics); no benchmark list, no answer."
- C: CQ-04→CQ-02 — "Direct-endpoint evidence is graded by control quality; without the CQ-02 stratification the grading cannot be performed."
- C: CQ-05→CQ-04 — "The extrapolation evidence domain is exactly the CQ-04 study set's exposure parameters; without it there is nothing to compare."

## C — Resolution-Condition Audit

```yaml
artifact_id: CQS-CQC-P0-A
question_count: 5
search_plan_leak_count_before: 5   # all five contained procedure/provider/query language
search_plan_leak_count_after: 0
remaining_known_leakage: none      # source mentions (Namiki 2018, VFB, dataset docs) retained as EVIDENCE TYPES, not instructions
```

```yaml
artifact_id: CQS-CQC-P0-B
question_count: 4
search_plan_leak_count_before: 4
search_plan_leak_count_after: 0
remaining_known_leakage: none
```

```yaml
artifact_id: CQS-CQC-P0-C
question_count: 5
search_plan_leak_count_before: 5
search_plan_leak_count_after: 0
remaining_known_leakage: none
```

## D — Source-Trace Semantic Audit

```yaml
artifact_id: CQS-CQC-P0-A
trace_count: 5
semantic_misanchors_found: 0
semantic_misanchors_repaired: 0
unresolved_trace_questions: none
```

```yaml
artifact_id: CQS-CQC-P0-B
trace_count: 4
semantic_misanchors_found: 0
semantic_misanchors_repaired: 0
unresolved_trace_questions: none
```

```yaml
artifact_id: CQS-CQC-P0-C
trace_count: 5
semantic_misanchors_found: 2
semantic_misanchors_repaired: 2
unresolved_trace_questions: none
```

Specific HBOT repairs (contract §4 minimum): **CQ-02** re-anchored to
"the quality of the interventional controls in the animal literature" (the
sentence actually naming the control-quality concern); **CQ-05** re-anchored to
"Clinical HBOT protocols differ widely … animal dosing rarely matches clinical
exposure" (the sentence actually naming the extrapolation gap). The two bad
traces had been cross-swapped: each pointed at the other question's rationale.
Narratives were NOT re-authored (§9 respected).

## E — Dependency Audit

```yaml
artifact_id: CQS-CQC-P0-A
dependency_edges_before: 1
dependency_edges_after: 1
edges_removed: 0
edges_retained: 1   # CQ-05→CQ-03 (rationale in section B)
```

```yaml
artifact_id: CQS-CQC-P0-B
dependency_edges_before: 3
dependency_edges_after: 1
edges_removed: 2    # CQ-02→CQ-01, CQ-04→CQ-01 (contextual only)
edges_retained: 1   # CQ-04→CQ-02
```

```yaml
artifact_id: CQS-CQC-P0-C
dependency_edges_before: 4
dependency_edges_after: 2
edges_removed: 2    # CQ-02→CQ-01, CQ-04→CQ-01 (independently decidable)
edges_retained: 2   # CQ-04→CQ-02, CQ-05→CQ-04
```

Every retained edge's prerequisite rationale appears in section B. Net: 8 → 4 edges.

## F — Mechanical Validation

Machine-derived facts (from `docs/CQC_P0_RA1_METRICS.json` and CI):

```yaml
schema_validation: 3/3 PASS
source_hash_validation: 3/3 PASS   # narratives untouched; hashes unchanged by re-digestion
exact_trace_validation: 3/3 PASS   # including both repaired quotes, verbatim in frozen narratives
dependency_dag_validation: 3/3 PASS
deterministic_render_validation: 3/3 PASS
test_count: 22
test_result: PASS
```

## G — Architecture Delta

```yaml
schema_fields_added: 0
new_artifact_types: 0
new_semantic_scorers: 0
new_rankers: 0
new_solvers: 0
new_llm_runtime: false
new_frameworks: 0
```

Implementation delta: `.gitignore` (hygiene), one CI hygiene step, RA1 docs.
Zero production-logic changes.

## H — Repository Hygiene

```yaml
committed_pyc_before: 5   # 3 in scripts/__pycache__, 2 in tests/__pycache__ (P0 cycle-1 residue)
committed_pyc_after: 0
gitignore_added: true     # __pycache__/ + *.pyc only
```

CI now fails on committed bytecode (minimal §14 hygiene step).

## I — Digestion Finding

RA1 exposed the precise seam the master contract draws: structural validity is
cheap and mechanical, but it can certify an artifact whose meaning is wrong. All
14 resolution_conditions passed schema validation while 14/14 leaked retrieval
procedure — the validator literally cannot see the difference between "query
PubMed" and "the bibliographic record exists or not". Two of five traces in the
hardest artifact were semantically mis-anchored while being byte-perfect
verbatim quotes: the quotes were real, but they argued for the *neighbor*
question. The repairs were pure cognition: swapping the two HBOT traces, deleting
four dependency edges that only expressed "this would help later", and rewriting
evidence-states out of procedures. The measurable lesson for CQC-P1: semantic
quality is a re-digestion loop (artifact → model re-read → minimal field edit),
and the only honest machine role is to make each such repair visible and
regression-locked — not to score it.

## J — Next-Step Recommendation

**CQC-P1 — Real-Task Digestion Replay.** Both RA1 semantic closure and P0
structure are stable; the highest-value unknown is now empirical (does the
artifact improve downstream behavior vs narrative-only), which only P1 can
measure. Its phase contract must first pin the evaluation protocol and
narrative-only baseline (HO + ChatGPT as protocol owner).
