# Compose 折叠顶栏（LargeTopAppBar 配 exitUntilCollapsedScrollBehavior）

agent 会看到什么：读到 Compose 的 LargeTopAppBar / LargeFlexibleTopAppBar 配 TopAppBarDefaults.exitUntilCollapsedScrollBehavior、按 collapsedFraction 插值，产物里是固定高度顶栏、onDidScroll 只变色或 onScrollIndex 两态切换的写法

## 规矩

- rule-50b2ab274522｜折叠顶栏的代码用列表 onScrollFrameBegin 联动顶栏高度，不写固定高度顶栏只变色｜读到：Compose 源码 LargeFlexibleTopAppBar 配 TopAppBarDefaults.exitUntilCollapsedScrollBehavior(...)，有 collapse() 动画；写错：目标顶栏是固定高度（如 64vp）的 Row，只在 onDidScroll 里按滚动量变色；或各页另写页内顶栏、注释「列表短，折叠行为不迁移」
- rule-dc3c9069dd0c｜顶栏随 collapsedFraction 折叠时按滚动偏移连续插值，不用 onScrollIndex 两态｜读到：Compose 顶栏 LargeTopAppBar / LargeFlexibleTopAppBar 配 TopAppBarDefaults.exitUntilCollapsedScrollBehavior，按 scrollBehavior.state.collapsedFraction 对背景色 lerp、阴影乘比例；写错：目标在 onScrollIndex 里按首个可见行 first > 0 做展开 / 收起两态切换，高度、标题字号跳变，并留 `// TODO` 说连续折叠是近似
- rule-78ecbce25515｜TopAppBar 带 enterAlways 时，目标用 List.onScrollFrameBegin 先改顶栏偏移｜读到：val scrollBehavior = TopAppBarDefaults.enterAlwaysScrollBehavior(rememberTopAppBarState())，Scaffold 挂 Modifier.nestedScroll(scrollBehavior.nestedScrollConnection)；写错：目标顶栏是固定高度的 Row（.height(56) 或 .height(64)），没有和 List 滚动联动，注释写「enterAlways 降级为固定顶栏」「ArkUI 无折叠联动等价」「同某页决策」
