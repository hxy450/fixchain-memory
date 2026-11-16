# 源端 NavHost 有自定义转场时，规格写可实现的承载机制和要改的页面，不给默认动画分支

审的是：规格
触发（任一种）：
- 读到：源 NavHost 写了 enterTransition / exitTransition / popEnterTransition / popExitTransition（如 scaleIn + slideIn、scaleOut + slideOut，带时长、延迟、缩放值）；写错的样子：规格把转场映射写成「NavDestination 系统转场 + 自定义参数近似（customNavContentTransition 或默认动画参数调优）」，验收判据只核转场常量与源逐值相等，没写页面绑定义务
适用范围：规格提取时写源端页面转场在目标端的承载机制和验收判据
做法：
- 规格写出机制：Navigation 设 customNavContentTransition，各 NavDestination 页面把 .opacity()/.translate()/.scale() 绑到共享转场状态，由转场回调里 animateTo 驱动；列出要改动的文件（各 NavDestination 页面），各参数逐值取自源端；不写「或默认动画」
- 验收判据写：Navigation 确实设置了 customNavContentTransition 且各页消费了共享状态；只核常量存在不算接入
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- customNavContentTransition(delegate: (from: NavContentInfo, to: NavContentInfo, operation: NavigationOperation) => NavigationAnimatedTransition | undefined): NavigationAttribute：Navigation 的自定义页面转场入口（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavigationAttribute.customNavContentTransition）
- NavContentInfo 只有 name、index、mode、param、navDestinationId，没有透明度、位移字段：转场回调里改不了页面外观，必须由页面自己绑定共享状态（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavContentInfo）
- 接入 customNavContentTransition、各 NavDestination 绑定 translate/opacity/scale 状态后与源端转场一致：修法（出处：卡里修好并验证过）
未核实：卡里观察到的行为出自鸿蒙 SDK API 24（6.1.1），本机核实用 API 23
来源：1 张卡，1 个应用
- case-7d5b3583abd06943248f（Cofi）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 3 ← 诊断
