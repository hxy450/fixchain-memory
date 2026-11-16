# 源控件没写的外观属性（主题的默认控件样式）

agent 会看到什么：读到 TextView、Button、AppCompatButton 子类、TabLayout 只写了部分外观属性（没写 style、textColor、textAllCaps、tabGravity 等，或只写了 textAppearance），交回的代码只照显式写的属性写，其余落到 ArkUI 默认

## 通用查法

### 源控件没显式写的外观属性，顺着主题的默认控件样式读出实际值后显式写

审的是：代码
触发（任一种）：
- 读到：源 TextView、Button、TabLayout 等只写了部分外观属性，没写 style=、android:textAppearance、android:textColor、android:textAllCaps，或只写 textAppearance 没写 textColor；写错的样子：目标组件只照源 XML 显式写的属性写，其余用 ArkUI 默认（Text 的近黑 fontColor、Button 的按压变暗、Tabs 的 BarMode.Fixed 均分），或套主文字色
适用范围：源控件的部分外观来自主题和默认控件样式时
做法：
- 从应用或 Activity 主题顺 parent 链找这类控件的默认样式（textViewStyle、buttonStyle、tabStyle），没覆盖就取依赖库或平台的 Widget 样式，再顺 textAppearance → ?attr → @color / @dimen 读到值，浅、深色各一份
- 列出默认样式的属性清单，和源 XML 已写的属性做差集；部分属性显式不等于整控件显式
- 差集逐项写成目标的显式写法（.fontColor、.fontSize、.fontWeight、投影、按压态、Tab 栏布局），不留给 ArkUI 默认值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.TextView：textAppearance = ?attr/textAppearanceSmall；Widget.Material.TextView 和 AppCompat 的 Base.Widget.AppCompat.TextView 都继承 Widget.TextView：TextView 没写 textAppearance、style 时，文字外观取主题的 textAppearanceSmall（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.TextView（按应用的 compileSdk 取对应平台）；androidx.appcompat:appcompat 包内 res/values/values.xml，Base.Widget.AppCompat.TextView（按应用依赖的版本））
- AppCompat 主题的 buttonStyle 是 Widget.AppCompat.Button；API 21+ 下 Base.Widget.AppCompat.Button 的 parent 是 android:Widget.Material.Button：AppCompat 主题下按钮默认样式最终落到平台的 Widget.Material.Button（出处：androidx.appcompat:appcompat 包内 res/values/values.xml 的 buttonStyle、res/values-v21/values-v21.xml 的 Base.Widget.AppCompat.Button（按应用依赖的版本））
- fontColor(value: ResourceColor): TextAttribute，默认值 '#e6182431'：Text 不写 fontColor 时用这个近黑默认色，和源端主题给的字色不同（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontColor）
针对本应用要查的：
- 这类控件在应用主题下的默认样式和其中的外观值：源工程 AndroidManifest 的 android:theme，到 res/values*/（含 values-night）的 styles.xml、themes.xml 顺 parent 链找 textViewStyle、buttonStyle、tabStyle、android:textAppearance*、android:textColor*；没覆盖的到 androidx.appcompat:appcompat、com.google.android.material:material 包内 res/values*/ 下的 values*.xml（按应用依赖的版本），以及 Android SDK 平台资源 data/res/values/styles_material.xml、themes_material.xml（按应用的 compileSdk）；顺着 style → textAppearance → ?attr → @color / @dimen 解到字面量，浅、深色各取一份；同名样式在 values-v21、values-land、values-sw600dp-v13 等限定符目录里另有定义的也读出来。例：继承 Theme.AppCompat.Light / DayNight 且都没覆盖时，没写颜色的 TextView 是次级文字色，浅色 #8A000000、夜间 #B3FFFFFF
未核实：默认值按本机 android-36 平台资源、appcompat 1.7.1、material 1.12.0 核实，应用的 compileSdk 和依赖版本不同时按要查的重查
来源：3 张卡，2 个应用
- case-29fdf1fe3faadb5933b9（MifareClassicTool）：做法第 1 步 ← 建议 4；做法第 3 步 ← 建议 4
- case-64a967d716ed18688332（Privacy Friendly 2048）：做法第 1 步 ← 建议 1
- case-c60be73d1f1f8c460922（Privacy Friendly 2048）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2

## 规矩

- rule-b98f03e9e927｜未声明颜色的 TextView 转成 Text 时，显式写 fontColor 取主题次要文字色｜读到：TextView 没写 android:textColor、android:textAppearance、style，主题继承 Theme.AppCompat / Theme.Material；写错：.fontColor(...) 绑主文字色（textColorPrimary、#DE000000），或链上没有 .fontColor(...)
- rule-1f0fe64a7c72｜TextView 只写 textAppearance 没写 textColor 时，字号和文字色一起展开｜读到：TextView 写了 android:textAppearance="?android:attr/textAppearanceMedium"（或 Small / Large），没写 android:textColor；写错：目标 Text 只按样式展开了 .fontSize(…)，.fontColor(…) 写成主文字色令牌或没写
- rule-16e106de8645｜Button 只显式写了背景、字色、字号时，其余 Widget 默认外观逐项补齐｜读到：源 `<Button>` 在 `Theme.AppCompat` 主题下只写了 `android:background`（无 pressed 态的 shape）、`android:textColor`、`android:textSize` 等部分属性，没写 `style=`、`android:textAllCaps`、`android:fontFamily`、`android:stateListAnimator`、`android:elevation`；写错：目标 `Button` 只有 `fontSize`、`fontColor`、背景和 `borderRadius`：文字没转大写、没有 `FontWeight.Medium`、没有投影，按压沿用默认 `stateEffect` 变暗
- rule-98604c6e6b37｜textAllCaps 全大写时，目标按 locale 调 toLocaleUpperCase，不用 textCase｜读到：android:textAllCaps="true"，或 Button / AlertDialog 按钮用 TextAppearance.AppCompat.Button、TextAppearance.Material.Button 默认样式；写错：目标写成 .textCase(TextCase.UpperCase)，或把原注释「不以 textCase 仿造」改掉
- rule-24d7463794b1｜继承 AppCompatButton 只换背景的自定义块，目标组件用 .shadow 补按钮默认投影｜读到：自定义块 extends AppCompatButton / Button，只调 setBackgroundResource 换背景，没有 setStateListAnimator(null) 或 setElevation(0)；写错：目标组件只有背景色和圆角，没有 .shadow(...)
- rule-9bbf558431ab｜用一个 Text 代替带自动字号的按钮子类时，按契约显式算出 fontSize，补内边距和 Medium 字重｜读到：源控件 extends AppCompatButton / Button，构造里 setAutoSizeTextTypeUniformWithConfiguration(min, max, step, TypedValue.COMPLEX_UNIT_SP)；写错：目标是一个宽高等于整块的 Text，挂 .maxLines(1).minFontSize(…).maxFontSize(…) 就当等价，没有 .padding，也没有 .fontWeight
- rule-45bc2006188b｜源端禁用不变透明时，用 HitTestMode.None 拦截点击，不写 .enabled(false)｜读到：规格或映射表写 .enabled(false)（如「setEnabled(false) → .enabled(false)」）；源端禁用只靠 setBackgroundResource 换背景，android:textColor 固定；写错：按钮修饰链上写 .enabled(状态变量) 加 backgroundColor(启用 ? 主色 : 灰)，禁用时背景和文字整体变半透明
- rule-49f3bebe95f3｜TabLayout 不写 tabGravity/tabMode/style 时，横屏和宽屏按库默认居中，不一律均分｜读到：源布局的 com.google.android.material.tabs.TabLayout 没写 app:tabGravity、app:tabMode、style，主题是 AppCompat 一族（几何取 Widget.Design.TabLayout）；写错：Tabs 用默认 BarMode.Fixed 加 .barWidth('100%')，横屏和宽屏也均分整行；或判定「页面外壳与方向无关」
- rule-fa9dc2ff17d0｜TabLayout 译成 Tabs 时，tabBar 用 SubTabBarStyle 显式写标签字号字重、颜色和指示条｜读到：com.google.android.material.tabs.TabLayout（tabMode、tabGravity 等），标签样式取库默认；写错：TabContent().tabBar($r(…)) 或 .tabBar('…') 直接传字符串，用的是 ArkUI 默认标签样式
- rule-760bca90bbf8｜ImageButton 没写背景时先沿主题解析默认背景，没显式写透明就补按钮底｜读到：ImageButton 没写 android:background 和 style，应用主题父链止于 android:Theme.Material（或 Theme、Theme.Holo）；写错：目标写成 Row { Image } 或裸 Image，只加 .stateStyles({ pressed: … }) 按压色，没有静态按钮底和 inset
