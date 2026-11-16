# 窗口的 navigationBarColor 按源端导航栏颜色设，不照搬模板的两栏透明

审的是：代码
触发（任一种）：
- 读到：源主题没设 android:navigationBarColor（或设了不透明色），也没有 windowTranslucentNavigation / SYSTEM_UI_FLAG_HIDE_NAVIGATION；写错的样子：EntryAbility 的 setWindowSystemBarProperties 把 navigationBarColor 设成 '#00000000'，照模板让两栏都透明
适用范围：在 EntryAbility 窗口层设置系统栏属性时
做法：
- navigationBarColor 写源端导航栏颜色：源主题没设、targetSdk < 35 时写黑色 '#FF000000'；拿不到源主题时先去源码根查 styles.xml 与 targetSdk，不按「不过度设计」默认透明
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- navigationBarColor?: string：SystemBarProperties 里导航栏背景色这一项（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，SystemBarProperties.navigationBarColor）
- navigationBarColor 是三键导航栏背景颜色，入参为十六进制 RGB 或 ARGB，如 '#FF00FF00'：颜色写法；手势条区的底色另靠入口占位还原（出处：arkts-apis-window-i.md，SystemBarProperties）
- setWindowSystemBarProperties(systemBarProperties: SystemBarProperties): Promise<void>：设置主窗口的状态栏、导航栏属性（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowSystemBarProperties）
- 主题没指定 navigationBarColor 且没强制 edge-to-edge 时，导航栏用 navigation_bar_compatible（@android:color/black）：源导航栏颜色的取法（出处：com.android.internal.policy.PhoneWindow#generateLayout；Android SDK 平台资源 data/res/values/colors.xml，navigation_bar_compatible（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 源导航栏颜色：源工程 res/values*/styles.xml、themes.xml 里应用 / Activity 主题的 android:navigationBarColor，Activity 代码里的 setNavigationBarColor，构建脚本里的 targetSdkVersion；设了就转成 ARGB 字符串；都没设、targetSdk < 35 时是黑色
来源：1 张卡，1 个应用
- case-11e45f7bea96bac1c5b5（Privacy Friendly 2048）：做法第 1 步 ← 建议 3
