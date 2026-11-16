# 全屏页的前景避让逐边落实：伸到窗口底边的内容层补 windowBottomPadding

审的是：代码
触发（任一种）：
- 读到：页面规格标 needs_immersive_safearea=true、按 arkts-immersive-safearea 四层架构实施；Layer 3 写明标题栏补 windowTopPadding、贴底内容补 windowBottomPadding；写错的样子：只给标题栏外层加了 .padding({ top: windowTopPadding })，伸到窗口底边的根 Column 只有 width/height 100%、没有底部 padding；报告 immersive_safearea_implemented 只列了顶部一处
适用范围：目标页是要沉浸式避让的全屏 NavDestination、内容层伸到窗口底边时；入口开没开全屏都适用
做法：
- 顶部加在标题栏外层，底部加在伸到窗口底边的那一层：如根 Column 写 .padding({ bottom: windowModel.windowBottomPadding })；入口还没开全屏时也照样接上（当下值为 0）
- 按 min(宽, 高) 取边长的区域（如棋盘）在避让之后的内容区里测量
- 报告 immersive_safearea_implemented 时按 top、bottom 分别列出位置；只接了顶部就不写「Layer 3 已实施」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setWindowLayoutFullScreen(isLayoutFullScreen: boolean): Promise<void>：设置主窗口或子窗口布局是否沉浸；开启后前景会伸到系统栏下（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowLayoutFullScreen）
- getWindowAvoidArea(type: AvoidAreaType): AvoidArea；TYPE_NAVIGATION_INDICATOR = 4 是底部导航区域，TYPE_SYSTEM = 0 是系统默认区域：底部避让值来自导航条区域（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getWindowAvoidArea、AvoidAreaType；arkts-apis-window-e.md，AvoidAreaType）
- 页面连接 WindowModel，内容列加 padding({ bottom: windowBottomPadding })：返修后横屏棋盘和重开按钮不再落进导航条区（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-4e1ab457a4fa55aaeb29（Privacy Friendly 2048）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1；取值 3 ← 诊断
