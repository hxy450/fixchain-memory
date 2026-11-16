# TextView / EditText 的文字外观

agent 会看到什么：读到 TextView / EditText 的 textColor、textSize、textAppearance、fontFamily、shadow* 属性，或这些属性没写、由主题决定；产物里 Text / TextInput 的 fontColor、fontSize、fontWeight、textShadow、height 是沿用值、近似值或 ArkUI 默认

## 通用查法

### 文字控件没写颜色、字号时，沿默认样式和主题链解析出值再显式写

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

## 规矩

- rule-baf483d3eb07｜源 TextView 没写 textSize/textColor 时，按默认样式链和主题推导后显式写到 Text｜读到：布局里 TextView 没声明 android:textSize / android:textColor（颜色可能只由 Span 给出局部）；写错：对应 Text 沿用旧实现或相邻组件的 fontSize(16)、fontColor 数值，或不写而落到 ArkUI 默认 16fp
- rule-8dbc3146c2a9｜EditText 没写 android:textColor 时，按主题解析默认文字色写 fontColor，不沿用硬编码｜读到：源布局的 EditText（含它的 style）没有 android:textColor，可能只写了 android:textColorHint；文字色由 Manifest 里 Activity 或 application 的 android:theme 决定；写错：对应 TextInput 的 .fontColor(...) 是目标端原有的硬编码色，或按「同组统一」给几个框写成同一个现值，不是从主题解析出的默认文字色
- rule-2a56e9436dbf｜平台主题下的文字控件按来源分别取主/次/提示色，显式 @android:color/white 不绑主题主色令牌｜读到：源 styles 父链止于 android:Theme.Holo 等平台主题；TextView 只写 textAppearanceLarge / Small 或不写颜色，EditText 没写 textColorHint，另有 TextView 显式 android:textColor="@android:color/white"；写错：目标 Text 一律用主色令牌（或默认未设色的 TextView 取 textColorPrimary）；显式白的 Text 也绑到主题主色令牌 $r('app.color.…_primary') 上
- rule-e7b595a7e4f6｜源字体是 sans-serif-light 时，目标写 .fontWeight(300)，不写 Lighter｜读到：TextView 或样式写 android:fontFamily="sans-serif-light"；写错：对应的 Text 写成 .fontWeight(FontWeight.Lighter)
- rule-5c5d266a9a44｜TextView 带文字阴影属性时，目标用 Text.textShadow，不用 .shadow｜读到：TextView 或它引用的样式里有 android:shadowColor / shadowRadius / shadowDx / shadowDy；写错：对应的 Text 上写的是 .shadow(...)（阴影投在组件框上），或者没有阴影
- rule-e08cb72735ee｜决定纵向排布的单行 Text 按源端行框显式写 height，列表行高取各行之和｜读到：wrap_content 单行 TextView（textAppearance 或 sp 字号，includeFontPadding 取默认）是标题、列表项两行文字或页脚；写错：对应 Text 只有 .fontSize(...)，没有 .height(...)，标题、列表行比源端矮
- rule-c51620d9c470｜源 TextView 贴顶且没关 includeFontPadding 时，目标 Text 按字号补顶部 padding｜读到：TextView 贴顶（android:layout_alignParentTop 加 android:layout_marginTop，或在定高盒内贴顶），没写 android:includeFontPadding（默认 true）；写错：对应的 Text 只照搬 margin 贴顶，没补顶部 padding，也没在转换报告里登记「字形纵向差待设备核对」
- rule-3d86175ad4d8｜源布局指定字体文件时，注册 rawfile 字体并在 Text 上写 fontFamily｜读到：源布局 TextView 上有 `pixlui:typeface`（指向 ttf 文件）或 `android:fontFamily`；写错：对应 Text 没有 `.fontFamily(...)`，字体名只写在注释里；粗体字体用 `.fontWeight(FontWeight.Bold)` 伪粗体代替
