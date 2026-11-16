# 源端挂在生命周期回调上的释放和移交

agent 会看到什么：源端在 DisposableEffect / onDispose、LifecycleEventObserver 的 ON_STOP / ON_RESUME 或引擎的 onStop() / onResume() 里做释放、移交、暂停，规格里写成「页面销毁」「退后台」「停摆」，没写 owner、触发路径和目标端的调用位

## 通用查法

### 源端的释放或移交挂在生命周期回调上时，规格先查清 owner 和触发路径，再写目标端调用位

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

## 规矩

- rule-c0a965d9be6e｜源端生命周期观察者的 ON_STOP 移交，规格先写清 owner 是谁，再逐条写进入 ON_STOP 的用户路径｜读到：Compose 里 DisposableEffect(LocalLifecycleOwner.current) 注册 LifecycleEventObserver，ON_STOP 时移交后台、ON_RESUME 时取回，而这个 Composable 是导航路由的目的地；写错：规格把它写成「前后台移交」「退后台移交」，验收只有「退后台再回前台」一个场景，没写 owner 是谁，也没写返回出栈、跳到其他目的地同样触发
- rule-11f50a756dd2｜DisposableEffect 挂在承载多屏的外层 Composable 时，规格把清理归到外层生命周期｜读到：同一个 Composable 里先声明 DisposableEffect(Unit) { onDispose { …cancel(); player.stop() } }，再用状态变量 if (screen == …) 切换两个屏幕；写错：目标拆成两个页面后，规格范围只写一个页面，对接点写「页面销毁：取消播放任务并 stop()」、判据写「页面退出后无持续音频」；没写切到另一屏时播放继续
- rule-1b32f0b7896d｜引擎有 onStop/onResume 入口时，页面规格写明它们在 NavDestination 哪个事件调用｜读到：规格或引擎代码里有 onStop()/onResume() 这类生命周期入口，注释写「页面退后台接线入口（由后面的 slice 调用）」；写错：页面的 feature spec 里没有生命周期接线项：没写 NavDestination 的哪个事件、哪个 reason 调 onStop / onResume，也没写应用前后台怎么接
- rule-7525ce0c9f85｜规格写前后台行为时把「后台不派帧」和「回前台按墙钟追平」分开写，不只写停摆｜读到：源端 Compose 动画的帧时钟随宿主 ON_STOP 暂停，回前台继续；写错：规格只写「停摆」「冻结」「照常停摆于前台」，没写回前台时进度怎么推进
