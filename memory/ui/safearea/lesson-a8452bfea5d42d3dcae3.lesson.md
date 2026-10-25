# 开启全屏布局前逐边核对源端系统栏：只沉浸状态栏（透明状态栏、未设 navigationBarColor、targetSdk≤34）时底部保留不透明导航栏底色；全屏后前景按测得的避让区逐边补 padding（顶部加在包住标题栏的层，底部加在伸到窗口底边的层）；expandSafeArea 只让背景越过安全区，预设系统标题栏也不会自动避让

ID：`lesson-a8452bfea5d42d3dcae3` · 版本：6

[本主题](index.md)

## 何时使用

界面实现阶段，为调用 setWindowLayoutFullScreen(true) 的入口壳（根 Navigation + Tabs/NavDestination）落实状态栏与底部导航条避让、决定各边背景是否延伸时；转换承载内嵌子页的壳 NavDestination、移植 Android insets 代码，或入口根 Navigation 四向 expandSafeArea 后逐页核对时

## 适用情境

规格或 ui-manifest 标注全屏页、需要沉浸式安全区，并把 API 细节委托给具名 skill（如 arkts-immersive-safearea）；EntryAbility 开启全屏布局，页面标题由 NavDestination 标题栏或自绘标题承担；源端通常是 enableEdgeToEdge 加 safeDrawingPadding。也包括源端只用 SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN 加透明 statusBarColor，没有 navigationBarColor、windowTranslucentNavigation、HIDE_NAVIGATION，targetSdk≤34：导航栏是不透明黑底，应用内容止于其上。也包括页面只给标题栏补了顶部避让，伸到窗口底边的内容（如按 min(宽,高) 取边长的棋盘）没有底部避让。也包括壳页承载声明豁免安全区、自绘工具栏的内嵌子页，源端顶部 inset 由子 Fragment 的 AppBarLayout 或 Toolbar 根布局 fitsSystemWindows 隐式消费；或 NavDestination 页保留预设系统标题栏。

## 原因

setWindowLayoutFullScreen(true) 让窗口内容铺到系统栏下，expandSafeArea 只允许容器背景延伸进安全区，两者都不会给前景留出避让空间；既不测量避让区也不补 padding，标题与返回键就画进状态栏。只补顶部时，伸到窗口底边的内容落进导航条区（来源中横屏棋盘最下一行与重开按钮被盖住）。“透明状态栏”也不等于整窗沉浸：源端导航栏不透明时，全屏后让页面底色填进导航区就与源端不同。来源中规格模板要求所有全屏页按四层架构实现，却没问每条系统栏在源端是什么样；只照搬源 Activity 显式写出的 insets 代码会漏掉经 fitsSystemWindows 隐式消费的顶部；预设系统标题栏不会因根容器扩展而自动避让。

## 做法

1. 开全屏前逐边列出源端状态栏、导航栏的颜色与是否沉浸：只有源端让内容画到某条系统栏下（enableEdgeToEdge、LAYOUT_HIDE_NAVIGATION、透明 navigationBarColor 或 targetSdk≥35）时，才让该边背景延伸；源端导航栏不透明时，全屏后在底部避让区叠同色、不参与命中的占位，不让页面底色填充。
2. 规格把沉浸式实现委托给具名 skill 时，先完整加载该 skill，按其分层清单（窗口全屏、避让区测量、前景 padding）实现，不以自拟的最简方案代替；找不到 skill 时在实现记录中写明缺口。
3. 用 getWindowAvoidArea(TYPE_SYSTEM) 的 topRect.height 取顶部避让；底部取 TYPE_SYSTEM 与 TYPE_NAVIGATION_INDICATOR 两者 bottomRect.height 的较大值。经 UIContext 的 px2vp 换算后按边落实：顶部加在包住标题栏的那一层，底部加在伸到窗口底边的内容层（入口尚未开全屏时也接上，当下值为 0），按 min(宽,高) 取边长的区域在避让之后测量；在 avoidAreaChange 时更新。背景需要延伸到系统栏下时，才在背景节点自身加 expandSafeArea。
4. 壳页承载声明豁免安全区的内嵌子页时，根容器同时补顶部与底部避让；移植 insets 时逐边核对四边各由谁负责，包括经 fitsSystemWindows 隐式消费的顶部。
5. 需要标题栏的全屏 NavDestination 页用 hideTitleBar(true)，自绘工具栏并给其所在容器加顶部避让；除非在根容器扩展状态下实测确认，不预设系统标题栏会自动避让。

## 可选检查

- 工程开启了全屏布局，却找不到任何 getWindowAvoidArea 读取或基于避让高度的 padding 时，视为安全区未落实；有设备时截图核对标题与状态栏的纵向区间不重叠。
- 开启全屏的一方逐页 grep 顶部与底部避让的消费点：只处理了顶部或只处理了底部的页面不算完成，并在横屏下核对贴底内容不落进导航条区。

来源支持：7 张卡 · 已知 5 次迁移（部分未记录） · 已知 5 个应用（部分未记录）

## 来源（按需复核）

- [case-01833db0536ba02ed2ce](../../../store/cases/case-01833db0536ba02ed2ce/19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79.json) · 结论：diagnosis, recommendation:2
  卡片版本：`19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79`
- [case-0a77d32c850d4767a2d4](../../../store/cases/case-0a77d32c850d4767a2d4/f1b0f704ea098891e19e7e62141a77777b9fac05a89eb4bc2d242d1b6b17917f.json) · 结论：recommendation:4
  卡片版本：`f1b0f704ea098891e19e7e62141a77777b9fac05a89eb4bc2d242d1b6b17917f`
- [case-11e45f7bea96bac1c5b5](../../../store/cases/case-11e45f7bea96bac1c5b5/263a41a9f4b0938d139f6cc94479f8613606ed593358dc8c1d8e420101b7f820.json) · 结论：diagnosis, recommendation:4
  卡片版本：`263a41a9f4b0938d139f6cc94479f8613606ed593358dc8c1d8e420101b7f820`
- [case-4e1ab457a4fa55aaeb29](../../../store/cases/case-4e1ab457a4fa55aaeb29/11acfe1b93418070b8355be20ceaebf8f80fc0b5792b14112a64b2e6c30bb6d9.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`11acfe1b93418070b8355be20ceaebf8f80fc0b5792b14112a64b2e6c30bb6d9`
- [case-57a2aab5dd7835648d69](../../../store/cases/case-57a2aab5dd7835648d69/ed5970e0c92c3f4c6519a62ea560cfbab2e6927727a69c6e7430ebc372453828.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ed5970e0c92c3f4c6519a62ea560cfbab2e6927727a69c6e7430ebc372453828`
- [case-b3c176b95cabcc03a434](../../../store/cases/case-b3c176b95cabcc03a434/acbf9ff15291867da7f28e180e80f8cb9c7277b41e553e0de94f4f92a056e637.json) · 结论：recommendation:4
  卡片版本：`acbf9ff15291867da7f28e180e80f8cb9c7277b41e553e0de94f4f92a056e637`
- [case-b4a2f2d65e01a68393e3](../../../store/cases/case-b4a2f2d65e01a68393e3/b45e9443ba0c8d589aa6a362a2f7e447bb656b4d5cf61a7e8f28c3af39dd8bb1.json) · 结论：recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`b45e9443ba0c8d589aa6a362a2f7e447bb656b4d5cf61a7e8f28c3af39dd8bb1`
