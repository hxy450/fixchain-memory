# 全屏窗口下先确认路由页的内容原点：已在状态栏 inset 之下就只补源端顶距的剩余部分，背景需延伸到状态栏时在背景节点自身 expandSafeArea

ID：`lesson-c7ee1769ca29abd236d3` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，为全屏窗口中的路由页（NavDestination/HMRouter 页，含 Tab 子页）确定顶部起点、状态栏 inset 的消费位置以及背景是否延伸到状态栏时

## 适用情境

Android 页面在透明状态栏下用自屏幕顶部起算的固定顶距（layout_marginTop、getStatusBarsHeight）给顶栏留位，背景铺到状态栏后面；目标 EntryAbility 全屏并发布 windowTopPadding，入口只在 Navigation 宿主上 expandSafeArea(TOP)，页面经路由框架承载。

## 原因

宿主级 expandSafeArea 不代表子页面也从窗口顶部排布；来源工程实测路由页节点从状态栏下沿开始。按“页面从窗口顶起算”处理会把 Android 顶距整段叠在 inset 之下形成空白，在未扩展的根上再加 padding(topInset) 会多出一条色带，背景不扩展又露出状态栏区。来源中四个页面分别出现这三类偏差，其中执行者已读到兄弟页注释“导航已消费 inset”仍重复叠加。

## 做法

1. 定顶部布局前先确认内容原点：用 dumpLayout 看页面根节点 bounds 是否从状态栏下沿开始，不凭宿主的 expandSafeArea 推断子页面已铺满窗口。
2. 迁移透明状态栏页面的固定顶距时二选一：页面已在 inset 之下就用“源端顶距 − 已消费的 inset”；页面根先 expandSafeArea(TOP) 才整额消费 windowTopPadding；inset 只计一次。
3. 背景、色块或工具栏需要延伸到状态栏后面时，在该背景节点自身加 expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP])，文字内容再按 windowTopPadding 避让。
4. 新增或重写路由页前先读同工程已修复的兄弟页如何处理 inset 并沿用其结论；要反着做须写明依据。

## 可选检查

- 需要确认时，用 dump 核对标题的 y 坐标与状态栏区域颜色。

## 来源（按需复核）

- [case-6597b7f7858db941262c](../../../store/cases/case-6597b7f7858db941262c/5df98131b17c6e84b2f61d4e454c9248bb40405f74bd41c3851a51f49d4e9697.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`5df98131b17c6e84b2f61d4e454c9248bb40405f74bd41c3851a51f49d4e9697`
