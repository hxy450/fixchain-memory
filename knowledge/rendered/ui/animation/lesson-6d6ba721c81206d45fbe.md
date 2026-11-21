# 帧时钟动画（Animatable、ValueAnimator）改自驱 ticker 时，时间分数取“当前帧时间 − 起始时间”再套源端插值：后台停帧、回前台按真实流逝追平，不钳制单次增量

## 何时使用

计时或动画引擎的规格与实现阶段，把 Animatable.animateTo(tween)、ValueAnimator/ObjectAnimator 等由帧时钟驱动的进度改写为 setInterval、displaySync、postFrameCallback 等自驱 ticker，确定进度曲线、刷新周期与退后台、回前台的时间推进时

## 适用情境

源端进度由 Compose Animatable.animateTo(tween(duration, easing)) 一类帧时钟动画驱动，或由 Android ValueAnimator/ObjectAnimator 逐帧写入绘制用的进度字段；插值曲线可能显式设置，也可能取框架默认。Compose 的帧时钟随宿主 ON_STOP 暂停、ON_START 恢复（只到 ON_PAUSE 时不暂停）；ValueAnimator 不随生命周期暂停，只有无限重复的 Animator 自 Android 13 起在应用窗口全部不可见一段时间后（Android 13 为 10s，14 起 1s）被暂停，恢复时扣除暂停时长、不追平后台时间；目标没有可直接复用的同语义帧时钟，自写 ticker 复刻进度推进与前后台切换。同一应用可能另有后台 Worker 以固定周期（如 tickerFlow + elapsedRealtime）推进，其周期与补偿方式不属于前台动画。

## 原因

Compose 动画的播放时间等于帧时间减起始时间：后台不出帧只是暂停绘制，回前台首帧按真实流逝时间推进，必要时一帧结束。改成逐 tick 累加增量并给单次增量设上限，会丢掉后台经过的时间，进度停在退后台时附近；用固定的长周期定时器代替逐帧刷新，进度环与高精度时间文本会成段跳变。规格里“后台停摆”一类措辞容易被读成丢弃后台时间。帧时间差除以时长得到的只是时间分数：源端插值曲线（显式设置或框架默认）不套上去，动画就变成匀速，起止快慢与源端不同。

## 做法

1. 时间分数按绝对时间计算：f = min(1, (frameTime − startTime) / duration)，frameTime 取帧回调时间戳或单调时钟；进度 = 源端插值(f)。只有源端显式线性（Compose LinearEasing、Android LinearInterpolator 或 setInterpolator(null)）才省去插值；未写插值时取框架默认：Compose tween 为 FastOutSlowInEasing（Animatable.animateTo 不传 animationSpec 时是弹簧 spring，没有固定时长，不按本式算），Android ValueAnimator/ObjectAnimator 为 AccelerateDecelerateInterpolator，即 cos((f+1)π)/2 + 0.5（本机 SDK sources/android-*/android/animation/ValueAnimator.java 的 sDefaultInterpolator）。暂停与恢复只控制是否派帧，不逐 tick 累加增量，也不对单次增量设上限。
2. 刷新节奏对齐源端逐帧：用 displaySync（或下一帧回调）按 vsync 驱动，并随宿主可见性暂停、恢复帧回调；固定周期定时器只用于源端本就按固定周期 tick 的逻辑。
3. 规格描述前后台行为时把“后台期间不派帧、不推进显示”和“回前台按真实流逝时间追平”分开写，不只写“停摆”；转写源端 Animator 时连同时长写明生效的插值器及其来源（显式设置或框架默认）。改用 animateTo/曲线时注意 Curve.EaseInOut 是三次贝塞尔，与 AccelerateDecelerate 的余弦曲线不等价，要一比一时用 curves.customCurve 写入同一公式。

## 可选检查

- 对追平语义有疑问时，取一段 10s 的进度，运行 3s 后退后台 4s 再回前台：进度应约为 0.7，而不是停在 0.3 附近。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；实现对照 OpenHarmony arkui_ace_engine 标签 OpenHarmony-v6.0-Release；安卓 Android SDK 源码 android-36.1；AOSP frameworks/base 标签 android-12.1.0_r1、android-13.0.0_r1（AnimationHandler）；androidx.compose.animation:animation-core 1.0.0、1.12.0；androidx.compose.ui:ui 1.0.0、ui-android 1.12.0（均为 Maven 源码包）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕Compose 的 tween() 不传参数时 durationMillis 为 300（AnimationConstants.DefaultDurationMillis），easing 为 FastOutSlowInEasing，即 CubicBezierEasing(0.4f, 0.0f, 0.2f, 1.0f)；Animatable.animateTo 不传 animationSpec 时用的是弹簧 defaultSpringSpec，不是 tween，没有固定时长。〔成立范围：androidx.compose.animation:animation-core 1.0.0 与 1.12.0 源码一致；只对 tween()/TweenSpec 与 Animatable.animateTo 的默认参数成立。不成立：源端显式传了 durationMillis、easing 或 animationSpec 时按源端；animate*AsState、updateTransition 等其他入口的默认规格本条未核，不按本条推。〕
- 〔原因〕Compose 里经 Animatable.animateTo 推进的动画每帧按 playTime = frameTimeNanos − startTimeNanos 取进度（1.12.0 再除以 durationScale，durationScale 为 0 时直接取结束），不逐帧累加、不钳制单帧间隔；WindowRecomposer 的帧时钟在宿主 Lifecycle 到 ON_STOP 时暂停、ON_START 时恢复，ON_PAUSE、ON_RESUME 不处理，所以回前台后的首帧按真实流逝时间一步追上。〔成立范围：androidx.compose.animation:animation-core 与 androidx.compose.ui:ui 1.0.0、1.12.0 源码；生命周期取窗口内容根（android.R.id.content 的直接子视图）上的 ViewTreeLifecycleOwner，通常是宿主 Activity（对话框窗口为该对话框），Fragment 里的 ComposeView 也随 Activity 而不是 Fragment 的生命周期暂停与恢复。不成立：页面只被对话框式或透明 Activity 盖住（只走到 ON_PAUSE）时帧时钟不被暂停；1.0.0 没有除以 durationScale 这一步。〕
- 〔做法第 1 步〕android.animation.ValueAnimator（含 ObjectAnimator）未设插值器时用 AccelerateDecelerateInterpolator，即 (float)(Math.cos((input + 1) * Math.PI) / 2.0f) + 0.5f；未设时长时为 300ms；setInterpolator(null) 改为 LinearInterpolator；每帧进度 = (当前帧时间 − mStartTime) / (时长 × 系统动画时长缩放)，缩放使有效时长为 0 时进度直接取 1。〔成立范围：android-36.1 源码；缩放取系统的动画程序时长缩放设置（开发者选项可改），默认 1。不成立：View.animate() 的 ViewPropertyAnimator、补间动画 android.view.animation.Animation、AnimatorSet 统一设置插值器的情形本条未核；XML 动画写了 android:interpolator 或代码设了插值器时按所设。〕
- 〔适用情境〕Android 13 起，应用的窗口全部不可见后，AnimationHandler 延迟一段时间（Android 13 为 10000ms，Android 14 起为 1000ms）把总时长为无限（repeatCount 为 INFINITE）的 Animator 暂停，窗口重新可见时恢复；ValueAnimator 恢复时把起始时间后移暂停的时长，进度从暂停处接着走，不追平后台经过的时间；有限时长的 Animator 不受这一机制影响，仍按当前帧时间减起始时间计算进度。〔成立范围：AOSP android-13.0.0_r1 与 android-36.1 的 AnimationHandler 有此逻辑，android-12.1.0_r1 没有；延迟取 Animator 的 sBackgroundPauseDelay，android-13.0.0_r1、android-13.0.0_r83 为 10000，android-14.0.0_r1 起为 1000；受系统属性 framework.pause_bg_animations.enabled（默认 true）控制，可见性由 ViewRootImpl 上报。不成立：Android 12L 及更早；窗口不可见的时间短于延迟时不暂停；有限时长动画在后台是否继续收到帧回调由系统调度决定，本条不涉及。〕
- 〔做法第 3 步〕鸿蒙 Curve.EaseInOut 为 CubicBezier(0.42, 0.0, 0.58, 1.0)，Curve.FastOutSlowIn 为 CubicBezier(0.4, 0.0, 0.2, 1.0)，与 Compose FastOutSlowInEasing 的控制点相同；animateTo 的 AnimateParam 不设 curve 时取 Curve.EaseInOut，不设 duration 时为 1000ms；这些贝塞尔曲线都不等于安卓 AccelerateDecelerateInterpolator 的余弦曲线。〔成立范围：依据：Curve 枚举文档、显式动画文档的 AnimateParam 默认值；控制点与 OpenHarmony arkui_ace_engine 标签 OpenHarmony-v6.0-Release 的 frameworks/core/animation/curves.cpp 的 Curves::EASE_IN_OUT、Curves::FAST_OUT_SLOW_IN 一致。不成立：curve 传字符串或 ICurve（如 curves.cubicBezierCurve、curves.customCurve）时按所传；curve 用 springMotion、responsiveSpringMotion、interpolatingSpring 时 duration 不生效（文档）；ArkTS 卡片上 duration 另有上限（文档）。〕
- 〔做法第 2 步〕displaySync 的 frame 回调参数 IntervalInfo.timestamp（当前帧到达时间）与 targetTimestamp（下一帧预期时间）单位是纳秒；UIContext.postFrameCallback 注册的 FrameCallback.onFrame(frameTimeInNano) 只在下一帧渲染时调用一次，要逐帧推进须在 onFrame 里再次 post；postDelayedFrameCallback 的 delayTime 单位是毫秒。〔成立范围：依据：displaySync 文档的 IntervalInfo 说明、@ohos.arkui.UIContext.d.ts 的 FrameCallback#onFrame 与 postDelayedFrameCallback 注释、UIContext 文档 postFrameCallback 小节。与 Date.now()、setInterval 的毫秒单位不同；两种帧时间的时间起点文档未写明，不能和 Date.now() 的值直接相减。〕
