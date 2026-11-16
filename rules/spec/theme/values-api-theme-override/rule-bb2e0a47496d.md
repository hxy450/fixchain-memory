# 规格的 ActionBar 行写明主题提供方、解析出的栏底色和标题色，以及应接的共享标题栏

审的是：规格
触发（任一种）：
- 读到：源 Activity 主题（含 values-vXX 覆盖）继承带窗口 ActionBar 的框架主题，如 android:Theme.Material.Light.DarkActionBar，colorPrimary 指向应用色；计划列了共享顶栏组件；写错的样子：规格的 ActionBar 行只写「标题 + Up 尖角」，安全区写「常规 NavDestination 标题栏」，主题只按 values/styles.xml 写成 Theme.Light，没写栏底色、标题色和应接的共享标题栏组件
适用范围：规格提取阶段写源页 ActionBar 行（标题栏、主题、安全区小节）时
做法：
- ActionBar 行写明：主题提供方（查 values-vXX 覆盖后解析出的主题名）、栏底色（colorPrimary 的解析值）、标题色，以及应接的共享标题栏组件
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.Material.ActionBar.Solid：background = ?attr/colorPrimary：Material 主题下窗口 ActionBar 的底色就是 colorPrimary（出处：Android SDK 平台资源 data/res/values/styles_material.xml，Widget.Material.ActionBar.Solid（按应用的 compileSdk 取对应平台））
- Theme.Material.Light.DarkActionBar：actionBarTheme = @style/ThemeOverlay.Material.Dark.ActionBar：栏内标题按深色覆盖层取 textColorPrimary（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light.DarkActionBar）
针对本应用要查的：
- 主题提供方和栏底色：源工程 AndroidManifest.xml 里 Activity 或 application 的 android:theme；res/values-vXX/styles.xml（版本限定高的优先）和 res/values/styles.xml 里同名 style 的 parent 链与 colorPrimary；写解析出的主题名和 colorPrimary 的颜色值；只看 values/styles.xml 会漏掉 values-v21 之类的覆盖
来源：1 张卡，1 个应用
- case-3d6b5f99f326a3e5e8e9（Sokoban）：做法第 1 步 ← 建议 3
