# EditText / Spinner 译成 TextInput / Select 时清掉默认填充底，输入框补下划线

审的是：代码
触发（任一种）：
- 读到：普通 <EditText>（Material 下是下划线、无底色）和 <Spinner>（无底色）；写错的样子：TextInput(…).type(…).fontSize(…) 和 Select(…).font(…) 没写 .backgroundColor(Color.Transparent)
适用范围：没有自定义背景的 EditText、Spinner 迁成 ArkUI TextInput、Select 时
做法：
- TextInput 写 .backgroundColor(Color.Transparent) 并加底部下划线；Select 写 .backgroundColor(Color.Transparent)，.font 的 weight 写 FontWeight.Normal
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- backgroundColor(value: ResourceColor): T：组件背景色（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.backgroundColor）
- showUnderline 只对 InputType.Normal 有效，默认 false：type(Number) 等其他类型的输入框不能靠 showUnderline 画下划线（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.showUnderline）
- font(value: Font): SelectAttribute：Select 下拉按钮本身的文字样式（出处：鸿蒙 SDK 的 ets/component/select.d.ts，SelectAttribute.font）
- 输入框改透明底加底部下划线，Select 改透明底和常规字重：修好后的写法（出处：卡里修好并验证过）
未核实：TextInput、Select 默认填充底按卡里上机看到的写，声明里没查到默认背景色
来源：1 张卡，1 个应用
- case-c40332380c19d002090d（AntennaPod）：做法第 1 步 ← 建议 1、诊断；取值 4 ← 诊断
