# CQC-P0-RA2 — Structured Summary

Human interpretation layer for HO + ChatGPT. Machine truth: `docs/CQC_P0_RA2_METRICS.json`,
`docs/CQC_P0_RA2_SHA256_MANIFEST.txt`.

## A — Acceptance Header

```yaml
contract_id: CQC-P0-RA2-DEPENDENCY-PREREQUISITE-FINAL-CLOSURE-v0.1
status: READY_FOR_REVIEW
repository: mo21cn/mafs-cqc
branch: dev/cqc-p0
verified_commit_sha: (pinned in docs/CQC_P0_RA2_METRICS.json)
ci_run_id: (pinned in docs/CQC_P0_RA2_METRICS.json)
meaningful_push_ci_cycles: 1
```

## B — Dependency Delta

| Artifact | Question | Edge Before | Edge After | Why Removed |
|---|---|---|---|---|
| B_virtual_cell | CQ-04 | CQ-04 → CQ-02 | (none) | CQ-04 (are combination-generalization protocols evaluated and reusable?) is answerable from published protocol designs alone; a paper can define a reusable held-out-combination protocol that never becomes a community benchmark. CQ-02's outcome changes the *interpretive flavor* of the answer, not its searchability or correctness. |
| C_hbot_ovary | CQ-05 | CQ-05 → CQ-04 | (none) | CQ-05 (animal→clinical exposure gap) can be evaluated over the broader HBOT-ovarian animal-study exposure set; it does not require the narrower direct-endpoint study set (CQ-04) to be resolved first. |

## C — Final Dependency Ledger

```yaml
A_gf_em:
  retained_edges:
    - CQ-05 -> CQ-03
  rationale: >-
    Entity queries under the canonical label DNp01 depend on the GF↔DNp01
    naming relation being established (CQ-03); without it, dataset-entity
    results are uninterpretable.

B_virtual_cell:
  retained_edges: []

C_hbot_ovary:
  retained_edges:
    - CQ-04 -> CQ-02
  rationale: >-
    Grading direct follicle activation/loss evidence as a causal claim depends
    on the control-quality stratification produced by CQ-02.
```

Final state: **2 edges total** (was 8 at P0, 4 after RA1, 2 after RA2).

## D — Resolution-Condition Delta

**B CQ-04**

- before_problem: Condition opened with "证据条件（依赖 CQ-02 的基准存在性结论）" —
  it made the protocol-evidence question logically hostage to benchmark existence.
- after_meaning: "证据条件：评测协议是否同时包含组合扰动设置与 held-out 组合类别划分——无论该协议是否已成为社区公认基准。已发表工作中的协议设计本身即证据……完全缺失此类协议时，即构成明确的协议缺口。"
- why_this_is_a_digestion_fix: The evidence condition is now defined directly
  (published protocol designs constitute the evidence), matching the contract
  insight that reusability and community-benchmark status are independent facts.

**C CQ-05**

- before_problem: Condition opened with "证据条件（依赖 CQ-04 的直接证据研究集）" —
  it narrowed the exposure-gap evidence domain to the direct-endpoint study set.
- after_meaning: "证据条件：HBOT-卵巢动物研究——涵盖储备终点与机制/红氧终点——所报告的暴露参数（压力 ATA、频次、总时长）与临床 HBOT 常规方案参数之间的差距本身。差距的大小即为外推效度的证据状态。"
- why_this_is_a_digestion_fix: The gap evidence domain is now the full relevant
  animal-exposure set, which is what dose translation actually requires.

## E — Mechanical Validation

Machine-derived facts (from `docs/CQC_P0_RA2_METRICS.json` and CI):

```yaml
schema_validation: 3/3 PASS
source_hash_validation: 3/3 PASS
exact_trace_validation: 3/3 PASS
dependency_dag_validation: 3/3 PASS
deterministic_render_validation: 3/3 PASS
test_count: 22
test_result: PASS
```

A-artifact unchanged check: `git diff --stat` empty for `cqs_A_gf_em.json` and
`cqs_A_gf_em.md` (contract §6 respected).

## F — Architecture Delta

```yaml
schema_fields_added: 0
new_artifact_types: 0
new_semantic_scorers: 0
new_rankers: 0
new_solvers: 0
new_llm_runtime: false
new_frameworks: 0
```

Implementation delta: RA2 docs only. Zero production-logic changes.

## G — Digestion Finding

RA2's two removals share one root error: treating a *helpful relation* as a
*prerequisite*. CQ-02's benchmark answer would have enriched how we read CQ-04,
and CQ-04's direct-endpoint evidence would have sharpened CQ-05 — but neither
question was unanswerable, uninterpretable, or unsearchable without the other.
The discriminator RA2 applied is blunt and honest: "can I state why the
downstream question fails without this edge?" A benefit statement ("it would
help interpretation") failed that test; both genuine prerequisites passed it
because they bind the *identity of the evidence itself* (which label to query,
which stratification grades the claim, which study set forms the comparison).
Sparse dependency semantics survive because the surviving edges assert
evidence-identity, not narrative convenience.

## H — Next Step

**CQC-P1** — the P0 semantic line is closed (structure, trace fidelity,
resolution semantics, dependency truth, hygiene all frozen and CI-guarded);
the only remaining unknown of value is empirical and requires the P1 phase
contract with the HO + ChatGPT-owned evaluation protocol.
