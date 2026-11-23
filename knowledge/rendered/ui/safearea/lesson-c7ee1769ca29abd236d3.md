# 全屏窗口下先确认路由页的内容原点：已在状态栏 inset 之下就只补源端顶距的剩余部分，背景需延伸到状态栏时在背景节点自身 expandSafeArea

## 何时使用

界面实现阶段，为全屏窗口中的路由页（NavDestination/HMRouter 页，含 Tab 子页）确定顶部起点、状态栏 inset 的消费位置以及背景是否延伸到状态栏时（减去已消费 inset 只用于源端顶距自屏幕顶部起算时）

## 适用情境

Android 页面在透明状态栏下用自屏幕顶部起算的固定顶距（layout_marginTop、getStatusBarsHeight）给顶栏留位，背景铺到状态栏后面；目标 EntryAbility 全屏并发布 windowTopPadding，入口只在 Navigation 宿主上 expandSafeArea(TOP)，页面经路由框架承载。“减去已消费的 inset”只用于源端顶距自屏幕顶部起算的情形；源端根布局设了 fitsSystemWindows=true（系统按状态栏给它加了内边距）或状态栏不透明、内容本就从状态栏下沿排起时，源端顶距不含状态栏高，照原值迁移，不再减 inset。

## 原因

宿主级 expandSafeArea 不代表子页面也从窗口顶部排布；来源工程实测路由页节点从状态栏下沿开始。按“页面从窗口顶起算”处理会把 Android 顶距整段叠在 inset 之下形成空白，在未扩展的根上再加 padding(topInset) 会多出一条色带，背景不扩展又露出状态栏区。来源中四个页面分别出现这三类偏差，其中执行者已读到兄弟页注释“导航已消费 inset”仍重复叠加。

## 做法

1. 定顶部布局前先确认内容原点：用 dumpLayout 看页面根节点 bounds 是否从状态栏下沿开始，不凭宿主的 expandSafeArea 推断子页面已铺满窗口。
2. 迁移透明状态栏页面的固定顶距时二选一：页面已在 inset 之下就用“源端顶距 − 已消费的 inset”；页面根先 expandSafeArea(TOP)、且按第 1 步看到根节点 bounds 已从窗口顶起时，才整额消费 windowTopPadding（expandSafeArea 只扩展绘制区域、不改变布局，路由页根节点加了它节点仍可能从状态栏下沿起）；inset 只计一次。
3. 背景、色块或工具栏需要延伸到状态栏后面时，在该背景节点自身加 expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP])，文字内容再按 windowTopPadding 避让。
4. 新增或重写路由页前先读同工程已修复的兄弟页如何处理 inset 并沿用其结论；要反着做须写明依据。

## 可选检查

- 需要确认时，用 dump 核对标题的 y 坐标与状态栏区域颜色。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕NavDestination 从 API 11 起默认带 expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP, SafeAreaEdge.BOTTOM])，开发者可重写该属性覆盖默认行为
- 〔原因 / 做法第 1、3 步〕expandSafeArea 只作用于当前组件，不会向父组件或子组件传递；它在不改变布局的情况下扩展组件的绘制区域
- 〔做法第 3 步〕除 KEYBOARD 外，expandSafeArea 只在组件边界与安全区重合时才能延伸进去（如状态栏高 100 时组件绝对位置须在 0 到 100 之间）；组件设了固定宽高或 'auto' 时只能向上（TOP）和起始方向（START）扩展，扩展后组件尺寸不变
- 〔做法第 3 步〕expandSafeArea() 不传参时 types 为 SYSTEM、CUTOUT、KEYBOARD，edges 为四边；传 ([], []) 两个空数组时该属性不生效
- 〔做法第 2、3 步〕窗口接口 getWindowAvoidArea、avoidAreaChange 返回的避让区矩形（Rect）以 px 为单位、取整数；ArkUI 的 padding、height 传数字时按 vp 解释，两者相加前要先用 px2vp 换算
- 〔原因 / 做法第 1、2 步〕全屏窗口、入口只在 Navigation 宿主上 expandSafeArea(TOP) 时，真机 dumpLayout 显示路由页节点从状态栏下沿起（状态栏 0–105px，节点 y=105px）；给页面根节点和入口 Column 各加 expandSafeArea 的情况下节点仍从 y=105px 起
