# Compose AlertDialog 迁成 openCustomDialog 弹窗层，不用 Stack 子节点模拟

审的是：代码
触发（任一种）：
- 读到：Compose AlertDialog(onDismissRequest, confirmButton, …) 或 Dialog，含组件内状态控制的子对话框；写错的样子：弹窗写成页面 Stack 或组件 Column 的条件子节点，加 backgroundColor('#66000000') 自绘遮罩
- 读到：规格写「AlertDialog → openCustomDialog / 自定义确认弹窗」；写错的样子：build() 里声明式写 AlertDialog({...})，或退化成 showAlertDialog
- 读到：工程内没有 openCustomDialog 用例，已有页面用 Stack 叠半透明层模拟弹窗；写错的样子：头注写「采用项目自绘 Stack 遮罩约定」「项目无 CustomDialog 用例」
适用范围：Compose AlertDialog/Dialog（含共享组件里的子对话框）迁成 ArkUI 时
做法：
- 用 getUIContext().getPromptAction().openCustomDialog 承载源端的标题、正文和按钮（保留 Button 或 TextButton），关闭用 closeCustomDialog（传 dialogId 或同一个 ComponentContent）；也可用 CustomDialogController
- 遮罩和宽度按源码与平台默认：M3 AlertDialog 遮罩 0.6（maskColor 黑色 60%），宽为内容固有宽夹在 280..560vp
- 首个写弹窗的公共组件建立共用窗口层（遮罩、宽度、onWillDismiss、返回键）供后续复用；规格、参考与工程先例冲突时以规格为准（能否沿用 Stack 遮罩先例有争议）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- openCustomDialog(options: promptAction.CustomDialogOptions): Promise<number>：PromptAction 打开自定义内容弹窗，返回 dialogId，配 closeCustomDialog(dialogId: number) 关闭（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
- openCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options?: promptAction.BaseDialogOptions): Promise<void>：以 ComponentContent 传内容的重载（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
- closeCustomDialog<T extends Object>(dialogContent: ComponentContent<T>): Promise<void>：同族接口：PromptAction 关闭对应 ComponentContent 的弹窗（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.closeCustomDialog）
- constructor(uiContext: UIContext, builder: WrappedBuilder<[T]>, args: T)：ComponentContent 的构造，builder 用 wrapBuilder 包一个全局 @Builder（出处：鸿蒙 SDK 的 ets/api/arkui/ComponentContent.d.ts，ComponentContent.constructor）
- constructor(value: CustomDialogControllerOptions)：CustomDialogController 的构造，open() / close() 开关弹窗（出处：鸿蒙 SDK 的 ets/component/custom_dialog_controller.d.ts，CustomDialogController.constructor）
- BaseDialogOptions：maskColor?: ResourceColor；isModal?: boolean（默认 true）；onWillDismiss?: Callback<DismissDialogAction>：遮罩色、模态和交互关闭回调（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，promptAction.BaseDialogOptions）
- 统一改为 openCustomDialog 系统弹窗层（遮罩 0.6、宽 280..min(560, 屏宽-40)、M3 按钮最小宽和触控高）后与源端一致：修法和取值（出处：卡里修好并验证过）
针对本应用要查的：
- 弹窗按钮类型和内容：源工程 Compose 文件里该 AlertDialog 的 confirmButton / dismissButton 参数；读出是 Button 还是 TextButton 及文案资源，目标照写
未核实：卡里观察到的行为出自鸿蒙 SDK API 24（6.1.1），本机核实用 API 23；能否沿用自绘 Stack 遮罩先例，两卡说法冲突：case-f63ccb39dd60e2abb04b 说沿用时核对覆盖层挂在页面全屏根 Stack 上、不是组件内 Column 的子项；case-79781a308d7df8726820 说不用页面 Stack/Column 条件子节点模拟（遮罩、层级与返回键都不对），「项目无 CustomDialog 用例」不是沿用自绘浮层的理由
来源：2 张卡，1 个应用
- case-79781a308d7df8726820（jerboa）：做法第 1 步 ← 建议 1、建议 4；做法第 2 步 ← 建议 3、诊断；做法第 3 步 ← 建议 2；取值 7 ← 诊断
- case-f63ccb39dd60e2abb04b（jerboa）：做法第 1 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2
