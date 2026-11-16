# 窗口与系统栏

读到源端有状态栏、导航栏、全屏和沉浸的写法（FLAG_FULLSCREEN、NoTitleBar 主题、WindowInsets、fitsSystemWindows、ImmersionBar、windowBackground、FLAG_KEEP_SCREEN_ON），或规格里写沉浸式、安全区避让、系统栏颜色和窗口背景时

## 触发族

- [Scaffold 的 innerPadding 和顶部安全区](scaffold-insets/index.md)（2 条）：读过的 Compose 源码里 Scaffold 不传 topBar、把 padding(innerPadding).consumeWindowInsets 交给嵌套子页，或同一 Box 里叠着列表、顶栏和浮层；交回的规格里顶部状态栏由谁消费、子页和浮层按什么口径避让
- [布局根没写背景时透出的窗口背景](window-background/index.md)（5 条）：读到布局根没写 android:background 或写 @null、铺满的 SurfaceView 没置顶、Activity 用 Translucent 主题或平台主题的 windowBackground；规格写「背景 #某色 透出」「暗底背景（Holo 默认）」「Stack + 底层 Image」「全屏 NavDestination + 半透明遮罩」
- [Activity 窗口的 FLAG_KEEP_SCREEN_ON](keep-screen-on/index.md)（2 条）：读到 Activity 的 onCreate 里 getWindow().addFlags(FLAG_KEEP_SCREEN_ON)，没有 clearFlags；规格的映射行或验收只写「onCreate 时机 setWindowKeepScreenOn(true)」「进入该页不熄屏」
- [根视图按状态栏 insets 设顶部 padding](decor-statusbar-padding/index.md)（2 条）：源 Activity 在 DecorView（根视图）上按 statusBarInsets.top 调 setPadding、有的还 setBackgroundColor 自绘状态栏底色，规格里写的是状态栏沉浸、安全区避让或系统栏底色
- [低 targetSdk 全屏窗口下以 DisplayMetrics 为基准的几何](legacy-fullscreen-display-metrics/index.md)（2 条）：源自绘 View 用 getDisplayMetrics() 的 widthPixels / heightPixels 作几何基准，Activity 是 FLAG_FULLSCREEN，Manifest 的 targetSdkVersion 低、没声明 windowLayoutInDisplayCutoutMode / maxAspectRatio，规格里按整屏或「全屏减底部避让」取值
- [源 Activity 的去标题和全屏窗口标志](no-title-fullscreen-flags/index.md)（3 条）：源 Activity 调 requestWindowFeature(FEATURE_NO_TITLE)、setFlags(FLAG_FULLSCREEN)，或主题是 Theme.*.NoTitleBar / *.NoTitleBar.Fullscreen，规格写成「无标题全屏」「真全屏」「沉浸式」，没逐边写哪一栏隐藏
- [嵌入页里的 ImmersionBar 沉浸调用](immersionbar-embedded-page/index.md)（2 条）：源嵌入页（Fragment 等）里有 ImmersionBar.with(this).statusBarView / titleBarMarginTop、fitsSystemWindows 这类沉浸调用或状态栏占位 View，规格按 page_type=sub_component 写 needs_immersive_safearea=false，或写「由宿主统一处理安全区」
- [窗口沉浸和系统栏外观](system-bars-immersive/index.md)（4 条）：读到源主题链和 Activity 代码里关于系统栏的写法（windowFullscreen、透明 statusBarColor、SYSTEM_UI_FLAG_LAYOUT_*、targetSdk），或什么都没写；规格的沉浸式节、全局约定照 page_type 默认值或一句「透明状态栏全屏」写成，没逐条系统栏写颜色和内容是否画到其下
- [只在某一导航模式下出现的底部遮挡](nav-mode-bottom-overlap/index.md)（1 条）：用户请求里说某种导航模式（隐藏导航栏、手势导航）正常、另一种（三键导航）底部被遮挡；验收条目里写的避让要求
- [靠隐藏系统资源判断的源端分支](hidden-resource-branch/index.md)（1 条）：源端用 Resources.getSystem().getIdentifier 读隐藏系统资源（如 config_navBarInteractionMode）决定行为，如非手势导航时 setNavigationBarColor；规格里以「无对等」删掉这段分支
