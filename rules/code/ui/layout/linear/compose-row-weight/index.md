# Compose Row 子项的 weight、fillMaxWidth 和基线对齐

agent 会看到什么：源端 Compose Row 里子项的 Modifier.weight、fillMaxWidth、wrapContentWidth、alignBy(LastBaseline)，对应目标 Row / Flex 子项上的 layoutWeight、textAlign、ItemAlign.Baseline 和可见性

## 规矩

- rule-f3f65bf161e3｜Row 里无 weight 的 fillMaxWidth 占满剩余宽，不写成 layoutWeight(1)｜读到：Compose Row 中某子项 Modifier.fillMaxWidth() 没有 weight，后面还有兄弟（如 IconButton）；写错：目标把这个子项写成 .layoutWeight(1)，后续兄弟给了固定宽，兄弟变得可见
- rule-ab9f8b35e161｜收到「近乎不可见、parity 保留」的元素时先分清成因，布局裁剪就用 Visibility.Hidden｜读到：规格或派工说某元素「近乎不可见——parity 保留」，源码里它在 Row 中排在不带 weight 的 fillMaxWidth() 兄弟之后；写错：目标按 .opacity(...) 降低透明度或用低对比色把它的 Text 画出来，或给前面的标题 .layoutWeight(1) 让出空间让它显示
- rule-175b666eecb0｜靠右的 weight 标签写成 layoutWeight 加 textAlign(End)｜读到：Compose Text 写 Modifier.weight(1f).wrapContentWidth(Alignment.End)；写错：目标 Text 只有 .layoutWeight(1) 或 .flexGrow(1)，没有 .textAlign(TextAlign.End)，文字靠左
- rule-c992844110c9｜alignBy(LastBaseline) 一端是自定义组件时，不用 Flex ItemAlign.Baseline｜读到：Compose Row 里 Text 和自定义组件都写 Modifier.alignBy(LastBaseline)；写错：目标写成 Flex({ alignItems: ItemAlign.Baseline })，自定义组件取不到基线被排到文本下方
