# 页面规格的顶栏写明 android:theme 覆盖和解析后的昼夜标题色、图标色及默认字号字重

审的是：规格
触发（任一种）：
- 读到：页面 include 的工具栏布局里 AppBarLayout 带 android:theme（ThemeOverlay.AppCompat.Light，夜间 .Dark），Toolbar 只写 background=?attr/colorPrimary；写错的样子：页面规格的「顶栏」只写「include 工具栏布局、背景 colorPrimary」，没写主题覆盖、解析后的标题色和导航图标色（昼夜两态）、Toolbar 默认字号字重
适用范围：规格提取阶段写带 AppBarLayout / Toolbar 的页面规格时
做法：
- 顶栏行写出：android:theme 覆盖是哪个 ThemeOverlay；解析后的标题色和导航图标色，昼、夜各一（Light：#DE000000 / #8A000000，Dark：#FFFFFFFF / #B3FFFFFF）；标题 20、Medium
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Light 覆盖：textColorPrimary 默认态 #de000000，textColorSecondary（= colorControlNormal）默认态 #8a000000：昼间标题色和导航图标色（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.ThemeOverlay.AppCompat.Light、primary_text_default_material_light（按应用依赖的版本））
- Dark 覆盖：#ffffffff 和 #b3ffffff：夜间标题色和导航图标色（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，primary_text_default_material_dark、secondary_text_default_material_dark（按应用依赖的版本））
针对本应用要查的：
- 顶栏用的是哪个 ThemeOverlay：源工程工具栏布局 XML 里 AppBarLayout / Toolbar 的 android:theme，再到 res/values 和 res/values-night 的 styles.xml 里该样式的 parent；parent 落到 ThemeOverlay.AppCompat.Light 或 .Dark 就按上面的值写；样式自己覆盖了文字色的以样式为准
来源：1 张卡，1 个应用
- case-d5cb8650c08eea9be356（Privacy Friendly 2048）：做法第 1 步 ← 建议 3、建议 1、建议 2
