# 列表、滚动与翻页

源端有 RecyclerView、ListView、ExpandableListView、Compose LazyColumn / LazyRow、ScrollView、ViewPager / TabLayout、PreferenceFragment，目标端有 List、ListItem、Grid、ForEach、LazyForEach、Repeat、Scroll、Swiper、Tabs、Refresh 时

## 子主题

- [数据、键与刷新](data/index.md)（28 条）：源端有 Adapter 的 setList / submitList / notifyItemChanged、removeAllViews 后逐项重建、SwipeRefreshLayout / SmartRefreshLayout、LazyForEach，目标端有 IDataSource、ForEach / Repeat 的键函数、Refresh、onReachEnd 时
- [翻页与标签页](pager/index.md)（24 条）：源端有 ViewPager / ViewPager2、TabLayout 和它承载的子 Fragment，目标端有 Swiper、Tabs、TabContent、.tabBar、SwiperController 时
- [滚动容器](scroll/index.md)（17 条）：源端有 ScrollView、NestedScrollView 和写在它外面的顶栏，目标端有 Scroll、它的内容 Column 的高度和 edgeEffect 时
- [设置页与偏好项](settings/index.md)（14 条）：源端有 PreferenceFragment / PreferenceActivity、res/xml 里的 Preference、ListPreference、SwitchPreference，目标端有 List / ListItem 写的设置行时

## 触发族

- [列表适配器的条目绑定](adapter-item-binding/index.md)（12 条）：读到 RecyclerView.Adapter / BaseQuickAdapter 的 onBindViewHolder、convert()、afterBindViewHolder 里对子视图的 setText、图标、背景、颜色和按 viewType 的分支；产物里 ListItem / GridItem / ForEach 条目的文字、图标、样式和列数
- [列表条目和行内按钮的点击](list-item-click/index.md)（3 条）：读到 adapter 的 onItemClickListener、addOnItemTouchListener 的 onSingleTapUp、行内按钮调远端接口；产物里 ForEach 条目上的 .onClick 和行内按钮请求在途时的防重
- [LazyColumn 列表页的内容结构](lazy-column-content/index.md)（3 条）：读到 Compose Screen 里 LazyColumn 的 items（按父项分组的卡片、isEmpty() 时的空态、列表卡片和状态 Tab）；产物里 List / ForEach 把子项拍平、没有空列表分支，或只用 Text(JSON.stringify(...)) 回显响应
- [工厂按 type 分派的编辑项列表](factory-type-dispatch/index.md)（5 条）：读到源端遍历配置列表、经工厂按每项 type 用 when 分支 create 对应 Fragment 并按顺序加进同一容器（else 落到空 Fragment）；产物里的列表提供函数、按类型分支的渲染、未匹配类型的回退和对应用例
- [RecyclerView 的列表和网格](recyclerview-list-grid/index.md)（7 条）：读到 RecyclerView 及其多类型 Adapter（addItemType、onCreateViewHolder）、GridLayoutManager / SpanSizeLookup、ItemDecoration、ItemTouchHelper；产物里 List / Grid 的区块内容、通栏和跨度、项间距和滑动操作
- [条目里用图标画的勾选和评分](item-icon-marks/index.md)（2 条）：源端条目里用 Icon 画的选中勾选图（Modifier.selectable 行）或星形评分（RatingBar、Icons.Filled.Star），目标写成了 Radio 或「好评 x.0」这类文本
- [LazyColumn 的程序滚动和左右分类联动](lazylist-scroll-linkage/index.md)（4 条）：读到源端 rememberLazyListState、animateScrollToItem，按 visibleItemsInfo / derivedStateOf 回写左侧选中态；交回的右侧是没有 Scroller 的 Scroll、scrollToIndex 对齐用 CENTER，或 onScrollIndex 在动画期间无条件回写
- [列表区域的空数据分支](list-empty-branch/index.md)（1 条）：读到页面里图表与侧栏列表并列、截图里空态文案在列表区域，列表有 empty view 或空态字符串；交回的 List / ForEach 没有 if 空数据分支，空态文案放在了别的组件里
- [ExpandableListView 的分组头](expandable-list-group/index.md)（2 条）：读到 ExpandableListView（expandGroup、groupIndicator、indicatorLeft）和 BaseExpandableListAdapter.getGroupView；产物里 List / ListItemGroup 写的组头、展开状态和箭头
- [Compose SwipeToDismissBox 的列表行滑删](swipe-to-dismiss/index.md)（3 条）：读到源端 SwipeToDismissBox / rememberSwipeToDismissBoxState（滑动方向、positionalThreshold、backgroundContent）；产物里 List 行用 PanGesture 加 translate 手写的滑删、阈值和背景层
- [LazyColumn、LazyRow 和 RecyclerView 列表容器](lazy-list-container/index.md)（3 条）：读到 Compose 的 LazyColumn / LazyRow（contentPadding、horizontalArrangement、verticalArrangement）或 RecyclerView 纵向列表，产物里是 List、Scroll 包 Column / Row 的容器写法
- [滚动中的可见比例判断](visible-area-ratio/index.md)（1 条）：读到 Compose Modifier.onGloballyPositioned 里用 boundsInWindow() 在滚动中算可见高度和比例（如 visibleHeight > height * 0.5f）；产物里挂在 .onAreaChange 上、用 globalPosition 加屏幕高算相交的可见性判断
- [LazyColumn 的 stickyHeader 吸顶](sticky-header/index.md)（2 条）：读到 Compose LazyColumn 里的 stickyHeader { … }（或按开关在 stickyHeader 和 item 之间切换），外层折叠顶栏有「内容未满不折叠」一类判断；产物里吸顶内容挪到 List 外做固定兄弟、List 没有 .sticky(StickyStyle.Header)，或决定折叠的高度测量没把 ListItemGroup 的 header 算进去
- [瀑布流迁成 WaterFlow 的列宽和间距](staggered-waterflow/index.md)（1 条）：读到 Compose LazyVerticalStaggeredGrid（StaggeredGridCells.Adaptive / Fixed、StaggeredGridItemSpan.FullLine）或 RecyclerView 配 StaggeredGridLayoutManager；产物里 WaterFlow 的 columnsTemplate、FlowItem 修饰链上有没有 .width('100%')、间距写在 padding 还是 margin
