# 规格的文字控件转换行写明决定纵向排布的行框，拿不到源字体度量就登记待设备核对

审的是：规格
触发（任一种）：
- 读到：布局里决定行高的 TextView 只有 textAppearance，没写 android:lineHeight 和 android:includeFontPadding；写错的样子：规格的控件转换行只写 textAppearance 与字号，没写文字行框（单行/多行、首末行 font padding），也没有登记待设备核对项
适用范围：规格提取阶段写计分条、列表行、偏好行、对话框标题与正文这类由文字撑高的控件的转换行时
做法：
- 转换行写出文字行框：单行写行框高度（源字体 top..bottom），多行写行距（ascent..descent）和首行上、末行下的 font padding
- 拿不到源字体度量时登记待设备核对项，写明要 dump 的控件，交给实现与验证阶段兑现
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- includeFontPadding：留出字形上下伸出的空间，不严格按字体 ascent/descent（通常为 true）：源 TextView 没写时取默认 true，行框带 font padding（出处：Android SDK 平台资源 data/res/values/attrs.xml，TextView 的 includeFontPadding（按应用的 compileSdk 取对应平台）；android.widget.TextView#setIncludeFontPadding）
- includePad 时首行 above = top、末行 below = bottom：单行行框是 top..bottom；多行只有首末行多出 font padding（出处：android.text.StaticLayout#out）
针对本应用要查的：
- 源 TextView 的字号和默认字体：Android SDK 平台资源 data/res/values/styles_material.xml 里 textAppearance 指向的样式的 textSize（按应用的 compileSdk 和主题），字体没另设时是框架默认 Roboto；写进转换行，作为换算行框的依据
来源：1 张卡，1 个应用
- case-5f8338dca042154176b8（Sokoban）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断
