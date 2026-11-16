# 框架溢出面板按源主题的溢出菜单样式和弹层底色定位置与颜色，Material 系盖住标题栏

审的是：代码
触发（任一种）：
- 读到：源主题是 Theme.Material 系（如 Theme.Material.Light.DarkActionBar）的窗口 ActionBar，菜单有进溢出的项；写错的样子：溢出面板 margin top 等于栏高、贴在标题栏下，底色写成 #FFFFFFFF 纯白
适用范围：自绘标题栏还原框架窗口 ActionBar 的溢出面板时
不适用的情形：源主题是 Holo 系时，溢出菜单样式没有 overlapAnchor，面板贴栏下沿
做法：
- 按源主题的 actionOverflowMenuStyle 取锚定：Material 系 overlapAnchor=true，面板盖住标题栏，水平按 dropDownHorizontalOffset −4dip 偏移
- 底色取 colorPopupBackground 的解析值：Material.Light 为 ?attr/colorBackground → #FFFAFAFA，不是纯白
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.Material.PopupMenu.Overflow：overlapAnchor=true，dropDownHorizontalOffset=-4dip：Material 溢出面板盖住锚点（标题栏）（出处：Android SDK 平台资源 data/res/values/styles_material.xml，Widget.Material.PopupMenu.Overflow（按应用的 compileSdk 取对应平台））
- Theme.Material.Light：actionOverflowMenuStyle=@style/Widget.Material.Light.PopupMenu.Overflow（parent 是 Widget.Material.PopupMenu.Overflow）：浅色 Material 主题用的溢出菜单样式（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light；styles_material.xml，Widget.Material.Light.PopupMenu.Overflow）
- Theme.Material.Light：colorPopupBackground=?attr/colorBackground，colorBackground=@color/background_material_light → material_grey_50 = #fffafafa：弹层底色（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light；data/res/values/colors_material.xml，background_material_light、material_grey_50）
- 面板改为盖住标题栏、底色 #FFFAFAFA、带投影后与安卓实测一致：修好后的结果（出处：卡里修好并验证过）
针对本应用要查的：
- 源主题的溢出菜单样式和弹层底色：Android SDK platforms/android-<compileSdk>/data/res/values/themes_material.xml（或 themes_holo.xml）里源主题的 actionOverflowMenuStyle、colorPopupBackground；顺着样式看有没有 overlapAnchor 和 dropDownHorizontalOffset；底色顺着 ?attr/、@color/ 解到颜色值
未核实：面板上沿与右缘的具体偏移要以源端截图实测为准（卡里说明）
来源：1 张卡，1 个应用
- case-45b40cf92799928188ab（Sokoban）：做法第 1 步 ← 建议 5、建议 2；做法第 2 步 ← 建议 2、诊断；例外 1 ← 建议 2；取值 4 ← 诊断
