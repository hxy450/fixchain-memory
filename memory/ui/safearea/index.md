# ui/safearea

沉浸式安全区：全屏布局下前景避让与 expandSafeArea 的区别，避让区测量与 px/vp 换算（状态栏、导航指示条），系统栏图标深浅，路由页内容原点与顶部 inset 的消费位置，Compose Scaffold innerPadding 的顶部 inset 由宿主还是子页消费，向子页与页内浮层下发的状态栏高度参数，Tab 宿主按各 Tab 沉浸设置处理顶部安全区（含嵌入页状态栏占位的背景延伸与前景避让分层），全屏页底部按钮、按键区与贴底弹层的避让及承载层，逐页落实前景避让，状态栏实色避让带的承载层（Tabs 宿主包进外层 Column）

[上一级](../index.md)

## 本级经验

- [Compose Scaffold 无 topBar 时 innerPadding 顶部就是状态栏 inset：目标端只在一处落实，同一内容区各层用同一基准](lesson-f64afc22d41b130f1628.lesson.md)
  - 时机：规格提取与界面实现阶段，把 Compose Scaffold 的 content padding 与 consumeWindowInsets 拆成宿主壳与各子页（含页内浮层）的顶部避让分工时
  - 情境：源端 Scaffold 不传 topBar、未覆写 contentWindowInsets（默认含状态栏），把 Modifier.padding(innerPadding).consumeWindowInsets(innerPadding) 交给嵌套内容；子页自身可能没有 statusBarsPadding，也可能另写 statusBarsPadding 或 windowInsetsTopHeight(statusBars + N)；目标端全屏窗口，由宿主 padding 或向子页下发状态栏高度来避让。
  - 例外：Scaffold 传了 topBar 或覆写了 contentWindowInsets 时，innerPadding 顶部不再等于状态栏高，按实际来源推导
- [Tab 宿主不给承载全部 Tab 的内容区统一加顶部安全区：按各 Tab 源 Fragment 的状态栏处理分别落实，背景延伸的 Tab 只让前景避让；只加在底栏的 padding 只加到 tabBar](lesson-48e9408812c28e934db8.lesson.md)
  - 时机：规格与界面实现阶段，实现 MainActivity/Tab 宿主的内容区内边距、为作为 Tab 子组件的 Fragment 写安全区分工或转换其顶部布局时
  - 情境：Android 主 Activity 以 ViewPager/Tab 承载多个 Fragment，主题 windowTranslucentStatus 或 ImmersionBar 让状态栏透明；各 Fragment 自行决定是否为状态栏让位：有的头图直接铺到状态栏下（未设 statusBarView，或用 titleBarMarginTop/fitsSystemWindows），有的在顶对父容器的背景上放一个由 statusBarView 撑成状态栏高度的占位 View（如 v_status_bar），只把前景内容约束在占位之下；MainActivity 的内边距可能只加在底栏容器上。目标用单个宿主页承载各 Tab，可能给承载全部 Tab 槽位的容器统一加顶部 windowTopPadding 和左右 padding；页面规格按 page_type（sub_component）标“无需沉浸”，或把页内占位概括成“安全区由宿主统一处理”。
- [getWindowAvoidArea 与 windowRect 的数值是 px：写入供 padding 消费的窗口模型前先 px2vp](lesson-cf111aadb8804649b578.lesson.md)
  - 时机：沉浸式安全区实现阶段，在 EntryAbility 或窗口服务里把避让区、窗口尺寸写进共享窗口模型时
  - 情境：目标用 setWindowLayoutFullScreen(true) 全屏，EntryAbility 通过 getWindowAvoidArea 取状态栏、导航条高度，通过 getWindowProperties().windowRect 取窗口尺寸，写入 AppStorageV2 共享的窗口模型；各页把这些值直接放进 .padding()/.height()，按 vp 解释。
- [全屏窗口下先确认路由页的内容原点：已在状态栏 inset 之下就只补源端顶距的剩余部分，背景需延伸到状态栏时在背景节点自身 expandSafeArea](lesson-c7ee1769ca29abd236d3.lesson.md)
  - 时机：界面实现阶段，为全屏窗口中的路由页（NavDestination/HMRouter 页，含 Tab 子页）确定顶部起点、状态栏 inset 的消费位置以及背景是否延伸到状态栏时
  - 情境：Android 页面在透明状态栏下用自屏幕顶部起算的固定顶距（layout_marginTop、getStatusBarsHeight）给顶栏留位，背景铺到状态栏后面；目标 EntryAbility 全屏并发布 windowTopPadding，入口只在 Navigation 宿主上 expandSafeArea(TOP)，页面经路由框架承载。
- [全屏窗口的底部避让：导航指示条取 bottomRect，贴底按钮、按键区、Tab 栏与 bindSheet 内容都让出避让值（原高度已含底部留白时先抵扣），并加在占据屏幕底边的那一层](lesson-0e1c846868f2683cc280.lesson.md)
  - 时机：沉浸式安全区实现阶段，测量导航指示条避让区，并为底部按钮行、按键区、Tab 栏或贴底弹层确定底部间距及承载它的容器层时；为已有固定高度（含内容下方留白）的底部 Tab 栏或底部定位元素补导航条避让时
  - 情境：目标页面在 setWindowLayoutFullScreen(true) 下用 getWindowAvoidArea 测避让值，写入页面或全局窗口模型；Android 源布局的底部按钮行、底部 sheet 没有导航栏间距（源窗口不延伸到导航栏下，BottomSheetDialog 由系统处理 inset）。或页面规格标注全屏页、需要沉浸式安全区，入口对 BOTTOM 边 expandSafeArea，根容器与底部内容层背景色不同。 也包括底部 Tab 栏原固定高度已在图标文字下方留有空白，避让值取自 TYPE_NAVIGATION_INDICATOR 的单一 px 快照、不区分三键与手势模式，用户只报告某一种导航模式被遮挡。
- [向子页或页内浮层下发状态栏高度参数时写明消费方式，挂在同一 Stack 的每一层都拿到它](lesson-2cf2614847a8dba832b3.lesson.md)
  - 时机：派工与界面实现阶段，向子页、页内浮层下发状态栏高度参数，或把浮层挂进从窗口顶起的宿主 Stack 时
  - 情境：宿主页采用“子页自理”分工，以组件参数下发状态栏高度；子页或浮层（遮罩 + 居中卡片、铺满父容器）与列表、顶栏同挂一个 Stack；派工或槽位契约可能只列出回调参数，或写“接收但本页不使用”。
  - 例外：目标父容器已替该层加了顶部避让，且能指出对应代码位置
- [开启全屏布局后，前景按测得的避让区补 padding；expandSafeArea 只让背景越过安全区，不是避让](lesson-a8452bfea5d42d3dcae3.lesson.md)
  - 时机：界面实现阶段，为调用 setWindowLayoutFullScreen(true) 的入口壳（根 Navigation + Tabs/NavDestination）落实状态栏与底部导航条避让时
  - 情境：规格或 ui-manifest 标注全屏页、需要沉浸式安全区，并把 API 细节委托给具名 skill（如 arkts-immersive-safearea）；EntryAbility 开启全屏布局，页面标题由 NavDestination 标题栏或自绘标题承担；源端通常是 enableEdgeToEdge 加 safeDrawingPadding。
- [状态栏实色避让带挂在只承担避让的外层 Column：宿主是 Tabs 时把 Tabs 包进该 Column，不在 Tabs 上挂 padding 加背景色](lesson-fe10bd2491ca4ba82cb5.lesson.md)
  - 时机：界面实现或修复阶段，为带 Tabs 等子页铺满容器的主框架页补源端状态栏实色带，决定避让 padding 与背景色挂在哪个组件时
  - 情境：源 Activity 基类在 onCreate 设置实色状态栏；目标全屏布局，用测得的顶部避让值做 padding；宿主页的避让 padding 写在 Tabs（或 Swiper）上，TabContent 是满铺白底子页；工程其他页面已用“padding + 背景色挂在只包标题条的普通 Column”实现同一色带。
- [系统栏图标深浅按源端状态栏配置设置，不照搬沉浸式模板的浅色文字默认值](lesson-824031d5fddf81036b54.lesson.md)
  - 时机：沉浸式窗口配置阶段，调用 setWindowSystemBarProperties 设置 statusBarContentColor/navigationBarContentColor 时
  - 情境：目标全屏窗口把系统栏背景设为透明，页面内容延伸到状态栏下；Android 源端 BaseActivity/主题用 ImmersionBar darkMode(true)、windowLightStatusBar 或白色状态栏配深色图标；沉浸式 skill 示意写“透明背景 + 浅色文字”。
