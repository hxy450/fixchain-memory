# 源导航栏不透明时，入口根节点在底部避让区叠同色占位，不让页面底色填进手势条区

审的是：代码
触发（任一种）：
- 读到：源 Activity 只用 SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN 加 setStatusBarColor(TRANSPARENT) 沉浸状态栏，主题没设 navigationBarColor，targetSdkVersion < 35；写错的样子：窗口 setWindowLayoutFullScreen(true)，入口根 Navigation 写 .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP, SafeAreaEdge.BOTTOM])，底部避让区没有还原源端导航栏颜色的东西
适用范围：按沉浸式模板开全屏布局、装配入口根节点，而源端导航栏不透明时
做法：
- 入口根改成 Stack({ alignContent: Alignment.Bottom })，在 Navigation 上叠 Row().width('100%').height(windowBottomPadding).backgroundColor(源导航栏颜色).hitTestBehavior(HitTestMode.None)，高度跟窗口的底部避让值走
- 或者不让背景延伸到底边：入口的 expandSafeArea 不带 SafeAreaEdge.BOTTOM
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- expandSafeArea(types?: Array<SafeAreaType>, edges?: Array<SafeAreaEdge>): T：组件向安全区扩展；不传时默认扩展 TOP、BOTTOM、START、END 四边（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.expandSafeArea）
- SafeAreaEdge.TOP = 0、BOTTOM = 1、START = 2、END = 3：扩展的边（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SafeAreaEdge）
- hitTestBehavior(value: HitTestMode): T；HitTestMode.None：自身不响应触摸命中，子组件仍响应：占位条不挡住下面的触摸（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.hitTestBehavior；ets/component/enums.d.ts，HitTestMode.None）
- 根改 Stack(alignContent Bottom)，Navigation 上叠一条高 windowBottomPadding、黑底、hitTestBehavior(None) 的 Row，并连接窗口避让值：修复后与源端底部一致（出处：卡里修好并验证过）
- 主题没指定 navigationBarColor 且没强制 edge-to-edge 时，导航栏用 navigation_bar_compatible（@android:color/black）：源导航栏颜色的取法（出处：com.android.internal.policy.PhoneWindow#generateLayout；Android SDK 平台资源 data/res/values/colors.xml，navigation_bar_compatible（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 源导航栏颜色：源工程 res/values*/styles.xml、themes.xml 里应用 / Activity 主题的 android:navigationBarColor，以及 Activity 代码里的 setNavigationBarColor；设了就用那个颜色；都没设、targetSdk < 35 时是黑色
来源：1 张卡，1 个应用
- case-11e45f7bea96bac1c5b5（Privacy Friendly 2048）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
