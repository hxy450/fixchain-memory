# BasicTextField 没传 textStyle 时，TextInput 写 14 号黑色字

审的是：代码
触发（任一种）：
- 读到：foundation 的 `BasicTextField(value, onValueChange, modifier)` 没传 `textStyle`；写错的样子：对应 `TextInput` 按 M3 `bodyLarge`（16）写字号或用宿主内容色，或者没写 `fontSize`
适用范围：把 Compose foundation 的 BasicTextField 迁成 ArkUI TextInput 时（M3 的 TextField 不在此列）
做法：
- 写 `TextInput(...).fontSize(14).fontColor(Color.Black)`，字体用系统字体；M3 的 bodyLarge 只用于 M3 TextField/Text
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fontSize(value: Length): TextInputAttribute：TextInput 字号，number 按 fp（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.fontSize）
- TextInput 字体默认大小 16fp：不写 fontSize 时比源端默认的 14 大（出处：ts-basic-components-textinput.md，fontSize）
- fontColor(value: ResourceColor): TextInputAttribute：TextInput 字色（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.fontColor）
- BasicTextField 不传 textStyle 时用 TextStyle.Default：14sp、黑色、系统字体，不读 M3 的 LocalTextStyle：源端的实际样式（出处：卡里修好并验证过）
- fontSize(value: Length): TextAreaAttribute：同族接口：TextArea 的字号（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.fontSize）
来源：1 张卡，1 个应用
- case-d54a9506e30031090325（Jetsnack）：做法第 1 步 ← 建议 4、诊断；取值 4 ← 诊断
