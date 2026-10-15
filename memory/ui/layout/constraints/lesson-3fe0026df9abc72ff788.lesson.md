# ConstraintLayout 改写成 Column 顺序流前先列出各子项锚点：多个子项锚父底、元素锚在兄弟上方时保留原锚点距离

ID：`lesson-3fe0026df9abc72ff788` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，把 ConstraintLayout 转成 Column/Row 顺序流或 Stack 层级，确定锚父底与锚兄弟子项的边距时

## 适用情境

源 ConstraintLayout 中有多个子项 constraintBottom_toBottomOf=parent（含 invisible 仍占位的行），或按钮上方的文字以 constraintBottom_toTopOf 锚在兄弟上；目标用 Column 顺序流、Visibility.Hidden 或父 Stack 的 BottomStart。

## 例外与边界

- 0dp×0dp 加 dimensionRatio 的子项尺寸按比例盒的规则另行计算
- 单个子视图四向锚定 parent 自身居中、兄弟只单向悬挂在它下方时，按居中与单向悬挂的规则转换

## 原因

顺序流里的 margin 相对前后兄弟，照抄锚父底的 margin 会叠在后续占位兄弟之上，位置偏高这些兄弟的占位高度；把锚兄弟简化成父容器底部对齐，会压到兄弟上。

## 做法

1. 转换前列出每个子项的纵向锚点（parent、哪个兄弟、哪条边）；多个子项锚父底时，用 Stack/RelativeContainer 按原 margin 贴底，或从原 margin 中扣除后续流式兄弟的占位高度（含 Hidden 行及其 margin）后重算。
2. 锚在兄弟上方的元素，到父底的距离 = 兄弟到父底的 marginBottom + 兄弟测量高度 + 自身 marginBottom；兄弟测量高度已含其 padding（View.java 的测量规则），不再另加 padding，也不简化成父容器底部对齐。
3. 也可用 RelativeContainer 的 alignRules 直接表达锚点：bottom: { anchor: '<兄弟 id>', align: VerticalAlign.Top }，并保留自身 margin。

## 可选检查

- dumpLayout 核对锚底子项到内容层底的距离等于源 margin，锚兄弟的元素不与兄弟重叠。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-50467dd451cd7c5be566](../../../../store/cases/case-50467dd451cd7c5be566/5252de23fda80022e42e0854a0d037a0dc80da44f0e76686e72fd88823b11917.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`5252de23fda80022e42e0854a0d037a0dc80da44f0e76686e72fd88823b11917`
- [case-c85d8667f78c2cc8f53a](../../../../store/cases/case-c85d8667f78c2cc8f53a/0a66d146244ac3bab2016664057dd3427c0c6c210bea434eab6b298234f871bf.json) · 结论：recommendation:2
  卡片版本：`0a66d146244ac3bab2016664057dd3427c0c6c210bea434eab6b298234f871bf`
