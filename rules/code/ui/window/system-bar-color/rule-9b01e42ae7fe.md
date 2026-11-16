# 源窗口非全屏时，入口写 setWindowLayoutFullScreen(false)，系统栏照源着色

审的是：代码
触发（任一种）：
- 读到：源主题非全屏（Theme.Holo 等，无 windowFullscreen / windowTranslucent* / FLAG_FULLSCREEN），系统栏不透明；写错的样子：EntryAbility 写 setWindowLayoutFullScreen(true)、系统栏 '#00000000' 透明、建 WindowModel 测避让；根 Navigation 写 expandSafeArea，各页加 windowTopPadding / windowBottomPadding
适用范围：源端窗口不延伸到系统栏下，迁移入口窗口设置和各页避让时
做法：
- 在 loadContent 回调里 await win.setWindowLayoutFullScreen(false)，再 setWindowSystemBarProperties({ statusBarColor, navigationBarColor, statusBarContentColor, navigationBarContentColor }) 照源着色（Holo：'#FF000000' + 白色图标）
- 加 setWindowSystemBarEnable(['status', 'navigation'])，横屏也显示系统栏
- 不建 WindowModel，根 Navigation 不写 expandSafeArea，各页不加 windowTopPadding / windowBottomPadding；页面根背景铺源窗口背景色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setWindowLayoutFullScreen(isLayoutFullScreen: boolean): Promise<void>：主窗口或子窗口布局是否沉浸；false 时内容在系统栏之间（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowLayoutFullScreen）
- setWindowSystemBarProperties(systemBarProperties: SystemBarProperties): Promise<void>：设置系统栏属性（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowSystemBarProperties）
- SystemBarProperties：statusBarColor?: string、statusBarContentColor?: string、navigationBarColor?: string、navigationBarContentColor?: string：栏底色和图标、文字色（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，SystemBarProperties）
- setWindowSystemBarEnable(names: Array<'status' | 'navigation'>): Promise<void>：设置主窗口显示哪些系统栏（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowSystemBarEnable）
- 鸿蒙横屏默认隐藏状态栏；补 setWindowSystemBarEnable(['status','navigation']) 后横屏也显示：源端任何方向都显示系统栏时要补这一句（出处：卡里修好并验证过）
针对本应用要查的：
- 源端系统栏底色和图标色：源工程主题链里的 android:statusBarColor、android:navigationBarColor、windowLightStatusBar；没写时看平台主题默认；读出颜色写进 SystemBarProperties；例：Theme.Holo 下两栏都是黑底白图标
来源：1 张卡，1 个应用
- case-af09311d7897ca1af0cd（Blockinger）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；做法第 3 步 ← 建议 3；取值 5 ← 诊断
