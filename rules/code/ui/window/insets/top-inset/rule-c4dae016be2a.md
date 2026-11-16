# 工具栏自带固定 paddingTop 时，用 max(源顶距, 安全区) 替换它，不再另加外层安全区

审的是：代码
触发（任一种）：
- 读到：根布局没有 android:fitsSystemWindows，工具栏 FrameLayout 固定 layout_height（如 80dp）并自带 android:paddingTop（如 40dp）给状态栏留白，正文 layout_marginTop 等于工具栏高度；写错的样子：外层 Column 写 .padding({ top: <顶部安全区值> })，同时标题 Row 保留 .height(<源高度>) 和源 paddingTop，两次避让叠加
适用范围：Android 全屏页由工具栏自身的固定顶部留白承担状态栏避让、迁成 ArkUI 标题栏时
做法：
- 顶距写成 titleTop = Math.max(<源 paddingTop vp>, <顶部安全区值>)；标题 Row .padding({ top: titleTop }).height(<源高度> − <源 paddingTop> + titleTop)；外层不再加安全区
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- titleTopPadding = max(源 paddingTop, topInset)，titleHeight = 源高度 − 源 paddingTop + titleTopPadding，删掉外层安全区 padding：修好的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 源工具栏的高度和顶部留白：源工程布局 XML 里工具栏容器的 android:layout_height、android:paddingTop，以及正文的 android:layout_marginTop；dp 数值照搬成 vp 代入上面的 max 和高度公式
来源：1 张卡，1 个应用
- case-7b7a48249f269a40a194（掌上燃气管家）：做法第 1 步 ← 建议 1、诊断；取值 1 ← 诊断
