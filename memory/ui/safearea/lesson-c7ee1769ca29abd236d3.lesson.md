# 全屏窗口下先确认路由页的内容原点：已在状态栏 inset 之下就只补源端顶距的剩余部分，背景延伸时在背景节点自身 expandSafeArea

ID：`lesson-c7ee1769ca29abd236d3` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，为全屏窗口中的路由页（NavDestination/HMRouter 页，含 Tab 子页）确定顶部起点、状态栏 inset 的消费位置以及背景是否延伸到状态栏时

## 适用情境

Android 页面在透明状态栏下用自屏幕顶部起算的固定顶距（layout_marginTop、getStatusBarsHeight）给顶栏留位，背景铺到状态栏后面；目标 EntryAbility 全屏并发布顶部避让值（例：windowTopPadding），入口只在 Navigation 宿主上 expandSafeArea(TOP)，页面经路由框架承载。

## 原因

宿主级 expandSafeArea 不代表子页面也从窗口顶部排布，路由页节点可能从状态栏下沿开始（已在路由框架承载的页面上实测观察）。按“页面从窗口顶起算”处理会把 Android 顶距整段叠在 inset 之下形成空白，在未扩展的根上再加 padding(topInset) 会多出一条色带，背景不扩展又露出状态栏区。

## 做法

1. 定顶部布局前先确认内容原点：用 dumpLayout 看页面根节点 bounds 是否从状态栏下沿开始，不凭宿主的 expandSafeArea 推断子页面已铺满窗口。
2. 迁移透明状态栏页面的固定顶距时二选一：页面已在 inset 之下就用“源端顶距 − 已消费的 inset”；页面根先 expandSafeArea(TOP) 才整额消费入口发布的顶部避让值（例：windowTopPadding）；inset 只计一次。
3. 背景、色块或工具栏需要延伸到状态栏后面时，在该背景节点自身加 expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP])，文字内容再按顶部避让值避让。
4. 参照同工程已修复的兄弟页前，先按第 1 步确认本页的路由宿主、祖先 padding 与页面 bounds 与它一致，再沿用其结论；不一致时按本页实测处理。

## 可选检查

- 需要确认时，用 dump 核对标题的 y 坐标与状态栏区域颜色。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-6597b7f7858db941262c](../../../store/cases/case-6597b7f7858db941262c/5df98131b17c6e84b2f61d4e454c9248bb40405f74bd41c3851a51f49d4e9697.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`5df98131b17c6e84b2f61d4e454c9248bb40405f74bd41c3851a51f49d4e9697`
