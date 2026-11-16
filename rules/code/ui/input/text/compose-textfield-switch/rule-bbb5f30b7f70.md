# 模型是未加 @ObservedV2/@Trace 的普通 DTO 时，开关和输入框用 onChange 写回

审的是：代码
触发（任一种）：
- 读到：源端 Switch(checked = …, onCheckedChange = …) 经回调写回状态；写错的样子：目标写成 Toggle({ type: ToggleType.Switch, isOn: $$this.model.field })，model 是没加 @ObservedV2 / @Trace 的普通 DTO
- 读到：源端 TextField(value = …, onValueChange = …) 经回调写回状态；写错的样子：目标写成 TextInput({ text: $$this.model.field })，model 是没加装饰器的普通 DTO
适用范围：表单里开关、输入框的值要进保存请求，而模型是普通类（未加装饰器）时
做法：
- 开关写成 Toggle({ type: ToggleType.Switch, isOn: this.model.field }).onChange((isOn: boolean) => { this.model.field = isOn })；输入框写成 TextInput({ text: this.model.field }).onChange((value: string) => { this.model.field = value })
- 或者把模型改成可观察类（@ObservedV2 加 @Trace）后再绑定
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onChange(callback: (isOn: boolean) => void): ToggleAttribute：Toggle 状态变化回调，在这里写回模型（出处：鸿蒙 SDK 的 ets/component/toggle.d.ts，ToggleAttribute.onChange）
- onChange(callback: EditableTextOnChangeCallback): TextInputAttribute；EditableTextOnChangeCallback = (value: string, previewText?: PreviewText, options?: TextChangeOptions) => void：TextInput 的内容变化回调（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.onChange；ets/component/text_common.d.ts，EditableTextOnChangeCallback）
- $$ 支持基础类型变量；变量由 @State、@Link、@Local 等装饰时，值变化才触发 UI 刷新：$$ 绑定普通 DTO 的嵌套字段不在文档说的支持范围里（出处：arkts-two-way-sync.md，使用规则）
- Toggle 改为 isOn 加 onChange 显式写回后保留至今：卡里的修复写法（出处：卡里修好并验证过）
- onChange(callback: EditableTextOnChangeCallback): TextAreaAttribute：同族接口：TextArea 的内容变化回调（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.onChange）
- onChange(callback: EditableTextOnChangeCallback): SearchAttribute：同族接口：Search 的内容变化回调（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.onChange）
未核实：$$ 绑定未观察 DTO 的嵌套字段时运行中是否真的没写回，卡里没有日志或抓包，以修复者的判断为准
来源：1 张卡，1 个应用
- case-03947f1730e7f74c490f（青商城）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
