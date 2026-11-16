# 系统栏颜色和全屏方式先从源主题链、Activity 代码和 targetSdk 查实再写

审的是：代码
触发（任一种）：
- 读到：源主题没显式写 android:navigationBarColor / windowFullscreen / windowTranslucent*，或 setNavigationBarColor 带条件调用；写错的样子：EntryAbility 照模板写 setWindowLayoutFullScreen(true) 和两栏 '#00000000'
适用范围：迁移 EntryAbility 的窗口布局和系统栏属性时
做法：
- 依次查：清单的 android:theme → styles.xml、themes.xml 里主题的 parent 链 → Activity 里的 FLAG_FULLSCREEN、SYSTEM_UI_FLAG_*、setNavigationBarColor 及条件 → targetSdkVersion
- 都没写的取平台默认：没指定 navigationBarColor 又没强制 edge-to-edge 时导航栏是黑色；颜色转成 '#AARRGGBB'
- 源端不延伸到系统栏下的写 setWindowLayoutFullScreen(false)；查出的底色和图标色填进 setWindowSystemBarProperties，源端带条件的照搬条件
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 主题没指定 navigationBarColor 且没强制 edge-to-edge 时，导航栏用 navigation_bar_compatible（@android:color/black）：源导航栏颜色的默认取法（出处：com.android.internal.policy.PhoneWindow#generateLayout；Android SDK 平台资源 data/res/values/colors.xml，navigation_bar_compatible（按应用的 compileSdk 取对应平台））
- setWindowLayoutFullScreen(isLayoutFullScreen: boolean): Promise<void>：主窗口布局是否沉浸；false 时内容在系统栏之间（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowLayoutFullScreen）
- SystemBarProperties：statusBarColor?: string、statusBarContentColor?: string、navigationBarColor?: string、navigationBarContentColor?: string：两栏的底色和图标、文字色（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，SystemBarProperties）
- navigationBarColor 入参为十六进制 RGB 或 ARGB，如 '#FF00FF00'：颜色写法（出处：arkts-apis-window-i.md，SystemBarProperties）
针对本应用要查的：
- 源窗口是否延伸到系统栏下：源工程清单里 application / activity 的 android:theme，res/values*/styles.xml、themes.xml 里该主题的 parent 链，Activity 代码里的 window flag 和 setSystemUiVisibility；有 windowFullscreen、windowTranslucentStatus / Navigation、FLAG_FULLSCREEN 或 SYSTEM_UI_FLAG_LAYOUT_* 的才延伸；都没有就是非全屏
- 源端两栏的底色和图标色：同一条主题链里的 android:statusBarColor、android:navigationBarColor、windowLightStatusBar，Activity 代码里 setStatusBarColor / setNavigationBarColor 的参数和条件，构建脚本的 targetSdkVersion；设了就转成 '#AARRGGBB'；都没设、targetSdk < 35 时导航栏是黑色；例：Theme.Holo 下两栏都是黑底白图标
未核实：targetSdkVersion 到 35 才强制 edge-to-edge 出自卡，族里规矩没有引平台源码核实这个对应；主题里的全屏属性和代码里的 window flag 同时出现时以哪个为准，族里规矩没有核实
来源：3 张卡，3 个应用
- case-01833db0536ba02ed2ce（Cofi）：做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-11e45f7bea96bac1c5b5（Privacy Friendly 2048）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
- case-af09311d7897ca1af0cd（Blockinger）：做法第 1 步 ← 建议 3；做法第 3 步 ← 建议 3
