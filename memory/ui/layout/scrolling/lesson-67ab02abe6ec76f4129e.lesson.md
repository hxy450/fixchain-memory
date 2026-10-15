# 源端 exitUntilCollapsed 连续折叠顶栏按顶栏已消费的滚动量算折叠比例插值，不用首个可见行索引做两态切换

ID：`lesson-67ab02abe6ec76f4129e` · 版本：5

[本主题](index.md)

## 何时使用

规格提取阶段为 LargeTopAppBar/LargeFlexibleTopAppBar 配合 exitUntilCollapsedScrollBehavior 的顶栏写转换决策时；界面转换阶段把这类顶栏落成 ArkUI 时

## 适用情境

源端顶栏由 collapsedFraction 驱动高度、标题、背景色与阴影，滚动行为可能带 fling 衰减、中间态吸附，以及 collapse() 一类程序化折叠动画；目标页用 List 或 Scroll 承载内容，ArkUI 没有现成的连续折叠顶栏组件。

## 原因

onScrollIndex 只在首个可见行变化时触发，两态切换丢掉了连续折叠。exitUntilCollapsed 上滑时顶栏先消费偏移（material3 AppBar.kt 的 ExitUntilCollapsedScrollBehavior.onPreScroll），折叠完之前列表不动，collapsedFraction = heightOffset / heightOffsetLimit；用列表 yOffset 求比例会在顶栏折叠期间停在 0。“没有现成组件”在规格阶段也容易被写成“简化为固定标题栏/只做变色”。

## 做法

1. 规格不因目标没有现成折叠顶栏组件，就把它写成固定标题栏或只做滚动变色（列表较短的页面同样按源端保留）；写成用滚动回调实现的连续折叠。确实无法等价时，按差异决策流程登记待批，不在转换决策或验收条目里自行定为降级目标。
2. 在承载内容的 List 或 Scroll 的 onScrollFrameBegin 中按方向先让顶栏消费偏移：上滑时累计并夹紧顶栏已折叠量 collapsed ∈ [0, 展开高 − 收起高]，把剩余偏移返回给列表；下滑时内容回到顶部后，余量再展开顶栏。fraction = collapsed / (展开高 − 收起高)，展开、收起高度取源端值。
3. 只有顶栏与内容同时滚动、顶栏不单独消费偏移的情形，才用列表偏移（Scroller.currentOffset().yOffset）求 fraction；源端的中间态吸附与 collapse() 折叠动画一并迁移。
4. 高度、标题字号，以及源端用 lerp 过渡的背景色和阴影，都按 fraction 插值；颜色端点取当前主题色板（随深浅色切换），不写成浅色字面值。

来源支持：2 张卡 · 2 次迁移 · 1 个应用

## 来源（按需复核）

- [case-66f3c1649b7b5c4f38b5](../../../../store/cases/case-66f3c1649b7b5c4f38b5/686410a72e498ff1fb1d9233686e5ebc690a444c3056d62bc78d50dbcb257140.json) · 结论：diagnosis, recommendation:1
  卡片版本：`686410a72e498ff1fb1d9233686e5ebc690a444c3056d62bc78d50dbcb257140`
- [case-d9c2b75062eb57796ca2](../../../../store/cases/case-d9c2b75062eb57796ca2/c0e0684d2567560ee8d44f49d9c8eb3a4d4b3cc9ba5d7380a8e25a3b0f7792e8.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`c0e0684d2567560ee8d44f49d9c8eb3a4d4b3cc9ba5d7380a8e25a3b0f7792e8`
