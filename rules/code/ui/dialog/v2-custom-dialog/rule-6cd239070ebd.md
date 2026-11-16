# 组件外函数开自定义弹窗时用 ComponentContent，不在 builder 闭包里调全局 @Builder

审的是：代码
触发（任一种）：
- 读到：安卓 BottomSheetDialog / DialogFragment 类弹窗要被多个入口复用；写错的样子：导出的普通函数（只持有 UIContext）里 openCustomDialog({ builder: () => { 全局Builder(...) } })，闭包不属于组件实例，直接调模块级 @Builder function 创建 @ComponentV2 组件
适用范围：ArkTS V2（@ComponentV2）工程用 openCustomDialog 打开自定义组件弹窗时
做法：
- 组件外的共享函数里：const content = new ComponentContent(uiContext, wrapBuilder(全局Builder), 参数对象)；await uiContext.getPromptAction().openCustomDialog(content, options)；关闭用 closeCustomDialog(content)
- 关闭后、onDidDisappear 回调里和打开失败的 catch 分支里调 content.dispose()
- 沿用 options.builder 时，把 @Builder 放进发起弹窗的 @ComponentV2，写成 builder: () => { this.xxx() }，由各入口组件自己打开，不能省掉 this 绑定
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- builder 要写成箭头函数 () => { this.XXX() }，XXX 是组件内部 builder；全局 builder 要在组件内部 builder 中调用：CustomDialogOptions.builder 的约束，组件外闭包直接调全局 builder 不满足（出处：js-apis-promptAction.md，CustomDialogOptions）
- openCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options?: promptAction.BaseDialogOptions): Promise<void>：按 ComponentContent 打开弹窗（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
- closeCustomDialog<T extends Object>(dialogContent: ComponentContent<T>): Promise<void>：用打开时的同一个 ComponentContent 关闭（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.closeCustomDialog）
- constructor(uiContext: UIContext, builder: WrappedBuilder<[T]>, args: T)；dispose(): void：全局 builder 只接一个参数对象 T；不用了要立即 dispose（出处：鸿蒙 SDK 的 ets/api/arkui/ComponentContent.d.ts，ComponentContent.constructor、ComponentContent.dispose）
- declare function wrapBuilder<Args extends Object[]>(builder: (...args: Args) => void): WrappedBuilder<Args>：把全局 @Builder 包成 WrappedBuilder 交给 ComponentContent（出处：鸿蒙 SDK 的 ets/component/common.d.ts，wrapBuilder）
- onDidDisappear?: () => void：BaseDialogOptions 里弹窗消失后的回调，在这里 dispose（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，BaseDialogOptions.onDidDisappear）
- updateCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options: promptAction.BaseDialogOptions): Promise<void>：同族接口：按同一个 ComponentContent 更新弹窗选项（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.updateCustomDialog）
- openCustomDialogWithController<T extends Object>(dialogContent: ComponentContent<T>, controller: promptAction.DialogController, options?: promptAction.BaseDialogOptions): Promise<void>：同族接口：带 DialogController 打开（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialogWithController）
未核实：卡里的崩溃和修复在 target 26.0.0（兼容 23）上观察；本机 API 23 的声明里 CustomDialogOptions.builder 没有 this.XXX 的说明，该约束出处取自文档
来源：1 张卡，1 个应用
- case-256a1816e74ef8a6f70d（组件岛Widget Island）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 2
