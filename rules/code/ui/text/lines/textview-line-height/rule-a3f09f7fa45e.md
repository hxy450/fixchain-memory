# 未声明行高的多行 TextView，行距取 ascent..descent，首末行差额补 padding

审的是：代码
触发（任一种）：
- 读到：多行正文 TextView（如对话框的 message）只有 textAppearance，没写 android:lineHeight，也没写 android:includeFontPadding；写错的样子：对应的 Text 没有 .lineHeight(...)；或者每行都按单行行框 top..bottom 设了 lineHeight；或者首行上方、末行下方没补 font padding
适用范围：源多行 TextView 取默认 includeFontPadding、字体是框架默认 Roboto，正文的总高决定对话框或容器高度时
做法：
- 行距写 Text(...).lineHeight(<源字体 descent − ascent 的 px> / <设备密度>)，不逐行套单行行框
- 首行上方补 .padding({ top: (<ascent − top 的 px>) / <密度> })，末行下方补 .padding({ bottom: (<bottom − descent 的 px>) / <密度> })；不用 margin
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- includePad 只作用在首行（above = top）和末行（below = bottom），中间各行按 ascent..descent：多行文本只有首末行多出 font padding（出处：android.text.StaticLayout#out）
- FontMetrics：top / bottom 是该字号下最高、最低字形离基线的最大距离；ascent / descent 是单倍行距推荐的上下距离：行距用 ascent..descent，首末行差额用 (ascent − top)、(bottom − descent)（出处：android.graphics.Paint.FontMetrics）
- lineHeight(value: number | string | Resource): TextAttribute；number 的单位是 fp：固定行距（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.lineHeight）
- padding(value: Padding | Length | LocalizedPadding): T：首末行的 font padding 差额放在 padding 的 top、bottom（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding）
- 对话框正文固定行距并在首末行补 font padding 差额后与安卓一致：多行正文的落法（出处：卡里修好并验证过）
针对本应用要查的：
- 源字体在该字号下的 top、ascent、descent、bottom（px）：真机上 dump 源正文 TextView 的行距和首末行位置，或用源默认字体（Roboto）的度量按 Paint.getFontMetrics 换算；本机 SDK 平台目录里没有字体文件；行距 = descent − ascent，首行上差额 = ascent − top，末行下差额 = bottom − descent，都除以设备密度；例：密度 2.75 的设备上 Roboto 16sp 行距 52px、首行上 +6px、末行下 +1px
未核实：lineHeight 传 number 按 fp 解释，系统字体缩放不为 1 时和按 vp 换算的值不同；卡里只在默认字体大小下验证
来源：1 张卡，1 个应用
- case-5f8338dca042154176b8（Sokoban）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 5 ← 诊断
