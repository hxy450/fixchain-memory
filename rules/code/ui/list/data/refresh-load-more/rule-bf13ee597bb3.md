# SmartRefreshLayout 加载更多转成 onReachEnd 时，建加载中门闩并与刷新互斥

审的是：代码
触发（任一种）：
- 读到：源页面 setEnableLoadMore(true)、setOnLoadMoreListener，观察者里 finishLoadMore() / finishRefresh() 收口；ViewModel 的 pageNum 只在响应成功后自增；写错的样子：onReachEnd 的处理函数直接调 loadMore().then(concat)，没有 isLoadingMore 门闩，也不查 isRefreshing；或把 finishLoadMore 并进「isRefreshing = false」
适用范围：把 Android SmartRefreshLayout 的加载更多实现为 ArkUI List / Grid 的 onReachEnd 分页处理时
做法：
- 为加载更多建显式标志（如 @Local isLoadingMore）：处理函数入口 if (this.isLoadingMore || this.isRefreshing) return；发请求前 this.isLoadingMore = true
- 响应无论成功失败都复位：复位写在 Promise 的 finally（或每个分支）里；源端 finishLoadMore() 对应「加载更多进行中」的结束，不并入 isRefreshing 复位
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onReachEnd(event: () => void): ListAttribute：List 到达末尾时触发（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.onReachEnd）
- 子组件未撑满列表、无须滚动即可完整展示时，首次加载也会触发；边缘效果为弹簧时划过末尾触发一次、回弹回末尾再触发一次：onReachEnd 会在首帧空列表或一次滑动中重复触发，必须有门闩（出处：ts-container-list.md，onReachEnd）
- onReachEnd(event: () => void): GridAttribute：同族接口：Grid 到达末尾（出处：鸿蒙 SDK 的 ets/component/grid.d.ts，GridAttribute.onReachEnd）
- onReachEnd(event: () => void): WaterFlowAttribute：同族接口：WaterFlow 到达末尾（出处：鸿蒙 SDK 的 ets/component/water_flow.d.ts，WaterFlowAttribute.onReachEnd）
- 加 isLoadingMore（或父层双闩），加载中或刷新中直接返回，响应后无条件复位，整页重复消失：修好后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-a77939503960ebd3437d（免费来电多多）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、建议 2、建议 5；取值 5 ← 诊断
