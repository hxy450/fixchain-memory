# 源端内容在 Scaffold innerPadding 内时，沿父链查顶部避让，没消费的那层补 padding top

审的是：代码
触发（任一种）：
- 读到：Compose Scaffold(topBar / bottomBar …) { innerPadding -> … } 承载的内容区、子页或浮层，内容从 innerPadding 之内起排；写错的样子：目标窗口全屏、根容器 expandSafeArea，这一层根节点没有 .padding({ top: … })，往上的父容器也没有哪一层加过顶部避让
适用范围：目标端窗口全屏或根容器 expandSafeArea、前景各层自己补状态栏避让，迁 Scaffold 承载的宿主、子页和浮层时
做法：
- 从这一层往上逐层看目标父容器（根 Navigation、宿主 tab 内容区、同一 Stack 的兄弟层）谁写了 .padding({ top: … })；Scaffold 的 innerPadding 每一边都对到宿主代码里确有的 padding 或底栏占位
- 父链上都没消费时，在这一层根节点写 .padding({ top: <顶部避让值> + <源端顶部 padding> })，其余三边照源端；子组件用 @Param statusBarHeight 接值，嵌入时传和兄弟层同一个值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- expandSafeArea(types?: Array<SafeAreaType>, edges?: Array<SafeAreaEdge>): T；默认 types 为 SYSTEM、CUTOUT、KEYBOARD，edges 为四边：根容器扩展到安全区后，内容从 y=0 起，前景要自己补 padding（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.expandSafeArea）
- padding(value: Padding | Length | LocalizedPadding): T，默认 0：传 Padding 对象可逐边给值（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding）
针对本应用要查的：
- 顶部避让值（状态栏高度）从哪里取：目标工程里发布窗口避让值的模型或 AppStorage 键（搜 getWindowAvoidArea、on('avoidAreaChange')）；用它发布的顶部值（已换成 vp 的那一个），宿主、子页、浮层都引用同一个
- 父链上哪一层已经消费了顶部避让：目标工程里从这个组件往上的各级 .ets：@Entry 页、根 Navigation、宿主 tab 内容区、同一 Stack 的兄弟层；看各层修饰链有没有 .padding({ top: … })；兄弟层（列表首项、顶栏）带了 statusBarHeight 而这一层没带，就是漏了
未核实：statusBarHeight 的单位按父页传入的口径，卡里没写明是 vp 还是 px
来源：3 张卡，1 个应用
- case-049d48a5d4b79983dde3（Jetsnack）：做法第 2 步 ← 建议 3
- case-b4d0b2f21cf92275a46b（Jetsnack）：做法第 2 步 ← 建议 3
- case-cfab70f115f2d290e44a（Jetsnack）：做法第 1 步 ← 建议 2
