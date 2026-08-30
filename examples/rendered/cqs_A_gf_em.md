# CandidateQuestionSet: CQS-CQC-P0-A

- schema_version: 0.1
- source_narrative_sha256: 35f47188c87e80086e3d355c682b71a39493dbed63690f2f284eafe6e4112c92
- questions: 5

## Source Narrative (verbatim)

# Narrative A — GF / EM identity-lineage task (real replay domain: mafs-v3-p0 Replay B)

## Task origin

This narrative comes from a real operator task in the MAFS v3.0 Replay B benchmark line. The verbatim operator request is:

请调整 MAFS 搜索：von Reyn et al. 2014/2020 等论文补充材料里的 GF 神经元 ID 清单。

## Background facts established by prior verified work

The Drosophila Giant Fiber (GF) escape circuit has been studied for decades with electrophysiology, and more recently with connectomics datasets.

The 2014 paper by the von Reyn team is "A spike-timing mechanism for action selection", published in Nature Neuroscience (volume 17, pages 962-970, DOI 10.1038/nn.3741, PMID 24908103).

The standardized descending-neuron nomenclature comes from Namiki et al. 2018 in eLife ("The functional organization of descending sensory-motor pathways in Drosophila", DOI 10.7554/eLife.34272), which labels the Giant Fiber as DNp01.

The FlyWire v783 and hemibrain v1.2.1 datasets identify GF candidate bodies by numeric root IDs, but the specific root IDs supplied by the operator for the right and left GF have not been independently confirmed against dataset annotations.

## Known ambiguities in the request

Whether "von Reyn 2020" refers to a real Giant Fiber paper is doubtful: the major 2020 Drosophila connectome work is Scheffer et al. 2020 ("A connectome and analysis of the adult Drosophila central brain", eLife), from a largely overlapping Janelia collaboration, which may be what the operator conflated.

The historical label "DNg01" appears in some pre-2018 literature; no authoritative primary source has confirmed that DNg01 is a synonym of DNp01, so the two must not be silently treated as the same neuron class.

It is also unverified whether the supplementary materials of von Reyn 2014 actually contain a GF neuron ID list at all.

## Goal

Prepare an executable question set for downstream MAFS retrieval: confirm source identity and content, confirm the naming lineage, and clarify whether the 2020 citation is a conflation.

## Questions

### CQ-01

- type: SOURCE_CONTENT
- statement: von Reyn 2014 (Nature Neuroscience 17:962-970, DOI 10.1038/nn.3741) 的补充材料中是否真的包含 GF 神经元 ID 清单？若存在，清单覆盖哪些神经元？
- source trace:
  - "It is also unverified whether the supplementary materials of von Reyn 2014 actually contain a GF neuron ID list at all."
- dependencies: (none)
- resolution condition: 直接获取 von Reyn 2014 论文的补充材料并逐项检查：存在 GF 神经元 ID 清单则提取并记录其覆盖范围；不存在则记录明确的不存在结论。标题与摘要层面的推断不作为判定依据。
- uncertainty: 补充材料的公开可及性未知；若仅部分可及，结论须区分『确认不存在』与『无法确认』。

### CQ-02

- type: ENTITY_RESOLUTION
- statement: 用户所引『von Reyn 2020』是否是一篇真实存在的 GF 研究论文，还是与 Scheffer et al. 2020（果蝇中央脑连接组，eLife）的引用混淆？
- source trace:
  - "Whether "von Reyn 2020" refers to a real Giant Fiber paper is doubtful: the major 2020 Drosophila connectome work is Scheffer et al. 2020 ("A connectome and analysis of the adult Drosophila central brain", eLife), from a largely overlapping Janelia collaboration, which may be what the operator conflated."
- dependencies: (none)
- resolution condition: 在 PubMed/Crossref 以 von Reyn + 2020 + Giant Fiber/Drosophila 组合检索：命中真实论文则确认其书目身份与 GF 相关性；无命中且检索充分则记录 NOT_FOUND，并将混淆假设标记为 LIKELY_CONFLATION。
- uncertainty: 若检索发现真实的 von Reyn 2020 GF 论文，本问题从『混淆判定』转为『确认该论文身份』；叙事当前只提供了怀疑依据，未提供否定证据。

### CQ-03

- type: TERMINOLOGY_OR_NAMING
- statement: GF / Giant Fiber / DNp01 的等同映射是否由权威一手来源确立？
- source trace:
  - "which labels the Giant Fiber as DNp01"
- dependencies: (none)
- resolution condition: 以 Namiki et al. 2018 (eLife 7:e34272) 原文对 DNp01 的定义，以及 Virtual Fly Brain 官方条目 FBbt:00004020 的记录为准，确认 GF（Giant Fiber）与 DNp01 的映射；两个来源一致则视为确立。
- uncertainty: (none)

### CQ-04

- type: HISTORICAL_LINEAGE
- statement: 历史文献中出现的标签 DNg01 是否与 DNp01 指同一神经元类别？
- source trace:
  - "no authoritative primary source has confirmed that DNg01 is a synonym of DNp01, so the two must not be silently treated as the same neuron class"
- dependencies: (none)
- resolution condition: 以权威一手来源（FlyBase 参考报告、Virtual Fly Brain 条目、原始文献的神经元命名表述）为准：明确确立同义则更新映射；确立二者为不同类别则按不同类别处理；均无法确立则保持 DISTINCT_NEURON_CLASS_UNLESS_AUTHORITATIVE_EVIDENCE 立场。
- uncertainty: 当前所有已知权威来源均未证实同义关系；本问题的结论可能随新的一手证据翻转。

### CQ-05

- type: ENTITY_RESOLUTION
- statement: GF（DNp01）在 FlyWire v783 与 hemibrain v1.2.1 数据集中的体节 root ID 分别是什么？
- source trace:
  - "the specific root IDs supplied by the operator for the right and left GF have not been independently confirmed against dataset annotations"
- dependencies: CQ-03
- resolution condition: 以数据集官方注释资源（flywire_annotations 发布库、neuPrint 兼容 API、hemibrain 官方文档）确认 DNp01 对应的左右体节 root ID；与操作者提供的 ID 比对并记录一致或不一致。
- uncertainty: 操作者提供的 root ID 未经独立验证，且 root ID 可能随数据集版本（v783、FAFB14.1、annotation v2.1.0）变化；结论必须绑定具体数据集版本。

