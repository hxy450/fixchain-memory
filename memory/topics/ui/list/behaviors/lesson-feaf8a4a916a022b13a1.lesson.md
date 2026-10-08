# 列表项滑动操作挂在 ListItem 上；把行内容抽成 @Builder 时核对容器专属属性实际接在哪个组件

ID：`lesson-feaf8a4a916a022b13a1` · 版本：4 · 阶段：execute · 主题：[ui/list/behaviors](index.md)

概要：滑动操作挂在 ListItem 节点而非行 Builder

信号：`swipeAction`, `ItemTouchHelper`, `SwipeActions`, `ListItem`, `@Builder`, `LazyForEach`, `ForEach`

## 何时使用

界面实现阶段，把 ItemTouchHelper/SwipeActions 的滑动操作转换为 ListItem.swipeAction，并把行布局抽成 @Builder 时

## 适用情境

规格与映射参考要求用 ListItem.swipeAction；行内容抽成 @Builder 方法，LazyForEach/ForEach 里的 ListItem 只调用该 builder。

## 原因

swipeAction 是 ListItem 的属性，接在 builder 根节点（Row 等）的属性链末尾时编译报 Property 'swipeAction' does not exist on type 'RowAttribute'。来源的规格、映射参考与写者自己的计划都是 ListItem() { row }.swipeAction(...)，输出却接在了 builder 的根 Row 上；自检只核了 SwipeActionItem 的字段形状，没核挂载宿主。

## 做法

1. swipeAction 这类只对容器子项生效的属性写在 ListItem 节点上：ListItem() { this.row(item) }.swipeAction({ start: ..., end: ... })，builder 只负责行内容。
2. 抽出 @Builder 后，对照实际输出确认每条容器专属属性的宿主与规格一致，不按计划推定。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [属性方法不传 ResourceStr 联合值按重载定型](../../../arkts/api-signatures/lesson-63660a8304f7d3920bfc.lesson.md)（共享 1 张卡）
- [写 SDK 调用前按本地 .d.ts 核对成员名与可空性](../../../arkts/api-signatures/lesson-6e558834938be19c04e2.lesson.md)（共享 1 张卡）
- [方向边距用 end 时各边统一 LengthMetrics](../../layout/sizing/lesson-e3077bf60cfc3f34d0a2.lesson.md)（共享 1 张卡）
- [两态按钮图标写成 if/else 或单 Image 选资源](../../interaction/click-binding/lesson-ed5556325b6d8f510e2f.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-de8de9ff9274ca3ce884](../../../../../store/cases/case-de8de9ff9274ca3ce884/d059c48a9b93c30e4e67d4f95f146b58539dcd29ad987d6d6a4b1dcdd3f6e3f8.json) · 结论：diagnosis, rec-4f2d7825be
  卡片版本：`d059c48a9b93c30e4e67d4f95f146b58539dcd29ad987d6d6a4b1dcdd3f6e3f8`
