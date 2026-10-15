# 开全屏前逐边核对源窗口：源窗口延伸到系统栏下才全屏沉浸，否则保持非全屏；只沉浸状态栏时保留导航栏底色

ID：`lesson-b0c7fc0e8053f24a4e08` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与入口窗口实现阶段，决定目标窗口是否 setWindowLayoutFullScreen(true)、各边背景是否延伸、系统栏底色与是否做内容避让时；规格模板或页面元数据按页面类型默认标注全屏页、需要沉浸式安全区时

## 适用情境

源 Activity 主题链与代码决定窗口是否延伸到系统栏下：windowFullscreen、windowTranslucentStatus/Navigation、FLAG_FULLSCREEN、SYSTEM_UI_FLAG_LAYOUT_*、setDecorFitsSystemWindows(false)/enableEdgeToEdge、targetSdk≥35 的强制 edge-to-edge，或者都没有（Theme.Holo/Theme.Black 等低 targetSdk 主题；requestWindowFeature(FEATURE_NO_TITLE) 只去标题栏）。也包括只用 SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN 加透明 statusBarColor、没有 navigationBarColor、windowTranslucentNavigation、HIDE_NAVIGATION 且 targetSdk≤34 的只沉浸状态栏页面；目标规格模板或沉浸式 skill 默认全屏、两栏透明。

## 原因

源 XML 没有系统栏间距，是因为源窗口不延伸到系统栏下；源端非全屏时套用全屏模板，标题栏或内容会压进状态栏，各页再用避让去补偿，几何与底色都偏离源端。“透明状态栏”也不等于整窗沉浸：只设透明 statusBarColor、没有布局延伸标志时内容并不画到状态栏下；源端导航栏不透明时，全屏后让页面底色填进导航区就与源端不同。

## 做法

1. 逐边判定源窗口是否延伸：状态栏边看 windowTranslucentStatus、SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN、setDecorFitsSystemWindows(false)/enableEdgeToEdge，透明 statusBarColor 单独不代表内容延伸；导航栏边看 windowTranslucentNavigation、SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION、透明 navigationBarColor 与 edge-to-edge；targetSdk≥35 在 Android 15 及以上强制 edge-to-edge。windowFullscreen、FLAG_FULLSCREEN 是隐藏状态栏，按“该边无可见栏”处理；FEATURE_NO_TITLE、Theme.*.NoTitleBar 只去标题栏。规格与源码冲突时以源主题链与代码为准。
2. 两边都不延伸时目标保持非全屏：在 loadContent 回调里 setWindowLayoutFullScreen(false)，按源设置系统栏底色与图标色，用 setWindowSystemBarEnable(['status', 'navigation']) 保证横屏也显示系统栏，不建避让窗口模型、各页不加避让 padding。
3. 只有某边延伸时才让该边背景延伸；源端导航栏不透明而目标需要全屏时，在底部避让区叠一条取源导航栏颜色、hitTestBehavior(HitTestMode.None) 的占位，或不让背景延伸到底边，不让页面底色填充。导航栏颜色取源主题链 android:navigationBarColor（含 values-vNN 与代码覆盖），未设时取参照设备平台版本的框架主题默认值（platforms/android-NN/data/res/values/themes_material.xml 与 colors.xml；例：android-30 为 @color/black）。
4. setWindowSystemBarProperties 的 statusBarColor、navigationBarColor 与图标深浅按源端逐边设置，不照搬模板的两栏透明。

## 可选检查

- 源端非全屏时对照两端截图：状态栏与导航栏区域为源端底色，内容起点在状态栏下沿、终点在导航栏上沿。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-11e45f7bea96bac1c5b5](../../../store/cases/case-11e45f7bea96bac1c5b5/263a41a9f4b0938d139f6cc94479f8613606ed593358dc8c1d8e420101b7f820.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`263a41a9f4b0938d139f6cc94479f8613606ed593358dc8c1d8e420101b7f820`
- [case-af09311d7897ca1af0cd](../../../store/cases/case-af09311d7897ca1af0cd/7fde16139bd54aa34665e50092f9effbfc31099aa437f126371778695bf3704c.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`7fde16139bd54aa34665e50092f9effbfc31099aa437f126371778695bf3704c`
