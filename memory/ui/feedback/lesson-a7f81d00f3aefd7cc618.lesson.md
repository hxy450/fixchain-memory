# Compose M3 不传 progress 的进度指示器与 PullToRefreshBox 指示器，不用 ArkUI 默认组件代替

ID：`lesson-a7f81d00f3aefd7cc618` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段（共享组件与页面），以及规格提取写转换决策时，把 Compose Material3 带默认动态视觉的进度与下拉刷新组件映射到 ArkUI 时

## 适用情境

源端 Compose 用不传 progress 的 LinearProgressIndicator/CircularProgressIndicator（加载条可能以 zIndex 叠放在内容上）或 PullToRefreshBox 默认指示器；目标 ArkUI Progress 只显示定值，LoadingProgress 是环绕点动画，Refresh 默认用系统指示器并把内容往下推。

## 原因

不传 progress 是持续动画，Progress 写成 value 0、30、50 就是一根静止条，换成 LoadingProgress 形状也不同；Refresh 默认指示器与 M3 指示器外观不同，下拉时内容随之下移。共享组件写成近似后，页面又各自内联近似版本，或把“无等价”注释当作既有决策沿用。

## 做法

1. 转换前确认是定值还是不定进度；不定进度在共享组件里用 Canvas 加逐帧回调（如 displaySync）复刻源端动画，保留叠放层级（zIndex），不推挤内容。
2. PullToRefreshBox 的映射写明指示器外观与“内容不随下拉移动”：Refresh 隐藏系统指示器、自绘指示器并抵消内容位移，保留源端的包裹范围。
3. 页面源码出现共享组件名时，先读该组件在源端的定义，再复用目标共享件，不在页面里内联近似版本；先例是静止条或写着“无等价”的，按源端定义纠正。

## 可选检查

- 生成后检索 Progress({ value: 常量、LoadingProgress 与无自定义 builder 的 Refresh(，逐处对照源端组件

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-f0512caa793e1ad8016c](../../../store/cases/case-f0512caa793e1ad8016c/79d02279686f94bcea5a9985313b86d9688fe54b12a0ac5d08a82d3464ddb832.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`79d02279686f94bcea5a9985313b86d9688fe54b12a0ac5d08a82d3464ddb832`
