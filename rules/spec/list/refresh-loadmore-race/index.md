# SmartRefreshLayout 下拉刷新和加载更多的互斥

agent 会看到什么：读到源页面用 SmartRefreshLayout 并 setEnableLoadMore(true)，ViewModel 的刷新和加载更多共用 pageNum；规格只把它标为 Refresh(onRefreshing / onReachEnd)「官方等价」，竞态文档没有分页互斥条目

## 规矩

- rule-80741780cec0｜页面启用加载更多时，规格的竞态或状态契约写明「加载中不重入、刷新中不派发加载更多」｜读到：源页面用 SmartRefreshLayout 并 setEnableLoadMore(true)；ViewModel 的刷新和加载更多共用 pageNum；写错：规格只把 SmartRefreshLayout→Refresh(onRefreshing / onReachEnd) 标为「官方等价」，竞态文档没有列表分页互斥条目；或写成「刷新与触底加载可交错，鸿蒙侧不做守卫（忠实还原）」
