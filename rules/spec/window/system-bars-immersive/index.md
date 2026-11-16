# 窗口沉浸和系统栏外观

agent 会看到什么：读到源主题链和 Activity 代码里关于系统栏的写法（windowFullscreen、透明 statusBarColor、SYSTEM_UI_FLAG_LAYOUT_*、targetSdk），或什么都没写；规格的沉浸式节、全局约定照 page_type 默认值或一句「透明状态栏全屏」写成，没逐条系统栏写颜色和内容是否画到其下

## 通用查法

### 规格写窗口沉浸和系统栏外观时，逐条系统栏查源主题链、窗口标志和 targetSdk

审的是：规格
触发（任一种）：
- 读到：源主题链和 Activity 代码里的系统栏写法（windowFullscreen、windowTranslucentStatus、statusBarColor / navigationBarColor、SYSTEM_UI_FLAG_*、enableEdgeToEdge），或这些都没写；写错的样子：规格的沉浸式节、系统栏约定照 page_type 默认值或一句「透明状态栏全屏」写成，没逐条栏写底色、内容是否画到其下和依据
适用范围：规格阶段写窗口是否全屏、系统栏底色和内容避让（含 needs_immersive_safearea）时
做法：
- 照下面「要查的」一项，状态栏、导航栏各查一遍主题链、Activity 代码和 targetSdkVersion 里的信号
- 全局约定每条栏写一行：底色、内容是否画到其下、依据的信号；没有信号的栏写不透明、内容止于其外，needs_immersive_safearea 按查出的结果填，不用 page_type 默认值
- 系统栏外观验收里每条栏各列一项
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- windowFullscreen：Flag indicating whether this window should fill the entire screen，对应 FLAG_FULLSCREEN：主题里要有这一项才是全屏窗口（出处：Android SDK 平台资源 data/res/values/attrs.xml，Window 的 windowFullscreen（按应用的 compileSdk 取对应平台））
- windowTranslucentStatus：请求半透明状态栏，对应 FLAG_TRANSLUCENT_STATUS：有这一项时内容才延伸到状态栏下（出处：Android SDK 平台资源 data/res/values/attrs.xml，Window 的 windowTranslucentStatus（按应用的 compileSdk 取对应平台））
- FLAG_FULLSCREEN：hide all screen decorations (such as the status bar) while this window is displayed：代码里设了它才隐藏状态栏（出处：android.view.WindowManager.LayoutParams#FLAG_FULLSCREEN）
- 主题没指定 navigationBarColor、没强制 edge-to-edge、设备 config_navBarDefaultTransparent 为 false 时，导航栏用 navigation_bar_compatible：未设导航栏颜色时框架给的兼容色（出处：com.android.internal.policy.PhoneWindow#generateLayout）
- navigation_bar_compatible = @android:color/black：兼容色是黑色（出处：Android SDK 平台资源 data/res/values/colors.xml，navigation_bar_compatible（按应用的 compileSdk 取对应平台））
- ENFORCE_EDGE_TO_EDGE 自 targetSdk VANILLA_ICE_CREAM（35）起默认开启：targetSdk < 35 时系统不强制 edge-to-edge（出处：com.android.internal.policy.PhoneWindow#ENFORCE_EDGE_TO_EDGE）
- 例：Theme.Holo + targetSdk 17、没有上述任何信号时，各页内容在黑色状态栏和导航栏之间：一个非全屏源窗口的实际样子（只在这个条件下成立）（出处：卡里修好并验证过）
针对本应用要查的：
- 每条系统栏的底色和内容是否画到其下：源工程 AndroidManifest 或构建脚本里的 targetSdkVersion；Activity / application 的 android:theme，沿 res/values*/styles.xml、themes.xml 的 parent 查到平台主题，看 windowFullscreen、windowTranslucentStatus / windowTranslucentNavigation、statusBarColor / navigationBarColor；Activity 代码里的 getWindow().addFlags、setSystemUiVisibility、setStatusBarColor / setNavigationBarColor、setDecorFitsSystemWindows(false)、enableEdgeToEdge；逐条栏记下找到的信号和颜色：有沉浸信号的那条栏按画到其下写；都没有就是不透明栏，底色取主题的 statusBarColor / navigationBarColor 或平台主题默认；没设 navigationBarColor、没有透明导航栏、targetSdk < 35 时导航栏是不透明黑底
未核实：主题和 Activity 代码对同一条系统栏都设了值时以哪个为准，族里规矩没有核实；状态栏没设 statusBarColor 时各平台主题、AppCompat 主题给的默认底色，族里规矩没有核实
来源：2 张卡，2 个应用
- case-11e45f7bea96bac1c5b5（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-af09311d7897ca1af0cd（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 7 ← 诊断

## 规矩

- rule-8d2a3b7406f3｜定 needs_immersive_safearea 前先核源窗口是否延伸到系统栏，全无信号写非全屏和 false｜读到：源主题链（如 parent=android:Theme.Holo / Theme.Black）和代码里没有 windowFullscreen、windowTranslucentStatus / Navigation、透明 statusBarColor、FLAG_FULLSCREEN、SYSTEM_UI_FLAG_LAYOUT_*、setDecorFitsSystemWindows(false) / enableEdgeToEdge，targetSdk 低于 35；写错：规格的沉浸式节写 needs_immersive_safearea=true、「全屏页必须显式四件套」、四层架构和底部避让落点，照 page_type 默认值填
- rule-c54d6d69be70｜规格全局约定逐条写源端状态栏、导航栏各自的颜色和是否沉浸，不把透明状态栏写成全屏｜读到：源 Activity 只用 SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN（没有 HIDE_NAVIGATION）加 setStatusBarColor(TRANSPARENT)，或 values-v21 的 statusBarColor 为 transparent；主题没设 navigationBarColor，targetSdkVersion < 35；写错：规格或界面清单只写「透明状态栏全屏」「全屏页统一四层架构」，没写导航栏颜色、内容是否画到导航栏下；系统栏外观验收里没有导航栏一项
- rule-d585fcbfa91a｜源 targetSdk≥35 时，规格登记强制 edge-to-edge，分页按源布局是否处理 insets 定避让｜读到：Android 构建配置的 targetSdkVersion（含 gradle.properties 里的间接值）≥ 35；页面布局根 android:fitsSystemWindows="false" 或没有 WindowInsets 处理，Toolbar 叠放在内容上；写错：规格全局约定没登记 targetSdk / edge-to-edge 前提，分页规格一律写「内容延伸系统栏 + 前景避让」，把自 y=0 起的 Toolbar 写成需要避让；或只凭 values-v21 的 statusBarColor / colorPrimaryDark 推断状态栏是不透明着色
