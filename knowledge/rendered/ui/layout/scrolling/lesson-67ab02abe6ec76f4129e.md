# 源端 exitUntilCollapsed 连续折叠顶栏按滚动偏移算折叠比例插值，不用首个可见行索引做两态切换；enterAlways 不降级为固定

## 何时使用

规格提取阶段为 LargeTopAppBar/LargeFlexibleTopAppBar 配合 exitUntilCollapsedScrollBehavior 的顶栏写转换决策时；界面转换阶段把这类顶栏落成 ArkUI 时；源 TopAppBar 配 enterAlwaysScrollBehavior 时同样适用

## 适用情境

源端顶栏由 collapsedFraction 驱动高度、标题、背景色与阴影，滚动行为可能带 fling 衰减、中间态吸附，以及 collapse() 一类程序化折叠动画；目标页用 List 或 Scroll 承载内容，ArkUI 没有现成的连续折叠顶栏组件。 也包括 small TopAppBar 配 enterAlwaysScrollBehavior 与 nestedScroll（上滑先收起、下滑先展开、停止按半高吸附、内容离顶时切换容器色），页面规格的转换决策把它写成“可选”或“可降级为固定”。

## 原因

onScrollIndex 只在首个可见行变化时触发，两态切换丢掉了连续折叠；按偏移计算只需十几行代码。来源中两位转换者读到了源码和陷阱表“用 onScroll 手动计算高度和透明度”，仍照搬兄弟页的两态近似并登记为不确定。“没有现成组件”在规格阶段也容易被写成“简化为固定标题栏/只做变色”，各页随之写出固定高度顶栏。

## 做法

1. 规格不因目标没有现成折叠顶栏组件，就把它写成固定标题栏或只做滚动变色（列表较短的页面同样按源端保留）；写成用滚动回调实现的连续折叠。确实无法等价时，按差异决策流程登记待批，不在转换决策或验收条目里自行定为降级目标。
2. 在承载内容的 List 或 Scroll 上挂 onScroll（或 onDidScroll），fraction = clamp(Scroller.currentOffset().yOffset / (展开高度 − 收起高度), 0, 1)，展开、收起高度取源端值。
3. 需要复现 exitUntilCollapsed 的滚动量分配时（上滑先由顶栏消费偏移折叠到最小高度、再滚内容；下滑内容回到顶部后，余量再展开顶栏），在 onScrollFrameBegin 中按方向先让顶栏消费偏移，把剩余量返回给列表；源端的中间态吸附与 collapse() 折叠动画一并迁移。
4. 高度、标题字号，以及源端用 lerp 过渡的背景色和阴影，都按 fraction 插值；颜色端点取当前主题色板（随深浅色切换），不写成浅色字面值。
5. enterAlways：在 onScrollFrameBegin 中按方向先改顶栏 heightOffset（上滑收起、下滑展开），改了就消费本帧偏移、余量返回列表；停止滚动按折叠比例 0.5 吸附；容器色按累计的用户滚动量判断离顶，不按列表绝对偏移。顶栏度量取库默认（material3 1.4 small TopAppBar：容器 64dp 不含状态栏、水平内边距 4dp、导航图标 48dp、标题起点 56dp）。

来源支持：3 张卡 · 3 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕Scroller.currentOffset() 在 Scroller 没有绑定到组件时返回空；返回的 OffsetResult.yOffset 是竖直滑动偏移，单位 vp
- 〔做法第 3、5 步〕List.onScrollFrameBegin 回调传入即将发生的滑动量，列表按回调返回的 offsetRemain 实际滑动；listDirection 为 Axis.Vertical 时是垂直方向的量；传入的 offset 单位 vp
- 〔做法第 3、5 步〕List.onScrollFrameBegin 只在用户交互（手指滑动、键鼠操作等）、惯性滚动和调用 fling 时触发；调用 fling 以外的滚动控制接口（如 scrollTo、scrollToIndex）、越界回弹、拖动滚动条时不触发
