# SmartRefreshLayout 的加载更多转成 onReachEnd 时，显式建立“加载中不重入、刷新中不派发”的门闩

## 何时使用

数据接线阶段，把 SmartRefreshLayout 的 onRefresh/onLoadMore 实现为 Refresh.onRefreshing 与 List/Grid.onReachEnd 分页处理时；规格提取阶段写分页竞态约束时

## 适用情境

源页面由 SmartRefreshLayout 驱动分页（setOnLoadMoreListener、观察者里 finishRefresh/finishLoadMore），页面本身没有 isLoading 变量；ViewModel 的页码在响应成功后才自增；目标用 Refresh + onReachEnd 并以 concat 追加。

## 例外与边界

- 门闩里读的 isRefreshing 应当就是以 $$ 双向绑定给 Refresh 的 refreshing 的那个状态变量：下拉手势触发时由组件把它置 true，不必在 onRefreshing 里重复置位；没有用 $$ 传入时组件的刷新状态不会写回这个变量，门闩读不到下拉刷新。

## 原因

SmartRefreshLayout 自带“加载中不重入、刷新与加载互斥”的状态机，页面代码里看不到；onReachEnd 在首帧空列表或快速滚动时会连续触发，与首刷或上一次加载并发，页码未自增时同一页被请求两次并各自追加，出现整页重复（刷新后消失）。把 finishLoadMore 映射成 isRefreshing 复位，或规格只写“Refresh 官方等价”，都会丢掉这层状态。

## 做法

1. onReachEnd 处理函数入口：isLoadingMore 或 isRefreshing 为真即返回；发请求前置位，响应无论成功失败都复位。
2. finishLoadMore 映射为“加载更多进行中”的结束，不并入 isRefreshing；首屏 aboutToAppear 刷新与事件触发的刷新都经过同一个刷新入口并置 isRefreshing。
3. 规格提取时，凡启用加载更多的页面，在竞态或状态契约里写明这两条互斥，并与“无重复 id”类验收绑定。

## 可选检查

- 逐个查看含 onReachEnd 的处理函数，确认都有门闩与互斥，且复位点覆盖 Promise 的所有分支。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕List 的 onReachEnd 在子组件未撑满列表、不用滚动就能完整展示时，首次加载也会触发；边缘效果为弹簧时，滑动经过末尾触发一次、回弹回到末尾再触发一次
- 〔原因〕应用没有另设 edgeEffect 时，List 的边缘效果默认 EdgeEffect.Spring；内容区小于一屏时默认没有回弹，要设 edgeEffect 的 options 为 { alwaysEnabled: true } 才有
