# SearchRequirementProfile: SRP-CQC-P3-06

- schema_version: 0.1
- source_cqs_id: CQS-CQC-P2-06-R1
- source_cqs_sha256: a67dc5c5e98c8351947f36e4b00e584bd695c0bf6c3166b81b2a768d484836ab
- source_narrative_sha256: 95f91f7c8dec4ece9f973a2607b8b8f5988963a83abf09fb11228c8a050da92d
- requirements: 1

## Source Narrative (verbatim)

请帮我查证一件事：Gould 2022 年那篇 Cell Reports 论文的补充材料里，到底有没有单细胞层面的海马体细胞类型注释表。

## Requirements

### R01

- target_question_ids: CQ-01
- evidence_need: 被指称论文（Gould 2022 × Cell Reports 的模糊指称，经消解确认）的补充材料内容证据——目标注释表的存在、缺失或材料不可及三态之一。
- epistemic routes:
  - source_content_verification [REQUIRED] — 在确认身份的论文补充材料中核对目标注释表的存在性
    condition: 指称消解成功且补充材料可及时激活
  - entity_resource_identity [CONDITIONAL] — 消解模糊指称（确定具体论文）
    condition: 指称歧义成为实质性障碍（无法唯一确定论文）时，身份验证升级为显式前置路线；否则作为 R01 的内嵌执行路径
- source_requirements: supplementary material, primary study
- stopping_condition: 三态之一（存在/明确不存在/无法确认）达成且指称消解依据被记录。
- uncertainty_binding: 指称模糊（作者+年份+期刊，无标题/DOI）保留——身份粒度（独立证据对象 vs 执行前置）依下游用途未决；重复表述已按单一疑问理解并记录。

