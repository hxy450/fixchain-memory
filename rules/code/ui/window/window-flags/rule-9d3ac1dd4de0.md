# 源主题全屏且沉浸只切导航栏时，非沉浸用 setWindowSystemBarEnable(['navigation'])

审的是：代码
触发（任一种）：
- 读到：主题 <item name="android:windowFullscreen">true</item>；Activity 的沉浸切换只显隐导航栏（注释如「only show/hide navigation bars, as we run with system bars always hidden」）；写错的样子：非沉浸分支调用 setWindowSystemBarEnable(['status', 'navigation'])，把源端始终隐藏的状态栏显示出来
适用范围：迁移源端窗口系统栏显隐策略、目标用 Window.setWindowSystemBarEnable 时
做法：
- 非沉浸写 win.setWindowSystemBarEnable(['navigation'])，沉浸写 win.setWindowSystemBarEnable([])；不默认 ['status', 'navigation']
- 拿到窗口之前已请求的沉浸态，在窗口就绪后重放一次
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setWindowSystemBarEnable(names: Array<'status' | 'navigation'>): Promise<void>：数组列的是要显示的栏（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowSystemBarEnable）
- 需全部显示，该参数设置为['status', 'navigation']；设置为[]，则不显示：只列 'navigation' 就是只显示导航栏、状态栏保持隐藏（出处：arkts-apis-window-Window.md，setWindowSystemBarEnable）
- windowFullscreen：format="boolean"，Flag indicating whether this window should fill the entire screen，对应 FLAG_FULLSCREEN：源主题设 true 时状态栏始终隐藏（出处：Android SDK 平台资源 data/res/values/attrs.xml，windowFullscreen（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 源端是否全屏、沉浸切换动了哪些栏：源工程 res/values*/styles.xml、themes.xml 里 Activity 所用主题的 android:windowFullscreen；Activity 里沉浸切换方法设的 SYSTEM_UI_FLAG_* 或显隐的栏类型；读出被显隐的栏，非沉浸时只把源端会显示的栏放进数组
未核实：卡里的环境是 HarmonyOS 6.1.1(24)，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-0ad4c0a7a8504a2d412a（opencamera-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 诊断
