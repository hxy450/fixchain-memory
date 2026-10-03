# ui/layout/scrolling

ScrollView/NestedScrollView 与 weight 剩余区列表的滚动范围（固定头部留在外、剩余区空态居中）、LazyRow/横向滚动行的交叉轴尺寸、Lazy 列表 contentPadding 的内容偏移、带高度上限的滚动卡片、连续折叠顶栏与滚动区内跟随等高。

[上一级](../index.md)

## 本级经验

- [LazyRow/LazyColumn 的 contentPadding 译为 contentStartOffset/contentEndOffset，不用 List.padding](lesson-4030f978a230df37de2b.lesson.md)
  - 时机：界面实现阶段为滚动列表确定首尾留白时；规格提取阶段描述 Lazy 列表留白时
  - 情境：源 LazyRow/LazyColumn 用 contentPadding（PaddingValues start/end）给首尾项留白；目标 ArkUI List 可写 .padding，也可写 contentStartOffset/contentEndOffset；映射参考只有通用的 padding → .padding()。
- [heightIn(max) 紧接 verticalScroll 的卡片拆成多节点时，把高度上限挂在 Scroll 上](lesson-420023d472f48bed8ef9.lesson.md)
  - 时机：界面实现阶段，把 heightIn(max) 紧接 verticalScroll 的卡片拆成“外层容器 + Scroll + 内容”结构时
  - 情境：源 Modifier 链里 heightIn(max = H) 紧接 verticalScroll，同一节点还带圆角、背景；目标需要拆成外层卡片包 Scroll 的多节点结构；迁移陷阱表有“滚动容器须显式给交叉轴尺寸”一类条目。
- [横向滚动容器给交叉轴写数值高度，按内容算出，不写 'auto' 也不留空](lesson-2d7c6de68f604ae77caf.lesson.md)
  - 时机：界面实现阶段，把 Compose 可滚动 Tab 行、LazyRow、horizontalScroll 等按内容定高的横向滚动行翻译成 ArkUI 滚动容器时
  - 情境：源端横向滚动行的高度由子项固有高度决定；目标用 Scroll(ScrollDirection.Horizontal) 或横向 List/Grid 实现，所在父容器在纵向上还有剩余空间。
- [源端 exitUntilCollapsed 连续折叠顶栏按滚动偏移算折叠比例插值，不用首个可见行索引做两态切换](lesson-67ab02abe6ec76f4129e.lesson.md)
  - 时机：界面转换阶段，把 LargeTopAppBar/LargeFlexibleTopAppBar 配合 exitUntilCollapsedScrollBehavior 的顶栏落成 ArkUI 时
  - 情境：源端顶栏由 collapsedFraction 驱动高度、标题、背景色与阴影；目标页用 List 或 Scroll 承载内容。
- [源端“右列 match_parent 跟随左卡等高”在 Scroll 内用实测高度传递实现，不用估算常量](lesson-8334433bea644f2a89ae.lesson.md)
  - 时机：界面实现与验证期修复阶段，为并排卡片确定跟随等高约束，而整行位于 Scroll 等纵向无界容器中时
  - 情境：Android 水平行里右列 height=match_parent 随左侧 wrap_content 卡片等高；整行在 NestedScrollView（ArkUI Scroll）中；目标在 Scroll 内用纵向 layoutWeight 或 height('100%') 会被撑高失控。
- [转换滚动区时只把源滚动容器内的子节点放进 Scroll/List，固定头部留在外面；weight 剩余区里与列表叠放的空态放在有确定高度的区域内居中](lesson-46a0d7f239efac925d33.lesson.md)
  - 时机：界面实现阶段，把 Android 页面转成 ArkUI 时确定固定区域与 Scroll/List 的包含范围，或借用相邻页面的页面骨架时；以及规格提取阶段书写滚动容器的转换决策时
  - 情境：源布局根为纵向 LinearLayout 或 RelativeLayout，顶部用户栏、工具栏或横幅位于 NestedScrollView 之前（RelativeLayout 中滚动容器以 layout_below 排在其下），滚动容器承载地图、主按钮、卡片、宫格等主体；目标用 ArkUI Scroll 实现。 也包括源根为纵向 LinearLayout：固定高度标题栏与 layout_height=0dp、layout_weight=1 的列表容器同级，容器内 RecyclerView 与 match_parent、gravity=center 的空态 TextView 叠放、按数据显隐；同工程相邻页面按其自身源码采用整页单一 Scroll，可能被当作骨架照搬。
