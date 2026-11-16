# 文字控件没写颜色、字号时，沿默认样式和主题链解析出值再显式写

审的是：代码
触发（任一种）：
- 读到：源 TextView / EditText（含 style）没写 android:textColor、android:textSize，颜色字号由默认样式和 android:theme 决定；写错的样子：目标 .fontColor(...)、.fontSize(...) 沿用旧值或统一主色令牌，或不写、落到 ArkUI 默认
适用范围：安卓文字控件的颜色、字号来自默认样式和主题，迁成 ArkUI 时
做法：
- 控件和它的 style 没写 textColor / textSize 时沿默认样式链找：TextView 从 textViewStyle 的 textAppearance=?attr/textAppearanceSmall、EditText 从 Widget.EditText 的 textColor=?attr/editTextColor 开始
- 到 Activity（没有就 application）的 android:theme 顺 parent 链读出该属性，解析到颜色和字号后写显式的 .fontColor(...) / .fontSize(...)，按来源分别取
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- TextView(Context, AttributeSet) 的默认样式属性是 textViewStyle：未声明的外观从主题的 textViewStyle 开始找（出处：android.widget.TextView#TextView(Context, AttributeSet)）
- Widget.TextView：textAppearance = ?attr/textAppearanceSmall：默认样式把外观交给主题的 textAppearanceSmall（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.TextView（按应用的 compileSdk 取对应平台））
- Widget.EditText：textColor = ?attr/editTextColor：EditText 默认样式的文字色取主题的 editTextColor（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.EditText（按应用的 compileSdk 取对应平台））
- Text 的 fontSize 默认值 16fp（number 按 fp）：不显式写就落到 16fp，和源端默认字号可能不同（出处：ts-basic-components-text.md，fontSize）
针对本应用要查的：
- 源控件实际生效的文字色和字号：源工程布局 XML 里控件的 style → AndroidManifest.xml 里 activity / application 的 android:theme → 应用 res/values 的 styles、themes 里这个主题的 parent 链 → 所继承的库主题（AppCompat、Material Components 包内 res/values/values.xml）或平台主题（Android SDK 平台资源 data/res/values/themes_material.xml）；找到第一个提供这个属性的项，顺着 @color/…、@dimen/… 或 ?attr/… 解析到值；是 selector 时取默认态的颜色；例：parent 是 Theme.AppCompat.Light 且没覆盖时，未写字号的 TextView 是 14sp，textColorTertiary 解析到 #8a000000
未核实：卡里没写 appcompat 版本，按本机 appcompat 1.7.1 和 android-36 核对；Material Components 主题下的解析，族里的卡没核对
来源：3 张卡，2 个应用
- case-701f2e2280bcc31423bd（企业安全培训）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4
- case-784ba4ab52f98f7156b6（企业安全培训）：做法第 1 步 ← 建议 1
- case-e6fd5f0c4d37710c1d97（Blockinger）：做法第 2 步 ← 建议 2
