# 列表、网格与翻页

读到源端有 ListView、GridView、RecyclerView / GridLayoutManager、LazyColumn / LazyRow、SmartRefreshLayout、ViewPager2 或 ActionMode 多选，规格里写列表、网格、刷新分页和翻页时

## 触发族

- [共享基类里的 ActionMode 多选](base-class-action-mode/index.md)（3 条）：读过的页面、Adapter 或 Fragment extends 一个共享基类，基类里有 startActionMode、onCreateActionMode、OnBackPressedCallback，或覆盖 lint 把基类报为未锚定；交回的规格没写基类建的上下文操作栏和多选的进出口
- [GridView / ListView 的滚动和按压态](grid-list-scroll/index.md)（2 条）：读到源 GridView / ListView 没改 listSelector、scrollbars、overScrollMode，条目高由内容量出、没有固定行高；页面规格只写列数和间距，或写「网格不滚动、一屏全可见」
- [Compose 惰性列表（LazyColumn / LazyRow）区块](lazy-list-block/index.md)（4 条）：读到 Compose 页面里的 LazyColumn / LazyRow 列表区块（可能在另一文件的子 Composable 里，带分区、空态、加载态）；交回的规格里这块只有一行组件映射，或少了状态分支和滚动方向
- [SmartRefreshLayout 下拉刷新和加载更多的互斥](refresh-loadmore-race/index.md)（1 条）：读到源页面用 SmartRefreshLayout 并 setEnableLoadMore(true)，ViewModel 的刷新和加载更多共用 pageNum；规格只把它标为 Refresh(onRefreshing / onReachEnd)「官方等价」，竞态文档没有分页互斥条目
- [多列容器里的 no-op 广告位](noop-ad-in-grid/index.md)（1 条）：源端 GridLayoutManager + SpanSizeLookup 让广告项通栏，而全局决策或派工把广告定为 no-op 空容器；规格对 Grid、WaterFlow 的转换决策
- [侧栏分类页的内容区](sidebar-category-page/index.md)（1 条）：安卓侧栏分类页：左侧一级分类列表，右侧同一滚动列表依次展示全部分类、左侧选中随滚动变化；规格对右侧内容区展示范围的描述
- [ViewPager2 加 FragmentStateAdapter 的实际页数](viewpager2-page-count/index.md)（1 条）：读到 ViewPager2 + FragmentStateAdapter，getItemCount 返回只含一个元素的 listOf(…) 的 size，currentItem = 1 之类切页入口在单页下无效或隐藏；规格按组件类型或 navigation_mode 写「ViewPager2 → Swiper」，还给不存在的页预置 Swiper index
- [Compose PullToRefreshBox 下拉刷新](compose-pull-to-refresh/index.md)（2 条）：读到 Compose 源端用 PullToRefreshBox(isRefreshing, onRefresh)，默认 M3 指示器，包住的范围可能是加载条和 TabRow + Pager 整体；规格的转换决策写「PullToRefreshBox → Refresh { List }」「官方下拉刷新 / 标准映射」，或让每个 Tab 各放一个 Refresh
- [按 position 从当前数据表取行的列表点击回调](click-row-by-position/index.md)（1 条）：读到源端列表点击回调（onListItemClick 等）按 position 从当前数据表取行，加载函数每次新建整张表；规格写了「每次整表重建」「ForEach 键含内容字段」，点击分发只写按状态分发、语义照抄，没写条目闭包里怎样定位当前行
- [源码自定义的触底加载 helper](custom-reach-end-helper/index.md)（1 条）：读到源端列表调用自定义的触底 helper，函数体是 derivedStateOf { 末项可见判定 } 加 if (条件 && !重试态) LaunchedEffect(Unit) { 加载下一页 }；规格的转换决策只写「helper → List.onReachEnd」或「onReachEnd / onScrollIndex」，没写触发条件、触发时机和调用点的重试参数
- [ViewPager 翻页的释放定页和归位动画](viewpager-release-settle/index.md)（1 条）：读到源码 import androidx.viewpager.widget.ViewPager（OnPageChangeListener、setOffscreenPageLimit），或 Activity 继承基于 ViewPager 的三方壳（如 AppIntro2）、库是 AAR 没有源码；规格只写「ViewPager → Swiper 标准映射」「默认即可对齐」「三方库无源码 → 按 Swiper 自研」，没有释放阈值、归位时长和曲线
