# 帧时钟动画（Animatable、ValueAnimator）改自驱 ticker 时，时间分数取“当前帧时间 − 起始时间”再套源端插值：后台停帧、回前台按真实流逝追平，不钳制单次增量

## 何时使用

计时或动画引擎的规格与实现阶段，把 Animatable.animateTo(tween)、ValueAnimator/ObjectAnimator 等由帧时钟驱动的进度改写为 setInterval、displaySync、postFrameCallback 等自驱 ticker，确定进度曲线、刷新周期与退后台、回前台的时间推进时

## 适用情境

源端进度由 Compose Animatable.animateTo(tween(duration, easing)) 一类帧时钟动画驱动，或由 Android ValueAnimator/ObjectAnimator 逐帧写入绘制用的进度字段；插值曲线可能显式设置，也可能取框架默认。Compose 的帧时钟随宿主 ON_STOP 暂停、ON_START 恢复（只到 ON_PAUSE 时不暂停）；ValueAnimator 不随生命周期暂停，只有无限重复的 Animator 自 Android 13 起在应用窗口全部不可见一段时间后（Android 13 为 10s，14 起 1s）被暂停，恢复时扣除暂停时长、不追平后台时间；目标没有可直接复用的同语义帧时钟，自写 ticker 复刻进度推进与前后台切换。同一应用可能另有后台 Worker 以固定周期（如 tickerFlow + elapsedRealtime）推进，其周期与补偿方式不属于前台动画。 「回前台按真实流逝追平」针对按帧时间减起始时间算播放时间的源端（Compose 帧时钟、有限时长的 Animator）；源端是无限重复的 Animator 并被系统后台暂停时，源端恢复后把暂停时长从进度里扣掉、不追平，目标端恢复时把起始时间后移同样的时长，不按本条追平。

## 原因

Compose 动画的播放时间等于帧时间减起始时间：后台不出帧只是暂停绘制，回前台首帧按真实流逝时间推进，必要时一帧结束。改成逐 tick 累加增量并给单次增量设上限，会丢掉后台经过的时间，进度停在退后台时附近；用固定的长周期定时器代替逐帧刷新，进度环与高精度时间文本会成段跳变。规格里“后台停摆”一类措辞容易被读成丢弃后台时间。帧时间差除以时长得到的只是时间分数：源端插值曲线（显式设置或框架默认）不套上去，动画就变成匀速，起止快慢与源端不同。

## 做法

1. 时间分数按绝对时间计算：f = min(1, (frameTime − startTime) / duration)，frameTime 取帧回调时间戳或单调时钟；进度 = 源端插值(f)。只有源端显式线性（Compose LinearEasing、Android LinearInterpolator 或 setInterpolator(null)）才省去插值；未写插值时取框架默认：Compose tween 为 FastOutSlowInEasing（Animatable.animateTo 不传 animationSpec 时是弹簧 spring，没有固定时长，不按本式算），Android ValueAnimator/ObjectAnimator 为 AccelerateDecelerateInterpolator，即 cos((f+1)π)/2 + 0.5（android.animation.ValueAnimator 的 sDefaultInterpolator）。暂停与恢复只控制是否派帧，不逐 tick 累加增量，也不对单次增量设上限。
2. 刷新节奏对齐源端逐帧：用 displaySync（或下一帧回调）按 vsync 驱动，并随宿主可见性暂停、恢复帧回调；固定周期定时器只用于源端本就按固定周期 tick 的逻辑。
3. 规格描述前后台行为时把“后台期间不派帧、不推进显示”和“回前台按真实流逝时间追平”分开写，不只写“停摆”；转写源端 Animator 时连同时长写明生效的插值器及其来源（显式设置或框架默认）。改用 animateTo/曲线时注意 Curve.EaseInOut 是三次贝塞尔，与 AccelerateDecelerate 的余弦曲线不等价，要一比一时用 curves.customCurve 写入同一公式。

## 可选检查

- 对追平语义有疑问时，取一段 10s 的进度，运行 3s 后退后台 4s 再回前台：进度应约为 0.7，而不是停在 0.3 附近。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境〕android-36.1 源码中，进程的窗口全部不可见后，AnimationHandler 延迟 Animator.getBackgroundPauseDelay()（应用没有调 setBackgroundPauseDelay 另设时为 1000 毫秒）把总时长为 DURATION_INFINITE 的 Animator 暂停，任一窗口重新可见时恢复；这一行为可由系统属性 framework.pause_bg_animations.enabled 关闭；有限时长的 Animator 不受影响
- 〔适用情境〕ValueAnimator 先 pause、随后 resume 时，下一帧把起始时间加上暂停时长（mStartTime += frameTime − mPauseTime），暂停期间经过的时间不计入进度
- 〔做法第 1 步〕ValueAnimator（及子类 ObjectAnimator）没有调 setInterpolator 时，插值器是 sDefaultInterpolator = new AccelerateDecelerateInterpolator()
- 〔做法第 1 步〕AccelerateDecelerateInterpolator.getInterpolation(input) 返回 (float)(Math.cos((input + 1) * Math.PI) / 2.0f) + 0.5f，结果是 float
- 〔做法第 1 步〕ValueAnimator.setInterpolator(null) 时插值器设为 new LinearInterpolator()，即线性
- 〔做法第 3 步〕ArkUI Curve.EaseInOut 是三次贝塞尔 CubicBezier(0.42, 0.0, 0.78, 1.0)，不是余弦曲线
