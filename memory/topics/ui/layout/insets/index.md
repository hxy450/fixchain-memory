# ui/layout/insets

系统栏与软键盘避让值的取值、单位与只消费一次

[上一级](../index.md)

## 本级经验

- [innerPadding 顶部即状态栏高，目标只在一处避让](lesson-f64afc22d41b130f1628.lesson.md) · 阶段：spec/execute · 信号：Scaffold, innerPadding, consumeWindowInsets, contentWindowInsets
- [下发状态栏高度参数需写明消费层，Stack 各层同基准](lesson-2cf2614847a8dba832b3.lesson.md) · 阶段：plan/execute · 信号：Stack, @Param, windowTopPadding, statusBarHeight
- [标题栏接 topInset 前判定源端避让方，内距只取一份](lesson-cde4120ab9ad7412b1da.lesson.md) · 阶段：spec/execute · 信号：fitsSystemWindows, topInset, paddingTop, .height()
- [源 adjustResize 时键盘避让设 RESIZE](lesson-f86b02e97cc77e31d51a.lesson.md) · 阶段：spec/execute · 信号：adjustResize, windowSoftInputMode, imePadding, KeyboardAvoidMode.RESIZE
- [路由页先核内容原点，已在 inset 下只补源顶距余量](lesson-c7ee1769ca29abd236d3.lesson.md) · 阶段：execute · 信号：NavDestination, HMRouter, expandSafeArea, SafeAreaType.SYSTEM
- [避让区与窗口尺寸是 px，写入窗口模型前先 px2vp](lesson-cf111aadb8804649b578.lesson.md) · 阶段：execute · 信号：getWindowAvoidArea, px2vp, windowRect, getWindowProperties
- [页面读避让值用主窗口，不用 getLastWindow](lesson-8e0e9fe5373a2bbe47af.lesson.md) · 阶段：execute/repair · 信号：getLastWindow, getMainWindowSync, getMainWindow, avoidAreaChange
