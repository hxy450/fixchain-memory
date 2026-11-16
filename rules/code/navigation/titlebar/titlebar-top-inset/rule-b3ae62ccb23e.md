# 迁 M3 small TopAppBar 时，自绘顶栏行固定 64vp、状态栏 padding 在外层、水平 4vp

审的是：代码
触发（任一种）：
- 读到：Compose TopAppBar(title = …, navigationIcon = …) 没写高度和内边距；写错的样子：自绘顶栏 Row .height(56)，或 .height(64) 配 .padding({ top: windowTopPadding }) 把状态栏算进 64，或 .padding({ left: 16, right: 16 })，标题前没有 4vp 内边距
适用范围：Material 3 small TopAppBar 迁成自绘 ArkUI 顶栏时
做法：
- 顶栏行 .height(64)，状态栏避让的 padding 加在外层容器上；行的水平 padding 4，导航图标 48，标题起点 56（4+48+4）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 顶栏行固定 64vp、状态栏 padding 在外层、标题水平 4vp：返修后的度量（出处：卡里修好并验证过）
针对本应用要查的：
- 应用所用 material3 版本里 small TopAppBar 的默认度量：源工程 compose BOM 决定的 androidx.compose.material3:material3 版本的源码里 small TopAppBar 容器高和水平内边距常量；读出 dp 值，按 1dp = 1vp 写进顶栏
未核实：默认度量出自卡，本机没有 material3 的源码，没核到原文
来源：1 张卡，1 个应用
- case-6aada7248be5df4c858e（jerboa）：做法第 1 步 ← 诊断、建议 2；取值 1 ← 诊断
