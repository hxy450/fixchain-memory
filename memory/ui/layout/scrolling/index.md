# ui/layout/scrolling

ScrollView/NestedScrollView 与 weight 剩余区列表的滚动范围（固定头部留在外、剩余区空态居中）、LazyRow/横向滚动行的交叉轴尺寸、Lazy 列表 contentPadding 的内容偏移、带高度上限的滚动卡片、连续折叠顶栏与滚动区内跟随等高；可滚动视图（ScrollView、GridView/ListView）越界效果与滚动条的平台默认值（IF_CONTENT_SCROLLS、进页先亮再淡出）；LazyRow 摘要行转可横滑容器，程序滚动到某项的对齐方式（animateScrollToItem → ScrollAlign.START）

[上一级](../index.md)

## 本级经验

- [Lazy 列表 contentPadding 按主轴拆分：首尾值写 contentStartOffset/EndOffset，交叉轴值放进条目 padding](lesson-4030f978a230df37de2b.lesson.md)
  - 时机：界面实现阶段为滚动列表确定首尾留白时；规格提取阶段描述 Lazy 列表留白时
  - 情境：源 LazyRow/LazyColumn 用 contentPadding（PaddingValues）给首尾项留白；目标 ArkUI List 可写 .padding，也可写 contentStartOffset/contentEndOffset；映射参考只有通用的 padding → .padding()。
  - 例外：源码是 Modifier.padding（缩小视口，滚动内容裁在内距内）时，写 List.padding
- [LazyRow 摘要行转成可横滑容器，不降成普通 Row：少量固定项用 Scroll 包最小满宽的 Row 保留 Arrangement，item 内 AnimatedVisibility 的槽位恒在](lesson-caa043fb95ff63e321e2.lesson.md)
  - 时机：规格提取与界面实现阶段，把 Compose LazyRow（含只放几个固定 item 的摘要行、信息行）映射为 ArkUI 容器，确定是否可滚动、排列方式与条件项写法时
  - 情境：源端用 LazyRow(horizontalArrangement = Arrangement.SpaceEvenly 等) 放少量固定 item，每个 item 恒在、显隐由 item 内部的 AnimatedVisibility 或条件控制；窄屏或大字号下内容可能超出行宽；映射表或规格可能把它写成“Row + 若干子项”。
  - 例外：源端是普通 Row（没有 LazyRow 或 horizontalScroll），超宽时按源端的裁切或压缩处理
- [heightIn(max) 紧接 verticalScroll 的卡片拆成多节点时，把高度上限挂在 Scroll 上](lesson-420023d472f48bed8ef9.lesson.md)
  - 时机：界面实现阶段，把 heightIn(max) 紧接 verticalScroll 的卡片拆成“外层容器 + Scroll + 内容”结构时
  - 情境：源 Modifier 链里 heightIn(max = H) 紧接 verticalScroll，同一节点还带圆角、背景；目标需要拆成外层卡片包 Scroll 的多节点结构；迁移陷阱表有“滚动容器须显式给交叉轴尺寸”一类条目。
- [scrollToItem、animateScrollToItem 映射 scrollToIndex(…, ScrollAlign.START)：项对齐视口起点](lesson-f0a40d990c62738fc04e.lesson.md)
  - 时机：界面实现阶段，把 Compose LazyListState 的程序滚动（scrollToItem、animateScrollToItem）翻译成 ArkUI Scroller.scrollToIndex 并选择对齐方式时
  - 情境：源端调用 animateScrollToItem(index) 或 scrollToItem(index)（scrollOffset 默认 0），同一函数可能还折叠顶栏等；目标 List 绑定 Scroller，scrollToIndex 的 align 可选 START、CENTER、END、AUTO。
- [可滚动视图未写 overScrollMode 与滚动条属性时按平台默认映射：越界效果仅在内容可滚时出现，列表网格的滚动条进页先亮再淡出](lesson-80dd4e626e1c207028e6.lesson.md)
  - 时机：界面转换阶段，把 ScrollView/NestedScrollView（含对话框内的滚动区）、GridView/ListView 转换为 ArkUI Scroll、Grid、List 并设置边缘效果与滚动条时
  - 情境：源 ScrollView/NestedScrollView、GridView/ListView 没有声明 overScrollMode（View.java 默认 OVER_SCROLL_IF_CONTENT_SCROLLS：内容可滚时才显示越界效果；该效果在 API 31 起的设备上为拉伸、更早为光晕，EdgeEffect.java）；映射参考只列显式 overScrollMode，且把 ifContentScrolls 与 always 都映射为不带选项的 EdgeEffect.Spring；目标 Scroll 默认 EdgeEffect.None，选项 alwaysEnabled 默认 true（scroll.d.ts），Grid 同样默认 EdgeEffect.None、滚动条 BarState.Auto（grid.d.ts）。源列表或网格显示时由 View.initialAwakenScrollBars 先亮滚动条（scrollBarDefaultDelayBeforeFade×4，ViewConfiguration 默认 300ms，即约 1.2s）再淡出，滚动时再出现。
- [横向滚动容器给交叉轴写数值高度，按内容算出，不写 'auto' 也不留空](lesson-2d7c6de68f604ae77caf.lesson.md)
  - 时机：界面实现阶段，把 Compose 可滚动 Tab 行、LazyRow、horizontalScroll 等按内容定高的横向滚动行翻译成 ArkUI 滚动容器时
  - 情境：源端横向滚动行（Compose LazyRow、horizontalScroll、可滚动 Tab 行）的高度由子项固有高度决定；目标用 Scroll(ScrollDirection.Horizontal) 或横向 List/Grid 实现，所在父容器在纵向上还有剩余空间。
  - 例外：横向滚动容器放在已定高的父槽位里（父级给出确定高度）时，交叉轴随父级即可
- [源端 exitUntilCollapsed 连续折叠顶栏按顶栏已消费的滚动量算折叠比例插值，不用首个可见行索引做两态切换](lesson-67ab02abe6ec76f4129e.lesson.md)
  - 时机：规格提取阶段为 LargeTopAppBar/LargeFlexibleTopAppBar 配合 exitUntilCollapsedScrollBehavior 的顶栏写转换决策时；界面转换阶段把这类顶栏落成 ArkUI 时
  - 情境：源端顶栏由 collapsedFraction 驱动高度、标题、背景色与阴影，滚动行为可能带 fling 衰减、中间态吸附，以及 collapse() 一类程序化折叠动画；目标页用 List 或 Scroll 承载内容，ArkUI 没有现成的连续折叠顶栏组件。
- [转换 ScrollView/NestedScrollView 时只把源滚动容器内的子节点放进 Scroll，固定区留在外面；内容不满一屏时显式贴顶](lesson-46a0d7f239efac925d33.lesson.md)
  - 时机：界面实现阶段，把 ScrollView/NestedScrollView 或纵向 Lazy 列表转成 ArkUI Scroll/List、确定固定区与滚动区边界和短内容位置时；借用相邻页面的页面骨架时；规格提取阶段书写滚动容器的转换决策时
  - 情境：源布局根为纵向 LinearLayout 或 RelativeLayout，用户栏、工具栏、横幅或固定高度标题栏位于滚动容器之前（RelativeLayout 中滚动容器以 layout_below 排在其下，或与 layout_weight=1 的列表区同级）；目标用 Scroll 包 Column 承载内容，条目数可变、可能不足一屏。同工程相邻页面可能按其自身源码采用整页单一 Scroll。
  - 例外：源端固定区本就写在 ScrollView 内、随内容滚动时，按源结构放进 Scroll；空态在剩余区域中的纵向位置按空态定位的规则处理
