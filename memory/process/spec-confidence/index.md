# process/spec-confidence

无真机 dump 时的置信标记

[上一级](../index.md)

## 本级经验

- [无真机 dump 的合成快照：源码字面的尺寸与可见性结论必须标 confidence 并交 verify 用真机量值](lesson-d036e54e65b0aec5a753.lesson.md)
  - 时机：规格提取阶段，在 ui-snapshot 由 Compose 源码合成、bounds 为空、无真机 UIAutomator dump 的条件下写视觉判据、决策台账或「近乎不可见/parity 保留」类结论时
  - 情境：基线 meta.json 自述 view_xml_synthesized / bounds 为空 / 无真机 dump；功能 spec 里有「判:visual」且带具体 dp 的验收条目，或 D0/决策台账里记了「近乎不可见、忠实复刻」的元素。
  - 例外：已有真机 dump 或截图分析产出的实测值
