# MDC / M3 按钮样式的字距和文字色从合并资源解析，字距写进内层 Text.letterSpacing

审的是：代码
触发（任一种）：
- 读到：MaterialButton 的 style 是 Widget.MaterialComponents.Button.TextButton，或继承自 Widget.Material3.Button.OutlinedButton 等 MDC / M3 按钮样式；写错的样子：Button(label) 直接设 fontSize / fontColor，没有 letterSpacing；文字色写的是 colorPrimary 对应的颜色
适用范围：源按钮的字距和前景色来自 MDC / M3 库样式、布局里没显式写时
做法：
- 从合并资源解析该样式 textAppearance 的 android:letterSpacing 和 android:textColor selector 的实际取值，不凭记忆默认取 colorPrimary
- 写成 Button() { Text(label).letterSpacing(<letterSpacing em × 字号>) }，文字色按 selector 里对应状态的颜色写
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- letterSpacing(value: number | ResourceStr): TextAttribute：Text 的字符间距（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.letterSpacing）
- letterSpacing 默认 0，单位 fp：Text 字符间距的默认值和单位（出处：ts-basic-components-text.md，letterSpacing）
- TextButton 改 Button{ Text.letterSpacing(1.25) }；可勾选的 OutlinedButton 文字取 colorOnSurface 对应的颜色：修好后的写法（14sp 的 MDC 按钮字距）（出处：卡里修好并验证过）
- letterSpacing(value: number | ResourceStr): SpanAttribute：同族接口：Span 的字符间距（出处：鸿蒙 SDK 的 ets/component/span.d.ts，SpanAttribute.letterSpacing）
- letterSpacing(value: number | string | Resource): TextInputAttribute：同族接口：TextInput 的字符间距（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.letterSpacing）
针对本应用要查的：
- 按钮文字的 letterSpacing 和字号：依赖库 com.google.android.material:material 包内 res/values/values.xml（按应用依赖的版本）：从控件 style 顺着 android:textAppearance 和 parent 一路找到 android:letterSpacing、android:textSize；letterSpacing 是 em，乘以字号得到 fp 数。例：1.12.0 的 Base.TextAppearance.MaterialComponents.Button 是 0.0892857143、14sp，即 1.25
- 按钮文字色：同一包内：style 的 android:textColor 指向的 res/color/ 下 selector 文件；按控件状态取对应 item 的 ?attr，再到应用主题里解析成颜色。例：1.12.0 的 m3_text_button_foreground_color_selector 里可勾选未选中是 ?attr/colorOnSurface
未核实：卡里没写应用依赖的 material 版本，例子按本机缓存的 1.12.0
来源：1 张卡，1 个应用
- case-c40332380c19d002090d（AntennaPod）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 1、诊断；取值 3 ← 诊断
