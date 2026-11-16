# TextInput 改透明底时显式写 borderRadius(0)、padding、height、caretColor

审的是：代码
触发（任一种）：
- 读到：源 EditText 外观来自主题背景（没写 android:background、padding、高度），layout_height 是 wrap_content；写错的样子：目标 TextInput 设了透明底或只设下边框，却没写 .borderRadius(0)、.padding(...)、.height(...)，边框两端随默认圆角上翘，高度和内边距是 ArkUI 默认值
适用范围：把主题提供外观的 EditText 迁成 TextInput、要去掉 ArkUI 默认填充底时
做法：
- 同时显式覆盖：.borderRadius(0)、.padding({ … }) 取源背景 9-patch 的内容区、.height(…) 按源端 wrap_content 的实际结果（9-patch 内边距 + 文字行高），.caretColor(…) 按主题 textCursorDrawable
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- TextInput 的 padding 默认 { top: 8vp, right: 16vp, bottom: 8vp, left: 16vp }：不覆盖就带着这组内边距（出处：ts-basic-components-textinput.md，属性）
- padding 设为 0 时可把 borderRadius 设为 0，避免光标被截断：官方文档对 padding 与 borderRadius 配合的说明（出处：ts-basic-components-textinput.md，属性）
- borderRadius(value: Length | BorderRadiuses | LocalizedBorderRadiuses): T：覆盖默认圆角（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.borderRadius）
- caretColor(value: ResourceColor): TextInputAttribute：光标颜色（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.caretColor）
- TextInput 默认圆角会让只设 bottom 的边框两端上翘；改成透明、borderRadius(0)、按 9-patch 写 padding 和高度后与源端一致：返修后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 源输入框的实际高度：Android SDK 平台资源里源背景 9-patch 的内容区内边距，加上源 EditText 的字号（布局 XML 或 textAppearance）；上下内边距 + 文字行高即 wrap_content 的高度，dp 写成 vp
来源：1 张卡，1 个应用
- case-0ce95f901f7e409784a3（Blockinger）：做法第 1 步 ← 建议 2、诊断；取值 5 ← 诊断
