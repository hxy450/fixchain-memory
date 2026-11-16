# 根 Navigation 扩展安全区时，NavDestination 隐藏系统标题栏并自绘工具栏

审的是：代码
触发（任一种）：
- 读到：规格把源端 ActionBar / Toolbar 映射为「NavDestination 自带标题栏」，根 Navigation 已有或将有 expandSafeArea；写错的样子：NavDestination 保留了 .title(...) 系统标题栏，前景只加 bottom padding，测得的 windowTopPadding 没用在任何前景上
适用范围：根 Navigation 四向 expandSafeArea 下需要标题栏的 NavDestination 全屏页
做法：
- 写 NavDestination() { … }.hideTitleBar(true)，在页内自绘工具栏行（返回键、标题）
- 根容器 .padding({ top: windowModel.windowTopPadding, bottom: windowModel.windowBottomPadding })；没在 Layer 2 生效状态下实测过的，不预设系统标题栏会自动避让
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- hideTitleBar(value: boolean): NavDestinationAttribute：关闭 NavDestination 的系统标题栏（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.hideTitleBar）
- hideTitleBar(hide: boolean, animated: boolean): NavDestinationAttribute：同一接口带动画开关的重载（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.hideTitleBar）
- hideTitleBar(true) + 自绘工具栏行，根容器取 windowTopPadding / windowBottomPadding 后标题栏不再叠进状态栏：修复后的写法（出处：卡里修好并验证过）
未核实：系统标题栏在四向 expandSafeArea 下叠进状态栏，依据是修复会话截图，卡里没查官方避让规则
来源：1 张卡，1 个应用
- case-b4a2f2d65e01a68393e3（AntennaPod）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 3 ← 诊断
