# Material 交互组件的 .size(x<48) 是修饰符字面，实绘按 minimumInteractiveComponentSize 为 48

ID：`lesson-7e0d06d6a8e9a544c53a` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段，为页面 spec 转换决策表与功能 spec 视觉验收判据确定 Material IconButton/Button 等交互组件的目标尺寸与位置时

## 适用情境

源为 Jetpack Compose，页面含 Material3 IconButton（或同类交互组件），源码在其外层显式写 .size(x) 且 x < 48dp 并带 background(CircleShape)；目标端要用固定 width/height 的 Button 复刻。

## 例外与边界

- 源码显式关闭了最小触控尺寸（LocalMinimumInteractiveComponentSize / minimumInteractiveComponentEnforcement=false）

## 原因

M3 IconButton 在调用方 .size(36) 之内套 minimumInteractiveComponentSize，背景圆实绘 48dp、圆心不变；spec 把 36 写成转换决策与 AC 判据，converter/slice 忠实实现，直到修复期真机 dump 才量出 48。

## 做法

1. 转换决策表区分「修饰符字面」与「实绘尺寸」：源码 .size(x) 且 x<48 时按 48 记实绘尺寸，用圆心而非左上角描述位置；或把该行列为 low_confidence 待真机 dump 复核。

## 检查

- grep 源码 IconButton( 出现处与 .size( 的数值，逐个与 48 比对；真机/模拟器 dump 的背景节点 bounds 应为 48dp。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-6eec56e15cefd5c659cb](../../../../store/cases/case-6eec56e15cefd5c659cb/f8f8a7033af1e730dc2c95dbe7c81b1f51fa0a89de63da4d5f391cb31626d4cc.json) · 结论：diagnosis, recommendation:1
  卡片版本：`f8f8a7033af1e730dc2c95dbe7c81b1f51fa0a89de63da4d5f391cb31626d4cc`
