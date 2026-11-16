# 复刻 NavigationView 默认外观时，在 color.json 登记选中底色、未选图标色和分隔线色

审的是：资源
触发（任一种）：
- 读到：NavigationView 没写 itemIconTint、itemBackground，菜单项外观来自 Material 默认样式；写错的样子：目标 element/color.json 没有菜单项选中底色、未选图标着色、分隔线色的键，抽屉只复用已有的主色、black 和近名灰
适用范围：为自定义抽屉复刻 NavigationView 默认外观、往目标颜色资源里登记状态色时
做法：
- 新增三个颜色键：选中底（白底约 #E0E0E0）、未选图标（#99000000）、组间分隔线，抽屉行引用这些键，不借名字相近的已有灰色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 选中底 #E0E0E0；未选图标 #99000000：返修新增颜色键的取值（出处：卡里修好并验证过）
- list_divider_opacity_material = #1f000000：分隔线 listDivider 的不透明度（浅色主题下配黑色）（出处：Android SDK 平台资源 data/res/values/colors_material.xml，list_divider_opacity_material（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 深色模式下的对应取值：源工程是否有 values-night 主题；平台 data/res/values/themes_material.xml 里深色主题的 colorForeground 和 colorListDivider；有深色模式就在 dark/element/color.json 里给同名键填深色主题解析出的值
来源：1 张卡，1 个应用
- case-cee85a6c89d26db1ef48（Privacy Friendly 2048）：做法第 1 步 ← 建议 1、诊断；取值 1 ← 诊断
