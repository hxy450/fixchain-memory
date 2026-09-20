# 亚阈关页不得放过：上轮 §6 的可量化预测必核，同根已修单并入同轮，几何差看 dump px 总宽

ID：`lesson-1cdbc30da8f082373bdf` · 版本：1

[本主题](index.md)

## 何时使用

视觉判读阶段，按页面相似度阈值（≥0.95）决定关页、以及决定哪些残差立单时

## 适用情境

judge notes 已测到与上轮修复 §6 预测不符的数值（25.4vp≠28）、或判「同根于已修单」、或 dump 显示 Row 总宽铺不满容器（1313 vs 1320），但页分仍 ≥0.95。

## 例外与边界

- 项目明确接受亚阈残差且不进入 100% 口径的下一轮

## 原因

round-1/2 judge 量到 Details 行距 25.4≠28 并指到具体公式，却按「页分 ≥0.95 关页」只记 residual，round-0 §6「Details 仍 28」的预测无人核销；FilterScreen 同根 Profile 已修单被两轮记录未并入；底栏 1313/1320px 在 ≥0.95 口径下 similarity 1.0——三者都拖到 100% 口径的 round-3 才立单。

## 做法

1. 把上一轮 §6「预期效果」里的可量化预测列为本轮必核项；测出与预测不符且能指到具体公式时，即使页分 ≥0.95 也单独立单或标为修复引入的回归。
2. notes 判「同根于已修单」的残差并入该单同轮修复，不等下一轮口径收紧。
3. 布局几何差异看 dump bounds 的 px 总宽是否铺满容器，不只看相似度分数。

## 检查

- 每轮 _summary 里上轮 §6 预测项逐条有核销结论；residual_low_not_ticketed 列表中无「同根已修」或「预测不符」项。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-049d48a5d4b79983dde3](../../../store/cases/case-049d48a5d4b79983dde3/03f1b058dbcb5149df2c8ad8d5cfcb27ff741f3cd3461e45e1f13f562864d130.json) · 结论：recommendation:4
  卡片版本：`03f1b058dbcb5149df2c8ad8d5cfcb27ff741f3cd3461e45e1f13f562864d130`
- [case-04c6d6166ebb2bcc3dfa](../../../store/cases/case-04c6d6166ebb2bcc3dfa/08cc614b7fd6dff41319ea673aceed9490eb8275b4fefb40e2711fb1fa952fdd.json) · 结论：recommendation:4
  卡片版本：`08cc614b7fd6dff41319ea673aceed9490eb8275b4fefb40e2711fb1fa952fdd`
- [case-0ff695bbe2304e899b77](../../../store/cases/case-0ff695bbe2304e899b77/d09e7f05d59d04549d82e8746a0de8d433534c1e9100e3f82d843c77249ee7b0.json) · 结论：recommendation:4
  卡片版本：`d09e7f05d59d04549d82e8746a0de8d433534c1e9100e3f82d843c77249ee7b0`
