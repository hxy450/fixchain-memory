# 开启全屏布局后，前景按测得的避让区补 padding；expandSafeArea 只让背景越过安全区，不是避让

ID：`lesson-a8452bfea5d42d3dcae3` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，为调用 setWindowLayoutFullScreen(true) 的入口壳（根 Navigation + Tabs/NavDestination）落实状态栏与底部导航条避让时

## 适用情境

规格或 ui-manifest 标注全屏页、需要沉浸式安全区，并把 API 细节委托给具名 skill（如 arkts-immersive-safearea）；EntryAbility 开启全屏布局，页面标题由 NavDestination 标题栏或自绘标题承担；源端通常是 enableEdgeToEdge 加 safeDrawingPadding。

## 原因

setWindowLayoutFullScreen(true) 让窗口内容铺到系统栏下，expandSafeArea 只允许容器背景延伸进安全区，两者都不会给前景留出避让空间；既不测量避让区也不补 padding，标题与返回键就画进状态栏。来源中规格模板与自写的 ui-manifest 都要求按该 skill 的分层架构实现，生成者没有加载 skill，只在根 Column 上加 expandSafeArea，并在入口注释为“由页面处理安全区”，所有全屏页标题都落在状态栏内。

## 做法

1. 规格把沉浸式实现委托给具名 skill 时，先完整加载该 skill，按其分层清单（窗口全屏、避让区测量、前景 padding）实现，不以自拟的最简方案代替；找不到 skill 时在实现记录中写明缺口。
2. 用 getWindowAvoidArea(TYPE_SYSTEM) 的 topRect.height 与 TYPE_NAVIGATION_INDICATOR 的 bottomRect.height 取避让值，经 UIContext 的 px2vp 换算后，作为承载前景那一层（如根 Navigation 或页面内容层）的 top/bottom padding，并在窗口尺寸变化时更新；背景需要延伸到系统栏下时，才在背景节点自身加 expandSafeArea。

## 可选检查

- 工程开启了全屏布局，却找不到任何 getWindowAvoidArea 读取或基于避让高度的 padding 时，视为安全区未落实；有设备时截图核对标题与状态栏的纵向区间不重叠。

## 来源（按需复核）

- [case-57a2aab5dd7835648d69](../../../store/cases/case-57a2aab5dd7835648d69/ed5970e0c92c3f4c6519a62ea560cfbab2e6927727a69c6e7430ebc372453828.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ed5970e0c92c3f4c6519a62ea560cfbab2e6927727a69c6e7430ebc372453828`
