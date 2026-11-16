# Compose 主题的深浅色和动态配色状态

agent 会看到什么：读到 @Composable 主题函数按 isSystemInDarkTheme()、DataStore 里的外观开关或 dynamicLightColorScheme / dynamicDarkColorScheme 选配色；产物里的主题状态类、EntryAbility 里的同步和 setColorMode、wallpaper.getColors 调用

## 规矩

- rule-a2ba4969e47b｜跟随系统深浅的主题，状态放 @ObservedV2 的 @Trace 字段并在入口两处同步｜读到：Compose 主题 Theme(darkTheme = isSystemInDarkTheme()) 选 Light / Dark 两套颜色，经 CompositionLocal 下发，组件在组合期读取；写错：主题层用模块级 `let` 布尔变量加一个同步函数存深浅状态（UI 不观察），注释只写「由宿主 EntryAbility 调用」；全工程 EntryAbility 的 onCreate / onConfigurationUpdate 里没有调用这个同步函数
- rule-4f6ebbbdb8bc｜外观开关驱动的主题状态用 @ObservedV2/@Trace，带写入与应用路径，入口重放｜读到：源端设置开关由 DataStore 持久化，并被 @Composable 主题函数实时读取；基础计划写「主题令牌支持 light/dark/dynamic」；写错：目标的主题状态类只有默认值字段，没有 @ObservedV2 / @Trace、没有写入方法，也没有任何地方调 setColorMode 或应用调色板
- rule-5258c1c010c0｜源端动态取色迁移时用 wallpaper.getColors 取主色做种子，失败回退固定配色｜读到：Compose 主题里 SDK_INT >= S 且开关打开时用 dynamicLightColorScheme(context) / dynamicDarkColorScheme(context)，否则用固定 scheme；设置行 enabled = Build.VERSION.SDK_INT >= Build.VERSION_CODES.S；写错：目标主题只按 isDark 二值返回固定 Palette，没有 wallpaper.getColors 调用；动态主题开关恒可用、只写偏好、无视觉效果
- rule-2d3120cb0847｜负责主题运行时的切片交付界面 build 可直接读的全局响应式主题状态｜读到：源端用 MaterialTheme（CompositionLocalProvider）包裹全树、按色板 × 明暗 × 字号计算 colors 与 typography；规格写主题「共享至全部页面」「变更即重算」；写错：主题控制器只把解析出的主题包发到没有界面订阅的状态流，界面 build 里没有可读的全局主题状态（没有 @ObservedV2 / @Trace 一类可观测状态）
