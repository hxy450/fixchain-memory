# ui/safearea

沉浸式安全区：全屏布局下前景避让与 expandSafeArea 的区别，避让区测量与 px/vp 换算（状态栏、导航指示条），系统栏图标深浅（按源端浅色状态栏标志推导），源根视图自设状态栏 padding 与底色时由页面容器承载（系统栏透明），路由页内容原点与顶部 inset 的消费位置，Compose Scaffold innerPadding 的顶部 inset 由宿主还是子页消费，向子页与页内浮层下发的状态栏高度参数，Tab 宿主按各 Tab 沉浸设置处理顶部安全区（含嵌入页状态栏占位的背景延伸与前景避让分层），全屏页底部按钮、按键区与贴底弹层的避让及承载层，逐页落实前景避让，状态栏实色避让带的承载层（Tabs 宿主包进外层 Column），自绘标题栏按源端避让来源接入 topInset（固定高度含内距、顶距与 inset 只取一份），页面级避让订阅取承载页面的主窗口；三键与手势导航的判定、按导航方式给导航栏着色、底部避让取两类避让区的较大值，以及页面级软键盘避让模式（adjustResize/imePadding）；开全屏前逐边核对源窗口是否延伸到系统栏下，DrawerLayout 根下抽屉头部与主内容列的状态栏避让分工

[上一级](../index.md)

## 本级经验

- [全屏窗口下先确认路由页的内容原点：已在状态栏 inset 之下就只补源端顶距的剩余部分，背景延伸时在背景节点自身 expandSafeArea](lesson-c7ee1769ca29abd236d3.lesson.md)
  - 时机：界面实现阶段，为全屏窗口中的路由页（NavDestination/HMRouter 页，含 Tab 子页）确定顶部起点、状态栏 inset 的消费位置以及背景是否延伸到状态栏时
  - 情境：Android 页面在透明状态栏下用自屏幕顶部起算的固定顶距（layout_marginTop、getStatusBarsHeight）给顶栏留位，背景铺到状态栏后面；目标 EntryAbility 全屏并发布顶部避让值（例：windowTopPadding），入口只在 Navigation 宿主上 expandSafeArea(TOP)，页面经路由框架承载。
- [全屏窗口下按边落实前景避让：贴底内容让出避让值，padding 与底色挂在实际占据该边的普通容器层](lesson-0e1c846868f2683cc280.lesson.md)
  - 时机：沉浸式安全区实现阶段，为全屏页的标题栏、底部按钮行、按键区、Tab 栏或贴底弹层确定顶部与底部避让及承载它的容器层时；为已有固定高度（含内容下方留白）的底栏或底部定位元素补导航条避让时
  - 情境：目标页面在 setWindowLayoutFullScreen(true) 下消费入口发布的顶部、底部避让值；Android 源布局的底部按钮行、底部 sheet 没有导航栏间距（源窗口不延伸到导航栏下，或 BottomSheetDialog、Material3 BottomSheet 由系统或库处理 inset）；根容器与底部内容层背景色不同；原 Tab 栏固定高度已在图标文字下方留有空白；NavDestination 页保留预设系统标题栏；壳页承载声明豁免安全区的内嵌子页。
  - 例外：目标窗口按源端保持非全屏时不做前景避让，内容本就在系统栏之间；宿主为 Tabs/Swiper 等由子页铺满的容器、要补状态栏实色带时，按 lesson-fe10bd2491ca4ba82cb5 用只承担避让的外层 Column 承载
- [各 Tab 源 Fragment 的状态栏处理不同或需背景延伸时，Tab 宿主不统一加顶部安全区，按 Tab 分层落实](lesson-48e9408812c28e934db8.lesson.md)
  - 时机：规格与界面实现阶段，实现 MainActivity/Tab 宿主的内容区内边距、为作为 Tab 子组件的 Fragment 写安全区分工或转换其顶部布局时
  - 情境：Android 主 Activity 以 ViewPager/Tab 承载多个 Fragment，主题 windowTranslucentStatus 或 ImmersionBar 让状态栏透明；各 Fragment 自行决定是否为状态栏让位：有的头图直接铺到状态栏下（未设 statusBarView，或用 titleBarMarginTop/fitsSystemWindows），有的在顶对父容器的背景上放一个由 statusBarView 撑成状态栏高度的占位 View，只把前景内容约束在占位之下；MainActivity 的内边距可能只加在底栏容器上。目标用单个宿主页承载各 Tab，可能给承载全部 Tab 槽位的容器统一加入口下发的顶部避让值（例：windowTopPadding）和左右 padding；页面规格把子页标为无需窗口级沉浸（例：page_type=sub_component、needs_immersive_safearea=false），或把页内占位概括成“安全区由宿主统一处理”。
  - 例外：各 Tab 源端都整体避让（前景与背景都在状态栏之下）、子页不再消费时，宿主可以统一消费一次
- [向子页或页内浮层下发状态栏高度参数时写明消费方式，挂在同一 Stack 的每一层都拿到它](lesson-2cf2614847a8dba832b3.lesson.md)
  - 时机：派工与界面实现阶段，向子页、页内浮层下发状态栏高度参数，或把浮层挂进从窗口顶起的宿主 Stack 时
  - 情境：宿主页采用“子页自理”分工，以组件参数下发状态栏高度；子页或浮层（遮罩 + 居中卡片、铺满父容器）与列表、顶栏同挂一个 Stack；派工或槽位契约可能只列出回调参数，或写“接收但本页不使用”。
  - 例外：目标父容器已替该层加了顶部避让，且能指出对应代码位置
- [开全屏前逐边核对源窗口：FLAG_FULLSCREEN 只隐藏状态栏，导航栏、旧应用挖孔边与宽高比上限都在窗口外；源窗口延伸到的边才沉浸](lesson-b0c7fc0e8053f24a4e08.lesson.md)
  - 时机：规格提取与入口窗口实现阶段，决定目标窗口是否 setWindowLayoutFullScreen(true)、隐藏哪些系统栏、各边背景是否延伸、系统栏底色与是否做内容避让时；源端以 DisplayMetrics 取应用窗口宽高作几何基准时；规格模板或页面元数据按页面类型默认标注全屏页、需要沉浸式安全区时
  - 情境：源 Activity 主题链与代码决定窗口是否延伸到系统栏下：windowFullscreen、windowTranslucentStatus/Navigation、FLAG_FULLSCREEN、SYSTEM_UI_FLAG_LAYOUT_*、setDecorFitsSystemWindows(false)/enableEdgeToEdge、targetSdk≥35 的强制 edge-to-edge，或者都没有（Theme.Holo/Theme.Black 等低 targetSdk 主题；requestWindowFeature(FEATURE_NO_TITLE) 只去标题栏）。也包括只用 SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN 加透明 statusBarColor、没有 navigationBarColor、windowTranslucentNavigation、HIDE_NAVIGATION 且 targetSdk≤34 的只沉浸状态栏页面；目标规格模板或沉浸式 skill 默认全屏、两栏透明，或把 FLAG_FULLSCREEN 当作整窗沉浸。低 targetSdk 的旧应用全屏窗口还受挖孔模式与最大宽高比限制。
- [根为 DrawerLayout 且 NavigationView 自带 fitsSystemWindows 时，状态栏避让只给主内容列，抽屉头部画到状态栏下](lesson-84bcbad22600d3763029.lesson.md)
  - 时机：界面实现与共享件收敛阶段，为抽屉页补状态栏避让、把 DrawerLayout + NavigationView + Toolbar 收进共享抽屉基座（SideBarContainer）时；规格提取阶段写抽屉页的沉浸与安全区段时
  - 情境：源布局根是 DrawerLayout fitsSystemWindows=true，内容列（Toolbar + 主内容）在状态栏之下；NavigationView 自身 android:fitsSystemWindows="true" 并带 app:headerLayout。目标用共享抽屉基座（SideBarContainer 同时承载抽屉面板和工具栏/内容列），页面用窗口模型的顶部避让值做前景避让。
- [源窗口 edge-to-edge、Compose Scaffold 无 topBar 时 innerPadding 顶部就是状态栏 inset：目标只在一处落实](lesson-f64afc22d41b130f1628.lesson.md)
  - 时机：规格提取与界面实现阶段，把 Compose Scaffold 的 content padding 与 consumeWindowInsets 拆成宿主壳与各子页（含页内浮层）的顶部避让分工时
  - 情境：源窗口已 edge-to-edge（enableEdgeToEdge、setDecorFitsSystemWindows(false) 或 targetSdk≥35），Scaffold 不传 topBar、未覆写 contentWindowInsets（默认含状态栏），把 Modifier.padding(innerPadding).consumeWindowInsets(innerPadding) 交给嵌套内容；子页自身可能没有 statusBarsPadding，也可能另写 statusBarsPadding 或 windowInsetsTopHeight(statusBars + N)；目标端全屏窗口，由宿主 padding 或向子页下发状态栏高度来避让。
  - 例外：Scaffold 传了 topBar 或覆写了 contentWindowInsets 时，innerPadding 顶部不再等于状态栏高，按实际来源推导；源窗口不是 edge-to-edge 时（decorFitsSystemWindows 为 true，框架让内容视图适配 inset；android-36.1 Window.setDecorFitsSystemWindows 注释）Compose 的 statusBars inset 为 0，innerPadding 顶部也是 0，内容本就在状态栏之下；祖先已用 consumeWindowInsets、windowInsetsPadding 一类修饰符消费过部分 inset 时，Scaffold 从 contentWindowInsets 中扣除这部分，innerPadding 只含剩余部分；它只按祖先消费量扣除，不按 Scaffold 在窗口中的位置扣除（material3 1.4.0 Scaffold.kt）
- [源窗口按 resize 避让软键盘时设 KeyboardAvoidMode.RESIZE（含未声明的隐式 adjustResize），不用默认 OFFSET](lesson-f86b02e97cc77e31d51a.lesson.md)
  - 时机：页面实现阶段，为含文本输入的页面（编辑表单等 NavDestination 子页）落实源端软键盘避让方式时；规格提取阶段为未声明 windowSoftInputMode 的含输入框窗口确定目标避让方式时
  - 情境：源 Activity 声明 windowSoftInputMode=adjustResize，页面在滚动内容或尾部用 imePadding 让键盘弹出时内容区收缩、仍可滚到末项；目标未设键盘避让模式，转换者不确定默认行为是否等价。也包括 manifest、主题与代码都未设 adjust 值，窗口里有显示中的滚动容器（ListView、ScrollView 或带竖向滚动条、android:isScrollContainer=true 的视图），规格只写“默认弹出”。
  - 例外：源窗口带 FLAG_FULLSCREEN：adjustResize 被忽略、窗口不缩放（android-36.1 WindowManager.java 说明），平台隐式 resize 同样不适用
- [源端只在三键导航时给导航栏着色：以 TYPE_SYSTEM 底部避让高度判定导航方式，非手势时用 navigationBarColor 着色并随避让区变化更新](lesson-8bc258c2833be65f4fcd.lesson.md)
  - 时机：规格提取与入口窗口实现阶段，把源 Activity 按导航方式设置导航栏颜色的分支映射到目标窗口系统栏属性时
  - 情境：源端在 Activity 中按是否手势导航决定导航栏底色（如非手势导航时 setNavigationBarColor(背景色带透明度)），判定依赖隐藏系统资源（config_navBarInteractionMode）或系统设置；目标为全屏沉浸窗口，入口用 getWindowAvoidArea 测避让区、用 setWindowSystemBarProperties 设置系统栏。
- [源端给根视图设状态栏高度的顶部 padding 并自绘底色时，目标在页面容器上设 padding 与背景色、系统栏保持透明](lesson-baf0ca22a69e7b76f636.lesson.md)
  - 时机：规格提取与界面实现阶段，把源端根视图（DecorView 或内容根）的状态栏 insets padding 与背景设色翻译为目标页面的避让方式和状态栏底色时
  - 情境：源 Activity（常见于 Android 15+ 边到边分支）给 DecorView 或根布局 setBackgroundColor，并 setPadding(top = 状态栏 inset)，内容 View 在 onSizeChanged 中按自身宽高布局；目标为全屏沉浸窗口，页面里可能有带遮罩的弹窗。
- [状态栏实色避让带挂在只承担避让的外层 Column：宿主是 Tabs 时把 Tabs 包进该 Column，不在 Tabs 上挂 padding 加背景色](lesson-fe10bd2491ca4ba82cb5.lesson.md)
  - 时机：界面实现或修复阶段，为带 Tabs 等子页铺满容器的主框架页补源端状态栏实色带，决定避让 padding 与背景色挂在哪个组件时
  - 情境：源 Activity 基类在 onCreate 设置实色状态栏；目标全屏布局，用测得的顶部避让值做 padding；宿主页的避让 padding 写在 Tabs（或 Swiper）上，TabContent 是满铺白底子页；工程其他页面已用“padding + 背景色挂在只包标题条的普通 Column”实现同一色带。
  - 例外：要补的是底部或普通容器上的避让时，按 lesson-0e1c846868f2683cc280 把 padding 挂在实际占据该边的层；源端给根视图设状态栏 padding 并自绘底色、弹窗遮罩需压暗状态栏区时，按 lesson-baf0ca22a69e7b76f636 由页面容器承载
- [系统栏图标深浅按源端浅色系统栏标志的最终值推导：未设时安卓图标为白色，不照搬模板默认，也不按主题名或底色对比度自选](lesson-824031d5fddf81036b54.lesson.md)
  - 时机：沉浸式窗口配置阶段，调用 setWindowSystemBarProperties 设置 statusBarContentColor/navigationBarContentColor 或修改系统栏底色时；规格提取阶段整理主题与状态栏外观时
  - 情境：Android 源端以主题（沿 parent 链，含 AppCompat/MDC 库主题与各 values-vNN、values-night 覆盖）或代码决定状态栏图标深浅：windowLightStatusBar=true、SYSTEM_UI_FLAG_LIGHT_STATUS_BAR、setSystemBarsAppearance(APPEARANCE_LIGHT_STATUS_BARS)、WindowInsetsControllerCompat.isAppearanceLightStatusBars=true、androidx 的 enableEdgeToEdge()（默认 SystemBarStyle.auto，非夜间配置下给深色图标）、基类沉浸式封装的 darkMode(true) 等表示深色图标；全都没有时为白色图标，即使主题是 Theme.AppCompat.Light 一类、状态栏底色偏浅。目标全屏窗口用 setWindowSystemBarProperties 设置系统栏，沉浸式 skill 示意写“透明背景 + 浅色文字”，规格可能只要求底色 parity。
- [自绘固定高度标题栏接入顶部避让前先判定源端由谁避让：inset 与源顶距只取一份，并保持工具栏可见高度](lesson-cde4120ab9ad7412b1da.lesson.md)
  - 时机：界面实现阶段，为全屏页自绘标题栏/工具栏接入顶部系统安全区（topInset）并确定其高度与顶部内距时
  - 情境：Android 全屏页工具栏为固定 dp 高度，状态栏避让由根布局 fitsSystemWindows=true 承担，或由工具栏自身的固定 paddingTop 承担（根无 fitsSystemWindows）；目标页以窗口模型的顶部避让值做前景避让，标题栏写固定 .height()，参照模板可能写成固定 height 加 padding top（避让值 + N）。
  - 例外：页面内容原点已在状态栏 inset 之下（宿主已消费 inset）时，按 lesson-c7ee1769ca29abd236d3 只补源端顶距的剩余部分，不再给标题栏加 topInset；根是 DrawerLayout 且 NavigationView 带 fitsSystemWindows 与 headerLayout 时，inset 只给主内容列，抽屉面板按抽屉头部的规则另行处理；源工具栏 paddingTop 里另含与状态栏无关的设计间距时，max(源 paddingTop, topInset) 会在状态栏更高的设备上吞掉这段间距，不直接套用第 2 步的公式
- [避让区写入窗口模型时按方位取矩形、底部取两类避让区的较大值，先 px2vp 再供 padding 消费](lesson-cf111aadb8804649b578.lesson.md)
  - 时机：沉浸式安全区实现阶段，在 EntryAbility 或窗口服务里用 getWindowAvoidArea、windowRect 测量并写入共享窗口模型时；把页面里的测量代码收敛成全局模型时
  - 情境：目标用 setWindowLayoutFullScreen(true) 全屏，EntryAbility 通过 getWindowAvoidArea 取状态栏、导航条高度，通过 getWindowProperties().windowRect 取窗口尺寸，写入 AppStorageV2 等共享的窗口模型；各页把这些值直接放进 .padding()/.height()，按 vp 解释；底部避让可能只用 TYPE_NAVIGATION_INDICATOR 测量，或复制 TYPE_SYSTEM 那一行只改了常量。
- [页面级安全区订阅从承载页面的主窗口取窗口对象：复用工程主窗口入口或入口 Ability 已维护的避让状态，不用 window.getLastWindow](lesson-8e0e9fe5373a2bbe47af.lesson.md)
  - 时机：界面实现或巡检修复阶段，为全屏页订阅 avoidAreaChange、调用 getWindowAvoidArea 取顶部与底部避让值并选择窗口对象时
  - 情境：ArkUI 页面需自行订阅避让区或读取避让值；工程已在 EntryAbility 用主窗口测量安全区并写入共享状态，或有 getMainWindow()、windowStage.getMainWindowSync() 一类主窗口入口；运行时可能出现分享面板、调试浮窗等其他窗口；skill 示例为设置系统栏属性用了 window.getLastWindow(context)。
