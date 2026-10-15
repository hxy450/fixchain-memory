# 双 0dp 加 dimensionRatio 的子项按“满足比例且不越出约束的最大尺寸”定宽高，不只写 width('100%').aspectRatio

ID：`lesson-ccf0b3ab6ebd6dd7c2e6` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，把 ConstraintLayout 中 0dp×0dp 加 layout_constraintDimensionRatio 的子项（封面、视频区等）转成 ArkUI 尺寸时

## 适用情境

源子项 layout_width 与 layout_height 都是 0dp，带 layout_constraintDimensionRatio，上下或左右分别锚在相邻子项或 parent 上；目标用 Column 顺序流配 layoutWeight 或 Stack 承载，可用空间随屏幕变化。

## 例外与边界

- 只有一个方向为 0dp、另一方向已定尺寸时，按已定的边乘或除比例求另一边
- dimensionRatio 带 W, 或 H, 前缀时本条未覆盖：来源为无前缀的双 0dp，本机只有 ConstraintLayout 字节码；先按所用 ConstraintLayout 版本的文档确认前缀指定哪一边，再决定是否套用下面的公式

## 原因

双 0dp 的比例子项取满足比例、又不越出约束区域的最大尺寸；只写 width('100%').aspectRatio(r) 是宽驱动，高度受限时会溢出容器；min(可用宽, 可用高) 只在 1:1 时成立。

## 做法

1. 设 r = 宽/高、约束区域可用宽 W、可用高 H：宽 = min(W, H × r)，高 = 宽 / r（r=1 时即 min(W, H)）。目标用承担约束区域的容器（如 layoutWeight(1) 的 Row/Column）提供 W×H；高度受限时写 height('100%').aspectRatio(r) 并用 constraintSize({ maxWidth }) 或父容器限制宽度，宽度受限时写 width('100%').aspectRatio(r)。
2. 源里比例子项上下的 margin 放到承担 layoutWeight 的容器上，使 W×H 是扣除边距后的区域。

## 可选检查

- dumpLayout 核对比例子项的 bounds 不超出其约束容器。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-50467dd451cd7c5be566](../../../../store/cases/case-50467dd451cd7c5be566/5252de23fda80022e42e0854a0d037a0dc80da44f0e76686e72fd88823b11917.json) · 结论：diagnosis, recommendation:2, recommendation:3
  卡片版本：`5252de23fda80022e42e0854a0d037a0dc80da44f0e76686e72fd88823b11917`
