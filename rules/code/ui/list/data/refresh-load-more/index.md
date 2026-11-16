# 下拉刷新和加载更多

agent 会看到什么：读到 SmartRefreshLayout（autoRefresh、setOnLoadMoreListener、finishRefresh / finishLoadMore）或带 page / size 的分页接口加 onRefresh / onLoadMore；产物里的 Refresh(refreshing)、onRefreshing 和 List.onReachEnd

## 规矩

- rule-1765deaf8f08｜首屏刷新和事件触发的 autoRefresh 等价调用都走同一个刷新处理函数并置 isRefreshing｜读到：源页面有 autoRefresh() 事件入口，或首屏进入就刷新，刷新经 SmartRefreshLayout 状态机；写错：aboutToAppear 或事件订阅里直接调 viewModel 的刷新 / getList(1)，没有经过 Refresh 的 onRefreshing 处理函数，也没置 isRefreshing
- rule-bf13ee597bb3｜SmartRefreshLayout 加载更多转成 onReachEnd 时，建加载中门闩并与刷新互斥｜读到：源页面 setEnableLoadMore(true)、setOnLoadMoreListener，观察者里 finishLoadMore() / finishRefresh() 收口；ViewModel 的 pageNum 只在响应成功后自增；写错：onReachEnd 的处理函数直接调 loadMore().then(concat)，没有 isLoadingMore 门闩，也不查 isRefreshing；或把 finishLoadMore 并进「isRefreshing = false」
- rule-8b2762f1ea13｜源端「查看全部」页走独立分页接口并带刷新和加载更多时，目标照接，不用详情接口附带的数组｜读到：源端列表页的 Service 接口带 `page` / `size` 参数分页取数，Screen 里有下拉刷新和 `onLoadMore` 加载更多；写错：目标「查看全部」页仍取详情接口附带的少量数组，没有 `Refresh`、加载更多、重试和空态
- rule-7bbab894e94d｜源端按末项可见状态触底加载时，用 onScrollIndex 做上升沿，不用 onReachEnd 替代｜读到：源端 derivedStateOf { 最后可见项下标 == totalItems - 1 } 加 if (条件 && !重试态) LaunchedEffect(Unit) { 加载下一页 }；写错：目标 List 上只写 .onReachEnd(() => this.loadMore())，或只在 onReachEnd 里补一个重试态判断，没有末项可见判定和上升沿
- rule-65130daa4093｜源调用点把触底 helper 的重试参数写成字面 false 时，目标不照搬别的列表的失败态抑制｜读到：源端调用点给触底 helper 传字面 false 作重试参数（helper 内是 derivedStateOf + LaunchedEffect）；写错：目标该列表的 .onReachEnd / onScrollIndex 回调里加了「追加失败态时不自动加载」的判断，照搬自源端传重试变量的另一个列表
- rule-cee611366a63｜PullToRefreshBox 迁 Refresh 时隐藏系统指示器、自绘指示器并抵消内容位移｜读到：源端 `PullToRefreshBox` 用默认 M3 指示器，或规格写明了指示器外观和内容不随下拉移动；写错：目标 `Refresh({ refreshing })` 没传 builder，用系统默认指示器，内容随下拉下移
