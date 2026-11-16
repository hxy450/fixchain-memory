# Compose 滚动容器的滚动条和越界效果

agent 会看到什么：读到 Compose 的 LazyColumn、Modifier.verticalScroll / horizontalScroll（包括 ModalBottomSheet 里的），modifier 上有没有滚动条修饰符、有没有用 LocalOverscrollFactory / overscrollEffect 覆盖越界效果；产物里 List、Scroll 的 .scrollBar(...)、.edgeEffect(...) 写没写、写的什么

## 通用查法

### Compose 滚动容器没写滚动条和越界修饰时，查两端默认值，在 List / Scroll 上显式写

审的是：代码
触发（任一种）：
- 读到：Compose 的 LazyColumn、Modifier.verticalScroll / horizontalScroll 上没有滚动条修饰符，也没用 LocalOverscrollFactory、overscrollEffect 覆盖越界效果；写错的样子：目标 List / Scroll 没写 .scrollBar(...)、.edgeEffect(...)，沿用了 ArkUI 默认
适用范围：Compose 滚动容器迁成 ArkUI List、Scroll 时的滚动条和越界效果
做法：
- 按下面要查的项确认源端有没有覆盖滚动条和越界效果；没有就按 Compose 默认：无滚动条、有平台越界效果
- 到鸿蒙 SDK 的 ets/component 下 list.d.ts、scroll.d.ts、grid.d.ts 读这个组件 scrollBar、edgeEffect 的 Default value，和源端效果不同的都显式写（例：Scroll 写 .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: false })，List、Scroll 写 .scrollBar(BarState.Off)）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- scrollBar(barState: BarState): T；List、Grid、Scroll 默认 BarState.Auto，WaterFlow 默认 BarState.Off：不写 scrollBar 时 List、Grid、Scroll 会显示系统滚动条（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ScrollableCommonMethod.scrollBar）
- edgeEffect(edgeEffect: EdgeEffect, options?: EdgeEffectOptions): ScrollAttribute；默认 EdgeEffect.None，options 默认 { alwaysEnabled: true }：Scroll 不写 edgeEffect 就没有越界效果（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，ScrollAttribute.edgeEffect）
- edgeEffect(value: EdgeEffect, options?: EdgeEffectOptions): ListAttribute；默认 EdgeEffect.Spring：List 的越界默认值和 Scroll 不同（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.edgeEffect）
针对本应用要查的：
- 源端容器有没有覆盖滚动条和越界效果：源工程 Kotlin 文件里搜 LocalOverscrollFactory、LocalOverscrollConfiguration、overscrollEffect，以及挂在这个容器 modifier 上的自定义滚动条扩展函数；搜不到覆盖就是平台默认越界效果；有自定义滚动条修饰符的，按它的定义读出宽度、颜色、滚动中和停止时的 α 与动画时长
未核实：Compose 的 LazyColumn 默认不显示滚动条、verticalScroll 默认带平台越界效果出自卡，本机没有 Compose 源码原文
来源：2 张卡，2 个应用
- case-cdc263993782c99990b7（GameOfLife）：做法第 1 步 ← 建议 4；做法第 2 步 ← 诊断
- case-f0512caa793e1ad8016c（jerboa）：做法第 1 步 ← 建议 4；做法第 2 步 ← 诊断

## 规矩

- rule-a7e312aaff92｜Compose verticalScroll 未覆盖越界效果时，目标 Scroll 写 Spring 边缘效果｜读到：Compose 里 Column(Modifier.verticalScroll(state)) 或 Modifier.horizontalScroll(state)，源工程没有用 LocalOverscrollFactory / LocalOverscrollConfiguration 或 overscrollEffect 参数覆盖越界效果；写错：目标 Scroll{Column} 的修饰链里没有 .edgeEffect(...)（Scroll 默认 EdgeEffect.None），或注释判断「Compose 默认没有越界效果」
- rule-c3f77cc7996c｜bindSheet FIT_CONTENT 弹层里可能超高的 Scroll 要写非 None 的 edgeEffect｜读到：源端 ModalBottomSheet(skipPartiallyExpanded = true) 的内容是 Column(Modifier.verticalScroll(...))，长列表、横屏或大字号时会超过弹层高度；写错：宿主 bindSheet(…, { height: SheetSize.FIT_CONTENT }) 的内容写成 Scroll{Column}，Scroll 修饰链只有 width、backgroundColor、scrollBar，没有 .edgeEffect(...)；注释写「按内容定高、到上限后就滚动」
- rule-40e01b393a12｜源 LazyColumn 无滚动条修饰符时，List 显式写 scrollBar(BarState.Off)｜读到：Compose `LazyColumn` / `Modifier.verticalScroll` 的 modifier 上没有任何滚动条修饰符（Compose 默认不显示滚动条）；写错：目标 `List` / `Scroll` 没写 `.scrollBar(...)`，或写了 `.scrollBar(BarState.Auto)`，显示出系统滚动条
- rule-b8a7f4360718｜源列表挂了自定义滚动条修饰符时，目标按它的参数自绘滚动条，不交给系统滚动条｜读到：Compose `LazyColumn` 的 modifier 上挂了源工程自定义的滚动条修饰符（传入 `LazyListState`，带宽度、颜色、滚动中和停止时的 α 与动画时长，按项数算 thumb）；写错：目标 `List` 没有对应的自绘滚动条：注释写「无 ArkUI 等价」交给系统滚动条，或写 `.scrollBar(BarState.Off)` 直接丢掉
