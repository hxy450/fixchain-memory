# 源端颜色引用主题属性 ?attr/… 时，顺着主题链解出日夜两值，绑成对的颜色键

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
