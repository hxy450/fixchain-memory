# TextInput 设光标宽度和颜色写 caretStyle({width, color})，不写 caretWidth

审的是：代码
触发（任一种）：
- 读到：安卓 EditText 的光标宽度、颜色要在目标端还原（textCursorDrawable 里的 <size android:width> 和颜色，或按所在页面主题取到的光标样子）；写错的样子：TextInput 上写了 .caretWidth(...)（编译报 10505001，TextInputAttribute 上没有这个属性），或者只写了 .caretColor(...) 而宽度没设
适用范围：把安卓输入框的光标外观迁成 ArkUI TextInput 时
做法：
- 宽度和颜色一起写成 .caretStyle({ width: <源端 dp 数值>, color: <颜色> })；width 写 number 时按 vp，源端 dp 数值照搬
- 写之前在 SDK 声明 text_input.d.ts 和 text_common.d.ts 里确认属性名和参数结构，不凭记忆写、不靠编译门兜底
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- caretStyle(value: CaretStyle): TextInputAttribute：TextInput 的光标风格（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.caretStyle）
- interface CaretStyle { width?: Length; color?: ResourceColor }：光标的宽度和颜色两项（出处：鸿蒙 SDK 的 ets/component/text_common.d.ts，CaretStyle）
- CaretStyle.width 默认 '2vp'，不支持百分比；CaretStyle.color 默认 '#ff007dff'：不写时的光标样子（出处：ts-text-common.md，CaretStyle）
- Length 写 number 时默认单位 vp：width: 2 即 2vp，对应源端 2dp（出处：ts-types.md，Length）
- 同时设 caretColor 和 caretStyle 的 color 时，后设置的生效：两处都写时以链上靠后的那个为准（出处：ts-basic-components-textinput.md，caretStyle）
- caretStyle(value: CaretStyle): TextAreaAttribute：同族接口：TextArea 的光标风格（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.caretStyle）
- caretStyle(value: CaretStyle): SearchAttribute：同族接口：Search 的光标风格（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.caretStyle）
未核实：卡里上机所用 SDK 是 API 22（6.0.2），声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-f6c7146888f4d05c7874（企业安全培训）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4
