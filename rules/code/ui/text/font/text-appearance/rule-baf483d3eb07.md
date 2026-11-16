# 源 TextView 没写 textSize/textColor 时，按默认样式链和主题推导后显式写到 Text

审的是：代码
触发（任一种）：
- 读到：布局里 TextView 没声明 android:textSize / android:textColor（颜色可能只由 Span 给出局部）；写错的样子：对应 Text 沿用旧实现或相邻组件的 fontSize(16)、fontColor 数值，或不写而落到 ArkUI 默认 16fp
适用范围：迁移未声明字号、颜色的安卓 TextView 时
做法：
- 字号按 TextView 默认样式链取：textViewStyle → Widget.TextView 的 textAppearance=?attr/textAppearanceSmall → 主题里 TextAppearance.*.Small 的 textSize（平台 Material 和 AppCompat 都是 14sp），写成 .fontSize(14)
- 颜色按 Activity 实际主题沿同一条链解析到 textColor 指向的主题属性和颜色值，写成显式 fontColor；不沿用旧实现或相邻组件的数值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- TextView(Context, AttributeSet) 的默认样式属性是 textViewStyle：未声明的外观从主题的 textViewStyle 开始找（出处：android.widget.TextView#TextView(Context, AttributeSet)）
- Widget.TextView：textAppearance = ?attr/textAppearanceSmall：默认样式把外观交给主题的 textAppearanceSmall（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.TextView（按应用的 compileSdk 取对应平台））
- TextAppearance.Material.Small：textSize = @dimen/text_size_small_material（14sp），textColor = ?attr/textColorTertiary：Material 系主题下默认字号和颜色属性（出处：Android SDK 平台资源 data/res/values/styles_material.xml，TextAppearance.Material.Small；data/res/values/dimens_material.xml，text_size_small_material（按应用的 compileSdk 取对应平台））
- Theme.Material.Light：textColorTertiary = @color/secondary_text_material_light，默认态 secondary_text_default_material_light = #8a000000：Material 浅色主题下默认文字色（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light；data/res/values/colors_material.xml，secondary_text_default_material_light（按应用的 compileSdk 取对应平台））
- AppCompat 主题设 android:textViewStyle = Widget.AppCompat.TextView，其 parent 是 android:Widget.TextView：AppCompat 下同样走 textAppearanceSmall（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.Widget.AppCompat.TextView（按应用依赖的版本））
- Base.TextAppearance.AppCompat.Small：textSize = @dimen/abc_text_size_small_material（14sp），textColor = ?android:attr/textColorTertiary：AppCompat 自带的 Small 外观（API 21 以下的主题链用它）（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.TextAppearance.AppCompat.Small（按应用依赖的版本））
- Text 的 fontSize 默认值 16fp（number 按 fp）：不显式写就和源端 14sp 不同（出处：ts-basic-components-text.md，fontSize）
针对本应用要查的：
- Activity 实际主题及其祖先对 textViewStyle、textAppearanceSmall、textColorTertiary 的覆盖：源工程 AndroidManifest.xml 里该 Activity（没有就看 application）的 android:theme，再到 res/values 的主题样式文件按 parent 链找；没覆盖的落到 AppCompat 包内 res/values/values.xml 或平台 data/res/values/themes_material.xml；沿链读到 textColor 指向的属性，再解析到颜色选择器的默认态颜色；例：parent 是 Theme.AppCompat.Light 且没覆盖时，textColorTertiary 解析到 #8a000000
未核实：卡里没写 appcompat 版本，按本机 appcompat 1.7.1 和 android-36 核对
来源：1 张卡，1 个应用
- case-701f2e2280bcc31423bd（企业安全培训）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4
