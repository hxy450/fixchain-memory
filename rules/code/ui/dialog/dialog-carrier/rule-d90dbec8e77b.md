# BottomSheetDialogFragment 迁成弹层，不写成标准 NavDestination 加自绘蒙层

审的是：代码
触发（任一种）：
- 读到：源类继承 BottomSheetDialogFragment / DialogFragment，在宿主上 show(manager, tag, …) 弹出、选中后回调并 dismiss()；规格 page_type 为 modal_overlay 或 dialog；写错的样子：目标写成没有 .mode(NavDestinationMode.DIALOG) 的 NavDestination 路由页，页内自绘半透明蒙层和底板，关闭用 navPathStack.pop()，对外只暴露路由 Builder 和路由参数
适用范围：页面转换阶段为安卓底部弹窗、对话框类 Fragment 选 ArkUI 承载容器和打开、关闭方式时；目标工程统一用 Navigation 路由时同样适用
做法：
- 先定承载方式：this.getUIContext().getPromptAction().openCustomDialog(…) 或 bindSheet，或 NavDestination 显式设 .mode(NavDestinationMode.DIALOG)；不用标准 NavDestination 加自绘蒙层模拟
- 打开关闭链照源端：宿主页保持可见；选中后回调并只关闭自己（closeCustomDialog(dialogId)，dialogId 是 openCustomDialog 返回的）；取消时保留原值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- openCustomDialog(options: promptAction.CustomDialogOptions): Promise<number>：在当前页打开自定义弹窗，返回给 closeCustomDialog 用的 dialogId（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
- closeCustomDialog(dialogId: number): void：按 id 只关闭这一个弹窗（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.closeCustomDialog）
- mode(value: NavDestinationMode): NavDestinationAttribute；NavDestinationMode.STANDARD = 0（默认），DIALOG = 1：DIALOG 模式默认透明，入栈出栈不影响下层页面的生命周期；不设就是标准页（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.mode、NavDestinationMode）
- bindSheet(isShow: boolean, builder: CustomBuilder, options?: SheetOptions): T：绑在宿主组件上的半模态底板（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindSheet）
- 弹层正文去掉 NavDestination，新增一个以 UIContext 和参数调用 openCustomDialog 的打开函数；选中后回填并只关闭自己的弹窗 id，取消保留原文：修复后宿主页可见、关闭只关弹层的写法（出处：卡里修好并验证过）
- function openCustomDialog(options: CustomDialogOptions): Promise<number>：同族接口：@ohos.promptAction 模块级的同名函数（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，promptAction.openCustomDialog）
未核实：卡里的行为出自 target_sdk 26.0.0，本机按 API 23 的声明核对
来源：1 张卡，1 个应用
- case-5a041592364ebe85240c（组件岛Widget Island）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2、诊断；取值 5 ← 诊断
