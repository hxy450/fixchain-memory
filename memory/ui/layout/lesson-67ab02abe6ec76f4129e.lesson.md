# 源端 exitUntilCollapsed 连续折叠顶栏按滚动偏移算折叠比例插值，不用首个可见行索引做两态切换

ID：`lesson-67ab02abe6ec76f4129e` · 版本：1

[本主题](index.md)

## 何时使用

界面转换阶段，把 LargeTopAppBar/LargeFlexibleTopAppBar 配合 exitUntilCollapsedScrollBehavior 的顶栏落成 ArkUI 时

## 适用情境

源端顶栏由 collapsedFraction 驱动高度、标题、背景色与阴影；目标页用 List 或 Scroll 承载内容。

## 原因

onScrollIndex 只在首个可见行变化时触发，两态切换丢掉了连续折叠；按偏移计算只需十几行代码。来源中两位转换者读到了源码和陷阱表“用 onScroll 手动计算高度和透明度”，仍照搬兄弟页的两态近似并登记为不确定。

## 做法

1. 在承载内容的 List 或 Scroll 上挂 onScroll（或 onDidScroll），fraction = clamp(Scroller.currentOffset().yOffset / (展开高度 − 收起高度), 0, 1)，展开、收起高度取源端值。
2. 高度、标题字号，以及源端用 lerp 过渡的背景色和阴影，都按 fraction 插值。

## 来源（按需复核）

- case-66f3c1649b7b5c4f38b5 · 结论：diagnosis, recommendation:1
  卡片版本：`686410a72e498ff1fb1d9233686e5ebc690a444c3056d62bc78d50dbcb257140`
