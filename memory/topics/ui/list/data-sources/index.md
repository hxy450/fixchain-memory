# ui/list/data-sources

列表数据源的绑定与并发：各列表各自的数据与排序器、本地变换随列表迁移、分页门闩、代次保护与行内在途锁。

[上一级](../index.md)

## 本级经验

- [LazyForEach 换数据不换源对象，通知重载](lesson-40efd2d02a5ea9554a95.lesson.md) · 阶段：execute/repair · 信号：LazyForEach, IDataSource, DataChangeListener, onDataReloaded
- [onReachEnd 分页加载中不重入、刷新中不派发](lesson-0a398b212a8a80bd0c7f.lesson.md) · 阶段：spec/execute · 信号：SmartRefreshLayout, onReachEnd, onRefreshing, setOnLoadMoreListener
- [onRefreshing 先判刷新已在运行再发起](lesson-fa79c5a6658c68b71a21.lesson.md) · 阶段：execute · 信号：Refresh, onRefreshing, SwipeRefreshLayout, setOnRefreshListener
- [多个 Adapter 列表各绑各自数据源并实现级联推进回退](lesson-b6146f290e871c82e61d.lesson.md) · 阶段：execute · 信号：onPClick, onCClick, onBack, RecyclerView
- [批量异步修补按列表代次丢弃过期结果按 ID 修补](lesson-4cfd4cbcecfb3de96037.lesson.md) · 阶段：execute · 信号：requestSerial, onReachEnd, Promise
- [新列表排序找源端该列表自己的排序器不复用他表](lesson-eb59181d6dfaeb014aef.lesson.md) · 阶段：execute · 信号：Comparator, sortedWith, compareBy, Repository
- [迁移列表连同条目点击与本地 shuffled 变换一起实现](lesson-46307bc26d725b4634ca.lesson.md) · 阶段：execute · 信号：addOnItemTouchListener, Fisher-Yates, RecyclerView, Adapter
