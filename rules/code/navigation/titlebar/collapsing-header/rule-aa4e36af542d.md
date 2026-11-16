# wrap_content 头部里 match_parent 的背景层，写显式高度，不写 .height('100%')

审的是：代码
触发（任一种）：
- 读到：wrap_content 的 AppBarLayout / CollapsingToolbarLayout 里放 android:layout_height="match_parent" 的背景 ImageView（高度由头部内容决定）；写错的样子：List 首个 ListItem 里的背景 Image 或遮罩层写 .height('100%')，头部行被撑成整个 List 视口，下面的行被挤出可视区
- 读到：AppBarLayout / CollapsingToolbarLayout 是 wrap_content，里面的背景 ImageView 写 android:layout_height="match_parent"（随头部等高）；写错的样子：背景 Image 或遮罩写成 .height('100%')，放在 Scroll / Column 这类不定高的父级里，撑满整个视口
适用范围：源端背景层随 wrap_content 头部等高，目标背景或遮罩层位于 List 行、Scroll、Column 等没有定高的父级里时
做法：
- 背景和遮罩层都写显式高度：按源布局的可见区域算出头部高度（如 marginTop=?attr/actionBarSize 的工具栏高度加头部块的 dp 高，dp 照数值写成 vp）
- 或者把背景画在头部容器自身上，或者用 onAreaChange 测得内容高度后再给背景层定高
- 写完后对 Scroll / List 子树搜一遍 width('100%') / height('100%')，逐个确认父级定高
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onAreaChange(event: (oldValue: Area, newValue: Area) => void): T：组件区域变化时回调，可从 newValue 取内容高度（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onAreaChange）
- 平台 Material 主题 actionBarSize = @dimen/action_bar_default_height_material：默认 56dp，values-land 48dp，values-sw600dp 64dp：?attr/actionBarSize 在平台主题下的取值，随横竖屏和宽度变（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material 的 actionBarSize；data/res/values*/dimens_material.xml，action_bar_default_height_material（按应用的 compileSdk 取对应平台））
- AppCompat 主题 actionBarSize = @dimen/abc_action_bar_default_height_material = 56dp：AppCompat / MaterialComponents 主题族下 ?attr/actionBarSize 的默认值（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，abc_action_bar_default_height_material（按应用依赖的版本））
- 背景层改按工具栏高度（actionBarSize）加头部块高度定高后，与源端等高，头部行不再占满 List：显式定高是上机核对过的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 头部可见区域的高度：源工程的布局 XML 里折叠头部各块的 layout_height，以及工具栏高度（?attr/actionBarSize 一类）；把头部块的 dp 值和工具栏高度相加，作为目标背景层的显式高度
- ?attr/actionBarSize 的实际值：源工程 res/values 主题文件里应用或 Activity 主题有没有覆盖 actionBarSize；没有就按主题族到平台资源或 appcompat 包内 values.xml，并看 values-land、values-sw600dp 等限定目录；读出 dp 值，照数值写成 vp，按目标支持的屏幕方向和宽度分别取
来源：2 张卡，1 个应用
- case-4f627840679361f165a3（AntennaPod）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 4 ← 诊断
- case-9058ac868b6feb3a04e0（AntennaPod）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2；取值 4 ← 诊断
