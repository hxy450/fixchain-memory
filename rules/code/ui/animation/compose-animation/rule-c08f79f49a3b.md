# NavHost 自定义转场迁成 customNavContentTransition 加页面绑定，常量要有消费点

审的是：代码
触发（任一种）：
- 读到：源 NavHost 的 enterTransition / exitTransition / popEnterTransition / popExitTransition 写了 scaleIn、slideIn、scaleOut、slideOut 和 tween 时长；写错的样子：Navigation 上没有 .customNavContentTransition(...)，只定义了一个没人引用的转场常量类，注释写「已知近似」
适用范围：源 Compose NavHost 自定义页面转场迁成 ArkUI Navigation/NavDestination 时
做法：
- Navigation 设 .customNavContentTransition((from, to, operation) => ({ timeout, transition: (proxy) => { animateTo 按源端时长、延迟改共享状态，结束时 proxy.finishTransition() } }))；各 NavDestination 根上把 .opacity()/.translate()/.scale() 绑到共享 @ObservedV2 状态
- 自检：为对齐源定义的转场常量至少有一个实际消费点；没被 Navigation 或页面使用的常量类不算完成的近似
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- customNavContentTransition(delegate: (from: NavContentInfo, to: NavContentInfo, operation: NavigationOperation) => NavigationAnimatedTransition | undefined): NavigationAttribute：Navigation 的自定义转场入口（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavigationAttribute.customNavContentTransition）
- NavigationAnimatedTransition：timeout?: number；transition: (transitionProxy: NavigationTransitionProxy) => void；onTransitionEnd?：回调返回的转场对象（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavigationAnimatedTransition）
- finishTransition(): void：NavigationTransitionProxy 结束自定义转场（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavigationTransitionProxy.finishTransition）
- NavContentInfo 只有 name、index、mode、param、navDestinationId，没有透明度、位移字段：页面外观要由页面自己绑定共享状态（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavContentInfo）
- 新增转场常量文件、Navigation 接入 customNavContentTransition、各 NavDestination 绑定 translate/opacity/scale 后与源端一致：修法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端转场的时长、延迟、缩放和位移量：源工程 NavHost 所在 Kotlin 文件里四个 transition 参数，以及它引用的导航工具文件里的时长常量和偏移计算；逐值读出，作为共享状态动画的 duration、delay 和起止值
未核实：卡里观察到的行为出自鸿蒙 SDK API 24（6.1.1），本机核实用 API 23
来源：1 张卡，1 个应用
- case-7d5b3583abd06943248f（Cofi）：做法第 1 步 ← 诊断；做法第 2 步 ← 建议 4；取值 5 ← 诊断
