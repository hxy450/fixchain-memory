# ConstraintLayout 改写成 Column 顺序流前先列出各子项锚点：锚父底、锚兄弟与双 0dp 比例子项都要保留语义

ID：`lesson-3fe0026df9abc72ff788` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把 ConstraintLayout 转成 Column/Row 顺序流或 Stack 层级，确定锚点边距与比例子项尺寸时

## 适用情境

源 ConstraintLayout 中有多个子项 constraintBottom_toBottomOf=parent（含 invisible 仍占位的行）、按钮上方的文字以 constraintBottom_toTopOf 锚在兄弟上、0dp×0dp 加 dimensionRatio 的子项夹在上下锚点之间；目标用 Column 顺序流、layoutWeight、Visibility.Hidden 或父 Stack 的 BottomStart。

## 原因

顺序流里的 margin 相对前后兄弟，照抄锚父底的 margin 会叠在后续占位兄弟之上（偏高一个兄弟高度）；把锚兄弟简化成父容器底部对齐会压到兄弟上；双 0dp 比例子项的边长是 min(可用宽, 可用高)，只写 width('100%').aspectRatio(1) 在高度受限时会溢出。写者往往在思考中复述了这些约束，写码时仍按顺序堆叠。

## 做法

1. 转换前列出每个子项的锚点；多个子项锚父底时，用 Stack/RelativeContainer 按原 margin 贴底，或扣除后续流式兄弟的占位高度重算 margin。
2. 锚在兄弟上方的元素，底距 = 兄弟高度 + 其 padding + 自身 margin，不简化成父容器底部对齐。
3. 双 0dp 加 dimensionRatio 的子项按 min(可用宽, 可用高) 定边长：高度受限时写 height('100%').aspectRatio(r) 并限制宽度，源里的上下 margin 放到承担 layoutWeight 的容器上。
4. 注释里列出的尺寸与边距逐项对照实际修饰链，注释有而代码没有的按缺失处理。

## 可选检查

- dumpLayout 核对比例子项不超出其容器、锚底子项到内容层底的距离等于源 margin。

## 来源（按需复核）

- case-50467dd451cd7c5be566 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`6513ec7414cb84e14b75d1fc1e2031c2a499520a4c3975f65d67fc995ec9adc7`
- case-c85d8667f78c2cc8f53a · 结论：recommendation:2, recommendation:3
  卡片版本：`88c863065eec4c8bbb44bce32612ea2302aed620bf50c9df7bf06ad13309abb8`
