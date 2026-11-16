# 首屏焦点应落在输入框时，首查完成后等窗口获焦再对 TextInput 请求焦点

审的是：代码
触发（任一种）：
- 读到：规格验收写首屏输入框获焦并弹键盘；或源 manifest 未声明 windowSoftInputMode、布局里 EditText 前没有常驻可获焦视图；写错的样子：目标页的 TextInput 没有任何初始焦点逻辑；或在 aboutToAppear、首查回调里直接 requestFocus，窗口还没激活，输入框 focused 却不弹键盘
适用范围：界面实现阶段，首屏按源条件应把焦点给输入框的页面（含冷启动）
做法：
- TextInput 设 .id('…')；首屏数据查询完成后按源条件（如列表为空）对它请求焦点，回前台重建时复用同一个方法
- 请求前先用 window.findWindow(this.getUIContext().getWindowName()).isFocused() 判断窗口已获焦；没获焦就 win.on('windowEvent', (e) => { if (e === window.WindowEventType.WINDOW_ACTIVE) { … } }) 等激活后再请求
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function findWindow(name: string): Window：按窗口名找到窗口对象（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，window.findWindow）
- getWindowName(): string | undefined：UIContext 取当前窗口名（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.getWindowName）
- isFocused(): boolean：Window 是否已获焦（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.isFocused）
- on(type: 'windowEvent', callback: Callback<WindowEventType>): void；WindowEventType.WINDOW_ACTIVE = 2：窗口生命周期事件，等到 WINDOW_ACTIVE 再请求焦点（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.on('windowEvent') / WindowEventType.WINDOW_ACTIVE）
- function requestFocus(value: string): boolean：按组件 id 请求焦点（出处：鸿蒙 SDK 的 ets/component/common.d.ts，focusControl.requestFocus）
- enableKeyboardOnFocus(value: boolean): TextInputAttribute，默认 true：TextInput 通过非点击方式获焦时默认拉起输入法（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.enableKeyboardOnFocus）
- 冷启动时窗口激活晚于首查；首查后直接请求只得到 focused=true 不绑定输入法，改成窗口获焦后（或等 WINDOW_ACTIVE）再请求后键盘弹出：请求时机（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-1b03af761b99c891e236（Blockinger）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 7 ← 诊断
