# 数据、键与刷新

源端有 Adapter 的 setList / submitList / notifyItemChanged、removeAllViews 后逐项重建、SwipeRefreshLayout / SmartRefreshLayout、LazyForEach，目标端有 IDataSource、ForEach / Repeat 的键函数、Refresh、onReachEnd 时

## 触发族

- [列表数据源、条目的键和更新后的刷新](list-data-refresh/index.md)（7 条）：读到 Adapter 的 getItemCount、setList / submitList、remove + add + notifyItemChanged、onResume 或回调后改数据、分页追加和返回刷新；产物里 IDataSource 的成员、ForEach / Repeat 的键函数、传给 @Builder 的数据和整表回写
- [列表项的键和位置相关值](list-item-key/index.md)（2 条）：读到 Compose LazyColumn 的 itemsIndexed 传 index、或无 key 的 item { }，交回的代码里 ForEach / Repeat 的键不含位置、行内用闭包 index 或常驻组件保留旧状态
- [removeAllViews 后逐项 addView 重建的行](rebuilt-rows/index.md)（3 条）：读过的源码里每次计算或刷新先 removeAllViews()，再循环 inflate / addView 重建结果行或整个编辑器、按序号 requestFocus；交回的 ForEach 键只用显示内容拼、不含序号或代次，或原地改属性不重建、不恢复焦点
- [刷新时被重建的列表内容](list-rebuild-on-refresh/index.md)（3 条）：产物里 ForEach / Repeat 的键拼了请求序号、加载状态等易变字段，条目模型是整体替换的普通 interface，或 if (加载中) 把内容整块换成 LoadingProgress，翻页、切换时内容被销毁重建
- [列表页的加载入口和刷新状态](list-load-refresh/index.md)（4 条）：源端 SwipeRefreshLayout 的 setOnRefreshListener / setRefreshing、列表进详情再返回；产物里 Refresh({ refreshing }) 和 .onRefreshing、aboutToAppear / onPageShow 里的加载调用，以及按 isLoading、errorMessage 分派的页面状态
- [LazyForEach 列表改写成 Repeat](lazyforeach-to-repeat/index.md)（2 条）：读到 LazyForEach(IDataSource) 渲染列表或 ListItem；产物里写成 Repeat<T>(…).each(…).virtualScroll()，或 each 里调 @Builder
- [下拉刷新和加载更多](refresh-load-more/index.md)（6 条）：读到 SmartRefreshLayout（autoRefresh、setOnLoadMoreListener、finishRefresh / finishLoadMore）或带 page / size 的分页接口加 onRefresh / onLoadMore；产物里的 Refresh(refreshing)、onRefreshing 和 List.onReachEnd
- [ForEach 键函数和项里随语言、状态变的文案](foreach-key-mutable-text/index.md)（1 条）：读到列表项文案改成渲染期按语言或别的 @Trace 状态经 t(key) 取值、切换时整体替换数组；产物里 ForEach / LazyForEach / Repeat 的 keyGenerator 只返回恒定 id（如 (opt) => opt.value），项内 Text(opt.label) 显示可变文案
