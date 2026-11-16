# 自绘标题栏的顶部避让

agent 会看到什么：目标页 hideTitleBar 或全屏布局下自绘标题栏；产物里标题栏的 .height(…) 与 .padding({ top: … })、NavDestination 的 .title(...) 和顶部避让值用在哪

## 规矩

- rule-aea9cf5feed7｜根 Navigation 扩展安全区时，NavDestination 隐藏系统标题栏并自绘工具栏｜读到：规格把源端 ActionBar / Toolbar 映射为「NavDestination 自带标题栏」，根 Navigation 已有或将有 expandSafeArea；写错：NavDestination 保留了 .title(...) 系统标题栏，前景只加 bottom padding，测得的 windowTopPadding 没用在任何前景上
- rule-ba03efff878a｜hideTitleBar 自绘工具栏时，外层容器实际写 padding top 接顶部避让值｜读到：源 Activity 用窗口 ActionBar（主题如 Theme.AppCompat.Light.DarkActionBar，Up 返回）；目标开启全屏布局，NavDestination 改 .hideTitleBar(true) 自绘工具栏；写错：包工具栏的外层 Column 只有「避状态栏」之类的注释，没有 .padding({ top: … }) 引用顶部避让值；窗口模型只声明并 connect，成了没被引用的成员
- rule-44c2648ca29c｜全屏自绘标题栏时，状态栏避让单独成块再接 56vp 栏，不在 height(56) 里加 top｜读到：源端是 AppCompat ActionBar（默认高 56dp），目标页 hideTitleBar 自绘标题栏、在全屏窗口内做安全区避让；写错：标题栏写成 .height(56).padding({ top: 顶部避让 }) 一行，避让挤占栏内高度，状态栏区域没有底色
- rule-7ca6c4c30079｜定高标题栏加顶部 padding 时按 height 含 padding 算，inset 放外层或同步增高｜读到：源标题栏或 ActionBar 是固定高度（如 48dp）的一行；写错：同一行写 .height(48) 又加 .padding({ top: topInset })，以为高度不含 padding，可见高度被压成 48 − inset
- rule-b3ae62ccb23e｜迁 M3 small TopAppBar 时，自绘顶栏行固定 64vp、状态栏 padding 在外层、水平 4vp｜读到：Compose TopAppBar(title = …, navigationIcon = …) 没写高度和内边距；写错：自绘顶栏 Row .height(56)，或 .height(64) 配 .padding({ top: windowTopPadding }) 把状态栏算进 64，或 .padding({ left: 16, right: 16 })，标题前没有 4vp 内边距
- rule-dcd14bdc16b2｜自绘顶栏不在同一容器上同时写 height(N) 和 padding(top: inset)，分两层或高度加 inset｜读到：源端顶栏用 TopAppBar 加 statusBars insets 避让，内容高度固定；写错：同一个 Row 上写 .height(64).padding({ top: windowTopPadding })，菜单却按 windowTopPadding + 64 定位
- rule-de42a83d2601｜全屏窗口加根 Navigation expandSafeArea 下，NavDestination 页不靠原生标题栏避让｜读到：页面规格 needs_immersive_safearea=true，转换决策把源端 TopAppBar 映射为 NavDestination 原生标题栏；写错：NavDestination 用 .title() 原生标题栏且没有 windowTopPadding，注释写「原生标题栏自动避让，无需手写 padding」
- rule-ac0eed05f74a｜延后状态栏避让时，自绘标题栏外层也留顶部 inset 钩子，FWD-REF 写明顶部和底部两处｜读到：派工写 needs_immersive_safearea=true；源页面用 IonHeader / IonToolbar 自绘顶部工具栏，目标是 NavDestination().hideTitleBar(true) 子页，WindowModel 还没落地；写错：自绘标题栏的头部 Stack 外层没有任何顶部 inset 钩子，唯一的 FWD-REF 放在 Scroll 底部，注释只写底部 safe-area 份额
