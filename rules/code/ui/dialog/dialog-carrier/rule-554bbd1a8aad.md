# 源端对话框不做成页内 Stack overlay，用 openCustomDialog 等独立弹窗

审的是：代码
触发（任一种）：
- 读到：源码用 MaterialDialog.Builder、MaterialAlertDialogBuilder 或 AlertDialog.Builder 弹出对话框；写错的样子：目标在页面 build 里用 Stack + 全屏遮罩 Column + 白卡、按 visible 状态显示弹窗组件，没有 openCustomDialog / CustomDialogController，返回键不能先关弹窗
适用范围：把源端对话框迁成目标弹窗、选容器时
做法：
- 写成独立弹窗：this.getUIContext().getPromptAction().openCustomDialog(content, options)，或 CustomDialogController({ builder, autoCancel, maskColor })；返回键先关弹窗
- 派工提示里对某个弹窗的形制结论只用于它点名的那个弹窗，同页其他弹窗按各自源码判断
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- openCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options?: promptAction.BaseDialogOptions): Promise<void>：UIContext 的 PromptAction 打开自定义弹窗（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
- openCustomDialog(options: promptAction.CustomDialogOptions): Promise<number>：同族接口：用 builder 选项打开，返回 dialogId（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
- openCustomDialogWithController<T extends Object>(dialogContent: ComponentContent<T>, controller: promptAction.DialogController, options?: promptAction.BaseDialogOptions): Promise<void>：同族接口：带控制器打开（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialogWithController）
- constructor(value: CustomDialogControllerOptions)：CustomDialogController 的构造（出处：鸿蒙 SDK 的 ets/component/custom_dialog_controller.d.ts，CustomDialogController.constructor）
- 按下返回键和 ESC 键时弹窗退出：独立弹窗自带返回键先关弹窗，页内 Stack overlay 没有（出处：ts-methods-custom-dialog-box.md，CustomDialogControllerOptions 的说明）
- 改成 openCustomDialog + 共享弹窗组件、独立窗口语义、按源按钮集合：修好后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-ac1b65b76f72e7be3fa6（omni-notes-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 6 ← 诊断
