# onValueChange 按长度条件写回时，目标用 TextInput.maxLength(N)

审的是：代码
触发（任一种）：
- 读到：Compose 受控输入框 OutlinedTextField / TextField(value = 状态, onValueChange = { if (it.length <= N) 状态 = it })；写错的样子：TextInput({ text: this.x }).onChange((v) => { if (v.length <= N) this.x = v })，没有 .maxLength(N)
适用范围：把 Compose 受控输入框在 onValueChange 里的拒绝条件迁成 ArkUI TextInput 时
做法：
- 长度上限写成 TextInput(...).maxLength(N)，N 取源码条件里的值；onChange 只负责同步状态
- 逐条列出源码 onValueChange 里的拒绝条件，每条在 ArkUI 侧都要有能阻止输入显示的属性：长度用 maxLength，字符集可用 inputFilter；不能只让状态不更新
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- maxLength(value: number): TextInputAttribute：最大输入长度；不设或无效时默认 Infinity（不限），小数取整数部分（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.maxLength）
- inputFilter(value: ResourceStr, error?: Callback<string>): TextInputAttribute：只显示符合正则的输入，正则按单个字符匹配；@since 18 的签名（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.inputFilter）
- maxLength(value: number): TextAreaAttribute：同族接口：TextArea 的最大长度（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.maxLength）
- maxLength(value: number): SearchAttribute：同族接口：Search 的最大长度（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.maxLength）
- 在 TextInput 上追加 .maxLength(N)、保留原 onChange；设备上输入到 N 再追加字符，文本仍为 N 个字符：修好并上机验证的写法（出处：卡里修好并验证过）
未核实：inputFilter 用于字符集约束卡里没上机验证；卡里没记鸿蒙 SDK 版本，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-e3cd92963aa40d922fdc（听音练习）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 5 ← 诊断
