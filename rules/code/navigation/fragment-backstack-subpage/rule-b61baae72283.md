# 源端每次 replace 新 Fragment 时，目标用 pushPath 加 NEW_INSTANCE

审的是：代码
触发（任一种）：
- 读到：已有详情 Fragment 时先 popBackStackImmediate() 再 replace(…, new 出来的 Fragment)，否则 replace + addToBackStack；每次都是新实例；写错的样子：同一轮里 navPathStack.pop() 后 pushPathByName(同名页, param)，或只写 pushPathByName 并注释「addToBackStack 由 NavPathStack 天然保留」；同名 NavDestination 被栈复用，新页 onReady 不触发
适用范围：把 FragmentTransaction 的 replace / addToBackStack / popBackStackImmediate 分支映射到 NavPathStack 时（LaunchMode 声明 @since 12）
做法：
- 先按分支列出源端每个事务调用点，逐条对应；恒新实例的分支写成 navPathStack.pushPath(new NavPathInfo('<页名>', param), { launchMode: LaunchMode.NEW_INSTANCE })
- 注释写「退化为 pop」「由 NavPathStack 天然保留」的分支算没实现，登记占位，不当作等价
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- pushPath(info: NavPathInfo, options?: NavigationOptions): void：按 NavPathInfo 入栈，第二个参数定栈操作模式（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPath）
- LaunchMode.NEW_INSTANCE = 3：新建 NavDestination 实例，不复用栈里同名的实例：对应源端每次 new 一个 Fragment（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，LaunchMode.NEW_INSTANCE）
- NavigationOptions.launchMode 默认 LaunchMode.STANDARD：不写 options 时走默认模式（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavigationOptions.launchMode）
- constructor(name: string, param: unknown, onPop?: Callback<PopInfo>, isEntry?: boolean)：NavPathInfo 的构造（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathInfo.constructor）
- popBackStackImmediate 在调用内立即执行出栈：源端先出栈再 replace 是同步完成的，目标端要换成新实例入栈（出处：android.app.FragmentManager#popBackStackImmediate）
- 同一轮 pop + pushPathByName 时复用了栈中同名 NavDestination，新页 onReady 不触发；改为 pushPath + NEW_INSTANCE 后修好：卡里观察到的行为和修法（出处：卡里修好并验证过）
- replacePath(info: NavPathInfo, options?: NavigationOptions): void：同族接口：替换栈顶，同样可传 launchMode（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.replacePath）
- pushDestination(info: NavPathInfo, options?: NavigationOptions): Promise<void>：同族接口：带结果的入栈（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushDestination）
未核实：复用同名页、onReady 不触发是在 API 24（HarmonyOS 6.1.1）上观察到的，本机按 API 23 核对声明
来源：1 张卡，1 个应用
- case-aebac48fa7acdb86e57e（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 6 ← 诊断
