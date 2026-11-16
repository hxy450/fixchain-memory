# 目标弹窗会把焦点自动给输入框时，加 defaultFocus 占位组件，不让弹窗一开就拉起键盘

审的是：代码
触发（任一种）：
- 读到：源端弹窗里有 EditText，打开时不主动 requestFocus；写错的样子：目标弹窗打开后焦点自动落到 TextInput 上，弹窗里没有 .defaultFocus(true) 的占位组件
适用范围：迁移带输入框的弹窗、源端打开时不给输入框焦点时
做法：
- 在弹窗内容里放一个可获焦的占位组件并写 .focusable(true).defaultFocus(true)，让初始焦点落在它上面
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- defaultFocus(value: boolean): T：设为页面创建时的默认焦点组件，传 false 没有效果（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.defaultFocus）
- 加 defaultFocus 占位修正弹窗自动给焦点：修复后弹窗打开时输入框不抢焦点（出处：卡里修好并验证过）
未核实：卡里只写了加 defaultFocus 占位，占位组件的具体写法（focusable、尺寸）是推断
来源：1 张卡，1 个应用
- case-9174c62c22f8d979372e（omni-notes-hmos）：做法第 1 步 ← 建议 2、诊断；取值 2 ← 诊断
