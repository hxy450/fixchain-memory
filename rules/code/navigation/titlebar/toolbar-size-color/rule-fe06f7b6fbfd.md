# 标题栏溢出钮按 Material 溢出钮样式分侧取内距，不按最小宽对称近似

审的是：代码
触发（任一种）：
- 读到：源主题是 Theme.Material 系的窗口 ActionBar，菜单有进溢出的项；写错的样子：溢出钮按 action_button_min_width_overflow_material 对称取左右 padding
适用范围：自绘标题栏还原 Material 窗口 ActionBar 的溢出钮时
做法：
- 溢出钮宽 = actionOverflowButtonStyle 的 paddingStart + 图标宽 + paddingEnd，左右分别写，不取对称值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.Material.ActionButton.Overflow：paddingStart=@dimen/action_bar_overflow_padding_start_material（6dp），paddingEnd=@dimen/action_bar_overflow_padding_end_material（10dp），minWidth=36dp：溢出钮左右内距不对称（出处：Android SDK 平台资源 data/res/values/styles_material.xml，Widget.Material.ActionButton.Overflow；data/res/values/dimens_material.xml（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 源主题实际用的溢出钮样式：Android SDK platforms/android-<compileSdk>/data/res/values/themes_material.xml 里源主题的 actionOverflowButtonStyle，再到 styles_material.xml 和 dimens_material.xml；顺着样式的 paddingStart、paddingEnd、minWidth 引用解到 dp 值
来源：1 张卡，1 个应用
- case-45b40cf92799928188ab（Sokoban）：做法第 1 步 ← 建议 5
