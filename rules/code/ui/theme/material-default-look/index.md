# Material 控件没写外观属性时的默认外观

agent 会看到什么：源布局里 Button、FloatingActionButton、BottomNavigationView 等 Material 控件没写 style 和外观属性、外观来自主题；产物里对应组件的 backgroundColor、fontColor、borderRadius、fontWeight、letterSpacing

## 通用查法

### 源 Material 控件没写外观属性时，沿主题和库默认样式查出实际值再显式写

审的是：代码
触发（任一种）：
- 读到：Button、FloatingActionButton、BottomNavigationView 等没写 style、backgroundTint、android:textColor，主题 parent 链到 Theme.MaterialComponents.* 或 Theme.Material3.*；写错的样子：目标组件只写了 XML 里显式的属性，backgroundColor、fontColor、borderRadius、fontWeight 等留着 ArkUI 默认值或照 M2 映射表写
适用范围：Material 主题下源控件外观来自主题和库默认样式时
做法：
- 按「控件 style → 主题里的默认样式属性 → 主题 parent」找到提供值的库样式，顺着 parent、textAppearance、selector 和 ?attr/ 读到颜色、圆角、字号字重、字距
- ?attr/ 落到 colorPrimary 等主题属性时取应用主题的覆写值，没覆写取库默认；颜色写成 color.json 里同值的 $r('app.color.…')
- 和 ArkUI 组件默认值逐项比，不同的显式写出；letterSpacing 是 em，乘字号得 fp
针对本应用要查的：
- 应用主题的 parent 链和覆写：源工程 res/values（含 values-night）下 styles.xml、themes.xml 里 AndroidManifest 的 android:theme 指的主题；沿 parent 追到 Theme.Material3.* 或 Theme.MaterialComponents.*，记下覆写了哪些控件默认样式属性和颜色属性
- 控件默认样式里的外观取值：应用依赖版本的 com.google.android.material:material 包内 res/values/values.xml 和 res/color/ 下的 selector，按样式名、宏名（m3_comp_…）找；顺着 @style、@macro、@dimen、?attr/ 读到具体值。例：material 1.12.0 下 Material3 FAB 的底色宏是 ?attr/colorPrimaryContainer，1.14.0 改成 ?attr/colorPrimary
- 目标组件的默认外观：鸿蒙 SDK ets/component 下该组件的 .d.ts 和 OpenHarmony 文档里该组件的属性表；读各属性的默认值，和源端不同的在目标代码里显式写
来源：2 张卡，1 个应用
- case-85baa9234cc4f4798784（AntennaPod）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4
- case-c40332380c19d002090d（AntennaPod）：做法第 1 步 ← 建议 3；做法第 3 步 ← 建议 1、建议 3

## 规矩

- rule-cf7bdfbaefd0｜Material 控件没显式写外观属性时，列出主题和库的默认外观，逐项对照 ArkUI 默认值显式设置｜读到：CheckBox、RadioButton、MaterialButton、TabLayout、EditText、Spinner 等 Material 控件在布局里没写外观属性，外观来自主题或组件库默认 style；写错：目标组件只直译了 XML 里显式写的属性（checked、onChange、颜色），形状、指示器、字距、底色、标签样式等都留着 ArkUI 默认值
- rule-37fed486a76c｜控件没写 style 时按应用主题父类解析默认外观，不套映射表的 M2 描述｜读到：FloatingActionButton 没写 style，应用主题继承 Theme.Material3.*；写错：Button 写成圆形 borderRadius(28)、强调色底、白图标，或按映射表加了硬 .shadow
- rule-de1618ed6602｜Material 按钮没写 style 和 backgroundTint 时，目标背景设主题 colorPrimary｜读到：布局 XML 里 `<Button>` 没写 `style` 和 `app:backgroundTint`，应用主题是 MaterialComponents 或 Material3 一族；写错：对应 ArkUI `Button` 只写了文本、`fontSize`、`height`，没有 `.backgroundColor(...)`，显示成 ArkUI 默认强调色
- rule-2e03355625e5｜源 Button 外观来自 Material 主题时，目标用语义色补 backgroundColor、fontColor｜读到：源布局 Button 没写 android:background、backgroundTint、textColor，主题父主题是 Theme.MaterialComponents.*；目标 color.json 已有 colorPrimary、colorOnPrimary 同名资源；写错：目标 Button 修饰链只有 fontSize、margin、onClick，没有 .backgroundColor(...) 和 .fontColor(...)，显示平台默认的蓝色按钮
- rule-aace548a71c5｜MDC / M3 按钮样式的字距和文字色从合并资源解析，字距写进内层 Text.letterSpacing｜读到：MaterialButton 的 style 是 Widget.MaterialComponents.Button.TextButton，或继承自 Widget.Material3.Button.OutlinedButton 等 MDC / M3 按钮样式；写错：Button(label) 直接设 fontSize / fontColor，没有 letterSpacing；文字色写的是 colorPrimary 对应的颜色
- rule-0bca1fb292b7｜Material3 底栏选中标签加粗，徽标宿主收到图标尺寸后 TopEnd 锚定｜读到：BottomNavigationView（Material3 主题、没有 bottomNavigationStyle 覆写），itemTextAppearanceActive / itemTextAppearanceInactive 指向 TextAppearance.Material3.* 系的样式；写错：目标端底栏选中和未选标签都写 FontWeight.Medium；徽标宿主 Stack({ alignContent: Alignment.TopEnd }) 设成 48×32 包住 24×24 图标，徽标不在图标右上
- rule-c860b548cb70｜Activity 用库主题时，颜色 attr 取库主题默认值，不复用应用 color.json 的同名 token｜读到：清单或规格写明 Activity 的 `android:theme` 是库主题（如 `Theme.MaterialComponents.Light.Dialog`、`Theme.AppCompat.*`），控件样式继承 `Widget.MaterialComponents.Button.TextButton` 且没覆盖 `android:textColor`；写错：目标写 `.fontColor($r('app.color.colorPrimary'))`，用的是应用主题里同名 token 的值
