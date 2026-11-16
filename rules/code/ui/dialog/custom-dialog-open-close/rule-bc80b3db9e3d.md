# ComponentContent 构造后才赋值的回调，builder 里写成箭头函数在点击时取值

审的是：代码
触发（任一种）：
- 读到：源端 DialogFragment / MaterialAlertDialogBuilder 的 setPositiveButton、setNegativeButton 点击后关闭或确认弹窗；写错的样子：builder 里写 onClose: args.onClose 这类把 args 回调字段直接交给内容组件 @Param 的写法，而该字段在 new ComponentContent(...) 之后才赋值（典型是 args.onClose = () => closeCustomDialog(content)），args 类里的默认值是 no-op
适用范围：用 new ComponentContent(uiContext, wrapBuilder(builder), args) 加 openCustomDialog 封装弹窗，且 args 里有回调字段要等构造后拿到 content 句柄才能赋值时
做法：
- builder 里把构造后才赋值的字段写成 onX: (...): void => args.onX(...)，点击时才读 args；或者把 args 整体传给内容组件，在点击时读取 args.onX。不要写 onX: args.onX
- 对每个 new ComponentContent(..., args) 往后找 args.xxx = 的赋值；同一字段在 builder 里以 xxx: args.xxx 直接传入的，判为失效接线，按上一步改
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- constructor(uiContext: UIContext, builder: WrappedBuilder<[T]>, args: T)：带参的 ComponentContent 构造，args 是 builder 函数的参数（出处：鸿蒙 SDK 的 ets/api/arkui/ComponentContent.d.ts，ComponentContent.constructor）
- new ComponentContent(...) 时 builder 就执行，@Param 拿到的是构造当时的值；之后再给普通 args 对象的字段赋值，不会传进已构建的内容；改成箭头函数延迟取值后按钮能关闭弹窗：构造后赋值的回调为什么不生效（出处：卡里修好并验证过）
- closeCustomDialog<T extends Object>(dialogContent: ComponentContent<T>): Promise<void>：按 content 句柄关闭弹窗，所以关闭回调只能在构造之后才写得出来（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.closeCustomDialog）
- openCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options?: promptAction.BaseDialogOptions): Promise<void>：用 ComponentContent 打开自定义弹窗（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
- closePopup<T extends Object>(content: ComponentContent<T>): Promise<void>：同族接口：PromptAction 按 ComponentContent 句柄关闭气泡（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.closePopup）
- closeMenu<T extends Object>(content: ComponentContent<T>): Promise<void>：同族接口：PromptAction 按 ComponentContent 句柄关闭菜单（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.closeMenu）
- closeBindSheet<T extends Object>(bindSheetContent: ComponentContent<T>): Promise<void>：同族接口：UIContext 按 ComponentContent 句柄关闭半模态（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.closeBindSheet）
未核实：「构造时就执行 builder」是卡里上机观察到的，声明和文档里没有写明构造时机
来源：1 张卡，1 个应用
- case-50d84809509dfadabf5c（AntennaPod）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2；取值 2 ← 诊断
