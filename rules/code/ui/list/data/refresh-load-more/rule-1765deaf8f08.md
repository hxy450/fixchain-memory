# 首屏刷新和事件触发的 autoRefresh 等价调用都走同一个刷新处理函数并置 isRefreshing

审的是：代码
触发（任一种）：
- 读到：源页面有 autoRefresh() 事件入口，或首屏进入就刷新，刷新经 SmartRefreshLayout 状态机；写错的样子：aboutToAppear 或事件订阅里直接调 viewModel 的刷新 / getList(1)，没有经过 Refresh 的 onRefreshing 处理函数，也没置 isRefreshing
适用范围：目标用 Refresh + onReachEnd 实现分页，且首屏或事件也会触发刷新时
做法：
- aboutToAppear 的首刷、事件触发的 autoRefresh 等价调用都调同一个刷新处理函数（与 Refresh.onRefreshing 绑定的那个），由它置 this.isRefreshing = true、响应后复位
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- refreshing: boolean（支持 $$ 双向绑定）：Refresh 的刷新中状态，刷新处理函数置位复位它（出处：鸿蒙 SDK 的 ets/component/refresh.d.ts，RefreshOptions.refreshing）
- onRefreshing(callback: () => void): RefreshAttribute：进入刷新状态时的回调（出处：鸿蒙 SDK 的 ets/component/refresh.d.ts，RefreshAttribute.onRefreshing）
- 子组件未撑满列表时首次加载也会触发 onReachEnd：首帧空列表时触底加载会和首刷同时发生，首刷必须置 isRefreshing 才挡得住（出处：ts-container-list.md，onReachEnd）
来源：1 张卡，1 个应用
- case-a77939503960ebd3437d（免费来电多多）：做法第 1 步 ← 建议 3
