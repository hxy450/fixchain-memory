# 取框架 ActionBar 默认外观时，每个平台资源名都查 values-land、values-sw* 覆盖并写成分支

审的是：代码
触发（任一种）：
- 读到：源 Activity 依赖框架主题自带的 ActionBar，栏高、标题字号等外观取自平台资源，源端没有自己定义；写错的样子：目标自绘标题栏只给一项做方向分支（如栏高 isLandscape ? 48 : 56），标题仍写死 .fontSize(20)
适用范围：目标自绘标题栏复刻安卓框架 ActionBar 的平台默认外观时
做法：
- 每查到一个平台资源名（栏高、标题字号等），都在同一平台的 values-land、values-sw* 目录按同名再检索一次
- 有覆盖的都写成方向分支，不只给已知的一项做：如 .fontSize(isLandscape ? 14 : 20)、.height(isLandscape ? 48 : 56)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- text_size_title_material_toolbar：values 下 20dp，values-land 下 14dp：Material ActionBar 标题字号，横屏变小（出处：Android SDK 平台资源 data/res/values/dimens_material.xml 与 values-land/dimens_material.xml，text_size_title_material_toolbar（按应用的 compileSdk 取对应平台））
- action_bar_default_height_material：values 下 56dp，values-land 下 48dp：Material ActionBar 栏高（出处：Android SDK 平台资源 data/res/values/dimens_material.xml 与 values-land/dimens_material.xml，action_bar_default_height_material（按应用的 compileSdk 取对应平台））
- TextAppearance.Material.Widget.ActionBar.Title 的 textSize = @dimen/text_size_title_material_toolbar：标题字号从这个资源来（出处：Android SDK 平台资源 data/res/values/styles_material.xml，TextAppearance.Material.Widget.ActionBar.Title（按应用的 compileSdk 取对应平台））
- Material 主题的 actionBarSize = @dimen/action_bar_default_height_material：栏高从这个资源来（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material 的 actionBarSize（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 主题实际给 ActionBar 的各项资源，以及它们在限定目录里的覆盖：Android SDK 平台资源（按应用的 compileSdk 取平台）：values/themes_material.xml 里主题的 actionBarSize、actionBarStyle → styles_material.xml 里的标题 TextAppearance → dimens_material.xml；再在 values-land、values-sw600dp 等目录的 dimens_material.xml 按同名找；每个资源名列出默认、横屏、sw 覆盖值，有几档写几档分支；例：android-34 下 values-sw600dp 的栏高是 64dp
来源：1 张卡，1 个应用
- case-db3da49c14f06085f3b8（Sokoban）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断
