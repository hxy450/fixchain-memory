# 源端只有 FLAG_FULLSCREEN 时，规格写只隐藏状态栏、导航栏保留、窗口止于其上

审的是：规格
触发（任一种）：
- 读到：源 Activity 调 requestWindowFeature(FEATURE_NO_TITLE) 和 setFlags(FLAG_FULLSCREEN)，或主题 android:windowFullscreen 为 true，没有隐藏导航栏或延伸到导航栏下的标志；写错的样子：规格写「源为真全屏窗口」「沉浸式四件套」、needs_immersive_safearea=true、背景延伸全屏，没写导航栏保留和应用窗口止于导航栏之上
适用范围：规格提取时翻译源 Activity 的全屏旗标、写目标窗口系统栏和页面安全区那一节
做法：
- 规格逐边写系统栏形态：状态栏隐藏；导航栏（三键栏、导航条）可见，应用窗口止于其上；页面背景和内容都不向导航区延伸；目标只隐藏状态栏、保留导航栏与手势条
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- FLAG_FULLSCREEN：窗口在顶层时隐藏状态栏；已废弃，替代写法是 WindowInsetsController#hide(Type.statusBars())：这个旗标对应的是状态栏，不涉及导航栏（出处：android.view.WindowManager.LayoutParams#FLAG_FULLSCREEN）
- android:windowFullscreen 控制同一个旗标，标准 *.NoTitleBar.Fullscreen 主题自动设置它：主题里的 windowFullscreen 与代码里的 FLAG_FULLSCREEN 同义（出处：android.view.WindowManager.LayoutParams#FLAG_FULLSCREEN）
- 参照机上 FLAG_FULLSCREEN 窗口：状态栏隐藏、导航栏保留、应用窗口止于导航栏之上：源端实际形态（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-bbb49cc9ec510f04eb33（Bubble Shooter）：做法第 1 步 ← 建议 1；取值 3 ← 诊断
