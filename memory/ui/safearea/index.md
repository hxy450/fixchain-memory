# ui/safearea

沉浸式安全区：全屏布局下前景避让与 expandSafeArea 的区别，避让区测量与 px/vp 换算（状态栏、导航指示条），系统栏图标深浅（按源端浅色状态栏标志推导），源根视图自设状态栏 padding 与底色时由页面容器承载（系统栏透明），路由页内容原点与顶部 inset 的消费位置，Compose Scaffold innerPadding 的顶部 inset 由宿主还是子页消费，向子页与页内浮层下发的状态栏高度参数，Tab 宿主按各 Tab 沉浸设置处理顶部安全区（含嵌入页状态栏占位的背景延伸与前景避让分层），全屏页底部按钮、按键区与贴底弹层的避让及承载层，逐页落实前景避让，状态栏实色避让带的承载层（Tabs 宿主包进外层 Column），自绘标题栏按源端避让来源接入 topInset（固定高度含内距、顶距与 inset 只取一份），页面级避让订阅取承载页面的主窗口；三键与手势导航的判定、按导航方式给导航栏着色、底部避让取两类避让区的较大值，以及页面级软键盘避让模式（adjustResize/imePadding）

[上一级](../index.md)

## 本级经验

- [Compose Scaffold 无 topBar 时 innerPadding 顶部就是状态栏 inset：目标端只在一处落实，同一内容区各层用同一基准](lesson-f64afc22d41b130f1628.lesson.md)
  - 时机：规格提取与界面实现阶段，把 Compose Scaffold 的 content padding 与 consumeWindowInsets 拆成宿主壳与各子页（含页内浮层）的顶部避让分工时
  - 情境：源端 Scaffold 不传 topBar、未覆写 contentWindowInsets（默认含状态栏），把 Modifier.padding(innerPadding).consumeWindowInsets(innerPadding) 交给嵌套内容；子页自身可能没有 statusBarsPadding，也可能另写 statusBarsPadding 或 windowInsetsTopHeight(statusBars + N)；目标端全屏窗口，由宿主 padding 或向子页下发状态栏高度来避让。
  - 例外：Scaffold 传了 topBar 或覆写了 contentWindowInsets 时，innerPadding 顶部不再等于状态栏高，按实际来源推导
- [Tab 宿主不给承载全部 Tab 的内容区统一加顶部安全区：按各 Tab 源 Fragment 的状态栏处理分别落实，背景延伸的 Tab 只让前景避让；只加在底栏的 padding 只加到 tabBar](lesson-48e9408812c28e934db8.lesson.md)
  - 时机：规格与界面实现阶段，实现 MainActivity/Tab 宿主的内容区内边距、为作为 Tab 子组件的 Fragment 写安全区分工或转换其顶部布局时
  - 情境：Android 主 Activity 以 ViewPager/Tab 承载多个 Fragment，主题 windowTranslucentStatus 或 ImmersionBar 让状态栏透明；各 Fragment 自行决定是否为状态栏让位：有的头图直接铺到状态栏下（未设 statusBarView，或用 titleBarMarginTop/fitsSystemWindows），有的在顶对父容器的背景上放一个由 statusBarView 撑成状态栏高度的占位 View（如 v_status_bar），只把前景内容约束在占位之下；MainActivity 的内边距可能只加在底栏容器上。目标用单个宿主页承载各 Tab，可能给承载全部 Tab 槽位的容器统一加顶部 windowTopPadding 和左右 padding；页面规格按 page_type（sub_component）标“无需沉浸”，或把页内占位概括成“安全区由宿主统一处理”。
- [getWindowAvoidArea 与 windowRect 的数值是 px：在 windowStage.loadContent 成功回调里取 UIContext、先 px2vp 再写入供 padding 消费的窗口模型（loadContent 之前调 getUIContext 抛 1300002）](lesson-cf111aadb8804649b578.lesson.md)
  - 时机：沉浸式安全区实现阶段，在 EntryAbility 或窗口服务里把避让区、窗口尺寸写进共享窗口模型时；安排 EntryAbility.onWindowStageCreate 中依赖 UIContext 的步骤相对 loadContent 的时机时
  - 情境：目标用 setWindowLayoutFullScreen(true) 全屏，EntryAbility 通过 getWindowAvoidArea 取状态栏、导航条高度，通过 getWindowProperties().windowRect 取窗口尺寸，写入 AppStorageV2 共享的窗口模型；各页把这些值直接放进 .padding()/.height()，按 vp 解释。 也包括换算或其他依赖 UIContext 的步骤（如 setKeyboardAvoidMode）写在 onWindowStageCreate 中、位于 loadContent 调用之前或在其回调之外同步执行。
- [仅当源窗口本身延伸到系统栏下才做全屏沉浸与底部避让：导航指示条取 bottomRect，贴底按钮、按键区、Tab 栏与 bindSheet 内容都让出避让值（原高度已含底部留白时先抵扣），并加在占据屏幕底边的那一层；FLAG_FULLSCREEN 只隐藏状态栏，导航栏与旧应用的挖孔边、宽高比截边在窗口外](lesson-0e1c846868f2683cc280.lesson.md)
  - 时机：沉浸式安全区实现阶段，测量导航指示条避让区，并为底部按钮行、按键区、Tab 栏或贴底弹层确定底部间距及承载它的容器层时；为已有固定高度（含内容下方留白）的底部 Tab 栏或底部定位元素补导航条避让时；决定目标窗口是否全屏（沉浸式）、系统栏底色与是否做内容避让时；源端以 DisplayMetrics 等屏幕宽高定游戏几何、为目标确定几何基准时
  - 情境：目标页面在 setWindowLayoutFullScreen(true) 下用 getWindowAvoidArea 测避让值，写入页面或全局窗口模型；Android 源布局的底部按钮行、底部 sheet 没有导航栏间距（源窗口不延伸到导航栏下，BottomSheetDialog 由系统处理 inset）。或页面规格标注全屏页、需要沉浸式安全区，入口对 BOTTOM 边 expandSafeArea，根容器与底部内容层背景色不同。 也包括底部 Tab 栏原固定高度已在图标文字下方留有空白，避让值取自 TYPE_NAVIGATION_INDICATOR 的单一 px 快照、不区分三键与手势模式，用户只报告某一种导航模式被遮挡。也包括 Material3 BottomSheet 页面（库默认带 paddingBottomSystemWindowInsets）迁为 bindSheet，规格把“弹层跳过沉浸式处理”理解为自动避让。也包括规格要求手势与三键两种导航模式下内容都不被导航栏遮挡，而入口按沉浸式模板只以 TYPE_NAVIGATION_INDICATOR 测底部。 也包括源主题非全屏（Theme.Holo/Theme.Black 等，targetSdk 低，主题与代码都没有全屏或透明系统栏标志；requestWindowFeature(FEATURE_NO_TITLE) 只去标题栏），规格模板或页面元数据却按页面类型默认标注全屏页、需要沉浸式安全区。 也包括源 Activity 只用 FEATURE_NO_TITLE 加 FLAG_FULLSCREEN（或 windowFullscreen），未设导航栏延伸或隐藏标志，targetSdk 低（&lt;28 无法声明挖孔模式、&lt;26 未声明最大宽高比）；目标按沉浸式模板 setWindowSystemBarEnable(\[\]) 隐藏全部系统栏、各页根容器四向 expandSafeArea，或把源端 getDisplayMetrics() 的宽高换算成“全屏窗口高减底部避让”。
  - 例外：源窗口不延伸到系统栏下（主题与代码都没有 windowFullscreen、windowTranslucentStatus/Navigation、透明 statusBarColor、FLAG_FULLSCREEN、SYSTEM_UI_FLAG_LAYOUT_*、setDecorFitsSystemWindows(false)/enableEdgeToEdge，targetSdk&lt;35）：目标保持非全屏，按做法第 1 步处理，其余各步不适用
- [全屏窗口下先确认路由页的内容原点：已在状态栏 inset 之下就只补源端顶距的剩余部分，背景需延伸到状态栏时在背景节点自身 expandSafeArea](lesson-c7ee1769ca29abd236d3.lesson.md)
  - 时机：界面实现阶段，为全屏窗口中的路由页（NavDestination/HMRouter 页，含 Tab 子页）确定顶部起点、状态栏 inset 的消费位置以及背景是否延伸到状态栏时
  - 情境：Android 页面在透明状态栏下用自屏幕顶部起算的固定顶距（layout_marginTop、getStatusBarsHeight）给顶栏留位，背景铺到状态栏后面；目标 EntryAbility 全屏并发布 windowTopPadding，入口只在 Navigation 宿主上 expandSafeArea(TOP)，页面经路由框架承载。
- [向子页或页内浮层下发状态栏高度参数时写明消费方式，挂在同一 Stack 的每一层都拿到它](lesson-2cf2614847a8dba832b3.lesson.md)
  - 时机：派工与界面实现阶段，向子页、页内浮层下发状态栏高度参数，或把浮层挂进从窗口顶起的宿主 Stack 时
  - 情境：宿主页采用“子页自理”分工，以组件参数下发状态栏高度；子页或浮层（遮罩 + 居中卡片、铺满父容器）与列表、顶栏同挂一个 Stack；派工或槽位契约可能只列出回调参数，或写“接收但本页不使用”。
  - 例外：目标父容器已替该层加了顶部避让，且能指出对应代码位置
- [开启全屏布局前逐边核对源端系统栏：只沉浸状态栏（透明状态栏、未设 navigationBarColor、targetSdk≤34）时底部保留不透明导航栏底色；全屏后前景按测得的避让区逐边补 padding（顶部加在包住标题栏的层，底部加在伸到窗口底边的层）；expandSafeArea 只让背景越过安全区，预设系统标题栏也不会自动避让](lesson-a8452bfea5d42d3dcae3.lesson.md)
  - 时机：界面实现阶段，为调用 setWindowLayoutFullScreen(true) 的入口壳（根 Navigation + Tabs/NavDestination）落实状态栏与底部导航条避让、决定各边背景是否延伸时；转换承载内嵌子页的壳 NavDestination、移植 Android insets 代码，或入口根 Navigation 四向 expandSafeArea 后逐页核对时
  - 情境：规格或 ui-manifest 标注全屏页、需要沉浸式安全区，并把 API 细节委托给具名 skill（如 arkts-immersive-safearea）；EntryAbility 开启全屏布局，页面标题由 NavDestination 标题栏或自绘标题承担；源端通常是 enableEdgeToEdge 加 safeDrawingPadding。也包括源端只用 SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN 加透明 statusBarColor，没有 navigationBarColor、windowTranslucentNavigation、HIDE_NAVIGATION，targetSdk≤34：导航栏是不透明黑底，应用内容止于其上。也包括页面只给标题栏补了顶部避让，伸到窗口底边的内容（如按 min(宽,高) 取边长的棋盘）没有底部避让。也包括壳页承载声明豁免安全区、自绘工具栏的内嵌子页，源端顶部 inset 由子 Fragment 的 AppBarLayout 或 Toolbar 根布局 fitsSystemWindows 隐式消费；或 NavDestination 页保留预设系统标题栏。
- [源窗口按 adjustResize 避让软键盘（声明 adjustResize，或未声明 windowSoftInputMode 而窗口含可滚动视图）时设 KeyboardAvoidMode.RESIZE：各页都如此时在窗口级统一设置，否则在该页显示期间设置、离开时还原；不以默认 OFFSET 记作等价](lesson-f86b02e97cc77e31d51a.lesson.md)
  - 时机：页面实现阶段，为含文本输入的页面（编辑表单等 NavDestination 子页）落实源端软键盘避让方式时；为未声明 windowSoftInputMode 的含输入框窗口确定目标避让方式时
  - 情境：源 Activity 声明 windowSoftInputMode=adjustResize，页面在滚动内容或尾部用 imePadding 让键盘弹出时内容区收缩、仍可滚到末项；规格或页面元数据写明 adjustResize + imePadding 并要求等价避让；目标未设键盘避让模式，转换者不确定默认行为是否等价。 也包括源 Activity 未声明 windowSoftInputMode、内容含 ListView/ScrollView（平台隐式 adjustResize），规格只写“默认弹出”，召回因“源端未声明 adjustResize”而排除了本条。
- [源端只在三键导航时给导航栏着色：以 TYPE_SYSTEM 底部避让高度判定导航方式，非手势时用 navigationBarColor 着色并随避让区变化更新](lesson-8bc258c2833be65f4fcd.lesson.md)
  - 时机：规格提取与入口窗口实现阶段，把源 Activity 按导航方式设置导航栏颜色的分支映射到目标窗口系统栏属性时
  - 情境：源端在 Activity 中按是否手势导航决定导航栏底色（如非手势导航时 setNavigationBarColor(背景色带透明度)），判定依赖隐藏系统资源（config_navBarInteractionMode）或系统设置；目标为全屏沉浸窗口，入口用 getWindowAvoidArea 测避让区、用 setWindowSystemBarProperties 设置系统栏。
- [源端给根视图设状态栏高度的顶部 padding 并自绘底色时：目标在页面容器上设 padding 与背景色、系统栏保持透明，子内容按扣除状态栏后的尺寸布局](lesson-baf0ca22a69e7b76f636.lesson.md)
  - 时机：规格提取与界面实现阶段，把源端根视图（DecorView 或内容根）的状态栏 insets padding 与背景设色翻译为目标页面的避让方式和状态栏底色时
  - 情境：源 Activity（常见于 Android 15+ 边到边分支）给 DecorView 或根布局 setBackgroundColor，并 setPadding(top = 状态栏 inset)，内容 View 在 onSizeChanged 中按自身宽高布局；目标为全屏沉浸窗口，页面里可能有带遮罩的弹窗。
- [状态栏实色避让带挂在只承担避让的外层 Column：宿主是 Tabs 时把 Tabs 包进该 Column，不在 Tabs 上挂 padding 加背景色](lesson-fe10bd2491ca4ba82cb5.lesson.md)
  - 时机：界面实现或修复阶段，为带 Tabs 等子页铺满容器的主框架页补源端状态栏实色带，决定避让 padding 与背景色挂在哪个组件时
  - 情境：源 Activity 基类在 onCreate 设置实色状态栏；目标全屏布局，用测得的顶部避让值做 padding；宿主页的避让 padding 写在 Tabs（或 Swiper）上，TabContent 是满铺白底子页；工程其他页面已用“padding + 背景色挂在只包标题条的普通 Column”实现同一色带。
- [系统栏图标深浅按源端浅色状态栏标志推导：未设标志时安卓图标为白色，不照搬模板默认，也不按主题名或底色对比度自选](lesson-824031d5fddf81036b54.lesson.md)
  - 时机：沉浸式窗口配置阶段，调用 setWindowSystemBarProperties 设置 statusBarContentColor/navigationBarContentColor 或修改系统栏底色时；规格提取阶段整理主题与状态栏外观时
  - 情境：Android 源端以主题、values-vNN 覆盖或代码决定状态栏图标深浅：windowLightStatusBar、SYSTEM_UI_FLAG_LIGHT_STATUS_BAR、setSystemBarsAppearance(APPEARANCE_LIGHT_STATUS_BARS)、ImmersionBar darkMode(true) 等表示深色图标，全都没有时为白色图标，即使主题是 Theme.AppCompat.Light 一类、状态栏底色偏浅；目标全屏窗口用 setWindowSystemBarProperties 设置系统栏，沉浸式 skill 示意写“透明背景 + 浅色文字”，规格可能只要求底色 parity。
- [自绘标题栏接入顶部安全区前先判定源端由谁避让：根 fitsSystemWindows 时 inset 放包住工具栏的主内容列（DrawerLayout 下不包抽屉，NavigationView 头部画到状态栏下并叠 insetForeground）、工具栏保持源高；工具栏自带固定顶距时顶距与 inset 只取一份并同步高度](lesson-cde4120ab9ad7412b1da.lesson.md)
  - 时机：界面实现阶段，为全屏页自绘标题栏/工具栏接入顶部系统安全区（topInset）并确定其高度与顶部内距时
  - 情境：Android 全屏页工具栏为固定 dp 高度，状态栏避让由根布局 fitsSystemWindows=true 承担，或由工具栏自身的固定 paddingTop（如 80dp 高、40dp 顶距，根无 fitsSystemWindows）承担；目标页以窗口模型的 topInset 做前景避让，标题栏写固定 .height()。也包括根为 DrawerLayout、NavigationView android:fitsSystemWindows="true" 且有 app:headerLayout，目标用同时承载抽屉与工具栏的共享基座（SideBarContainer）。 也包括源 targetSdk≥35（常经 gradle.properties 间接定义）、运行在 Android 15 及以上而强制 edge-to-edge：根 fitsSystemWindows=false、无 WindowInsets 处理，工具栏叠放在铺满的内容之上；目标套用沉浸式分层范式，结构检查按页面类型要求前景避让。
  - 例外：页面内容原点已在状态栏 inset 之下（宿主已消费 inset），此时只补源端顶距的剩余部分，不再给标题栏加 topInset
- [页面级安全区订阅从承载页面的主窗口取窗口对象：复用工程主窗口入口或入口 Ability 已维护的避让状态，不用 window.getLastWindow](lesson-8e0e9fe5373a2bbe47af.lesson.md)
  - 时机：界面实现或巡检修复阶段，为全屏页订阅 avoidAreaChange、调用 getWindowAvoidArea 取顶部与底部避让值并选择窗口对象时
  - 情境：ArkUI 页面需自行订阅避让区或读取避让值；工程已在 EntryAbility 用主窗口测量安全区并写入共享状态，或有 getMainWindow()、windowStage.getMainWindowSync() 一类主窗口入口；运行时可能出现分享面板、调试浮窗等其他窗口；skill 示例为设置系统栏属性用了 window.getLastWindow(context)。
