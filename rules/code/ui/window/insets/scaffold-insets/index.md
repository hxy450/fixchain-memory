# Compose Scaffold 外壳和内容区的顶部避让

agent 会看到什么：读过的 Compose 源码里宿主用 Scaffold（常只传 bottomBar，content 带 innerPadding）承载 tab 子页、子页和浮层；交回的根 Navigation 没隐藏标题栏、工具栏，或宿主 tab 内容区、子页、浮层的根节点上没有顶部 padding

## 通用查法

### 源端内容在 Scaffold innerPadding 内时，沿父链查顶部避让，没消费的那层补 padding top

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

## 规矩

- rule-c0d786f555e5｜根 Navigation 只作路由容器、栏位自绘时，hideTitleBar 和 hideToolBar 写 true｜读到：源端外壳没有系统标题栏或工具栏：Compose Scaffold 只传 bottomBar 和 snackbarHost（topBar 为空），自绘底部导航贴屏幕底；规格把 ComponentActivity 映射为 @Entry + Navigation(Stack) + pageMap；写错：根 Navigation 的属性链只有 .mode(NavigationMode.Stack).navDestination(...).expandSafeArea(...)，没有 .hideTitleBar(true) 和 .hideToolBar(true)；内容区比 NavBar 短一截，自绘底栏离屏幕底悬空
- rule-6714d58b1810｜宿主壳的 tab 内容区要显式写顶部 padding 消费状态栏，只靠 layoutWeight 不算消费｜读到：Scaffold(bottomBar = …) { padding -> … Modifier.padding(padding).consumeWindowInsets(padding) }，Scaffold 不传 topBar；写错：窗口全屏、根 Navigation 已 expandSafeArea，宿主的 tab 内容区却只有 .width('100%').layoutWeight(1)，没有 .padding({ top: … })；报告仍写「宿主已统一避让」
- rule-6713d74589fb｜子页收到接了线却没用的 statusBarHeight 时，父容器没加顶部避让就在根容器 padding.top 加上它｜读到：源端子页根布局 modifier.fillMaxSize().padding(24.dp)，modifier 由 Scaffold content 带着 innerPadding 传入；写错：目标子页声明了 @Param statusBarHeight 却没用，根容器只有 .padding(24)；注释写「No statusBarsPadding on Android」
- rule-aed49ed3eb38｜浮层组件挂在自窗口顶起的 Stack 时，接 statusBarHeight 并在根节点 padding top｜读到：Compose 浮层 Box(Modifier.fillMaxSize()) 里 scrim + 居中卡片，和列表、顶栏同在一个 Box，整体在 Scaffold innerPadding 之内；写错：浮层组件根 Stack 只有 .width('100%').height('100%')，没有顶部偏移；父页嵌入时只传回调，同一 Stack 的列表首项、顶栏却带了 statusBarHeight
- rule-a5125c68ee3b｜宿主已消费状态栏时，tab 子页的 spacer 不再加状态栏高度，悬浮顶栏与列表同一基准｜读到：子页源码 Spacer(Modifier.windowInsetsTopHeight(WindowInsets.statusBars.add(WindowInsets(top = N.dp)))) 或 Spacer(Modifier.statusBarsPadding())，宿主已 consumeWindowInsets；写错：子页首项 spacer 写成 .height(顶部避让值 + N)，或顶部多一个 Column().height(顶部避让值)；悬浮顶栏从 y=0 起不带避让
- rule-1b93619709cb｜子组件按约定豁免 Layer 3 时，Tab 宿主给内容区和抽屉面板补顶部和底部避让｜读到：页面规格 needs_immersive_safearea=true；沉浸约定的责任分层表写子组件/overlay 不订阅窗口避让、安全区由宿主全屏页统一负责（子组件豁免 Layer 3）；写错：Tab 宿主头注释写「Tab 内容区顶部避让由各 Tab 页自行处理」，内容区 Stack 和抽屉面板 Column 都没有 .padding({ top: windowTopPadding })；Tab 子页又写「由宿主统一处理」
