# 源 AlertDialog 带 icon 时不用没有图标槽的 showAlertDialog，用自定义对话框保留图标

审的是：代码
触发（任一种）：
- 读到：Material3 `AlertDialog(icon = { Icon(painterResource(…)) }, …)`；写错的样子：目标改用 getUIContext().showAlertDialog(…)，图标被省略，注释或思考写「视觉降级」「与兄弟页同模式」
适用范围：把带图标槽的 Compose AlertDialog 迁成 ArkUI 对话框时
做法：
- 改用自定义对话框组件（@CustomDialog 或 openCustomDialog 承载的内容组件），保留图标、标题、正文和按钮布局
- 确需降级时先查决策台账，未命中就报 decision gap，不以「与兄弟页同模式」为由省略
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- showAlertDialog(options: AlertDialogParamWithConfirm | AlertDialogParamWithButtons | AlertDialogParamWithOptions): void：系统警告弹窗接口（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.showAlertDialog）
- AlertDialogParam 的字段有 title、subtitle、message、autoCancel、alignment 等，没有图标字段：showAlertDialog 放不下源端的 icon 槽（出处：鸿蒙 SDK 的 ets/component/alert_dialog.d.ts，AlertDialogParam）
- 三个对话框改用带图标的自定义对话框组件后与源端一致：卡里的修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-3b8b620c1c7fa2848a34（Cofi）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 3 ← 诊断
