# 源端的释放或移交挂在生命周期回调上时，规格先查清 owner 和触发路径，再写目标端调用位

审的是：规格
触发（任一种）：
- 读到：源端在 DisposableEffect { onDispose { … } }、LifecycleEventObserver 的 ON_STOP / ON_RESUME，或引擎的 onStop() / onResume() 入口里做释放、移交或取回；写错的样子：规格把它写成「页面销毁」「退后台」「前后台移交」一笔带过：没写源端回调挂在哪个 owner 上、哪些用户路径会触发它，也没写目标端在哪个事件调用
适用范围：规格提取阶段翻译源端挂在生命周期回调上的释放、移交、取回时
做法：
- 在源码里查清这个回调挂在哪个 owner 上（外层 Composable、导航目的地的返回栈条目、Activity 或进程），写进规格
- 把会让这个 owner 离开组合或进入 ON_STOP / ON_RESUME 的用户路径逐条写成触发契约和验收条目（退后台、返回出栈、跳到其他目的地、回到本页、切屏），不用「退后台」一笔带过
- 写明目标端的调用位：NavDestination 的 .onHidden / .onShown 按 VisibilityChangeReason 各调哪个入口；归外层的清理写到 Ability 或 Navigation 宿主页
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onShown(callback: Callback<VisibilityChangeReason>): NavDestinationAttribute：NavDestination 页显示后回调，带显示原因（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onShown）
- onHidden(callback: Callback<VisibilityChangeReason>): NavDestinationAttribute：NavDestination 页隐藏后回调，带隐藏原因（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onHidden）
- VisibilityChangeReason.TRANSITION = 0、CONTENT_COVER = 1、APP_STATE = 2：TRANSITION 是页面导航引起，CONTENT_COVER 是 bindContentCover 引起，APP_STATE 是应用前后台切换引起（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，VisibilityChangeReason）
- onHidden 在非栈顶页面 push 进栈、栈顶页面 pop 出栈或应用切到后台时执行：目标端能一并覆盖这几条用户路径的事件（出处：arkts-navigation-navdestination.md，页面生命周期）
- navigation-compose 目的地内的 LocalLifecycleOwner 是返回栈条目，返回出栈或跳到其他目的地时同样进入 ON_STOP：源端 ON_STOP 不只是应用退后台（出处：卡里修好并验证过）
- 只改 screen 状态切到另一屏时外层 Composable 仍在组合中，onDispose 不触发：外层 DisposableEffect 的清理不随切屏发生（出处：卡里修好并验证过）
针对本应用要查的：
- 回调挂在哪个 owner 上：源工程里声明 DisposableEffect / LifecycleEventObserver 的 Composable 或 Activity，顺着它被谁调用找（NavHost 的 composable 路由、外层 Composable 里按状态变量切屏的 if）；在 NavHost 路由目的地里取 LocalLifecycleOwner.current 的，owner 是返回栈条目；在承载多屏的外层 Composable 里的，只在外层离开组合时触发
- 会触发它的用户路径：源工程里改切屏状态的入口、navigate / popBackStack 调用和返回键处理（BackHandler）；逐个列出，对上目标端的导航动作和 VisibilityChangeReason
未核实：导航离开时 ON_STOP 先于观察者注销，依据的是修复期对 navigation-compose 2.9.1 源码的查证，没在设备上复现
来源：2 张卡，2 个应用
- case-1f17a64b74c60410dad7（Cofi）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 2；取值 5 ← 诊断
- case-f4de4c0baf567b736a95（听音练习）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 1；取值 6 ← 诊断
