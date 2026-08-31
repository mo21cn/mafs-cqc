# SearchRequirementProfile: SRP-CQC-P3-02

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
- evidence_need: 候选范式级工作的公开记录所构成的清单——候选空间必须由证据生成，而非由模型先验预置。所需的证据状态是『范式归属自述与互认』的可枚举集合。
- epistemic routes:
  - historical_lineage [REQUIRED] — 枚举领域内自称/被互认为范式级的工作及其归属记录
    condition: 始终需要；候选清单是 CQ-03 谱系映射的输入
- source_requirements: authoritative review, primary study, formal resource documentation
- stopping_condition: 多来源检索不再产生新的候选范式类别（类别饱和）。
- uncertainty_binding: 『新范式』判定基准缺失由 CQ-02 承接；本 requirement 采用宽收策略，不预筛。原文拼写 "Virtual Cel" 的实体歧义由源叙事上下文承接（按领域解读，保留记录）。

### R02

- target_question_ids: CQ-02
- evidence_need: 范式判定基准的使用先例——领域内哪些文献/共同体以什么标准把工作称为新范式。
- epistemic routes:
  - terminology_boundary [REQUIRED] — 厘清『范式』判定基准的可操作定义来源
    condition: 始终需要；基准未定则 CQ-01 的候选无法筛选
- source_requirements: authoritative review, historical prior-art record
- stopping_condition: 至少一个可操作的判定基准被确立（来自操作者确认或领域权威先例）。
- uncertainty_binding: 判定基准歧义是本案例最大未消歧点；基准确定前 CQ-01 维持宽收状态。

### R03

- target_question_ids: CQ-03
- evidence_need: 候选范式与其扩展/取代对象之间承继关系的文献记录。
- epistemic routes:
  - historical_lineage [REQUIRED] — 映射候选范式与既有范式的承继/扩展/取代关系
    condition: 依赖 CQ-01 的候选清单先存在（无清单则无谱系对象）
- source_requirements: primary study, historical prior-art record
- stopping_condition: 每个候选范式的谱系映射完成或记录为不可考。
- uncertainty_binding: 无额外歧义；本 requirement 的激活条件完全由 CQS 依赖边（CQ-03→CQ-01）承载。

