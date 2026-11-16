# LazyColumn 的程序滚动和左右分类联动

agent 会看到什么：读到源端 rememberLazyListState、animateScrollToItem，按 visibleItemsInfo / derivedStateOf 回写左侧选中态；交回的右侧是没有 Scroller 的 Scroll、scrollToIndex 对齐用 CENTER，或 onScrollIndex 在动画期间无条件回写

## 规矩

- rule-bab87c02e7ee｜源端左右分类双向联动时，右侧用带 Scroller 的分组 List 并接 onScrollIndex｜读到：源端 Compose 左侧分类栏 + 右侧分组列表：rememberLazyListState、左侧选中后 animateScrollToItem、按 visibleItemsInfo / derivedStateOf 可见项回写选中态；写错：目标右侧是没有控制器的 Scroll（只渲染选中分组，或用 Repeat 堆全部分组），左侧 onClick 只改 selectedIndex，没有 Scroller、scrollToIndex、onScrollIndex
- rule-080179ffbb66｜animateScrollToItem 迁成 scrollToIndex，对齐用 ScrollAlign.START｜读到：源端 lazyListState.animateScrollToItem(index)，同一处还调顶栏的 collapse()；写错：目标写 scrollToIndex(index, true, ScrollAlign.CENTER)，或漏了顶栏收起
- rule-b139d9edc80c｜左点右滚的联动要迁移程序滚动保护，动画期间忽略 onScrollIndex 的中间索引｜读到：源端用一个布尔标志位在左侧点击触发的 animateScrollToItem 期间屏蔽可见项回写（注释如「避免循环联动」）；写错：目标 .onScrollIndex((start) => { 选中索引 = start }) 无条件写回，左侧点击 scrollToIndex(index, true) 的动画期间中间索引覆盖点击选中态
- rule-b811b65d4fdc｜规格要求侧栏与内容区滚动联动时，内容区用 List＋Scroller 承载全部一级分组｜读到：规格或计划写着侧栏与内容区「滚动联动」「列表控制器」（如用 Repeat 和列表控制器表达选择与滚动联动），或写着安卓用 scroll synchronization；写错：内容区是 Scroll 里按 selectedIndex 取出的单个分组，没有 Scroller，也没有点击滚动或滚动回写选中项的回调
