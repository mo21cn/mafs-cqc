# CandidateQuestionSet: CQS-CQC-P1-02-RC1

- schema_version: 0.1
- source_narrative_sha256: aac9f8ba4abad9f60cc0c517f1d2f217435e4c0ac473a2df7f7a5801f243a1f7
- questions: 3

## Source Narrative (verbatim)

"Virtual Cel"包含了哪些学术研究方向？

## Questions

### CQ-01

- type: ENTITY_RESOLUTION
- statement: 『Virtual Cell』所指领域的学术研究方向集合与边界是什么（哪些方向属于其核心、哪些属于相邻/交叉）？
- source trace:
  - ""Virtual Cel"包含了哪些学术研究方向？"
- dependencies: (none)
- resolution condition: 证据条件：权威综述、领域立场文章与主要计划/资源（含数据基础设施）对 virtual cell 方向构成的明确归类。当新增检索不再产生新的方向类别时，盘点达到饱和，即为该问题的解决状态。
- uncertainty: 原文拼写为 "Virtual Cel"（少一个 l）；消化假设其指 Virtual Cell 领域，但未与操作者确认。

### CQ-02

- type: TERMINOLOGY_OR_NAMING
- statement: Virtual Cell 与相邻术语（whole-cell model、in silico cell、digital cell、cell digital twin）的边界如何划分，哪些方向只有用相邻术语才能检索到？
- source trace:
  - "包含了哪些学术研究方向"
- dependencies: (none)
- resolution condition: 证据条件：各术语族下的代表性工作集合及其自称归属（论文关键词/摘要自述）。术语间工作集的重叠与差异被明确记录时，边界划分即为可核验状态。
- uncertainty: (none)

### CQ-03

- type: ENTITY_RESOLUTION
- statement: 原文拼写 "Virtual Cel" 是否指向其他专有实体（如 VCell 建模软件、某公司/计划的产品名）而非该研究领域？
- source trace:
  - ""Virtual Cel""
- dependencies: (none)
- resolution condition: 证据条件：以原拼写检索到的专有实体记录（软件、数据库、产品）。存在与『研究领域』解读冲突的显著实体→必须请操作者消歧；不存在→领域解读为唯一合理解读。
- uncertainty: 拼写歧义保留：同一原话可能指领域概念、VCell 软件（生物建模工具）或其他产品；未与操作者确认前不合并。

