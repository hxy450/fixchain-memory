# FontWeight.SemiBold/Light 迁成 600/300，不换成 Medium/Lighter

审的是：代码
触发（任一种）：
- 读到：Compose 源里 fontWeight = FontWeight.SemiBold 或 FontWeight.Light；写错的样子：目标写 .fontWeight(FontWeight.SemiBold) 编译报「Property 'SemiBold' does not exist on type 'typeof FontWeight'」，或被就近替换成 FontWeight.Medium / FontWeight.Lighter
- 读到：规格写字重 SemiBold；或编译报 Property 'SemiBold' does not exist on type 'typeof FontWeight'；写错的样子：目标写 .fontWeight(FontWeight.SemiBold)，或编译修复把它换成 .fontWeight(FontWeight.Medium)
适用范围：源端字重在 ArkUI FontWeight 枚举里没有对应成员时，迁到 Text 等文字组件，含修编译错误和批量替换
做法：
- 写数值字重：SemiBold 写 .fontWeight(600)，Light 写 .fontWeight(300)
- 编译修复替换不存在的枚举成员时按数值语义保持原值，不就近降成 Medium / Lighter；批量替换前确认不改视觉语义
- 修完把字重、颜色等视觉数值与源码对一遍
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fontWeight(value: number | FontWeight | ResourceStr): TextAttribute：Text 的字重可以直接传数值（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontWeight）
- number 类型取值 [100, 900]，间隔 100，默认 400：600、300 都是合法取值（出处：ts-basic-components-text.md，fontWeight；鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontWeight）
- FontWeight 枚举只有 Lighter、Normal、Regular、Medium、Bold、Bolder：没有 SemiBold、Light，只能用数值（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，FontWeight）
- Medium 是 500 字重，Bold 是 700 字重：Medium 比 SemiBold（600）轻一档（出处：ts-appendix-enums.md，FontWeight）
- FontWeight.SemiBold 是 600 字重，改为 fontWeight(600) 后字重与源一致：修好后标题粗细恢复（出处：卡里修好并验证过）
- fontWeight(value: number | FontWeight | ResourceStr): SpanAttribute：同族接口：Span 的字重（出处：鸿蒙 SDK 的 ets/component/span.d.ts，SpanAttribute.fontWeight）
- fontWeight(value: number | FontWeight | ResourceStr): TextInputAttribute：同族接口：TextInput 的字重（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.fontWeight）
- fontWeight(value: number | FontWeight | string): ButtonAttribute：同族接口：Button 的字重（第三种类型是 string）（出处：鸿蒙 SDK 的 ets/component/button.d.ts，ButtonAttribute.fontWeight）
未核实：Compose FontWeight.SemiBold = 600、Light = 300 出自卡，本机没有 Compose 源码
来源：3 张卡，1 个应用
- case-036361d8949e7daf5247（Cofi）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 5 ← 诊断
- case-0848ab137044cb92d1bc（Cofi）：做法第 1 步 ← 建议 7、诊断；做法第 2 步 ← 建议 7
- case-7ced02d9c41ab6f4919a（Cofi）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4；做法第 3 步 ← 建议 4；取值 5 ← 诊断
