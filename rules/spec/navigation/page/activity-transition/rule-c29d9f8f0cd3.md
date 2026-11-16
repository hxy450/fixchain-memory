# 源 Activity 跳转没自定义转场时，规格写平台默认动画和各页 pageTransition 目标值

审的是：规格
触发（任一种）：
- 读到：源端多个 Activity 用 startActivity 跳转、finish 返回，源码里没有 overridePendingTransition，styles 也没覆盖 windowAnimationStyle；写错的样子：规格的导航关系、ui-manifest 只写「router.pushUrl 页面跳转」，或写「无转场」，没有页面切换动画这一项，也没给 pageTransition 的目标值
适用范围：规格提取阶段，把 Activity 之间的跳转和返回映射成目标页面路由契约时
做法：
- 导航契约里把页面切换动画当作可观察行为逐条写：源端没调 overridePendingTransition、主题没覆盖 windowAnimationStyle 时写「平台默认 Activity 动画（<主题名>）」，不写「无转场」
- 沿主题 parent 链（含 values-v11、values-v14 等限定目录）找到 windowAnimationStyle，按参照机 API 从 SDK 读 activity_open_enter、open_exit、close_enter、close_exit 四段参数，写成每个目标页 pageTransition 在 Push/Pop × Enter/Exit 下的目标值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Theme 的 windowAnimationStyle = @style/Animation.Activity：平台基础主题的 Activity 切换动画样式（出处：Android SDK 平台资源 data/res/values/themes.xml，Theme 的 windowAnimationStyle（按参照机的 API 取对应平台））
- Theme.Holo 的 windowAnimationStyle = @style/Animation.Holo.Activity，它的 parent 是 Animation.Activity：Holo 主题链最终也落到 Animation.Activity（出处：Android SDK 平台资源 data/res/values/themes_holo.xml，Theme.Holo；data/res/values/styles_holo.xml，Animation.Holo.Activity）
- Theme.Material 的 windowAnimationStyle = @style/Animation.Material.Activity：Material 主题链的 Activity 切换动画样式（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material）
- Animation.Activity：activityOpenEnterAnimation=@anim/activity_open_enter、activityOpenExitAnimation=@anim/activity_open_exit、activityCloseEnterAnimation=@anim/activity_close_enter、activityCloseExitAnimation=@anim/activity_close_exit：四段切换动画各在哪个 anim 文件（出处：Android SDK 平台资源 data/res/values/styles.xml，Animation.Activity）
- 例：android-30 的 activity_open_enter 是 alpha 0→1 加 scale 0.85→1（400ms）；android-36 是 alpha 0→1 加 translate 96dp→0（450ms）：四段动画随平台版本变化，要按参照机的 API 读（出处：Android SDK 平台资源 data/res/anim/activity_open_enter.xml（android-30、android-36 两个平台对照））
针对本应用要查的：
- 源 Activity 实际用的 windowAnimationStyle：源工程 AndroidManifest.xml 里 Activity / application 的 android:theme，res/values*/styles.xml、themes.xml（含 values-v11、values-v14 等）的主题 parent 链；找最近一个给 windowAnimationStyle 赋值的主题；都没给就落到平台父主题：Theme → Animation.Activity，Theme.Holo → Animation.Holo.Activity，Theme.Material → Animation.Material.Activity
- 四段切换动画的参数：Android SDK platforms/android-<参照机 API>/data/res/values/styles*.xml 里那个动画样式的四个 item，及它们指向的 data/res/anim/activity_{open,close}_{enter,exit}.xml；读每段里 alpha、scale、translate 的 from / to、duration、startOffset、interpolator，分别写成 Push Enter、Push Exit、Pop Enter、Pop Exit 的目标值
未核实：参照机 Android 12（API 31/32）的平台动画本机没装对应平台，没能对照
来源：1 张卡，1 个应用
- case-6f936bc6ca2d4ec18528（Bubble Shooter）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
