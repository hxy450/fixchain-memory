# SmartRefreshLayout 的加载更多转成 onReachEnd 时，显式建立“加载中不重入、刷新中不派发”的门闩

ID：`lesson-0a398b212a8a80bd0c7f` · 版本：1

[本主题](index.md)

## 何时使用

数据接线阶段，把 SmartRefreshLayout 的 onRefresh/onLoadMore 实现为 Refresh.onRefreshing 与 List/Grid.onReachEnd 分页处理时；规格提取阶段写分页竞态约束时

## 适用情境

源页面由 SmartRefreshLayout 驱动分页（setOnLoadMoreListener、观察者里 finishRefresh/finishLoadMore），页面本身没有 isLoading 变量；ViewModel 的页码在响应成功后才自增；目标用 Refresh + onReachEnd 并以 concat 追加。

## 原因

SmartRefreshLayout 自带“加载中不重入、刷新与加载互斥”的状态机，页面代码里看不到；onReachEnd 在首帧空列表或快速滚动时会连续触发，与首刷或上一次加载并发，页码未自增时同一页被请求两次并各自追加，出现整页重复（刷新后消失）。把 finishLoadMore 映射成 isRefreshing 复位，或规格只写“Refresh 官方等价”，都会丢掉这层状态。

## 做法

1. onReachEnd 处理函数入口：isLoadingMore 或 isRefreshing 为真即返回；发请求前置位，响应无论成功失败都复位。
2. finishLoadMore 映射为“加载更多进行中”的结束，不并入 isRefreshing；首屏 aboutToAppear 刷新与事件触发的刷新都经过同一个刷新入口并置 isRefreshing。
3. 规格提取时，凡启用加载更多的页面，在竞态或状态契约里写明这两条互斥，并与“无重复 id”类验收绑定。

## 可选检查

仅在适用条件不确定、与当前输入冲突或需要验证关键假设时按需执行；优先复用已有证据和正常测试。
不因读取本条经验而额外启动验证流程；项目原有必需测试照常执行。

- 逐个查看含 onReachEnd 的处理函数，确认都有门闩与互斥，且复位点覆盖 Promise 的所有分支。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-a77939503960ebd3437d · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4, recommendation:5
  卡片版本：`0e8da288462f1f4fb5f4252448c80d0fe152e8837a0a31bfc36609973553695b`
