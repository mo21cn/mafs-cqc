# CandidateQuestionSet: CQS-CQC-P2-03-R1

- schema_version: 0.1
- source_narrative_sha256: 5975fee3490826bf06cd2005c2230bc19e7797ee4d46fdf4ac27c7068f7a4e6c
- questions: 3

## Source Narrative (verbatim)

拮抗剂研究的应用领域有哪些

## Questions

### CQ-01

- type: TERMINOLOGY_OR_NAMING
- statement: 『拮抗剂』在此请求中的指称范围是什么（药理受体拮抗剂？运动科学拮抗肌？其他『拮抗』策略？），默认解读应如何与操作者确认？
- source trace:
  - "拮抗剂研究"
- dependencies: (none)
- resolution condition: 证据条件：『拮抗剂』一词在相关语料与文献中的实体类型分布记录，结合操作者对指称范围的确认。指称范围锁定后，后续盘点的证据边界才被正确界定。
- uncertainty: 重度歧义：分子类型、靶点、疾病域全部未指定。类型标注说明：本问题同时可标 ENTITY_RESOLUTION（消歧对象是实体指称）——选择 TERMINOLOGY_OR_NAMING 是描述性判断，两类型均 plausible，非本体裁决。

### CQ-02

- type: GENERALIZATION
- statement: 药理拮抗剂研究的应用领域版图是什么（治疗领域 × 靶点/机制家族的盘点矩阵）？
- source trace:
  - "应用领域有哪些"
- dependencies: CQ-01
- resolution condition: 证据条件：以『拮抗剂』药理解读为界的领域盘点证据（权威综述、药物分类体系、靶点家族记录）。盘点矩阵在新增领域类目不再出现时达到饱和。
- uncertainty: 盘点维度（按疾病/靶点/分子模态）原话未指定（另见 CQ-04）。

### CQ-03

- type: TRANSLATION
- statement: 拮抗剂作为研究工具（chemical probes、体外/体内实验工具）的非治疗应用有哪些？
- source trace:
  - "拮抗剂研究"
- dependencies: CQ-01
- resolution condition: 证据条件：拮抗剂分子被用作研究工具的公开记录。工具用途清单与治疗用途清单分离呈现即为解决状态。
- uncertainty: 本问题同样预设药理分子解读（受 CQ-01 消歧约束）。

