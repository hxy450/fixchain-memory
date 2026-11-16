# 规格只写「按平台默认」没给数值时，对话框外观从平台资源取，不凭记忆或兄弟页先例填

审的是：代码
触发（任一种）：
- 读到：源端是没有自定义样式的 AlertDialog.Builder；规格的弹窗契约只写「按平台默认」，没有数值；写错的样子：自绘对话框面板写 .width('85%') 加 constraintSize({ maxWidth: 320 })、标题 .fontSize(20)、按钮行 .height(48)、圆角描边框，注释写「先例」或「近似」；或把已写对的平台值（如 22 的标题字号）改成兄弟页的值
适用范围：界面实现阶段在规格没给外观数值、要自绘平台 AlertDialog 面板时
做法：
- 先按源主题读 Android SDK 平台资源取值，或回报规格缺项；不凭记忆、兄弟页先例或 magic-numbers 报告填字号、宽度比例、maxWidth、圆角描边和行高
- 已知的平台值不为「同族一致」改成兄弟页的近似值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- TextAppearance.Holo.DialogWindowTitle：textSize 22sp，textColor @color/holo_blue_light：Theme.Holo 下标题的平台值，不是 20（出处：Android SDK 平台资源 data/res/values/styles_holo.xml，TextAppearance.Holo.DialogWindowTitle（按应用的 compileSdk 取对应平台））
- dialog_min_width_minor = 95%，dialog_min_width_major = 65%：Holo 对话框的宽度规则，不是 85% 加 maxWidth（出处：Android SDK 平台资源 data/res/values/dimens.xml，dialog_min_width_minor、dialog_min_width_major（按应用的 compileSdk 取对应平台））
- Holo 按钮条 53.33dp 带分隔线；面板宽 = 窗口宽 ×（竖 0.95 / 横 0.65）− 32：返修取得的值，按钮行不是 48（出处：卡里修好并验证过）
针对本应用要查的：
- 源主题下平台对话框各项外观：Android SDK 平台资源 data/res/values/themes*.xml 里源主题的 alertDialogTheme、alertDialogStyle，及其指向的 styles*.xml、layout、dimens（按应用的 compileSdk 取对应平台）；读出标题字号颜色、分隔线、消息字号、背景 drawable、最小宽度比例后照写；读不出的回报规格缺项
来源：1 张卡，1 个应用
- case-ed0c3a60e7342aa867b4（Blockinger）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；取值 3 ← 诊断
