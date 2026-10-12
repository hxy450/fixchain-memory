# 开启全屏布局后，前景按测得的避让区逐边补 padding；expandSafeArea 只让背景越过安全区，预设系统标题栏也不会自动避让

ID：`lesson-a8452bfea5d42d3dcae3` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，为调用 setWindowLayoutFullScreen(true) 的入口壳（根 Navigation + Tabs/NavDestination）落实状态栏与底部导航条避让时；转换承载内嵌子页的壳 NavDestination、移植 Android insets 代码，或入口根 Navigation 四向 expandSafeArea 后逐页核对时

## 适用情境

规格或 ui-manifest 标注全屏页、需要沉浸式安全区，并把 API 细节委托给具名 skill（如 arkts-immersive-safearea）；EntryAbility 开启全屏布局，页面标题由 NavDestination 标题栏或自绘标题承担；源端通常是 enableEdgeToEdge 加 safeDrawingPadding。也包括壳页承载声明豁免安全区、自绘工具栏的内嵌子页，源端顶部 inset 由子 Fragment 的 AppBarLayout 或 Toolbar 根布局 fitsSystemWindows 隐式消费、Activity 代码只显式处理底部和左右；或 NavDestination 页保留预设系统标题栏。

## 原因

setWindowLayoutFullScreen(true) 让窗口内容铺到系统栏下，expandSafeArea 只允许容器背景延伸进安全区，两者都不会给前景留出避让空间；既不测量避让区也不补 padding，标题与返回键就画进状态栏。来源中规格模板与自写的 ui-manifest 都要求按该 skill 的分层架构实现，生成者没有加载 skill，只在根 Column 上加 expandSafeArea，并在入口注释为“由页面处理安全区”，所有全屏页标题都落在状态栏内。只照搬源 Activity 显式写出的 insets 代码会漏掉经 fitsSystemWindows 隐式消费的顶部；预设系统标题栏不会因根容器扩展而自动避让，标题栏会叠进状态栏（依据修复期截图）。

## 做法

1. 规格把沉浸式实现委托给具名 skill 时，先完整加载该 skill，按其分层清单（窗口全屏、避让区测量、前景 padding）实现，不以自拟的最简方案代替；找不到 skill 时在实现记录中写明缺口。
2. 用 getWindowAvoidArea(TYPE_SYSTEM) 的 topRect.height 取顶部避让；底部取 TYPE_SYSTEM 与 TYPE_NAVIGATION_INDICATOR 两者 bottomRect.height 的较大值，覆盖三键导航栏与手势条。经 UIContext 的 px2vp 换算后，作为承载前景那一层（如根 Navigation 或页面内容层）的 top/bottom padding，并在窗口尺寸或避让区变化（avoidAreaChange）时更新；背景需要延伸到系统栏下时，才在背景节点自身加 expandSafeArea。
3. 壳页承载声明豁免安全区的内嵌子页时，根容器同时补顶部与底部避让；移植 insets 时逐边核对四边各由谁负责，包括经 fitsSystemWindows 隐式消费的顶部。
4. 需要标题栏的全屏 NavDestination 页用 hideTitleBar(true)，自绘工具栏并给其所在容器加顶部避让；除非在根容器扩展状态下实测确认，不预设系统标题栏会自动避让。

## 可选检查

- 工程开启了全屏布局，却找不到任何 getWindowAvoidArea 读取或基于避让高度的 padding 时，视为安全区未落实；有设备时截图核对标题与状态栏的纵向区间不重叠。
- 入口根容器扩展安全区后逐页确认顶部由本页或宿主负责；只处理了底部避让的页面不算完成

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-01833db0536ba02ed2ce](../../../store/cases/case-01833db0536ba02ed2ce/19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79.json) · 结论：diagnosis, recommendation:2
  卡片版本：`19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79`
- [case-57a2aab5dd7835648d69](../../../store/cases/case-57a2aab5dd7835648d69/ed5970e0c92c3f4c6519a62ea560cfbab2e6927727a69c6e7430ebc372453828.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ed5970e0c92c3f4c6519a62ea560cfbab2e6927727a69c6e7430ebc372453828`
- [case-b4a2f2d65e01a68393e3](../../../store/cases/case-b4a2f2d65e01a68393e3/b45e9443ba0c8d589aa6a362a2f7e447bb656b4d5cf61a7e8f28c3af39dd8bb1.json) · 结论：recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`b45e9443ba0c8d589aa6a362a2f7e447bb656b4d5cf61a7e8f28c3af39dd8bb1`
