# 启动 Activity 没覆写返回时，根页 onBackPressed 里移到后台并返回 true

审的是：代码
触发（任一种）：
- 读到：启动 Activity 没有覆写 onBackPressed，没有 OnBackPressedDispatcher 回调，onKeyDown 也不处理 KEYCODE_BACK；存档写在 onPause、读档写在 onResume；写错的样子：入口页是 Navigation(this.navPathStack){} 空首页，aboutToAppear 里 pushPathByName 压入唯一页面；该 NavDestination 没有 .onBackPressed，按返回出栈露出空白首页
适用范围：单 Activity 应用迁成 Navigation 加 NavDestination 入口壳时，根页面的返回键行为
做法：
- 按栈推演：空首页上压了唯一页面后栈深为 1，返回会出栈回到空首页，不会退出；「空栈返回才退出」只在首页成立
- 根 NavDestination 写 .onBackPressed(() => { 弹窗开着就先关弹窗并 return true；否则 (this.getUIContext().getHostContext() as common.UIAbilityContext).moveAbilityToBackground(); return true })，存档交给 onBackground / onHidden
- 也可以把首页内容直接放在 Navigation 首页，不压栈
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onBackPressed(callback: () => boolean): NavDestinationAttribute：导航控制器里有内容时生效；返回 true 表示重写返回键逻辑，false 表示回退到上一个页面（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onBackPressed；ts-basic-components-navdestination.md，onBackPressed）
- moveAbilityToBackground(): Promise<void>：把当前 Ability 移到后台；只能在前台时调用（错误码 16000065），@since 12（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.moveAbilityToBackground）
- getHostContext(): Context | undefined：页面里取所在 Ability 的上下文，再转成 UIAbilityContext（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.getHostContext）
- Android 12（S）起，任务根且声明 ACTION_MAIN + CATEGORY_LAUNCHER 的 Activity 按返回时，Activity 和任务移到后台而不是 finish：源端没覆写返回时的默认行为：回到桌面、进程和局面保留（出处：android.app.Activity#onBackPressed）
- pushPathByName(name: string, param: unknown, animated?: boolean): void：把页面压入导航栈；压在空首页上后栈深为 1（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- onBackPressed 里 moveAbilityToBackground() 并 return true 后，返回键回到桌面、应用保留局面，与安卓一致：修好后的写法（出处：卡里修好并验证过）
未核实：第 3 步（首页内容直接放在 Navigation 首页）卡里没上机验证；空栈按返回是退到后台还是结束 Ability 没查实
来源：1 张卡，1 个应用
- case-e8db862eb02b52da96d0（2048）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2；取值 6 ← 诊断
