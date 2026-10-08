# ui/layout/constraints

锚点与对齐语义的转换：源端默认对齐与锚点落到 Column/Row/Stack/RelativeContainer。

[上一级](../index.md)

## 本级经验

- [ConstraintLayout 转顺序流前先列出各子项锚点](lesson-3fe0026df9abc72ff788.lesson.md) · 阶段：execute · 信号：constraintBottom_toBottomOf, constraintBottom_toTopOf, dimensionRatio, layoutWeight
- [Stack 子项 .align() 无效，对齐用满高容器](lesson-92aee54a305ea0bde363.lesson.md) · 阶段：execute/repair · 信号：.align(, alignContent, Alignment.TopStart, layout_gravity
- [单视图居中加兄弟悬挂用 RelativeContainer](lesson-e607a28fcd91acd2b40f.lesson.md) · 阶段：spec/execute · 信号：RelativeContainer, alignRules, __container__, constraintTop_toBottomOf
- [基线对齐用 Row 居中近似，内距逐行复制，标签靠右对齐](lesson-c4990fef246323ffda03.lesson.md) · 阶段：execute · 信号：alignBy(LastBaseline), wrapContentWidth(End), weight(1), layoutWeight
- [纵向容器默认起始对齐与贴顶在目标显式写出](lesson-08b9064f678f1635e647.lesson.md) · 阶段：execute · 信号：alignItems(HorizontalAlign.Start), alignItems(VerticalAlign.Top), Alignment.Top, constraintSize
