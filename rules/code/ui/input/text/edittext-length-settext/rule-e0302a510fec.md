# 源端先载入文本再注册 TextWatcher 时，目标 onChange 把与已载入文本相同的回调视为回显

审的是：代码
触发（任一种）：
- 读到：源端先 setText 载入已有文本，之后才 addTextChangedListener(TextWatcher)，载入不算修改；写错的样子：目标 TextArea 的 onChange 无条件把变化计为修改，状态回写触发的 onChange 也标成已修改
适用范围：源端用「先载入、后监听」区分载入和用户修改，目标用 onChange 标记修改状态时
做法：
- onChange((value: string) => { if (value === 已载入的文本) { return; } 标记已修改 })，状态回写引起的回调按回显忽略
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onChange(callback: EditableTextOnChangeCallback): TextAreaAttribute：TextArea 的文本变化回调（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.onChange）
- 加入「text 与已载入文本相同视为回显」的守卫后，未改动不再被计为修改：卡里的修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-4a5592fd88f74b1c16a4（MifareClassicTool）：做法第 1 步 ← 诊断；取值 2 ← 诊断
