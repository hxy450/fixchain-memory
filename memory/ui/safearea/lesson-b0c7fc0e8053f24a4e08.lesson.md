# 开全屏前逐边核对源窗口：FLAG_FULLSCREEN 只隐藏状态栏，导航栏、旧应用挖孔边与宽高比上限都在窗口外；源窗口延伸到的边才沉浸

ID：`lesson-b0c7fc0e8053f24a4e08` · 版本：2

[本主题](index.md)

## 何时使用

规格提取与入口窗口实现阶段，决定目标窗口是否 setWindowLayoutFullScreen(true)、隐藏哪些系统栏、各边背景是否延伸、系统栏底色与是否做内容避让时；源端以 DisplayMetrics 取应用窗口宽高作几何基准时；规格模板或页面元数据按页面类型默认标注全屏页、需要沉浸式安全区时

## 适用情境

源 Activity 主题链与代码决定窗口是否延伸到系统栏下：windowFullscreen、windowTranslucentStatus/Navigation、FLAG_FULLSCREEN、SYSTEM_UI_FLAG_LAYOUT_*、setDecorFitsSystemWindows(false)/enableEdgeToEdge、targetSdk≥35 的强制 edge-to-edge，或者都没有（Theme.Holo/Theme.Black 等低 targetSdk 主题；requestWindowFeature(FEATURE_NO_TITLE) 只去标题栏）。也包括只用 SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN 加透明 statusBarColor、没有 navigationBarColor、windowTranslucentNavigation、HIDE_NAVIGATION 且 targetSdk≤34 的只沉浸状态栏页面；目标规格模板或沉浸式 skill 默认全屏、两栏透明，或把 FLAG_FULLSCREEN 当作整窗沉浸。低 targetSdk 的旧应用全屏窗口还受挖孔模式与最大宽高比限制。

## 原因

源 XML 没有系统栏间距，是因为源窗口不延伸到系统栏下；源端非全屏时套用全屏模板，标题栏或内容会压进状态栏，各页再用避让去补偿，几何与底色都偏离源端。“透明状态栏”也不等于整窗沉浸：只设透明 statusBarColor、没有布局延伸标志时内容并不画到状态栏下；源端导航栏不透明时，全屏后让页面底色填进导航区就与源端不同。FLAG_FULLSCREEN 只隐藏状态栏，当成整窗沉浸并隐藏全部系统栏，内容会铺进导航区与挖孔边；以整窗高减底部避让作几何基准，整数截断出的格数、行数随之与源端不同。

## 做法

1. 逐边判定源窗口是否延伸：状态栏边看 windowTranslucentStatus、SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN、setDecorFitsSystemWindows(false)/enableEdgeToEdge，透明 statusBarColor 单独不代表内容延伸；导航栏边看 windowTranslucentNavigation、SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION、透明 navigationBarColor 与 edge-to-edge；targetSdk≥35 在 Android 15 及以上强制 edge-to-edge。windowFullscreen、FLAG_FULLSCREEN 只隐藏状态栏：导航栏仍可见且应用窗口止于其上，目标只隐藏状态栏（window.setSpecificSystemBarEnabled('status', false)，保留导航栏与导航指示条），setWindowSystemBarEnable([]) 会连导航条一起隐藏。FEATURE_NO_TITLE、Theme.*.NoTitleBar 只去标题栏。规格与源码冲突时以源主题链与代码为准。
2. 两边都不延伸时目标保持非全屏：在 loadContent 回调里 setWindowLayoutFullScreen(false)，按源设置系统栏底色与图标色，用 setWindowSystemBarEnable(['status', 'navigation']) 保证横屏也显示系统栏，不建避让窗口模型、各页不加避让 padding。
3. 只有某边延伸时才让该边背景延伸；源端导航栏不透明而目标需要全屏时，在底部避让区叠一条取源导航栏颜色、hitTestBehavior(HitTestMode.None) 的占位，或不让背景延伸到底边，不让页面底色填充。导航栏颜色取源主题链 android:navigationBarColor（含 values-vNN 与代码覆盖），未设时取参照设备平台版本的框架主题默认值（platforms/android-NN/data/res/values/themes_material.xml 与 colors.xml；例：android-30 为 @color/black）。
4. setWindowSystemBarProperties 的 statusBarColor、navigationBarColor 与图标深浅按源端逐边设置，不照搬模板的两栏透明。
5. 旧应用的窗口区另按两条平台规则收窄：主题链未把 android:windowLayoutInDisplayCutoutMode 设为 shortEdges/always 时（低 targetSdk 应用只能取默认），隐藏状态栏的全屏窗口不进入挖孔所在边，该边留黑；targetSdk<26 且未声明 android:maxAspectRatio 或 meta-data android.max_aspect、resizeableActivity 不为 true 时，系统按最大宽高比 1.86 截长边（PackageParser 的 DEFAULT_PRE_O_MAX_ASPECT_RATIO）。源端以 getResources().getDisplayMetrics() 或 Display.getSize/getMetrics 取的宽高就是这块应用窗口区，目标几何基准取等价内容区（windowRect 减挖孔边与底部避让，再按宽高比上限截长边），不写成“全屏窗口减底部避让”。取值：AndroidManifest 的 targetSdkVersion 与 activity 属性、主题链的挖孔模式，参照机 adb shell dumpsys window windows 中该窗口的 mAppBounds，目标端 window.getWindowAvoidArea 的 TYPE_CUTOUT、TYPE_SYSTEM、TYPE_NAVIGATION_INDICATOR 与 windowRect。

## 可选检查

- 源端非全屏时对照两端截图：状态栏与导航栏区域为源端底色，内容起点在状态栏下沿、终点在导航栏上沿。

来源支持：4 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-11e45f7bea96bac1c5b5](../../../store/cases/case-11e45f7bea96bac1c5b5/263a41a9f4b0938d139f6cc94479f8613606ed593358dc8c1d8e420101b7f820.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`263a41a9f4b0938d139f6cc94479f8613606ed593358dc8c1d8e420101b7f820`
- [case-af09311d7897ca1af0cd](../../../store/cases/case-af09311d7897ca1af0cd/7fde16139bd54aa34665e50092f9effbfc31099aa437f126371778695bf3704c.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`7fde16139bd54aa34665e50092f9effbfc31099aa437f126371778695bf3704c`
- [case-bbb49cc9ec510f04eb33](../../../store/cases/case-bbb49cc9ec510f04eb33/30bc8c5f48ca1bb3364ca8cd4bb74dad4fe323222a7076820e9bc64230cf4f1b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`30bc8c5f48ca1bb3364ca8cd4bb74dad4fe323222a7076820e9bc64230cf4f1b`
- [case-c4e98fefcf3a1a74e62e](../../../store/cases/case-c4e98fefcf3a1a74e62e/843c7274d8afd8a4554b447f768fec19e69332ec008b26b9e81c1032db2d4322.json) · 结论：diagnosis, recommendation:1, recommendation:4
  卡片版本：`843c7274d8afd8a4554b447f768fec19e69332ec008b26b9e81c1032db2d4322`
