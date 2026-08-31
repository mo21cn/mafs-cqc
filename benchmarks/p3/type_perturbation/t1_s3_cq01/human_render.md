# SearchRequirementProfile: SRP-CQC-P3-03-PERTURBED

- schema_version: 0.1
- source_cqs_id: CQS-CQC-P2-03-R1
- source_cqs_sha256: 20d8c3480559bda563e507f656af86656552893e079eba1bdb2019ba3bcb9143
- source_narrative_sha256: 5975fee3490826bf06cd2005c2230bc19e7797ee4d46fdf4ac27c7068f7a4e6c
- requirements: 3

## Source Narrative (verbatim)

拮抗剂研究的应用领域有哪些

## Requirements

### R01

- target_question_ids: CQ-01
- evidence_need: 『拮抗剂』一词在相关语料与文献中的实体类型分布记录，加上操作者对指称范围的确认——两者共同构成消歧的证据状态。
- epistemic routes:
  - entity_resource_identity [REQUIRED] — 确定『拮抗剂』在该请求语境下指向的实体类型分布
    condition: 始终需要；指称范围锁定是 R02/R03 的证据边界前提
  - terminology_boundary [CONDITIONAL] — 识别与『拮抗剂』竞争的解读（如运动科学拮抗肌）并排除或纳入
    condition: 仅当实体类型分布显示存在显著竞争解读时激活
- source_requirements: formal resource documentation, primary study
- stopping_condition: 指称范围被操作者确认或证据分布明确支持唯一解读。
- uncertainty_binding: 指称范围歧义（重度）由本 requirement 显式承接；R02/R03 均为其下游（CONDITIONAL）。类型标注（TERMINOLOGY_OR_NAMING vs ENTITY_RESOLUTION）的双 plausible 状态保留，不作为路由依据。

### R02

- target_question_ids: CQ-02
- evidence_need: 以药理解读为界的领域盘点证据——治疗领域 × 靶点/机制家族矩阵，类别饱和为准。
- epistemic routes:
  - domain_coverage_inventory [CONDITIONAL] — 在药理解读边界内盘点拮抗剂研究的应用领域类别
    condition: gated on R01：『拮抗剂』指称被确认为药理解读后激活；若消歧离开药理解读，本 requirement 失效
- source_requirements: authoritative review, historical prior-art record
- stopping_condition: 矩阵在新增领域类目不再出现时饱和。
- uncertainty_binding: 盘点维度歧义（疾病/靶点/模态）保留——维度选择影响矩阵结构，留操作者确认。

### R03

- target_question_ids: CQ-03
- evidence_need: 拮抗剂分子被用作研究工具（非治疗用途）的公开使用记录。
- epistemic routes:
  - domain_coverage_inventory [CONDITIONAL] — 盘点拮抗剂作为 chemical probe / 实验工具的使用证据
    condition: gated on R01：同 R02，药理解读确认后激活
- source_requirements: primary study, historical prior-art record
- stopping_condition: 工具用途清单与治疗用途清单分离呈现。
- uncertainty_binding: 药理解读假设显式声明（承自 CQ-03.uncertainty）；R01 消歧离开药理时本 requirement 需重新表述。

