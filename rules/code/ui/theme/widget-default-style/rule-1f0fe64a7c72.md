# TextView 只写 textAppearance 没写 textColor 时，字号和文字色一起展开

审的是：代码
触发（任一种）：
- 读到：TextView 写了 android:textAppearance="?android:attr/textAppearanceMedium"（或 Small / Large），没写 android:textColor；写错的样子：目标 Text 只按样式展开了 .fontSize(…)，.fontColor(…) 写成主文字色令牌或没写
适用范围：源 TextView 的文字色来自 textAppearance 样式（自身没写 textColor），迁成 ArkUI Text 时
做法：
- 按应用主题解析 textAppearance 指向的样式，同时读出 textSize 和 textColor，分别写成 .fontSize(…) 和 .fontColor(…)
- AppCompat 主题下 Medium 是 18sp 加 ?android:attr/textColorSecondary：写 .fontSize(18) 和次级文字色令牌的 .fontColor(…)，不默认用主文字色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- android:textAppearanceMedium → @style/TextAppearance.AppCompat.Medium：AppCompat 主题给平台属性 textAppearanceMedium 的取值（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.V7.Theme.AppCompat 的 android:textAppearanceMedium（按应用依赖的版本））
- Base.TextAppearance.AppCompat.Medium：android:textSize = @dimen/abc_text_size_medium_material（18sp），android:textColor = ?android:attr/textColorSecondary：AppCompat Medium 的字号和文字色（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.TextAppearance.AppCompat.Medium（按应用依赖的版本））
- TextAppearance.Material.Medium：textSize = @dimen/text_size_medium_material（18sp），textColor = ?attr/textColorSecondary：平台 Theme.Material 下 textAppearanceMedium 指向的样式（出处：Android SDK 平台资源 data/res/values/styles_material.xml，TextAppearance.Material.Medium（按应用的 compileSdk 取对应平台））
- TextAppearance.Medium 只写 textSize 18sp，文字色继承 TextAppearance 的 ?textColorPrimary：平台老 Theme 下 textAppearanceMedium 指向的样式，文字色和 Material / AppCompat 不同（出处：Android SDK 平台资源 data/res/values/styles.xml，TextAppearance.Medium、TextAppearance（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 应用主题下 textAppearance 指向的样式和 textColorSecondary 的具体色：源工程 AndroidManifest 的 android:theme 和 res/values 下的主题，顺着 parent 找到 AppCompat 或平台主题；AppCompat 在 androidx.appcompat:appcompat 包内 res/values/values.xml，平台在 Android SDK 平台资源 data/res/values/themes_material.xml；读主题里 android:textAppearanceMedium（Small / Large 同理）的样式，再读该样式的 textSize、textColor；textColor 是 ?android:attr/textColorSecondary 时再从主题读它的颜色。例：AppCompat 深色主题下是 @color/abc_secondary_text_material_dark
未核实：卡里没记 appcompat 版本，核实用的是 appcompat 1.7.1
来源：1 张卡，1 个应用
- case-29fdf1fe3faadb5933b9（MifareClassicTool）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4、诊断
