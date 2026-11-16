# 要恢复页面栈时，Navigation 设 id 和 recoverable，每个 NavDestination 也设

审的是：代码
触发（任一种）：
- 读到：规格要求进程回收后恢复页面栈，或源宿主用 rememberNavController + NavHost / onCreate(savedInstanceState)；写错的样子：根 Navigation(pathStack) 上没有 .id(...) 和 .recoverable(true)；各页的 NavDestination() 上没有 .recoverable(true)
适用范围：实现阶段装配根 Navigation 和各页 NavDestination，需要进程回收后恢复路由栈时（recoverable 声明 @since 14）
做法：
- 根 Navigation 加通用属性 .id('…') 和 .recoverable(true)
- 每个 NavDestination 加 .recoverable(true)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- recoverable(recoverable: Optional<boolean>): NavigationAttribute；默认 false，要先设 Navigation 的 id：Navigation 在进程异常退出后重新冷启时恢复到退出时的路由栈（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavigationAttribute.recoverable）
- recoverable(recoverable: Optional<boolean>): NavDestinationAttribute；默认 false，要和 Navigation 的 recoverable 一起用：同族接口：NavDestination 的可恢复（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.recoverable）
- 根 Navigation 加 id 与 recoverable(true)，各 NavDestination 在 hideTitleBar(true) 后加 recoverable(true)：修好的做法（还需配合 UIAbility 的备份恢复）（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-30dbf63ea8a03d315607（Cofi）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 3 ← 诊断
