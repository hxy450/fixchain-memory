# ui/layout/safearea

全屏窗口安全区：避让值单位、expandSafeArea 与前景 padding 之别、inset 只消费一次及承载层

[上一级](../index.md)

## 本级经验

- [Tab 宿主不统一加顶部安全区，按子页源处理分别避让](lesson-48e9408812c28e934db8.lesson.md) · 阶段：spec/execute · 信号：ImmersionBar, statusBarView, titleBarMarginTop, fitsSystemWindows
- [expandSafeArea 非避让，前景按避让区补内距](lesson-a8452bfea5d42d3dcae3.lesson.md) · 阶段：execute · 信号：expandSafeArea, setWindowLayoutFullScreen, getWindowAvoidArea, TYPE_SYSTEM
- [innerPadding 顶部即状态栏高，目标只在一处避让](lesson-f64afc22d41b130f1628.lesson.md) · 阶段：spec/execute · 信号：Scaffold, innerPadding, consumeWindowInsets, contentWindowInsets
- [下发状态栏高度参数需写明消费层，Stack 各层同基准](lesson-2cf2614847a8dba832b3.lesson.md) · 阶段：plan/execute · 信号：Stack, @Param, windowTopPadding, statusBarHeight
- [导航条避让取 bottomRect，加在占屏底那一层](lesson-0e1c846868f2683cc280.lesson.md) · 阶段：execute · 信号：getWindowAvoidArea, TYPE_NAVIGATION_INDICATOR, bottomRect, setWindowLayoutFullScreen
- [标题栏接 topInset 前判定源端避让方，内距只取一份](lesson-cde4120ab9ad7412b1da.lesson.md) · 阶段：execute · 信号：fitsSystemWindows, topInset, paddingTop, .height()
- [状态栏实色带挂外层 Column，把 Tabs 包进该层](lesson-fe10bd2491ca4ba82cb5.lesson.md) · 阶段：execute/repair · 信号：Tabs, TabContent, Column, Swiper
- [路由页先核内容原点，已在 inset 下只补源顶距余量](lesson-c7ee1769ca29abd236d3.lesson.md) · 阶段：execute · 信号：NavDestination, HMRouter, expandSafeArea, SafeAreaType.SYSTEM
- [避让区与窗口尺寸是 px，写入窗口模型前先 px2vp](lesson-cf111aadb8804649b578.lesson.md) · 阶段：execute · 信号：getWindowAvoidArea, px2vp, windowRect, getWindowProperties
