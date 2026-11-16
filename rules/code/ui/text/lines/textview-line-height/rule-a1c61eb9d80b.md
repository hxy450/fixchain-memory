# 未声明行高的单行 TextView 撑起行高时，Text 按源字体 top..bottom 写 lineHeight

审的是：代码
触发（任一种）：
- 读到：TextView 只有 textAppearance 或 textSize，没写 android:lineHeight，也没写 android:includeFontPadding="false"，高度是 wrap_content，它的文字撑起所在行或容器的高度；写错的样子：对应的 Text 只写 fontSize/fontColor/padding，没有 .lineHeight(...)，或用 .margin 凑行间距
适用范围：源 TextView 取默认 includeFontPadding、字体是框架默认 Roboto，单行文字决定计分条、列表行、偏好行、对话框标题这类纵向尺寸时
做法：
- 单行文字写 Text(...).lineHeight(<源字体在该字号下 bottom − top 的 px> / <设备密度>)，即源 TextView 单行行框的高度；不依赖 ArkUI Text 的自然行高
- 不用 .margin 凑行间距：源布局里两个 TextView 之间没有间距的（如 layout_below 紧贴），目标也不加
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- includeFontPadding 默认是 true：源 TextView 没写这个属性时，首行上方、末行下方都带 font padding（出处：android.widget.TextView#setIncludeFontPadding）
- includePad 时首行 above = top、末行 below = bottom：单行 TextView 的行框是字体的 top..bottom，不是 ascent..descent（出处：android.text.StaticLayout#out）
- lineHeight(value: number | string | Resource): TextAttribute；number 的单位是 fp，≤ 0 时不限行高：固定 Text 的行高；按 px/密度 换算出的数在系统字体缩放为 1 时与 vp 等值（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.lineHeight）
- 不设 lineHeight 时鸿蒙按自身字体自然行高排：18fp 约 21.1vp（安卓 24.4dp），16fp 约 18.9vp（安卓单行 21.45dp）；按 Roboto 行盒反算写 lineHeight 后与安卓一致：两边行框差 2–3vp，列表行、偏好行因此变矮、第二行上移（出处：卡里修好并验证过）
- lineHeight(value: Length): SpanAttribute：同族接口：Span 的行高（出处：鸿蒙 SDK 的 ets/component/span.d.ts，SpanAttribute.lineHeight）
- lineHeight(value: number | string | Resource): TextInputAttribute：同族接口：TextInput 的行高（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.lineHeight）
- lineHeight(value: number | string | Resource): TextAreaAttribute：同族接口：TextArea 的行高（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.lineHeight）
针对本应用要查的：
- 源 TextView 的字号：Android SDK 平台资源 data/res/values/styles_material.xml 里 textAppearance 指向的 TextAppearance.Material.* 的 textSize，再到 dimens_material.xml 取值（按应用的 compileSdk 和主题）；例：textAppearanceMedium 在 Material 主题下是 TextAppearance.Material.Medium，textSize 为 @dimen/text_size_medium_material = 18sp
- 源字体在该字号下单行行框的 px（bottom − top）：真机上 dump 源 TextView 的高度，或用源默认字体（Roboto）的度量按 Paint.getFontMetrics 换算；本机 SDK 平台目录里没有字体文件；取 bottom − top 的 px 除以设备密度写进 lineHeight；例：密度 2.75 的设备上 Roboto 18sp 单行是 67px，写 lineHeight(67 / 2.75)。拿不到时登记待设备核对项
未核实：lineHeight 传 number 按 fp 解释，系统字体缩放不为 1 时和按 vp 换算的值不同；卡里只在默认字体大小下验证
来源：1 张卡，1 个应用
- case-5f8338dca042154176b8（Sokoban）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 4 ← 诊断
