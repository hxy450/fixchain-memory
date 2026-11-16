# 构造期从主题属性取色的自绘 View，迁移时把取色写成可重入方法，主题变化时重取并重绘

审的是：代码
触发（任一种）：
- 读到：自定义 View 在构造或 setup() 里用 obtainStyledAttributes / 主题属性取色，设给 Paint；写错的样子：目标端只在 aboutToAppear 里 getColorSync 一次存成字符串（strokeColor 等），没有主题或配置变化时的重解析和重绘路径；其他组件以它为先例照抄
适用范围：把构造期按主题取色的安卓自绘 View 迁成 ArkUI Canvas 组件、应用支持主题切换时
做法：
- 把取色写成方法 resolveColors()：用覆写 colorMode 的资源管理器取色后触发重绘；aboutToAppear 调一次
- 监听主题状态（@Watch 或 @Monitor 订阅主题态）和环境配置变化，变化时再调 resolveColors() 并重绘；落盘前补齐，因为组件会被当作先例复用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Context.obtainStyledAttributes：从这个 Context 的主题里取样式属性：源端颜色取自当前主题，换主题重建后会重取（出处：android.content.Context#obtainStyledAttributes）
- 进度环和章节条加上环境回调与主题态监听、改用覆写 colorMode 的资源管理器后，切主题时颜色正确：验证过的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-e1b1f9786e31a8d527cc（AntennaPod）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4、诊断；取值 2 ← 诊断
