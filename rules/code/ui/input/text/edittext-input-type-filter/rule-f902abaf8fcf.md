# 源端输入按小数解析时，TextInput 不用 InputType.Number，改 Normal 加 onChange

审的是：代码
触发（任一种）：
- 读到：源端 EditText 没写数字类的 android:inputType（只有 android:maxLength 等），读输入的代码用 toDoubleOrNull() 解析；写错的样子：目标 TextInput 写成 .type(InputType.Number)，输入框打不出小数点
适用范围：源端输入框允许小数（按 toDoubleOrNull 解析）、迁成 ArkUI TextInput 时
做法：
- 写成 TextInput({ text: 草稿 }).type(InputType.Normal).onChange((value: string) => { … })：在 onChange 里只留数字和第一个小数点，小数位截到源端允许的位数，再写回草稿
- 源端 android:maxLength 的值写成 .maxLength(同值)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- InputType.Number：纯数字输入模式，不支持负数、小数：用它时小数点键入不进去（出处：ts-basic-components-textinput.md，InputType枚举说明；鸿蒙 SDK 的 ets/component/text_input.d.ts，InputType.Number）
- type(value: InputType): TextInputAttribute，默认 InputType.Normal：TextInput 的输入类型（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.type）
- onChange(callback: EditableTextOnChangeCallback): TextInputAttribute；EditableTextOnChangeCallback = (value: string, previewText?: PreviewText, options?: TextChangeOptions) => void：在回调里拿到 value 做规范化（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.onChange；ets/component/text_common.d.ts，EditableTextOnChangeCallback）
- maxLength(value: number): TextInputAttribute：对应源端 android:maxLength（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.maxLength）
- InputType.Normal 加 onChange 限定一个小数点、最多两位小数后，小数能正常输入：卡里的修法；只把输入值规范化而保留 Number 类型时问题仍在（出处：卡里修好并验证过）
- type(value: TextAreaType): TextAreaAttribute；TextAreaType.NUMBER = 2 也是纯数字输入：同族接口：TextArea 的输入类型（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.type、TextAreaType.NUMBER）
- type(value: SearchType): SearchAttribute，默认 SearchType.Normal：同族接口：Search 的输入类型（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.type）
针对本应用要查的：
- 源端允许的字符、长度和小数位：源工程里这个输入框所在布局 XML 的 EditText（android:inputType、android:maxLength），以及读取输入的那段代码；解析用 toDoubleOrNull 且 inputType 没限定为整数的，按允许小数处理；maxLength 照搬；小数位按源端保存或格式化时保留的位数定
未核实：卡里判断 Number 吞小数点的依据是用户反馈；本机声明只写 Pure digital input mode，「不支持负数、小数」出自文档副本
来源：1 张卡，1 个应用
- case-0d37e50dbb1a2e0a9bee（android-train-ticket-vest7）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 5 ← 诊断
