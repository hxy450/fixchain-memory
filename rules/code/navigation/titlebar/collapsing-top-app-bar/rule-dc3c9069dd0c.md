# 顶栏随 collapsedFraction 折叠时按滚动偏移连续插值，不用 onScrollIndex 两态

审的是：代码
触发（任一种）：
- 读到：Compose 顶栏 LargeTopAppBar / LargeFlexibleTopAppBar 配 TopAppBarDefaults.exitUntilCollapsedScrollBehavior，按 scrollBehavior.state.collapsedFraction 对背景色 lerp、阴影乘比例；写错的样子：目标在 onScrollIndex 里按首个可见行 first > 0 做展开 / 收起两态切换，高度、标题字号跳变，并留 `// TODO` 说连续折叠是近似
- 读到：工程里的兄弟页用 onScrollIndex 首个可见行做顶栏两态折叠；写错的样子：新页照搬兄弟页的两态写法，而本页源码写的是 collapsedFraction 连续折叠
适用范围：源端顶栏随滚动连续折叠，目标用 List 或 Scroll 承载内容时
做法：
- List / Scroll 绑定 Scroller，在 onDidScroll（或 onScroll）里算 fraction = clamp(scroller.currentOffset().yOffset / (展开高度 − 收起高度), 0, 1)，高度、标题字号和源端做了 lerp 的背景色、阴影都按 fraction 插值
- 兄弟页的写法和本页源码不一致时按源码实现，并在报告里写明兄弟页与源码的差异
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- currentOffset(): OffsetResult：Scroller 取当前滚动偏移，没绑定组件时返回空（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，Scroller.currentOffset）
- OffsetResult.yOffset 竖直滑动偏移，返回值单位 vp：除数（展开高度 − 收起高度）也用 vp（出处：ts-container-scroll.md，OffsetResult对象说明）
- onDidScroll(handler: OnScrollCallback): T（ScrollableCommonMethod）；OnScrollCallback = (scrollOffset: number, scrollState: ScrollState) => void：List、Grid 等可滚动组件的滚动回调，@since 12（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ScrollableCommonMethod.onDidScroll）
- onScroll(event: (scrollOffset: number, scrollState: ScrollState) => void): ListAttribute，@deprecated since 12，@useinstead onDidScroll：List 的旧滚动回调，卡里用它修好；新写法用 onDidScroll（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.onScroll）
- onDidScroll(handler: ScrollOnScrollCallback): ScrollAttribute：同族接口：Scroll 的滚动回调（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，ScrollAttribute.onDidScroll）
- List 挂 Scroller，onScroll 里读 currentOffset().yOffset 除以（展开高度 − 收起高度）得 fraction，高度和标题字号连续插值：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 顶栏展开高度、收起高度、两态标题字号，以及哪些量随 collapsedFraction 插值：源工程里顶栏 Composable 的 Kotlin 文件，按 collapsedFraction、lerp、expandedHeight / collapsedHeight 找；源端做了 lerp 或乘 fraction 的量，在目标里都按同一个 fraction 插值
未核实：卡里上机的是 HarmonyOS 6.0.1（API 21），本机核对用的是 API 23 的声明
来源：1 张卡，1 个应用
- case-66f3c1649b7b5c4f38b5（Cofi）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 6 ← 诊断
