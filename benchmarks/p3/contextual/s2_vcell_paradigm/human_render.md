# SearchRequirementProfile: SRP-CQC-P3-02-R1

- schema_version: 0.1
- source_cqs_id: CQS-CQC-P2-02-R1
- source_cqs_sha256: 39b0f15a28d663bd3ee6d8453ddf45379714b6b721c773a23719e11248e4081d
- source_narrative_sha256: 37f34e945191656a338bfec3cee788dd959cccc3bdbe94fc60171ff88a5a8df4
- requirements: 3

## Source Narrative (verbatim)

"Virtual Cel"产生了哪些新的研究范式？

## Requirements

### R01

- target_question_ids: CQ-01
- evidence_need: 候选范式类别达到证据饱和——在 CQ-02 所声明的范式准入标准下，已接纳的候选范式类别集合不再随新证据扩大。所需证据状态是范式归属的自述/互认记录所构成的饱和集合。
- epistemic routes:
  - historical_lineage [REQUIRED] — 收集范式归属的自述与互认记录，供候选集合在准入标准下达到饱和
    condition: 始终需要；饱和判定以 CQ-02 的准入标准为标尺，不以检索过程为标尺
- source_requirements: authoritative review, primary study, formal resource documentation
- stopping_condition: 在已确立的范式准入标准下，候选范式类别达到证据饱和（新增证据不再产生新类别），或饱和性因准入标准未定而显式不可判定。
- uncertainty_binding: 『新范式』判定基准缺失由 CQ-02 承接；本 requirement 的饱和判定依赖该基准，基准未定前饱和性标注为不可判定。

### R02

- target_question_ids: CQ-02
- evidence_need: 一个可操作的范式判定基准被显式确立——来源为操作者确认或领域权威使用先例。
- epistemic routes:
  - terminology_boundary [REQUIRED] — 确立『范式』判定基准的可操作定义
    condition: 始终需要；基准未立则 R01 的饱和判定无标尺
- source_requirements: authoritative review, historical prior-art record
- stopping_condition: 至少一个可操作的判定基准被确立（操作者确认或权威先例）。
- uncertainty_binding: 判定基准歧义是本案例最大未消歧点；确立前 R01 的饱和性保持『不可判定』状态。

### R03

- target_question_ids: CQ-03
- evidence_need: 每个已接纳候选范式的谱系关系——与其扩展/取代对象的承继映射，或显式记录为不可考。
- epistemic routes:
  - historical_lineage [REQUIRED] — 为已接纳候选建立谱系映射
    condition: 依赖 R01 的已接纳候选集合（无候选则无谱系对象）
- source_requirements: primary study, historical prior-art record
- stopping_condition: 每个已接纳候选获得谱系关系或显式未决标注。
- uncertainty_binding: 无额外歧义；激活条件由 CQS 依赖边（CQ-03→CQ-01）承载。

