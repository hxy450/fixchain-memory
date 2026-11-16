# 安卓 onStart 里的初始化，目标写进 onWillShow，回前台在 onShown 里补

审的是：代码
触发（任一种）：
- 读到：Activity 的 onStart() / onResume() 里每次都重读 getIntent()、重建列表、校验目录或重设界面文字；写错的样子：对应 NavDestination 把这段初始化挂在一次性的 .onReady(...) 或 aboutToAppear 里，.onShown 只做别的事；注释仍写着源自 onStart
适用范围：安卓 Activity 迁成 NavDestination 页面，源端在 onStart/onResume 做「每次可见」的初始化时
做法：
- 把源 onStart/onResume 的初始化写进 NavDestination(){…}.onWillShow(() => { 初始化 })，进入和从子页返回都会重跑，首帧前就绪；不写进 .onReady 或 aboutToAppear
- 从后台回前台不经过 onWillShow，再加 .onShown((reason: VisibilityChangeReason) => { if (reason === VisibilityChangeReason.APP_STATE) { 初始化 } })
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onWillShow(callback: Callback<void>): NavDestinationAttribute：NavDestination 布局显示之前执行；应用切换到前台不会执行（@since 12）（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onWillShow；arkts-navigation-navdestination.md，页面生命周期）
- onShown(callback: Callback<VisibilityChangeReason>): NavDestinationAttribute：显示之后执行，回调带显示原因（带原因的这一版 @since 21）（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onShown）
- VisibilityChangeReason.TRANSITION = 0、CONTENT_COVER = 1、APP_STATE = 2：APP_STATE 表示因应用前后台切换而显示或隐藏（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，VisibilityChangeReason）
- onReady(callback: Callback<NavDestinationContext>): NavDestinationAttribute：NavDestination 即将构建子组件时调用，只在创建时一次，不随每次可见重跑（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onReady）
- onHidden(callback: Callback<VisibilityChangeReason>): NavDestinationAttribute：同族接口：NavDestination 隐藏后执行，同样带 VisibilityChangeReason（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onHidden）
- onStart 在 onCreate 之后、或停止后经 onRestart 重新显示给用户时调用：源端 onStart 是「每次可见」，不是一次性（出处：android.app.Activity#onStart）
未核实：卡里的行为在 API 24（6.1.1）上观察，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-7d097177e497ea9e202c（MifareClassicTool）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断
