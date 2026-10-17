# 源端 exitUntilCollapsed 连续折叠顶栏按滚动偏移算折叠比例插值，不用首个可见行索引做两态切换

ID：`lesson-67ab02abe6ec76f4129e` · 版本：4 · 阶段：spec/execute · 主题：[ui/layout/scrolling](index.md)

概要：折叠顶栏按滚动偏移算 fraction 插值不两态切换

信号：`exitUntilCollapsedScrollBehavior`, `LargeTopAppBar`, `collapsedFraction`, `onDidScroll`, `onScrollFrameBegin`, `Scroller.currentOffset`, `yOffset`, `lerp`

## 何时使用

规格提取阶段为 LargeTopAppBar/LargeFlexibleTopAppBar 配合 exitUntilCollapsedScrollBehavior 的顶栏写转换决策时；界面转换阶段把这类顶栏落成 ArkUI 时

## 适用情境

源端顶栏由 collapsedFraction 驱动高度、标题、背景色与阴影，滚动行为可能带 fling 衰减、中间态吸附，以及 collapse() 一类程序化折叠动画；目标页用 List 或 Scroll 承载内容，ArkUI 没有现成的连续折叠顶栏组件。

## 原因

onScrollIndex 只在首个可见行变化时触发，两态切换丢掉了连续折叠；按偏移计算只需十几行代码。来源中两位转换者读到了源码和陷阱表“用 onScroll 手动计算高度和透明度”，仍照搬兄弟页的两态近似并登记为不确定。“没有现成组件”在规格阶段也容易被写成“简化为固定标题栏/只做变色”，各页随之写出固定高度顶栏。

## 做法

1. 规格不因目标没有现成折叠顶栏组件，就把它写成固定标题栏或只做滚动变色（列表较短的页面同样按源端保留）；写成用滚动回调实现的连续折叠。确实无法等价时，按差异决策流程登记待批，不在转换决策或验收条目里自行定为降级目标。
2. 在承载内容的 List 或 Scroll 上挂 onScroll（或 onDidScroll），fraction = clamp(Scroller.currentOffset().yOffset / (展开高度 − 收起高度), 0, 1)，展开、收起高度取源端值。
3. 需要复现 exitUntilCollapsed 的滚动量分配时（上滑先由顶栏消费偏移折叠到最小高度、再滚内容；下滑内容回到顶部后，余量再展开顶栏），在 onScrollFrameBegin 中按方向先让顶栏消费偏移，把剩余量返回给列表；源端的中间态吸附与 collapse() 折叠动画一并迁移。
4. 高度、标题字号，以及源端用 lerp 过渡的背景色和阴影，都按 fraction 插值；颜色端点取当前主题色板（随深浅色切换），不写成浅色字面值。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [沿用已生成页面或兄弟写法前回源码核对语义](../../../process/secondary-over-source/lesson-e9c6e8ef1b29a6fe9c26.lesson.md)（共享 2 张卡）
- [必读 skill 与源码逐份读全，截断即重读再写码](../../../process/unloaded-input/lesson-42df1ac4d4030421da34.lesson.md)（共享 1 张卡）
- [跨文件补实现的功能登记带负责方与验证的移交项](../../../process/handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md)（共享 1 张卡）
- [推进阶段前核对约定产物与放行门，待接事项落负责方](../../../process/handoff-loss/lesson-5754b7be28238f1bdf57.lesson.md)（共享 1 张卡）
- [成本类降级按范围裁剪，闸门自动批准不算改判](../../../process/unapproved-deviation/lesson-7827e0707780cb7546ee.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 2 次迁移 · 1 个应用

## 来源（按需复核）

- [case-66f3c1649b7b5c4f38b5](../../../../../store/cases/case-66f3c1649b7b5c4f38b5/686410a72e498ff1fb1d9233686e5ebc690a444c3056d62bc78d50dbcb257140.json) · 结论：diagnosis, rec-d7d385d1bd
  卡片版本：`686410a72e498ff1fb1d9233686e5ebc690a444c3056d62bc78d50dbcb257140`
- [case-d9c2b75062eb57796ca2](../../../../../store/cases/case-d9c2b75062eb57796ca2/c0e0684d2567560ee8d44f49d9c8eb3a4d4b3cc9ba5d7380a8e25a3b0f7792e8.json) · 结论：diagnosis, rec-6c7afe27cf
  卡片版本：`c0e0684d2567560ee8d44f49d9c8eb3a4d4b3cc9ba5d7380a8e25a3b0f7792e8`
