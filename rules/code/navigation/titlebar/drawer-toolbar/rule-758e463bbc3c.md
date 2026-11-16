# Toolbar 由 ActionBarDrawerToggle 接管导航时，按 AppCompat 默认几何画汉堡和标题

审的是：代码
触发（任一种）：
- 读到：AppBarLayout 里的 Toolbar 没写 titleTextAppearance / contentInsetStartWithNavigation，代码里 setSupportActionBar + ActionBarDrawerToggle 接管导航图标；写错的样子：汉堡用 SymbolGlyph 系统符号（如 sys.symbol.line_3_horizontal），标题常规字重、起点很靠左（左距 4 左右），工具栏没有投影
适用范围：带抽屉开关的 AppCompat Toolbar 迁成目标端自绘工具栏，源端没改 Toolbar 和 DrawerArrowToggle 默认样式时
做法：
- 导航区宽 56vp，里面画三条 18×2vp 横条、条间距 3vp（DrawerArrowDrawable 默认），颜色取 textColorSecondary 的解析值，不用系统符号
- 标题 .fontSize(20).fontWeight(FontWeight.Medium)，带导航按钮时标题起点 72vp（contentInsetStartWithNavigation）
- 工具栏加对应 AppBarLayout 4dp elevation 的投影并 .zIndex(1)；注释写出每项取值来源
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Base.Widget.AppCompat.DrawerArrowToggle：barLength 18dp、gapBetweenBars 3dp、drawableSize 24dp；.Common：thickness 2dp、color ?android:attr/textColorSecondary：抽屉开关三条横条的尺寸和颜色（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.Widget.AppCompat.DrawerArrowToggle（按应用依赖的版本））
- Base.Widget.AppCompat.Toolbar.Button.Navigation：android:minWidth 56dp：导航按钮宽度（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.Widget.AppCompat.Toolbar.Button.Navigation（按应用依赖的版本））
- contentInsetStartWithNavigation = @dimen/abc_action_bar_content_inset_with_nav = 72dp；contentInsetStart 16dp：有导航按钮时标题起点 72dp，没有时 16dp（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.V7.Widget.AppCompat.Toolbar、abc_action_bar_content_inset_with_nav（按应用依赖的版本））
- abc_text_size_title_material_toolbar = 20dp：Toolbar 标题字号（TextAppearance.Widget.AppCompat.Toolbar.Title 经 ActionBar.Title 取它）（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，abc_text_size_title_material_toolbar（按应用依赖的版本））
- font_family_title_material = sans-serif-medium：标题字重 Medium（API 21+ 标题样式继承 TextAppearance.Material.Title）（出处：Android SDK 平台资源 data/res/values/donottranslate_material.xml，font_family_title_material；data/res/values/styles_material.xml，TextAppearance.Material.Title（按应用的 compileSdk 取对应平台））
- design_appbar_elevation = 4dp：AppBarLayout 默认投影高度（出处：com.google.android.material:material 包内 res/values/values.xml，design_appbar_elevation（按应用依赖的版本））
- fontSize(value: number | string | Resource): TextAttribute；number 按 fp：目标端字号单位（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontSize）
针对本应用要查的：
- 源端是否改过 Toolbar 或抽屉开关的默认样式：源工程布局 XML 里 Toolbar 的 style、titleTextAppearance、contentInsetStartWithNavigation，主题里的 toolbarStyle、drawerArrowStyle；都没写就用上面的默认值；写了就顺着样式取覆盖后的值
未核实：源端标题 20dp 不随系统字体缩放，目标 fontSize(20) 按 fp 会缩放；卡里没验证放大字体时的表现；投影的具体参数卡里只写了「投影常量」
来源：1 张卡，1 个应用
- case-d5cb8650c08eea9be356（Privacy Friendly 2048）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2、诊断
