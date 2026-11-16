# 源字体是 sans-serif-light 时，目标写 .fontWeight(300)，不写 Lighter

审的是：代码
触发（任一种）：
- 读到：TextView 或样式写 android:fontFamily="sans-serif-light"；写错的样子：对应的 Text 写成 .fontWeight(FontWeight.Lighter)
适用范围：源端用 sans-serif-light 这类按字重区分的系统字体族，迁成 ArkUI Text 时
做法：
- 写成 Text(...).fontWeight(300)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- sans-serif-light = Typeface.create(sansSerif, 300, false)：源端 sans-serif-light 是 300 字重（出处：android.graphics.Typeface（系统字体族注册处））
- FontWeight.Lighter 是 100 字重，对应 number 100：Lighter 比 light 细两档（出处：ts-appendix-enums.md，FontWeight）
- fontWeight(value: number | FontWeight | ResourceStr): TextAttribute：Text 的字重可直接写数字（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontWeight）
- fontWeight(value: number | FontWeight | ResourceStr): SpanAttribute：同族接口：Span 的字重（出处：鸿蒙 SDK 的 ets/component/span.d.ts，SpanAttribute.fontWeight）
- fontWeight(value: number | FontWeight | ResourceStr): TextInputAttribute：同族接口：TextInput 的字重（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.fontWeight）
来源：1 张卡，1 个应用
- case-9058ac868b6feb3a04e0（AntennaPod）：做法第 1 步 ← 诊断
