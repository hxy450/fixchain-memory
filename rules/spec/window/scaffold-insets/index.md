# Scaffold 的 innerPadding 和顶部安全区

agent 会看到什么：读过的 Compose 源码里 Scaffold 不传 topBar、把 padding(innerPadding).consumeWindowInsets 交给嵌套子页，或同一 Box 里叠着列表、顶栏和浮层；交回的规格里顶部状态栏由谁消费、子页和浮层按什么口径避让

## 规矩

- rule-17aa049bf801｜Scaffold 无 topBar 时 innerPadding 含状态栏，规格不能写成只消费底栏｜读到：Scaffold 没传 topBar、没改 contentWindowInsets，content 用 Modifier.padding(innerPadding)（常接 .consumeWindowInsets）挂子页；写错：壳页规格写「只消费底栏高度，顶部状态栏由各 Tab 页自行处理」；子页规格消费真实 statusBarHeight 或写「不做顶部占位」
- rule-48e050558cc0｜同一内容区的列表、顶栏、浮层共用一个避让口径，改一处 inset 时同区规格一并改｜读到：源端同一个 Box 里叠着列表、顶栏和浮层（scrim + 居中卡片，Modifier.fillMaxSize()），整体在 Scaffold innerPadding 之内；写错：列表首项、顶栏的规格按 statusBarHeight 避让，浮层规格却写「needs_immersive_safearea=false → 跳过本契约；scrim 覆盖整个区域（含顶部状态栏占位区）」，状态接口没有 statusBarHeight；或收到 inset 纠正后只改了一页的规格
