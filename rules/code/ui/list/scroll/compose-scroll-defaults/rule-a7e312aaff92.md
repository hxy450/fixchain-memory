# Compose verticalScroll 未覆盖越界效果时，目标 Scroll 写 Spring 边缘效果

审的是：代码
触发（任一种）：
- 读到：Compose 里 Column(Modifier.verticalScroll(state)) 或 Modifier.horizontalScroll(state)，源工程没有用 LocalOverscrollFactory / LocalOverscrollConfiguration 或 overscrollEffect 参数覆盖越界效果；写错的样子：目标 Scroll{Column} 的修饰链里没有 .edgeEffect(...)（Scroll 默认 EdgeEffect.None），或注释判断「Compose 默认没有越界效果」
适用范围：Compose 的 verticalScroll / horizontalScroll 容器迁成 ArkUI Scroll 时
做法：
- 先在源工程搜 LocalOverscrollFactory、LocalOverscrollConfiguration 和 overscrollEffect 参数；没有覆盖就按「有平台越界效果」处理，不以规格没写为由保留 Scroll 默认的 None
- 目标写 Scroll() { … }.edgeEffect(EdgeEffect.Spring, { alwaysEnabled: false })：内容可滚时才有弹性越界
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- edgeEffect(edgeEffect: EdgeEffect, options?: EdgeEffectOptions): ScrollAttribute；默认 EdgeEffect.None，options 默认 { alwaysEnabled: true }：Scroll 不写 edgeEffect 就没有越界效果；写 Spring 时要显式给 alwaysEnabled: false（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，ScrollAttribute.edgeEffect）
- EdgeEffectOptions.alwaysEnabled: boolean：内容比组件小时是否也启用越界效果（出处：鸿蒙 SDK 的 ets/component/common.d.ts，EdgeEffectOptions.alwaysEnabled）
- EdgeEffect.Spring、EdgeEffect.Fade、EdgeEffect.None：边缘效果的三个取值，Spring 是弹性回弹（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，EdgeEffect）
- edgeEffect(value: EdgeEffect, options?: EdgeEffectOptions): ListAttribute；默认 EdgeEffect.Spring，options 默认 { alwaysEnabled: false }：同族接口：List 的默认值和 Scroll 不同（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.edgeEffect）
- edgeEffect(value: EdgeEffect, options?: EdgeEffectOptions): GridAttribute；默认 EdgeEffect.None，options 默认 { alwaysEnabled: false }：同族接口：Grid 和 Scroll 一样默认 None（出处：鸿蒙 SDK 的 ets/component/grid.d.ts，GridAttribute.edgeEffect）
- edgeEffect(edgeEffect: EdgeEffect, options?: EdgeEffectOptions): T：同族接口：ScrollableCommonMethod 上的通用写法（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ScrollableCommonMethod.edgeEffect）
针对本应用要查的：
- 源工程有没有覆盖 Compose 的越界效果：源工程 Kotlin 文件里搜 LocalOverscrollFactory、LocalOverscrollConfiguration、overscrollEffect；搜不到就是平台默认越界效果（卡里记 Android 12+ 为拉伸）；置空了才按无越界处理
未核实：Compose foundation 的 verticalScroll 默认带平台越界效果，卡里核了字节码，本机三类来源里没有源码原文
来源：1 张卡，1 个应用
- case-cdc263993782c99990b7（GameOfLife）：做法第 1 步 ← 建议 4；做法第 2 步 ← 诊断、建议 4
