# 引用主题属性 ?attr 的颜色

agent 会看到什么：读到源端颜色写成 ?attr/…（vector 的 android:fillColor、Toolbar 背景、图标的 colorControlNormal）或取主题的 windowBackground，交回的代码给 Image 的 fillColor、backgroundColor、fontColor 绑了颜色键或没绑

## 通用查法

### 源端颜色引用主题属性 ?attr/… 时，顺着主题链解出日夜两值，绑成对的颜色键

审的是：代码
触发（任一种）：
- 读到：源端颜色写成 ?attr/…（vector 的 android:fillColor、控件的 android:background、Toolbar 图标的 colorControlNormal），或控件没写底色、取主题的 android:windowBackground；写错的样子：目标写成单态常量 $r('app.color.colorPrimary')、$r('app.color.white')，或沿用 SVG 里固化的 #000000、借用语义不同的颜色键，深色模式下不切换
适用范围：源端颜色来自主题属性，目标用 color.json 的颜色键着色时
做法：
- 按控件 style → 祖先 android:theme → Activity 主题 → 应用主题，找到给这个 attr 赋值的 <item>，顺着 ?attr/、@color/ 引用解到颜色字面量；values-night 下的同名主题再解一次，得到浅、深两值
- 目标绑一个在 base 和 dark 的 element/color.json 里各有值、和这两值相同的键，同一主题属性全工程只映射到一个键；没有就补键
- 源布局里写死 @color/ 的位置仍用单态常量
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 深色值放在 resources/dark/element/color.json：颜色模式限定词 dark 的 element 目录，深色模式下按同名键取值（出处：resource-categories-and-access.md，创建资源目录和资源文件）
- fillColor(color: ResourceColor | ColorContent | ColorMetrics): ImageAttribute：Image 叠加的填充色，只对 SVG 图生效（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.fillColor）
针对本应用要查的：
- 主题属性在浅色、深色主题下的值：源工程 AndroidManifest 的 android:theme 所指主题；res/values*/styles.xml、themes.xml 里控件 style、Toolbar 的 android:theme / app:theme、Activity 主题和应用主题的父主题链；res/values-night/ 下的同名主题；找到提供值的 <item name="属性名">，顺着 ?attr/、@color/ 引用解到颜色字面量，浅色、深色各记一个。例：Toolbar 主题里 colorControlNormal=?attr/colorOnSurface 时，取应用主题里 colorOnSurface 的浅、深两值
- 主题链走到依赖库主题时的值：依赖库包内 res/values/values.xml（androidx.appcompat:appcompat、com.google.android.material:material，按应用依赖的版本），按主题或控件 style 名找；找到该 attr 的 <item> 后继续顺着引用解到颜色；例：appcompat 的 Base.Widget.AppCompat.ActionBar.Solid 里 background 是 ?attr/colorPrimary
未核实：主题链一直走到平台主题（Theme.Material 等）时各属性的默认值，族里规矩没有逐项查实
来源：3 张卡，2 个应用
- case-0693d5ce6cf6356203d5（AntennaPod）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、建议 2
- case-7af8ba0d85382021da91（Privacy Friendly 2048）：做法第 3 步 ← 诊断
- case-e82be6ce5af181afb98d（AntennaPod）：做法第 1 步 ← 建议 3

## 通用查法

### 源端颜色引用 ?attr/… 主题属性时，顺应用主题查出浅深两值，写成成对的颜色资源

审的是：代码
触发（任一种）：
- 读到：布局或样式里的颜色属性写 ?attr/…（如 android:textColor、自定义 View 的 app:foregroundColor），值由应用主题提供；写错的样子：目标的 .fontColor / 颜色 @Param 用了按属性名猜的色、借用的别的颜色，或写死某一模式的 Color.White
适用范围：源端颜色经应用主题的属性提供，迁成 ArkUI 颜色时
做法：
- 从 AndroidManifest.xml 的 android:theme 找到应用主题，在 res/values/ 和 res/values-night/ 的 styles.xml、themes.xml 里找给这个 attr 赋值的 <item name="…">
- 顺着 ?attr/、@color/ 引用解到颜色字面量（@color/ 到 colors.xml 里找），浅色、深色各记一个；每个调用点按它自己引用的 attr 分别解
- 在 base/element 和 dark/element 的 color.json 里补同名颜色，目标写 $r('app.color.<名>')；不按名字猜、不借用语义不同的颜色、不写死某一模式的色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 在两个 color.json 里定义同名配色并赋予不同色值，系统切换深浅色时自动取对应的值：页面只要引用同名 token 就会随深浅色切换（出处：ui-dark-light-color-adaptation.md，应用跟随系统的深浅色模式）
针对本应用要查的：
- 这个主题属性在浅色、深色主题下的颜色值：源工程 AndroidManifest.xml 的 android:theme 指向的主题；res/values/ 与 res/values-night/ 下 styles.xml、themes.xml 里的 <item name="<attr 名>">，以及 colors.xml；item 是颜色字面量就直接用；是 @color/… 就到 colors.xml 解出颜色；是 ?attr/… 就再按同样的办法解下一层；浅色、深色各取一份
- 每个调用点引用的是哪个主题属性：源工程里用到这个控件的每个布局 XML，控件上的颜色属性；逐个记下引用的 attr，按上一项解出值后在对应调用点传参
未核实：应用主题没有给这个 attr 赋值、值来自父主题（平台主题或 AppCompat 库主题）时去哪个文件查、按什么顺序解析，族里规矩没有查实
来源：3 张卡，2 个应用
- case-0693d5ce6cf6356203d5（AntennaPod）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
- case-720d51456fccb920411f（AntennaPod）：做法第 1 步 ← 诊断；做法第 3 步 ← 诊断
- case-ee2085c48fe78dbd3a2f（MifareClassicTool）：做法第 3 步 ← 建议 3

## 规矩

- rule-06cce98c599a｜源 vector 用 ?attr 主题色填充时，显示它的 Image 加 .fillColor 按主题着色｜读到：源 vector 的 android:fillColor="?attr/…"（随主题变色），布局里 ImageView 用 android:src 显示它；写错：页面里显示转换后 SVG 的 Image 没有 .fillColor(...)，颜色固定成资源里的默认色或不可见
- rule-e675c196142f｜源图标没写 tint、颜色来自主题属性时，fillColor 用与主题同值的深浅色键，不借次要文字灰｜读到：矢量图标的 android:fillColor="?attr/…"（主题属性），使用它的 ImageView / 菜单项上没有 android:tint 或 app:tint；写错：目标 Image(...).fillColor($r('app.color.…')) 用的是次要文字色一类语义不同的灰，或只按 SVG 里的浅色值写死
- rule-aed55377b276｜源端取主题色或窗口底的位置，目标绑主题成对键，不写 colorPrimary、colorAccent、white 常量｜读到：Toolbar android:background="?attr/colorPrimary"；ActionBar、抽屉选中项取 colorPrimary；平台 AlertDialog 按钮、开关、单选、链接取 colorAccent；页面或列表没设底色、取主题的 android:windowBackground；写错：目标写成 .backgroundColor($r('app.color.colorPrimary'))、.fontColor($r('app.color.colorAccent'))、.backgroundColor($r('app.color.white')) 这类直迁常量
- rule-e800c6de25a1｜源 textColor 引用应用主题自定义 attr 而目标缺同名颜色时，按主题值补建资源，不借用别的颜色｜读到：源布局 TextView 写 android:textColor="?attr/…"，引用的是应用自己在主题里定义的属性（不是 android: 平台属性），值在应用主题的 styles.xml 里；写错：目标 color.json 里没有对应颜色，Text 的 .fontColor($r('app.color.…')) 换成了另一个已有颜色（如通用错误色）；既没补建资源，也没登记 resource-pending 或 UNC 占位
- rule-5cc690b0a4c0｜自绘组件的颜色属性写成 ?attr/… 时，先查主题实际值再定默认色，各调用点按自己布局传参｜读到：布局 XML 里自定义 View（如自绘进度环）写 app:foregroundColor="?attr/…"；写错：ArkTS 自绘组件颜色 @Param 的默认值按属性名猜成强调色（accent 一类的键），或调用点没有按各自布局里的 foregroundColor 传参
- rule-b0a34605bf56｜源端主题是 DayNight 时，页面颜色只引用 base/dark 成对 token，不写死某一模式的色｜读到：styles.xml 里 AppTheme 只继承 Theme.AppCompat.DayNight；写错：页面的 .backgroundColor / .fontColor 写死某一模式的调色板色（Color.White、白色或深灰的 $r('app.color.…')），或注释写「深色留待以后」
- rule-57d9257244a4｜窗口底色来自主题 windowBackground 时，页面根 NavDestination 等显式设底色｜读到：源端页面布局根上没写 android:background，窗口底色来自生效主题的 windowBackground（Material 系为 ?attr/colorBackground）；写错：页面根 Navigation 或 NavDestination 的属性链里没有 .backgroundColor(...)
