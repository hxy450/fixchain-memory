# process/repair

修复阶段的假设标注与回归基线

[上一级](../index.md)

## 本级经验

- [改主题层文本度量公式时把「已核」和「假设」分开，先在同轮 dump 里找多行回归基线](lesson-0e10b578fa6f2cb0a75e.lesson.md)
  - 时机：视觉对齐修复阶段，把 Compose TextStyle 的 lineHeight 语义改写成 ArkUI Text 属性（lineHeight / lineSpacing）并确定折算公式、且不允许当场重编实测时
  - 情境：源样式带 lineHeight；目标用同一主题令牌同时服务单行与多行段落；单行盒高已有 Android dump 与字体度量支撑，多行行距如何由 fontSize / 自然行盒 / lineSpacing 合成 SDK d.ts 无说明、当前 dump 无 lineSpacing 样本。
