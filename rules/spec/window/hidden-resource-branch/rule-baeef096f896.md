# 源端分支依赖隐藏 API 或系统资源时，规格写可观察条件和效果，找目标等价信号，不删行为

审的是：规格
触发（任一种）：
- 读到：源端按隐藏系统资源判断（如读 config_navBarInteractionMode 的 isUsingGestures），非手势导航时 setNavigationBarColor(…) 给导航栏着色；写错的样子：规格以「检测用的隐藏资源无对等」为由把检测分支和着色整体删除，相关验收条目被标为 superseded
适用范围：规格阶段处理依赖隐藏 API、系统资源才能检测的源端行为时
做法：
- 先写出用户可观察的条件和效果（如「三键导航栏存在时，导航栏涂源端的颜色和透明度」）
- 再写目标平台的可观测等价信号：getWindowAvoidArea(AvoidAreaType.TYPE_SYSTEM).bottomRect.height > 0 判定三键导航，用 setWindowSystemBarProperties 的 navigationBarColor 着色；「检测手段无对等」不推出「行为删除」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getWindowAvoidArea(type: AvoidAreaType): AvoidArea：取某类避让区（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getWindowAvoidArea）
- AvoidAreaType.TYPE_SYSTEM = 0（Default area of the system）：系统栏避让区，三键导航栏在它的底部（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，AvoidAreaType.TYPE_SYSTEM）
- usingGestures = TYPE_SYSTEM.bottomRect.height === 0；非手势时按源端颜色着色导航栏：用避让区高度代替隐藏资源判断导航方式（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-01833db0536ba02ed2ce（Cofi）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 3 ← 诊断
