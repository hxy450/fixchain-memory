# 源页声明 adjustResize 时，页面显示时设 KeyboardAvoidMode.RESIZE、隐藏时还原

审的是：代码
触发（任一种）：
- 读到：Manifest 里 android:windowSoftInputMode="adjustResize"，编辑页用 Modifier.imePadding()；写错的样子：页面没调 setKeyboardAvoidMode，注释写「键盘避让由系统默认行为承担」或报告写「取系统默认 OFFSET 行为」
适用范围：迁移声明了 adjustResize 的编辑类页面（NavDestination）时
做法：
- 在该 NavDestination 的 .onShown(() => this.getUIContext().setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)) 设置，.onHidden(...) 里还原成进入前的模式（可先 getKeyboardAvoidMode() 记下）
- 尾部留白按键盘高度计算，对应源端 imePadding；对默认 OFFSET 是否等价不确定时先查 API，不以「保持默认并记录」结束
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setKeyboardAvoidMode(value: KeyboardAvoidMode): void；getKeyboardAvoidMode(): KeyboardAvoidMode：UIContext 上设置、读取键盘避让模式（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.setKeyboardAvoidMode）
- KeyboardAvoidMode.OFFSET = 0（布局上移）、RESIZE = 1（布局被压缩）：adjustResize 对应 RESIZE，OFFSET 只是整体上移（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，KeyboardAvoidMode）
- onShown(callback: Callback<VisibilityChangeReason>): NavDestinationAttribute；onHidden 同型：页面显示、隐藏时的回调（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onShown）
- adjustResize：Always resize the window: the content area of the window is reduced to make room for the soft input area：源端语义是压缩内容区，不是上移（出处：Android SDK 平台资源 data/res/values/attrs.xml，windowSoftInputMode 的 adjustResize（按应用的 compileSdk 取对应平台））
来源：1 张卡，1 个应用
- case-01833db0536ba02ed2ce（Cofi）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3
