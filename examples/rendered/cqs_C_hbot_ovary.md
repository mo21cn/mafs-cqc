# CandidateQuestionSet: CQS-CQC-P0-C

- schema_version: 0.1
- source_narrative_sha256: 81a0ad71e3206dcaf0bb67d1ca919afb9004706446634130419d120572d803c2
- questions: 5

## Source Narrative (verbatim)

# Narrative C — Hyperbaric oxygen and ovarian reserve (mechanism / mixed narrative)

## Research intent

A clinical collaborator asked whether hyperbaric oxygen therapy (HBOT) could harm ovarian reserve in women of reproductive age, because patients in our center sometimes report menstrual-cycle changes after multi-session HBOT courses.

The mechanistic background cuts both ways: oxidative stress is a known contributor to ovarian reserve decline, via reactive oxygen species driving primordial follicle over-activation and atresia; yet HBOT is also reported to upregulate antioxidant defenses in some tissues.

So the net direction of the redox effect in ovarian tissue under repeated hyperoxic exposure is genuinely unresolved.

## What the literature seems to say

Animal studies of ovarian ischemia-reperfusion injury report that HBOT preoperatively can preserve ovarian follicle reserve, measured by AMH levels, antral follicle counts, and histological primordial follicle counts.

Clinical HBOT protocols differ widely in pressure, session count, and duration, and the animal dosing rarely matches clinical exposure.

Human evidence on HBOT and ovarian reserve specifically appears thin and mostly indirect.

## Where we need help

Before designing any study or counseling patients, we need to know what the existing evidence actually supports: the direction and dose-dependence of the redox effect in ovarian tissue, the quality of the interventional controls in the animal literature, which ovarian-reserve measurements are comparable across studies, whether any direct evidence ties HBOT to primordial follicle activation or loss rates, and how animal dosing could translate to clinical HBOT regimens.

The confounder list includes concurrent oxidative exposures, age, and indication-for-treatment itself.

## Questions

### CQ-01

- type: MECHANISM
- statement: 在重复高压氧暴露下，卵巢组织中氧化-抗氧化净效应的方向是什么，其剂量/方案依赖性如何？
- source trace:
  - "So the net direction of the redox effect in ovarian tissue under repeated hyperoxic exposure is genuinely unresolved."
- dependencies: (none)
- resolution condition: 检索卵巢组织在高压/高氧暴露下 ROS 水平与抗氧化标志物（SOD、CAT、GPx、MDA 等）的定量研究，按方案参数（压力、次数、时长）归纳效应方向；若双向证据并存，归纳出方向切换的条件。
- uncertainty: 叙事明确双向假设均有组织学外证据支持（促氧化：ROS 驱动原始卵泡过度激活；抗氧化：上调抗氧化防御）；方向未定是本问题的起点而非待清除的噪声。

### CQ-02

- type: INTERVENTION_OR_CONTROL
- statement: 现有 HBOT-卵巢动物实验的对照设置（常氧高压、常压氧、假处理）是否足以把观察到的效应归因于高压氧本身？
- source trace:
  - "Clinical HBOT protocols differ widely in pressure, session count, and duration, and the animal dosing rarely matches clinical exposure."
- dependencies: CQ-01
- resolution condition: 对 CQ-01 收录的动物研究逐篇核对对照类型、随机化与盲法设置；以对照质量分层后重新审视归因强度，输出按证据等级分组的研究清单。
- uncertainty: (none)

### CQ-03

- type: MEASUREMENT_OR_OBSERVABILITY
- statement: 卵巢储备的三类测量（血清 AMH、窦卵泡计数 AFC、组织学原始卵泡计数）在跨研究比较中的效度与可比性如何？
- source trace:
  - "measured by AMH levels, antral follicle counts, and histological primordial follicle counts"
- dependencies: (none)
- resolution condition: 检索卵巢储备测量方法学文献与权威指南，比较三类测量的信度、效度与跨物种/跨批次可比性；输出各测量适用场景与已知偏差。
- uncertainty: (none)

### CQ-04

- type: CAUSAL_CLAIM
- statement: 是否有直接证据（以原始卵泡激活或丢失率为终点）表明 HBOT 改变卵巢储备的消耗速率？
- source trace:
  - "whether any direct evidence ties HBOT to primordial follicle activation or loss rates"
- dependencies: CQ-01, CQ-02
- resolution condition: 在 CQ-01/CQ-02 的证据清单上，检索以原始卵泡激活/丢失组织学计数为终点的 HBOT 研究：有则以对照质量分级记录；无则记录『直接证据缺失』，不视为阴性结论。
- uncertainty: 叙事中的『preoperatively can preserve』说法来自卵巢缺血再灌注损伤模型；该保护效应外推到健康卵巢或临床 HBOT 人群未经证实，需保持假设状态。

### CQ-05

- type: TRANSLATION
- statement: 动物 HBOT 剂量方案向临床 HBOT 方案的外推效度如何，暴露量差距有多大？
- source trace:
  - "Human evidence on HBOT and ovarian reserve specifically appears thin and mostly indirect."
- dependencies: CQ-04
- resolution condition: 将 CQ-04 收录研究的动物暴露参数（压力 ATA、频次、总时长）与临床 HBOT 常规方案逐项对照，量化暴露差距并评估外推风险等级。
- uncertainty: (none)

