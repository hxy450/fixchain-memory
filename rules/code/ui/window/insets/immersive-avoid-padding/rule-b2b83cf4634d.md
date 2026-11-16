# 全屏沉浸后每个 NavDestination 页都要真用避让值加 padding，不能只写注释标记

审的是：代码
触发（任一种）：
- 读到：窗口 setWindowLayoutFullScreen(true)，根 Navigation 加了四向 expandSafeArea；派工的安全区修复口径写「复用 ImmersiveScaffold 或手动 padding windowTop/BottomPadding」；写错的样子：NavDestination 页里只有「// ImmersiveScaffold contract: …」之类的注释，没有订阅共享避让模型，顶部仍是固定 top 间距，找不到 windowTopPadding / windowBottomPadding 的 .padding 表达式
适用范围：窗口全屏、根 Navigation expandSafeArea 之后，各 NavDestination 页自己做前景避让时
做法：
- 每个 NavDestination 页订阅共享避让模型：顶部前景写 .padding({ top: windowTopPadding + <源端在状态栏高度之外的额外间距> })，列表等底部内容写 .padding({ bottom: windowBottomPadding })
- 安全区检查按关键字搜时，不用含关键字的注释去满足；每页都要有实际引用避让值的 padding 表达式
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setWindowLayoutFullScreen(isLayoutFullScreen: boolean): Promise<void>：Window 上开关窗口沉浸式布局；开了以后内容画到状态栏和导航条下面（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowLayoutFullScreen）
- expandSafeArea(types?: Array<SafeAreaType>, edges?: Array<SafeAreaEdge>): T：CommonMethod：把组件扩展进安全区；不传参时 types 是 SYSTEM、CUTOUT、KEYBOARD，edges 是四向（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.expandSafeArea）
- 源端顶部间距 = 状态栏高 + 额外 dp 时，鸿蒙端顶部写 windowTopPadding + 同样的额外值，列表底部留 windowBottomPadding：改成这样后搜索栏不再落进状态栏区（出处：卡里修好并验证过）
未核实：卡里环境是 API 24（6.1.1），本机按 API 23 的声明核对
来源：1 张卡，1 个应用
- case-436d1b16d79796c667d6（android-panorama-map-vest7）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 3 ← 诊断
