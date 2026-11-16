# 共享播放服务不在页面 aboutToDisappear 里 stop，页面离开只解除监听，Ability 销毁时停止

审的是：代码
触发（任一种）：
- 读到：源端 DisposableEffect 的 onDispose 挂在承载多屏的外层 Composable 上，切屏只改状态变量；写错的样子：页面的 aboutToDisappear() / onDisappear() 里调用 dispose() 或共享播放服务的 stop()
适用范围：把源端多屏共享的播放器、播放任务迁成目标端共享服务，页面挂在 Navigation 下时
做法：
- 页面离开（打开另一屏）时只把自己注册在服务上的监听置空，不调 dispose() / stop()；回到页面时在 aboutToAppear / onShown 里恢复
- 共享服务在拥有它的 EntryAbility 的 onDestroy() 里 stop()
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 打开另一屏时页面只解除播放监听、其他离开仍 dispose，aboutToAppear 与 onShown 复位；EntryAbility.onDestroy 停止共享播放服务：修复后保留到截止的写法（出处：卡里修好并验证过）
- onDestroy(): void | Promise<void>：UIAbility 的销毁回调（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onDestroy）
- onHidden(callback: Callback<VisibilityChangeReason>): NavDestinationAttribute：NavDestination 被推入的页面盖住时触发，不是销毁（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onHidden）
- 非栈顶页面 push 进栈时下层触发 onHidden；aboutToDisappear 只在自定义组件析构销毁前执行：推入子页时下层页面的 aboutToDisappear 不一定触发，别靠它判断「切屏」（出处：arkts-navigation-navdestination.md，页面生命周期）
未核实：卡里没有设备复现「播放中打开另一屏」，Navigation 首页内容在推入子页时 aboutToDisappear 是否触发只是推断
来源：1 张卡，1 个应用
- case-f4de4c0baf567b736a95（听音练习）：做法第 1 步 ← 诊断、建议 3；做法第 2 步 ← 诊断、建议 3；取值 1 ← 诊断
