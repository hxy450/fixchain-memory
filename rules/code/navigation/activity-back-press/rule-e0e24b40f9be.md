# 非 @Entry 子组件的返回拦截要由 @Entry 壳页 onBackPress 转调，不靠自身回调

审的是：代码
触发（任一种）：
- 读到：源端在非 Activity 根的 Composable 里用 BackHandler / PredictiveBackHandler 按状态条件拦截返回；写错的样子：目标组件不是 @Entry、被 @Entry 壳页直接组合（不在 Navigation 栈内），却只在自身写 onBackPress() 或挂 NavDestination().onBackPressed(...)；壳页没有转调
- 读到：子组件文件头注明 onBackPress 等平台钩子需要入口页转发；写错的样子：@Entry 页直嵌这个子组件，没有写 onBackPress() 转调，也没有作为阻塞项上报
适用范围：源端返回拦截落在目标端非 @Entry 的组件上、且该组件由 @Entry 页直接组合而不是驻留在 Navigation 栈内时
做法：
- 子组件加回调属性（@ComponentV2 用 @Event，如 onBackHandlerReady），aboutToAppear 里回传 () => this.onBackPress()，aboutToDisappear 里回传 null
- @Entry 壳页保存这个函数，在自己的 onBackPress() 里转调并返回它的结果；未注册时返回 false 交系统
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onBackPress?(): void | boolean：只对 @Entry 装饰的组件回调；返回 true 表示自己处理返回，false（默认）走系统返回（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.onBackPress）
- onBackPressed(callback: () => boolean): NavDestinationAttribute：NavDestination 的返回回调；组件被 @Entry 页直接组合、不在 Navigation 栈内时不触发（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onBackPressed）
- declare const Event: PropertyDecorator：@ComponentV2 子组件向父组件回传函数用的装饰器（出处：鸿蒙 SDK 的 ets/component/common.d.ts，Event）
- aboutToAppear?(): void；aboutToDisappear?(): void：子组件在这两个生命周期里注册、注销返回裁决函数（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.aboutToAppear、BaseCustomComponent.aboutToDisappear）
- 子组件经 @Event 回传裁决函数、壳页 onBackPress 转调、未注册返回 false 后，抽屉打开时按返回关抽屉，关闭时退出：按此改后通过设备判定（出处：卡里修好并验证过）
未核实：卡里上机的行为出自 HarmonyOS 5.0.0（API 12），本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-2b9869554cf9027174a0（JetLagged）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、建议 3、诊断；取值 2 ← 诊断；取值 5 ← 诊断
