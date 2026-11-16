# 安全区与避让

源端有 fitsSystemWindows、透明状态栏下的留白、WindowInsets、Compose Scaffold 的 innerPadding、ImmersionBar，目标端有 getWindowAvoidArea 取值，或页面、Tabs 宿主、贴底元素上的避让 padding 和 expandSafeArea 时

## 触发族

- [全屏页的顶部状态栏避让](top-inset/index.md)（9 条）：读到根布局、DrawerLayout、AppBarLayout 上的 android:fitsSystemWindows 或工具栏自带的 paddingTop；产物里 .padding({ top: 顶部安全区值 }) 或状态栏高度占位落在哪一层容器、落了几处
- [全屏页贴底元素的导航条避让](bottom-inset/index.md)（2 条）：读到贴底按钮行、底部弹层的根布局只有固定的 android:paddingBottom / layout_marginBottom；产物里全屏页贴底元素的 .padding({ bottom: … }) 没加导航条避让值
- [Compose Scaffold 外壳和内容区的顶部避让](scaffold-insets/index.md)（7 条）：读过的 Compose 源码里宿主用 Scaffold（常只传 bottomBar，content 带 innerPadding）承载 tab 子页、子页和浮层；交回的根 Navigation 没隐藏标题栏、工具栏，或宿主 tab 内容区、子页、浮层的根节点上没有顶部 padding
- [包住 Tabs 的宿主容器上的内边距](tab-host-padding/index.md)（6 条）：读到单 Activity 宿主承载各 Tab Fragment（ViewPager2、TabLayout），源端用 ImmersionBar 沉浸、titleBarMarginTop、transparentStatusBar、windowTranslucentStatus，或 paddingStart / paddingEnd 只写在底栏上；产物里包住整个 Tabs 的容器加了顶部状态栏 padding 或左右 padding
- [窗口避让区的取值和换算](avoid-area-value/index.md)（7 条）：EntryAbility 或页面里用 getWindowAvoidArea / on('avoidAreaChange') 取避让高度（AvoidAreaType、topRect、bottomRect），写进共享模型或 AppStorage 前的 px2vp 换算、getUIContext 的时机和取窗口用的 API
- [透明状态栏下的顶部留白和背景](translucent-status-bar/index.md)（2 条）：源端透明状态栏下用 layout_marginTop / topMargin 给顶栏留位、背景铺到状态栏后；产物里路由页的 .margin / .padding({ top })、状态栏高度和 expandSafeArea 写在哪个节点
- [底部避让 padding 所在的容器层](bottom-avoid-padding/index.md)（3 条）：交回的根容器自带背景色、height('100%') 并写 .padding({ bottom: 底部避让 })，而延伸到屏幕底边的是里面背景色不同的 layoutWeight(1) 内容层
- [DecorView 上的状态栏底色和顶部避让](decorview-status-bar/index.md)（2 条）：读到源端在 DecorView 上 setBackgroundColor 画状态栏底色、setPadding(0, statusBarInsets.top, 0, 0) 避让状态栏，产物里是 setWindowSystemBarProperties 的 statusBarColor、页面容器的顶部 padding 或布局输出上的 Y 平移
- [全屏沉浸页的避让 padding](immersive-avoid-padding/index.md)（10 条）：读到入口 Ability 调 setWindowLayoutFullScreen(true)、规格标 needs_immersive_safearea / full_screen_page 或源端 enableEdgeToEdge，产物里是页面上的 expandSafeArea、固定 padding、安全区注释和引用避让值的 padding 表达式
