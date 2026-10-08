# ui/layout/scrolling

滚动容器的包含范围、交叉轴尺寸、首尾留白与高度上限，以及 Scroll 内嵌套内容的测高与滚动归属。

[上一级](../index.md)

## 本级经验

- [Lazy 首尾留白用 contentStartOffset](lesson-4030f978a230df37de2b.lesson.md) · 阶段：spec/execute · 信号：contentStartOffset, contentEndOffset, contentPadding, PaddingValues
- [只把源滚动区子节点放进 Scroll，固定头部留外面](lesson-46a0d7f239efac925d33.lesson.md) · 阶段：spec/execute · 信号：NestedScrollView, layout_below, layout_weight, layoutWeight(1)
- [嵌套滚动的 Web 高度跟文档，并锁 H5 自身滚动](lesson-fd2dd522fdb03b3e5385.lesson.md) · 阶段：execute/repair · 信号：wrap_content, nestedScroll, PARENT_FIRST, onPageEnd
- [并排卡等高用 onSizeChange 实测高度传递](lesson-8334433bea644f2a89ae.lesson.md) · 阶段：execute/repair · 信号：onSizeChange, SizeOptions, NestedScrollView, match_parent
- [折叠顶栏按滚动偏移算 fraction 插值不两态切换](lesson-67ab02abe6ec76f4129e.lesson.md) · 阶段：execute · 信号：exitUntilCollapsedScrollBehavior, LargeTopAppBar, collapsedFraction, onDidScroll
- [拆卡片时 heightIn 上限挂在 Scroll 上](lesson-420023d472f48bed8ef9.lesson.md) · 阶段：execute · 信号：heightIn, verticalScroll, constraintSize, maxHeight
- [横向滚动容器交叉轴高度写数值不写 auto](lesson-2d7c6de68f604ae77caf.lesson.md) · 阶段：execute · 信号：ScrollDirection.Horizontal, horizontalScroll, LazyRow, ScrollableTabRow
