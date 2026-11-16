# Material 对话框（含 setView）转居中弹窗，底部面板才转 bindSheet

审的是：代码
触发（任一种）：
- 读到：源码 `new MaterialAlertDialogBuilder(…).setView(…)` 加 `setPositiveButton` / `setNegativeButton` 后 `show()`；页面规格的映射行并列写「bindSheet/CustomDialog」；写错的样子：这个对话框被写成 `bindSheet(…)` 半模态，理由是工程既定模式
适用范围：按源端构造方式选择目标弹层形态时
做法：
- MaterialAlertDialogBuilder（含 setView 输入框、下拉）写成居中模态：getUIContext().getPromptAction().openCustomDialog(content, options)
- BottomSheetDialog 才写 bindSheet(isShow, builder, options)；规格并列两种时按源码择一，不按工程惯例替换
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- openCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options?: promptAction.BaseDialogOptions): Promise<void>：居中模态自定义弹窗（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
- bindSheet(isShow: boolean, builder: CustomBuilder, options?: SheetOptions): T：半模态底部面板，对应 BottomSheetDialog（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindSheet）
- setView 的居中选择对话框由 bindSheet 改为新建的居中 openCustomDialog 弹窗：返修后保留的形态（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-9c819765c4d3d422d7bb（AntennaPod）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3；取值 3 ← 诊断
