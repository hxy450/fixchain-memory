# 弹窗按钮只照源码设了文案的 positive / negative / neutral 渲染，不补 Cancel

审的是：代码
触发（任一种）：
- 读到：MaterialDialog.Builder 只调了 positiveText(...)，或 MaterialAlertDialogBuilder 只 setPositiveButton(...)、没有 setNegativeButton(...)；写错的样子：目标弹窗的按钮行多出源码没有的取消 Button / Text 按钮
适用范围：把源端对话框迁成目标弹窗、落实按钮集合时
做法：
- 按钮只按源码里设了文案的 positiveText / negativeText / neutralText（或 setPositiveButton / setNegativeButton / setNeutralButton）渲染，没设的不出现
- 工程里已有按空文案不渲染按钮的共享弹窗组件时复用它，不手写 Stack overlay
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- AlertDialog 的按钮文案为空时该按钮 setVisibility(View.GONE)：源端没设文案的按钮不显示（出处：com.android.internal.app.AlertController#setupButtons）
未核实：material-dialogs 和 MaterialAlertDialogBuilder 自己的按钮渲染逻辑本机只有编译产物，按卡和平台 AlertController 写
来源：1 张卡，1 个应用
- case-ac1b65b76f72e7be3fa6（omni-notes-hmos）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3
