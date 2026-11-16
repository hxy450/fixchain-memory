# 规格全局约定逐条写源端状态栏、导航栏各自的颜色和是否沉浸，不把透明状态栏写成全屏

审的是：规格
触发（任一种）：
- 读到：源 Activity 只用 SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN（没有 HIDE_NAVIGATION）加 setStatusBarColor(TRANSPARENT)，或 values-v21 的 statusBarColor 为 transparent；主题没设 navigationBarColor，targetSdkVersion < 35；写错的样子：规格或界面清单只写「透明状态栏全屏」「全屏页统一四层架构」，没写导航栏颜色、内容是否画到导航栏下；系统栏外观验收里没有导航栏一项
适用范围：规格提取时为应用决定窗口沉浸范围、写系统栏全局约定和外观验收时
做法：
- 全局约定里每条系统栏各写一行：状态栏是否透明、内容是否画到其下；导航栏颜色（取 navigationBarColor，未设时系统默认黑底）、有无 HIDE_NAVIGATION / enableEdgeToEdge、targetSdk 是否 ≥ 35（强制 edge-to-edge）
- 只沉浸状态栏的应用写明「导航栏不透明黑底，应用内容止于其上方」，并把它列进系统栏外观验收
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 主题没指定 navigationBarColor、没强制 edge-to-edge、设备 config_navBarDefaultTransparent 为 false 时，导航栏用 navigation_bar_compatible：未设导航栏颜色时框架给的兼容色（出处：com.android.internal.policy.PhoneWindow#generateLayout）
- navigation_bar_compatible = @android:color/black；navigation_bar_default = #00808080（只用来判断主题是否自己设过）：兼容色是黑色（出处：Android SDK 平台资源 data/res/values/colors.xml，navigation_bar_compatible、navigation_bar_default（按应用的 compileSdk 取对应平台））
- ENFORCE_EDGE_TO_EDGE 自 targetSdk VANILLA_ICE_CREAM（35）起默认开启：targetSdk < 35 时系统不强制 edge-to-edge，导航栏不会被改成透明（出处：com.android.internal.policy.PhoneWindow#ENFORCE_EDGE_TO_EDGE）
- 取色确认源端导航栏为黑底，应用内容止于其上方：只沉浸状态栏时导航栏的实际外观（出处：卡里修好并验证过）
针对本应用要查的：
- 源端每条系统栏的颜色和是否沉浸：源工程 res/values*/styles.xml、themes.xml 里应用 / Activity 主题的 android:navigationBarColor、android:statusBarColor、windowTranslucentNavigation；Activity 代码里的 setSystemUiVisibility 标志、setNavigationBarColor、enableEdgeToEdge；构建脚本里的 targetSdkVersion；逐条写进约定：没设 navigationBarColor、没有 HIDE_NAVIGATION / 透明导航栏、targetSdk < 35 时，导航栏是不透明黑底
来源：1 张卡，1 个应用
- case-11e45f7bea96bac1c5b5（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 4 ← 诊断
