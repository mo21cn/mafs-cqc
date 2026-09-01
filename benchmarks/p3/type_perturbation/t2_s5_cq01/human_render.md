# SearchRequirementProfile: SRP-CQC-P3-05-PERTURBED

- schema_version: 0.1
- source_cqs_id: CQS-CQC-P2-05-R1
- source_cqs_sha256: 9970868e6d2b38a93b1ff2c7782c7bd2bd32be6f3a71797988832656bad87eea
- source_narrative_sha256: 21c183e3b096f988d3a80c6ebbd145a1255efab08052009380b154ff48ec7d8d
- requirements: 3

## Source Narrative (verbatim)

我们在推进一项肿瘤代谢方向的研究，现在需要把检索问题梳理清楚。背景是这样的：我们队列里有一部分 IDH1 突变的胶质瘤患者，在使用一种 mTOR 通路抑制剂之后，代谢影像上看到了一些变化，我们怀疑这是代谢通路上游被抑制之后对下游代谢物造成的连锁效应。同时我们不太确定的一点是，这种"上游通路抑制"的思路，相对于已有的直接针对突变代谢酶本身的那些策略，到底算不算一种新的治疗范式，还是只是已有思路的变体。另外，组里的高分辨质谱平台能不能在单个细胞或者接近单个细胞的分辨率上把 relevant 的代谢物水平测出来，我们也拿不准，这直接决定后面动物实验的设计。

## Requirements

### R01

- target_question_ids: CQ-01
- evidence_need: 上游通路抑制在 IDH1 突变胶质瘤背景下产生下游代谢连锁效应的细胞/通路层面研究证据——确立、修正或证伪任一状态均实质改变 CQ-01。
- epistemic routes:
  - mechanism_evidence [REQUIRED] — 获取上游抑制与下游代谢物变化之间因果/关联的细胞通路层面证据
    condition: 始终需要
- source_requirements: primary study, authoritative review
- stopping_condition: 连锁效应的方向/强度在通路层面被确立、修正或证伪。
- uncertainty_binding: 『代谢影像变化』的具体表型源未说明——不代填，证据检索按操作者后续澄清保持开放。

### R02

- target_question_ids: CQ-02
- evidence_need: 既有直接靶向策略的公开盘点，及其与上游抑制策略之间差异的记录——两者对照后才可判定范式新意。
- epistemic routes:
  - historical_lineage [REQUIRED] — 盘点直接针对突变代谢酶的既有策略及其变体
    condition: 始终需要；没有对照集就没有新意判定
  - counterexample_negative_evidence [CONDITIONAL] — 检索上游抑制思路已被尝试并失败/放弃的记录
    condition: 当宽泛盘点暗示该思路可能已被尝试时激活
- source_requirements: authoritative review, historical prior-art record
- stopping_condition: 新意判定所需的两类证据（对照集 + 差异记录）齐备，或明确记录证据缺口。
- uncertainty_binding: 『治疗范式』判定基准缺失由 CQ-02.uncertainty 承接——判定在基准厘清前保持悬置。

### R03

- target_question_ids: CQ-03
- evidence_need: 单细胞/近单细胞代谢组学的技术能力边界记录（检出限、代谢物覆盖面、通量），以及该边界对动物实验测量方案的约束含义。
- epistemic routes:
  - measurement_observability [REQUIRED] — 确认质谱平台在目标分辨率下的能力与边界
    condition: 始终需要；其结论直接约束操作者明示的动物实验设计
- source_requirements: methods literature, authoritative review
- stopping_condition: 可行/不可行/仅部分可行三态判定达成。
- uncertainty_binding: 『relevant 的代谢物』种类未指定——证据检索保持开放，不代为指定。

