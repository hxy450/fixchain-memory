# 无真机 dump 的合成快照：源码字面的尺寸与可见性结论必须标 confidence 并交 verify 用真机量值

ID：`lesson-d036e54e65b0aec5a753` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段，在 ui-snapshot 由 Compose 源码合成、bounds 为空、无真机 UIAutomator dump 的条件下写视觉判据、决策台账或「近乎不可见/parity 保留」类结论时

## 适用情境

基线 meta.json 自述 view_xml_synthesized / bounds 为空 / 无真机 dump；功能 spec 里有「判:visual」且带具体 dp 的验收条目，或 D0/决策台账里记了「近乎不可见、忠实复刻」的元素。

## 例外与边界

- 已有真机 dump 或截图分析产出的实测值

## 原因

合成快照只有声明树没有度量：Up 圆钮 36 vs 实绘 48、Reset 文案「渲染但看不见」vs 实际不渲染，都是把源码字面当实测写进 AC 与决策台账，让实现者原样复刻并让验收把它当已知缺陷。

## 做法

1. 凡「判:visual」且带具体 dp 的 AC 带 confidence=medium 标记，并要求 verify 阶段以真机 dump/截图量值取代源码字面。
2. 「颜色近乎不可见」「parity 保留」类结论降级为待真机核对项写入 spec，不写进 D0/决策台账当已知缺陷。

## 检查

- spec 中所有含 dp 的 visual AC 都带 confidence 字段；决策台账里没有以合成快照为唯一依据的「忠实复刻某缺陷」条目。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-6eec56e15cefd5c659cb](../../../store/cases/case-6eec56e15cefd5c659cb/c485b924cd70665967de43755b2e70352a1b4ceb7eb6723c9079f3d09eba0b93.json) · 结论：recommendation:2
  卡片版本：`c485b924cd70665967de43755b2e70352a1b4ceb7eb6723c9079f3d09eba0b93`
- [case-72a54efb333474d03d1a](../../../store/cases/case-72a54efb333474d03d1a/9ad6a4ed2bf9f3d9f783fc402bbd30da0d113c1560aff110134af9367ef644d7.json) · 结论：recommendation:2
  卡片版本：`9ad6a4ed2bf9f3d9f783fc402bbd30da0d113c1560aff110134af9367ef644d7`
