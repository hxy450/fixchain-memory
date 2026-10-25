# ui/layout/scrolling

ScrollView/NestedScrollView 与 weight 剩余区列表的滚动范围（固定头部留在外、剩余区空态居中）、LazyRow/横向滚动行的交叉轴尺寸、Lazy 列表 contentPadding 的内容偏移、带高度上限的滚动卡片、连续折叠顶栏与滚动区内跟随等高。，ScrollView 越界回弹的默认值（IF_CONTENT_SCROLLS）；LazyRow 摘要行转可横滑容器，程序滚动到某项的对齐方式（animateScrollToItem → ScrollAlign.START）；GridView/ListView 转 Grid/List 时的越界效果与滚动条初次显示；Compose LazyColumn/verticalScroll 默认无滚动条与自定义滚动条修饰符的复刻

[上一级](../index.md)

## 本级经验

- [Compose LazyColumn 默认无滚动条：ArkUI List/Scroll 显式 BarState.Off，自定义滚动条按参数复刻](lesson-29b42ac7502c0f284b9a.lesson.md)
  - 时机：列表与滚动区实现阶段，把 Compose LazyColumn、verticalScroll 或自定义滚动条修饰符转成 ArkUI List/Scroll 时
  - 情境：源端 Compose LazyColumn/verticalScroll 没有滚动条修饰符，或用自定义修饰符（如 simpleVerticalScrollbar：按项数绘制、滚动时淡入淡出）画滚动条；目标 ArkUI List/Scroll 默认按 BarState.Auto 显示系统滚动条。
- [LazyListState.scrollToItem/animateScrollToItem 把目标项滚到可视区起始边：映射 scrollToIndex(index, smooth, ScrollAlign.START)，不自选居中；同一函数里的其他滚动副作用一并迁移](lesson-f0a40d990c62738fc04e.lesson.md)
  - 时机：界面实现阶段，把 Compose LazyListState 的程序滚动（scrollToItem、animateScrollToItem）翻译成 ArkUI Scroller.scrollToIndex 并选择对齐方式时
  - 情境：源端调用 animateScrollToItem(index) 或 scrollToItem(index)（scrollOffset 默认 0），同一函数可能还折叠顶栏等；目标 List 绑定 Scroller，scrollToIndex 的 align 可选 START、CENTER、END、AUTO。
- [LazyRow 摘要行转成可横滑容器，不降成普通 Row：少量固定项用 Scroll 包最小满宽的 Row 保留 Arrangement，item 内 AnimatedVisibility 的槽位恒在](lesson-caa043fb95ff63e321e2.lesson.md)
  - 时机：规格提取与界面实现阶段，把 Compose LazyRow（含只放几个固定 item 的摘要行、信息行）映射为 ArkUI 容器，确定是否可滚动、排列方式与条件项写法时
  - 情境：源端用 LazyRow(horizontalArrangement = Arrangement.SpaceEvenly 等) 放少量固定 item，每个 item 恒在、显隐由 item 内部的 AnimatedVisibility 或条件控制；窄屏或大字号下内容可能超出行宽；映射表或规格可能把它写成“Row + 若干子项”。
  - 例外：源端是普通 Row（没有 LazyRow 或 horizontalScroll），超宽时按源端的裁切或压缩处理
- [LazyRow/LazyColumn 的 contentPadding 译为 contentStartOffset/contentEndOffset，不用 List.padding](lesson-4030f978a230df37de2b.lesson.md)
  - 时机：界面实现阶段为滚动列表确定首尾留白时；规格提取阶段描述 Lazy 列表留白时
  - 情境：源 LazyRow/LazyColumn 用 contentPadding（PaddingValues start/end）给首尾项留白；目标 ArkUI List 可写 .padding，也可写 contentStartOffset/contentEndOffset；映射参考只有通用的 padding → .padding()。
- [ScrollView 未写 overScrollMode 也按 Android 默认 IF_CONTENT_SCROLLS 映射：Scroll 写 edgeEffect(EdgeEffect.Spring, { alwaysEnabled: false })；GridView/ListView 同此，滚动条按源端默认显式设置](lesson-80dd4e626e1c207028e6.lesson.md)
  - 时机：界面转换阶段，把 ScrollView/NestedScrollView（含对话框内的滚动区）转换为 ArkUI Scroll 并设置边缘效果时；把会滚动的 GridView/ListView 转成 Grid/List 并决定滚动条与越界效果时
  - 情境：源 ScrollView 没有声明 overScrollMode（Android 默认 IF_CONTENT_SCROLLS：内容可滚时越界回弹）；映射参考只列显式 overScrollMode，且把 ifContentScrolls 与 always 都映射为不带选项的 EdgeEffect.Spring；目标 Scroll 默认没有边缘效果。 也包括 GridView/ListView 没有改写 scrollbars、overScrollMode（AbsListView 同样默认 IF_CONTENT_SCROLLS），目标 Grid/List 没有显式设置 scrollBar 与 edgeEffect。
- [heightIn(max) 紧接 verticalScroll 的卡片拆成多节点时，把高度上限挂在 Scroll 上](lesson-420023d472f48bed8ef9.lesson.md)
  - 时机：界面实现阶段，把 heightIn(max) 紧接 verticalScroll 的卡片拆成“外层容器 + Scroll + 内容”结构时
  - 情境：源 Modifier 链里 heightIn(max = H) 紧接 verticalScroll，同一节点还带圆角、背景；目标需要拆成外层卡片包 Scroll 的多节点结构；迁移陷阱表有“滚动容器须显式给交叉轴尺寸”一类条目。
- [横向滚动容器给交叉轴写数值高度，按内容算出，不写 'auto' 也不留空](lesson-2d7c6de68f604ae77caf.lesson.md)
  - 时机：界面实现阶段，把 Compose 可滚动 Tab 行、LazyRow、horizontalScroll 等按内容定高的横向滚动行翻译成 ArkUI 滚动容器时
  - 情境：源端横向滚动行的高度由子项固有高度决定；目标用 Scroll(ScrollDirection.Horizontal) 或横向 List/Grid 实现，所在父容器在纵向上还有剩余空间。
- [源端 exitUntilCollapsed 连续折叠顶栏按滚动偏移算折叠比例插值，不用首个可见行索引做两态切换；enterAlways 不降级为固定](lesson-67ab02abe6ec76f4129e.lesson.md)
  - 时机：规格提取阶段为 LargeTopAppBar/LargeFlexibleTopAppBar 配合 exitUntilCollapsedScrollBehavior 的顶栏写转换决策时；界面转换阶段把这类顶栏落成 ArkUI 时；源 TopAppBar 配 enterAlwaysScrollBehavior 时同样适用
  - 情境：源端顶栏由 collapsedFraction 驱动高度、标题、背景色与阴影，滚动行为可能带 fling 衰减、中间态吸附，以及 collapse() 一类程序化折叠动画；目标页用 List 或 Scroll 承载内容，ArkUI 没有现成的连续折叠顶栏组件。 也包括 small TopAppBar 配 enterAlwaysScrollBehavior 与 nestedScroll（上滑先收起、下滑先展开、停止按半高吸附、内容离顶时切换容器色），页面规格的转换决策把它写成“可选”或“可降级为固定”。
- [源端“右列 match_parent 跟随左卡等高”在 Scroll 内用实测高度传递实现，不用估算常量](lesson-8334433bea644f2a89ae.lesson.md)
  - 时机：界面实现与验证期修复阶段，为并排卡片确定跟随等高约束，而整行位于 Scroll 等纵向无界容器中时
  - 情境：Android 水平行里右列 height=match_parent 随左侧 wrap_content 卡片等高；整行在 NestedScrollView（ArkUI Scroll）中；目标在 Scroll 内用纵向 layoutWeight 或 height('100%') 会被撑高失控。
- [转换滚动区时只把源滚动容器内的子节点放进 Scroll/List，固定头部留在外面；weight 剩余区里与列表叠放的空态放在有确定高度的区域内居中](lesson-46a0d7f239efac925d33.lesson.md)
  - 时机：界面实现阶段，把 Android 页面转成 ArkUI 时确定固定区域与 Scroll/List 的包含范围，或借用相邻页面的页面骨架时；以及规格提取阶段书写滚动容器的转换决策时
  - 情境：源布局根为纵向 LinearLayout 或 RelativeLayout，顶部用户栏、工具栏或横幅位于 NestedScrollView 之前（RelativeLayout 中滚动容器以 layout_below 排在其下），滚动容器承载地图、主按钮、卡片、宫格等主体；目标用 ArkUI Scroll 实现。 也包括源根为纵向 LinearLayout：固定高度标题栏与 layout_height=0dp、layout_weight=1 的列表容器同级，容器内 RecyclerView 与 match_parent、gravity=center 的空态 TextView 叠放、按数据显隐；同工程相邻页面按其自身源码采用整页单一 Scroll，可能被当作骨架照搬。
