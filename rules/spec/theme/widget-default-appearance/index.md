# TextView 和 Button 没写的外观属性

agent 会看到什么：读过的源布局里 TextView、Button 只写了文本、字号、背景，没写 textColor、textAppearance、textAllCaps、includeFontPadding 等；交回的规格里这个控件缺了主题或默认样式给的颜色、大小写、字重和行框高度

## 通用查法

### 源控件没写某个外观属性时，顺主题和控件默认样式读出实际值写进规格

审的是：规格
触发（任一种）：
- 读到：源布局的 TextView、Button 没写 android:textColor、android:textAppearance、style、android:textAllCaps、android:includeFontPadding 这类外观属性；写错的样子：规格里这个控件只记了显式写出的属性（文本、字号、背景），没写缺省时实际生效的颜色、大小写、字重或行框高度及其出处
适用范围：规格阶段写源端控件外观、有属性由主题或控件默认样式隐式提供时
做法：
- 从 AndroidManifest 的 android:theme（或 Activity 主题）出发，在 res/values*/styles.xml、themes.xml 里顺 parent 链找应用对这个属性或控件样式（textViewStyle、textColorSecondary 等）的覆盖
- 没覆盖就读控件默认样式和平台或依赖库主题，顺 ?attr、@style、@color 引用一路读到值；属性本身的缺省看平台 attrs.xml 的注释或控件的 setter
- 把值和出处写成这个控件的一项（如「文字颜色：未声明 textColor，取主题的 ?android:textColorSecondary」），目标端显式写出
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.TextView：<item name="textAppearance">?attr/textAppearanceSmall</item>：TextView 没写 textAppearance / style 时，文字外观取主题的 textAppearanceSmall（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.TextView（按应用的 compileSdk 取对应平台））
- secondary_text_default_material_light = #8a000000；secondary_text_default_material_dark = #b3ffffff：例：AppCompat / Material 主题、应用没覆盖时的次要文字色（浅色 / 深色主题）（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，secondary_text_default_material_light / secondary_text_default_material_dark（按应用依赖的版本））
- includeFontPadding：Leave enough room for ascenders and descenders instead of using the font ascent and descent strictly. (Normally true)：例：属性的缺省写在平台 attrs.xml 的注释里；没写就带上下字体留白（出处：Android SDK 平台资源 data/res/values/attrs.xml，TextView 的 includeFontPadding（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 应用主题对这个属性或控件样式有没有覆盖：源工程 AndroidManifest.xml 的 android:theme 指向的主题，在 res/values*/styles.xml 或 themes.xml 里顺 parent 链找对应属性；有覆盖就写覆盖值及其出处；没有就顺到依赖库或平台主题读默认值
未核实：Button 的默认外观（全大写、Medium 字重、投影和按压反馈）出自主题里的哪个样式，族里规矩没有查实平台或依赖库资源
来源：2 张卡，2 个应用
- case-9ec2a14cbd1df18e3620（Privacy Friendly 2048）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 3
- case-c3ff122a5abfda1fa55d（Blockinger）：做法第 2 步 ← 建议 2

## 规矩

- rule-01f0594e8fed｜页面规格列出 TextView 的文本和字号时，同时写明未声明 textColor 时主题给的颜色｜读到：源布局的 TextView 有 android:text、android:textSize，没有 android:textColor、android:textAppearance、style；写错：页面规格或映射参考里这个控件只记了文本和字号，没有颜色这一项，也没写颜色来自主题
- rule-778e7d423078｜规格描述 Button 行时，写明未被覆写的控件默认外观，不只写字号字色背景｜读到：源 `<Button>` 只写了 `android:background`、`android:textColor`、`android:textSize`，没写 `android:textAllCaps`、`android:stateListAnimator`、`style=`，主题是 `Theme.AppCompat` 一族；写错：规格的 Button 控件行只列「textSize、白字、背景 drawable」，没写全大写、Medium 字重、投影与按压反馈这些默认外观
- rule-11a02816f16e｜wrap_content 单行 TextView 参与纵向排布时，规格写出默认行框高度并列为验收项｜读到：wrap_content 的单行 TextView（textAppearanceLarge / Small 或 sp 字号，没写 includeFontPadding）是标题、列表项或页脚，决定下方分隔线、行高或按钮位置；写错：规格只写字号（Large / Small、30sp / 18sp），没有写这行文字的视图高度，也没有对应验收项
- rule-5ce6d5eb3981｜规格的文字控件转换行写明决定纵向排布的行框，拿不到源字体度量就登记待设备核对｜读到：布局里决定行高的 TextView 只有 textAppearance，没写 android:lineHeight 和 android:includeFontPadding；写错：规格的控件转换行只写 textAppearance 与字号，没写文字行框（单行/多行、首末行 font padding），也没有登记待设备核对项
