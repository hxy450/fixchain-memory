# 宿主已消费状态栏时，tab 子页的 spacer 不再加状态栏高度，悬浮顶栏与列表同一基准

审的是：代码
触发（任一种）：
- 读到：子页源码 Spacer(Modifier.windowInsetsTopHeight(WindowInsets.statusBars.add(WindowInsets(top = N.dp)))) 或 Spacer(Modifier.statusBarsPadding())，宿主已 consumeWindowInsets；写错的样子：子页首项 spacer 写成 .height(顶部避让值 + N)，或顶部多一个 Column().height(顶部避让值)；悬浮顶栏从 y=0 起不带避让
适用范围：宿主壳已在 tab 内容区消费状态栏的 ArkUI tab 子页（宿主内嵌的子组件）
做法：
- statusBars + N 的 spacer 写成 .height(N)；statusBarsPadding 的 spacer 删掉；子页不再订阅窗口避让值去叠加状态栏
- 叠在列表上方的悬浮顶栏和列表首项 spacer 用同一个顶部基准：都从宿主已让出状态栏的内容区顶边算
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Feed/Cart 类子页 spacer 只留 56、Search 类去掉状态栏 spacer 后与安卓对齐：修好后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-cfab70f115f2d290e44a（Jetsnack）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 1 ← 诊断
