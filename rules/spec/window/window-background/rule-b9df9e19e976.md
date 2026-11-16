# 源端是 Theme.Holo 等平台主题时，规格把 windowBackground 解析到最终 drawable

审的是：规格
触发（任一种）：
- 读到：styles.xml 里应用主题 parent="android:Theme.Holo"（或其他 android:Theme.*），布局根没有 android:background；写错的样子：页面规格只写「暗底背景（Holo 默认，取不到精确值处标待核）」没有值；或把窗口背景写成 @color/background_holo_dark 那样的单色 #ff000000
适用范围：源 Activity 的主题链止于 Android 平台主题、页面底色来自 windowBackground 时，规格里每页的页面根背景契约
做法：
- 沿主题的 parent 链找到平台主题，在 Android SDK 平台资源 platforms/android-<compileSdk>/data/res 里顺着 windowBackground 解析到最终 drawable（selector 取默认项，shape 读出 gradient 或 solid）
- 把结果写成每页的页面根背景契约（渐变写起止色和 angle），并写明它和同名的 @color 资源（colorBackground）是两个资源
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Theme 的 windowBackground = @drawable/screen_background_selector_dark；Theme.Holo 没有改写它，按名字前缀继承 Theme：Theme.Holo 的窗口背景从 Theme 来（出处：Android SDK 平台资源 data/res/values/themes.xml，Theme 的 windowBackground；data/res/values/themes_holo.xml，Theme.Holo（按应用的 compileSdk 取对应平台））
- screen_background_selector_dark：state_accelerated=false 时取 screen_background_dark，默认项取 @android:drawable/background_holo_dark：硬件加速下实际用的是 background_holo_dark 这个 drawable（出处：Android SDK 平台资源 data/res/drawable/screen_background_selector_dark.xml（按应用的 compileSdk 取对应平台））
- @drawable/background_holo_dark = <gradient startColor="#ff000000" endColor="#ff272d33" angle="270">：Theme.Holo 窗口背景是从上到下的渐变（出处：Android SDK 平台资源 data/res/drawable/background_holo_dark.xml（按应用的 compileSdk 取对应平台））
- @color/background_holo_dark = #ff000000，是 Theme.Holo 的 colorBackground：和同名 drawable 是两个资源，不是窗口背景（出处：Android SDK 平台资源 data/res/values/colors_holo.xml，background_holo_dark；data/res/values/themes_holo.xml，Theme.Holo 的 colorBackground（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 应用主题的 parent 链止于哪个平台主题，以及 compileSdk：源工程 res/values*/styles.xml 里主题的 parent 属性、AndroidManifest 的 android:theme、模块构建脚本的 compileSdk；按 compileSdk 取对应平台的 data/res，在 values/themes*.xml 找该主题的 windowBackground（没写的按名字前缀找父主题），再顺着 @drawable 解析到 shape
来源：1 张卡，1 个应用
- case-2a82c31c11fb4f1c7fa5（Blockinger）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断
