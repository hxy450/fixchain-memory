# Compose 的输入框和开关控件

agent 会看到什么：读到 Compose 的 TextField / OutlinedTextField / BasicTextField(value, onValueChange) 或 Switch(checked, onCheckedChange)；产物里对应的 TextInput、Toggle 及其 onChange、$$ 绑定和样式

## 规矩

- rule-2f3af7d1c436｜onValueChange 按长度条件写回时，目标用 TextInput.maxLength(N)｜读到：Compose 受控输入框 OutlinedTextField / TextField(value = 状态, onValueChange = { if (it.length <= N) 状态 = it })；写错：TextInput({ text: this.x }).onChange((v) => { if (v.length <= N) this.x = v })，没有 .maxLength(N)
- rule-c8587a40fa36｜Compose 受控输入丢弃非法输入时，TextInput 用 onWillChange 返回 false 拦截｜读到：源端 OutlinedTextField(value, onValueChange = { if (!合法) return@OutlinedTextField … })，非法输入不调用 onValueChange；写错：目标写 TextInput({ text: value }).onChange(...)，拒绝时回调旧值、指望父值不变就回退，被拒字符留在框里
- rule-d7f1af6083a3｜BasicTextField 没传 textStyle 时，TextInput 写 14 号黑色字｜读到：foundation 的 `BasicTextField(value, onValueChange, modifier)` 没传 `textStyle`；写错：对应 `TextInput` 按 M3 `bodyLarge`（16）写字号或用宿主内容色，或者没写 `fontSize`
- rule-1039d756d635｜源端字段是只读框加弹窗选择回填时，目标也做选择流程，不退化成并列的自由输入框｜读到：源端表单字段是 onValueChange = {} 的只读 OutlinedTextField，上面盖一层透明可点击层打开选择弹窗，选中结果拆成几段后经一个回调一次性回填（如省、市、区）；写错：目标写成几个并列的 TextInput({ text: $$…, placeholder: … }) 自由输入框，没有选择器，也没有多级联动
- rule-bbb5f30b7f70｜模型是未加 @ObservedV2/@Trace 的普通 DTO 时，开关和输入框用 onChange 写回｜读到：源端 Switch(checked = …, onCheckedChange = …) 经回调写回状态；写错：目标写成 Toggle({ type: ToggleType.Switch, isOn: $$this.model.field })，model 是没加 @ObservedV2 / @Trace 的普通 DTO
- rule-847c53c46935｜源 Switch 有 thumbContent 勾选图标时，不用原生 Toggle 了事，用工程图标资源自绘｜读到：源端 material3 Switch 写 thumbContent = { if (checked) Icon(Icons.Rounded.Check) }；写错：目标只写 Toggle({ type: ToggleType.Switch }) 加颜色，注释里假定原生开关选中时会显示勾选图标
- rule-3ebc4956ec47｜源受控值是 TextFieldValue（文本加选区）时，回写文本后用 setTextSelection 落选区｜读到：Compose 输入组件的受控值是 TextFieldValue，格式键算出新文本和新选区后以 TextFieldValue(新文本, 新选区) 交给 onValueChange；写错：ArkTS 只回写了文本，新选区存在组件内的 @Local 变量里；TextAreaController 声明了却没有任何 setTextSelection 调用
- rule-00b266ffa9af｜规格写开关色取主题令牌时，Toggle 用 selectedColor 和 switchStyle 配 M3 色｜读到：规格写 Slider / Switch / SegmentedButton 的颜色取主题对象的 M3 令牌；写错：Toggle({ type: ToggleType.Switch }) 没设颜色（显示系统蓝）；或写了 Toggle 上不存在的 .trackColor(...)，删掉后关闭态落回默认色
