# GlanceTheme 的颜色迁成 color.json 时，取 Glance 库的回退色，不用 M3 基线近似

审的是：资源
触发（任一种）：
- 读到：源端用 GlanceTheme.colors.widgetBackground（或 GlanceTheme 的其他颜色角色）作背景或前景；写错的样子：base 或 dark 的 color.json 里写的是 Material 3 baseline 色（如 #FEF7FF、深色 #1C1B1F）或注明「近似」
适用范围：把 Glance 小部件用到的 GlanceTheme 颜色迁成鸿蒙 color.json（浅色和深色两份）时
做法：
- 从应用依赖的 androidx.glance 版本的 aar 里取 res/values 与 res/values-night 中对应的 glance_color* 资源（背景是 glance_colorWidgetBackground），浅色写进 base/element/color.json，夜间写进 dark/element/color.json
- 取不到时在回报里登记待核，不拿别的设计体系基线代替
针对本应用要查的：
- 应用依赖的 Glance 版本里各颜色角色的回退值：Gradle 缓存里 androidx.glance 对应版本的 aar 解包目录，res/values/values.xml 和 res/values-night/values-night.xml，按 glance_colorWidgetBackground 等 glance_color* 资源名找；取 <color> 的值分别写进浅色和深色的 color.json；例：卡里查到的那个版本浅色 #E0F3FF、深色 #20333D
未核实：glance_colorWidgetBackground 的资源名和回退值本机没有核对到
来源：1 张卡，1 个应用
- case-77c6596fcdf362f9e832（Jetsnack）：做法第 1 步 ← 建议 7；做法第 2 步 ← 建议 7
