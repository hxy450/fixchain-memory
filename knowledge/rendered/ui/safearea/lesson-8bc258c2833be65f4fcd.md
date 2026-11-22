# 源端只在三键导航时给导航栏着色：以 TYPE_SYSTEM 底部避让高度判定导航方式，非手势时用 navigationBarColor 着色并随避让区变化更新

## 何时使用

规格提取与入口窗口实现阶段，把源 Activity 按导航方式设置导航栏颜色的分支映射到目标窗口系统栏属性时

## 适用情境

源端在 Activity 中按是否手势导航决定导航栏底色（如非手势导航时 setNavigationBarColor(背景色带透明度)），判定依赖隐藏系统资源（config_navBarInteractionMode）或系统设置；目标为全屏沉浸窗口，入口用 getWindowAvoidArea 测避让区、用 setWindowSystemBarProperties 设置系统栏。前提是源端的着色调用真的生效：源应用 targetSdkVersion 为 35（Android 15）及以上时，setNavigationBarColor 的颜色固定为透明、改不了（窗口要求导航栏对比度时由系统自己决定是否加遮罩），这时源端导航栏实际是透明的（是否加遮罩由系统决定），目标也保持透明，不按代码里的调用着色。

## 原因

源端判定导航方式的手段在目标没有同名对应，但被判定的状态可以观察：三键导航栏表现为 TYPE_SYSTEM 的底部避让区，手势导航时该高度为 0。把“检测手段无对等”当成“行为无对等”，会删掉着色分支，三键模式下导航栏恒透明。

## 做法

1. 规格先写出用户可观察的条件与效果（如“三键导航栏存在时导航栏涂背景色并带源端透明度”），再映射目标信号；检测 API 不同不构成删除该行为的理由。
2. 入口按 getWindowAvoidArea(TYPE_SYSTEM).bottomRect.height > 0 判定三键导航：此时用 setWindowSystemBarProperties({ navigationBarColor }) 写源端颜色（透明度并入 #AARRGGBB），手势导航保持透明；订阅 avoidAreaChange 在导航方式切换时重算，颜色取自主题背景时按当前深浅色取值。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕AvoidAreaType.TYPE_SYSTEM 表示系统默认区域，包含状态栏和三键导航栏区域；TYPE_NAVIGATION_INDICATOR（API 11 起）表示底部导航区域，三键导航显示时这块避让区始终存在
- 〔做法第 2 步〕getWindowAvoidArea 返回的避让区各值全为 0 时表示该类避让区为空；AvoidArea 的 bottomRect 等矩形以 px 为单位
- 〔做法第 2 步〕SystemBarProperties.navigationBarColor 作为入参时是十六进制 RGB 或 ARGB 颜色（不区分大小写，如 '#00FF00'、'#FF00FF00'），透明度写在 ARGB 的前两位；作为返回值固定为 ARGB；不设时为系统配置的颜色
- 〔原因〕安卓窗口在应用没有用代码强制设导航栏颜色时：主题没有指定 navigationBarColor、没有强制 edge-to-edge、且 config_navBarDefaultTransparent 为 false 时，导航栏取 navigation_bar_compatible（@android:color/black）；主题指定了就取主题的值（android-36.1 源码）
