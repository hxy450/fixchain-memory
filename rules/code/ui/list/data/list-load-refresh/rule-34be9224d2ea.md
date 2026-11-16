# Refresh.refreshing 绑定的状态会被事件置真时，onRefreshing 里先判断刷新是否已在运行

审的是：代码
触发（任一种）：
- 读到：源端 SwipeRefreshLayout 同时有 setOnRefreshListener(…)（只响应用户下拉）和事件回调里的 setRefreshing(event.…)（只同步指示器）；写错的样子：Refresh({ refreshing: $$状态 }) 的状态由运行态事件或菜单刷新置 true，同时 .onRefreshing(() => 刷新入口()) 无条件发起刷新
- 写错的样子：给已用 $$ 绑到 Refresh.refreshing 的状态新接了事件处理（this.状态 = event.…），同组件的 .onRefreshing 没有守卫
适用范围：安卓 SwipeRefreshLayout 迁成 ArkUI Refresh，且 refreshing 绑定的状态不只由用户下拉改变时
做法：
- 写成 .onRefreshing(() => { if (全局刷新已在运行) { return; } 刷新入口(); })：已在运行就只让指示器跟随 refreshing，不再调用刷新入口
- 在 onRefreshing 旁的注释里写明触发来源（用户下拉 / 程序把 refreshing 置真）和守卫条件，同批页面复用同一守卫，不复制无守卫写法
- 给已绑定 refreshing 的状态接运行态事件时，回读同组件的 onRefreshing，没有守卫就按第 1 步补上
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- refreshing: boolean：Refresh 的构造参数，组件是否处于刷新中，支持 $$ 双向绑定（出处：鸿蒙 SDK 的 ets/component/refresh.d.ts，RefreshOptions.refreshing）
- onRefreshing(callback: () => void): RefreshAttribute：进入刷新状态时回调，不区分进入的原因（出处：鸿蒙 SDK 的 ets/component/refresh.d.ts，RefreshAttribute.onRefreshing）
- refreshing 被程序置 true 时，Refresh 同样进入刷新态并回调 onRefreshing：这和 SwipeRefreshLayout.setRefreshing 只改指示器不同，无守卫时一次程序刷新会再发起一次刷新（出处：卡里修好并验证过）
- onRefreshing 里加「全局刷新未在运行才发起」的守卫：加上后菜单刷新只发起一次，不再出现节流提示、指示器不被提前复位（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-9f075619772b433d319a（AntennaPod）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 3；取值 3 ← 诊断；取值 4 ← 诊断
