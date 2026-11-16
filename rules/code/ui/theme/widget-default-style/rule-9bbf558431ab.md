# 用一个 Text 代替带自动字号的按钮子类时，按契约显式算出 fontSize，补内边距和 Medium 字重

审的是：代码
触发（任一种）：
- 读到：源控件 extends AppCompatButton / Button，构造里 setAutoSizeTextTypeUniformWithConfiguration(min, max, step, TypedValue.COMPLEX_UNIT_SP)；写错的样子：目标是一个宽高等于整块的 Text，挂 .maxLines(1).minFontSize(…).maxFontSize(…) 就当等价，没有 .padding，也没有 .fontWeight
适用范围：把带自动字号的安卓按钮子类迁成单个 ArkUI Text 时
做法：
- 不把 minFontSize/maxFontSize 挂在整块上当等价（ArkUI 在整块内按 HarmonyOS Sans 度量自适应）；按契约在 px 域算字号：取区间内满足 行高×字号 ≤ 可用高、位数×数字步进×字号 ≤ 可用宽 的最大 fp，写成固定的 .fontSize(…)
- 补上与源端一致的内边距（.padding({ top, bottom, left, right })）和字重：Button → .fontWeight(FontWeight.Medium)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 按内边距、按钮字体行高和数字步进在 px 域算出 1..max sp 内的字号，固定 fontSize，加 FontWeight.Medium：修好后的写法；两端同一盘面上数字的字形高与块边之比对齐（出处：卡里修好并验证过）
- minFontSize 要和 maxFontSize、maxLines 或布局约束一起用才生效；自适应时 fontSize 不生效；单位 fp：ArkUI 的自适应在组件自身尺寸内进行，和源端「尺寸减内边距、按按钮字体」不是一回事（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.minFontSize）
- fontWeight(value: number | FontWeight | ResourceStr): TextAttribute：Text 的字重（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontWeight）
- FontWeight.Medium：中等字重，对应安卓 sans-serif-medium（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，FontWeight.Medium）
- fontWeight(value: number | FontWeight | string): ButtonAttribute：同族接口：Button 的字重（出处：鸿蒙 SDK 的 ets/component/button.d.ts，ButtonAttribute.fontWeight）
- fontWeight(value: number | FontWeight | ResourceStr): SpanAttribute：同族接口：Span 的字重（出处：鸿蒙 SDK 的 ets/component/span.d.ts，SpanAttribute.fontWeight）
针对本应用要查的：
- 源按钮的实际内边距和字体：规格里已写的自动字号契约；没写的，查源工程主题里的 buttonStyle，顺着 parent 找提供 background / padding / textAppearance 的那一项；内边距换成 vp 写进 .padding；字体是 sans-serif-medium 的写 FontWeight.Medium；推不出的按规格的实测方法取值
来源：1 张卡，1 个应用
- case-314b7ba3e75b6d6b3a9d（Privacy Friendly 2048）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 1 ← 诊断
