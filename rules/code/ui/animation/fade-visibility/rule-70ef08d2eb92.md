# 源端显隐带淡入淡出动画时，目标用 animateTo 带源时长并在 onFinish 里切显隐

审的是：代码
触发（任一种）：
- 读到：源码在 setVisibility(View.VISIBLE / View.GONE) 前后调用淡入淡出（fade 辅助方法、startAnimation、res/anim 的 alpha 动画），动画结束才切显隐；写错的样子：目标直接改 if 条件渲染所依赖的状态（如置空串）让这一行瞬显瞬隐，没有 animateTo，注释写「fade 等价：状态驱动可见性」之类
适用范围：安卓 View 的显隐带 alpha 淡入淡出、迁成 ArkUI 条件渲染或 visibility 时
做法：
- 先列出源端动画的资源和时长：res/anim 里的 android:duration（引 @android:integer/config_*AnimTime 的解析成毫秒数）、代码常量、插值器
- 写成 this.getUIContext().animateTo({ duration: <源时长>, curve: <对应曲线>, onFinish: () => { <切显隐状态> } }, () => { <opacity 改到目标值> })；淡出在 onFinish 里再隐藏，淡入先置可见再把 opacity 动画到 1，保留「动画结束才切显隐」的顺序
- 不写「fade 等价：状态驱动可见性」这类把动画折叠成即时显隐的注释
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- animateTo(value: AnimateParam, event: () => void): void：UIContext 上的显式动画，闭包里改的状态按 AnimateParam 过渡（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.animateTo）
- 全局 animateTo 自 API 18 起废弃，改用 UIContext#animateTo：代码里写 this.getUIContext().animateTo，不写裸的 animateTo（出处：鸿蒙 SDK 的 ets/component/common.d.ts，animateTo）
- AnimateParam.duration 单位 ms，默认 1000；curve 默认 Curve.EaseInOut；onFinish 在动画播完时回调：源时长要显式写进 duration，不写就按 1 秒；切显隐放 onFinish（出处：鸿蒙 SDK 的 ets/component/common.d.ts，AnimateParam）
- config_shortAnimTime = 200、config_mediumAnimTime = 400、config_longAnimTime = 500（毫秒）：源端 duration 引 @android:integer/config_*AnimTime 时的取值（出处：Android SDK 平台资源 data/res/values/config.xml，config_mediumAnimTime（按应用的 compileSdk 取对应平台））
- @android:anim/fade_in：alpha 0.0→1.0，interpolator @interpolator/decelerate_quad，duration @android:integer/config_longAnimTime：源端引平台自带淡入时的起止值、曲线和时长（出处：Android SDK 平台资源 data/res/anim/fade_in.xml，fade_in（按应用的 compileSdk 取对应平台））
- animateToImmediately(value: AnimateParam, event: () => void): void：同族接口：立即下发的显式动画（出处：鸿蒙 SDK 的 ets/component/common.d.ts，animateToImmediately）
- animation(value: AnimateParam): T：同族接口：CommonMethod 上的属性动画（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.animation）
针对本应用要查的：
- 源端这段淡入淡出的时长、插值器和起止 alpha：源工程 res/anim 下被引用的 XML（<alpha> 的 android:duration、android:interpolator、fromAlpha/toAlpha），或 Java 里的时长常量；duration 写的是数就照搬毫秒；引 @android:integer/config_* 的按平台 config.xml 解析；插值器对到 curve
未核实：源端插值器（如 accelerate）对到哪条 Curve 没有在声明里查到对应关系；卡里环境是 API 24，本机按 API 23 声明核实
来源：1 张卡，1 个应用
- case-298a11d6f7705b3a9362（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 诊断、建议 1；做法第 3 步 ← 建议 1
