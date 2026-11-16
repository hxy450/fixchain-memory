# exitUntilCollapsed 折叠大标题顶栏

agent 会看到什么：读到 Compose 顶栏是 LargeFlexibleTopAppBar / LargeTopAppBar 加 TopAppBarDefaults.exitUntilCollapsedScrollBehavior(...)，另有 collapse() 动画写 heightOffset；转换决策写「无现成件，简化为标题栏滚动渐变」「保底固定标题栏」，或 AC 以固定标题栏为目标

## 规矩

- rule-892ee13eee0a｜源端是 exitUntilCollapsed 折叠大标题顶栏时，规格不因没有现成组件就写成固定标题栏｜读到：Compose 源码顶栏是 LargeFlexibleTopAppBar（或 LargeTopAppBar）加 TopAppBarDefaults.exitUntilCollapsedScrollBehavior(flingAnimationSpec = rememberSplineBasedDecay())，另有 collapse() 动画写 heightOffset；写错：转换决策写「HarmonyOS 无 exitUntilCollapsed 现成件，简化为标题栏滚动渐变」「保底固定标题栏」「设置类页面无需折叠行为」，或 AC 把「固定标题栏 + 变色」定为验收目标
- rule-846a6b6c1c60｜源 TopAppBar 带 enterAlways scrollBehavior 时，规格写成必须还原的折叠契约｜读到：Compose 页面 Scaffold + TopAppBar，val scrollBehavior = TopAppBarDefaults.enterAlwaysScrollBehavior(rememberTopAppBarState())，Scaffold 挂 Modifier.nestedScroll(scrollBehavior.nestedScrollConnection)；写错：页面规格的转换决策写「滚动收起可选」「或降级固定，差异登记」「简化决策允许降级为固定顶栏」，或转换表里没单列 scrollBehavior
