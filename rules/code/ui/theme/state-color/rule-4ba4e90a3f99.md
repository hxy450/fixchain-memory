# Text 写了显式 color 和禁用 alpha 时，目标写 fontColor 加按状态的 opacity

审的是：代码
触发（任一种）：
- 读到：Text(color = <颜色>.copy(alpha = if (!enabled) 0.38f else 1f)) 这类写法；写错的样子：目标 fontColor 用了按钮的品牌色，只靠 .enabled() 表示禁用，没有按状态设 opacity
适用范围：把 Compose 里用 color.copy(alpha = …) 表达启用、禁用状态的文字迁成 ArkUI 时
做法：
- 写成 Text(...).fontColor(<源 color 对应的颜色资源>).opacity(enabled ? 1 : 0.38)，alpha 两个值照源端，不换成品牌色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fontColor(value: ResourceColor): TextAttribute：文字颜色，写源端 color 的那个色（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontColor）
- opacity(value: number | Resource): T，取值 0 到 1：源端 alpha 的值照搬，0.38f 写 0.38（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.opacity）
- fontColor(value: ResourceColor): ButtonAttribute：同族接口：Button 的文字颜色（出处：鸿蒙 SDK 的 ets/component/button.d.ts，ButtonAttribute.fontColor）
- fontColor(value: ResourceColor): SpanAttribute：同族接口：Span 的文字颜色（出处：鸿蒙 SDK 的 ets/component/span.d.ts，SpanAttribute.fontColor）
- fontColor 改成源端 color 对应的资源，默认状态下 opacity 0.38：修复后默认状态的文字变淡，与源端一致（出处：卡里修好并验证过）
未核实：卡里记的环境没写鸿蒙 SDK 版本，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-40b9281a2c93eda1c790（Jetsnack）：做法第 1 步 ← 建议 4、诊断；取值 5 ← 诊断
