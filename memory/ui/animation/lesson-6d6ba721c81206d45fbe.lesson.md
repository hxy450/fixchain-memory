# 帧时钟动画（Animatable、ValueAnimator）改自驱 ticker 时，时间分数取“当前帧时间 − 起始时间”再套源端插值：后台停帧、回前台按真实流逝追平，不钳制单次增量

ID：`lesson-6d6ba721c81206d45fbe` · 版本：2

[本主题](index.md)

## 何时使用

计时或动画引擎的规格与实现阶段，把 Animatable.animateTo(tween)、ValueAnimator/ObjectAnimator 等由帧时钟驱动的进度改写为 setInterval、displaySync、postFrameCallback 等自驱 ticker，确定进度曲线、刷新周期与退后台、回前台的时间推进时

## 适用情境

源端进度由 Compose Animatable.animateTo(tween(duration, easing)) 一类帧时钟动画驱动，或由 Android ValueAnimator/ObjectAnimator 逐帧写入绘制用的进度字段；插值曲线可能显式设置，也可能取框架默认。帧时钟随宿主 ON_STOP 暂停；目标没有可直接复用的同语义帧时钟，自写 ticker 复刻进度推进与前后台切换。同一应用可能另有后台 Worker 以固定周期（如 tickerFlow + elapsedRealtime）推进，其周期与补偿方式不属于前台动画。

## 原因

Compose 动画的播放时间等于帧时间减起始时间：后台不出帧只是暂停绘制，回前台首帧按真实流逝时间推进，必要时一帧结束。改成逐 tick 累加增量并给单次增量设上限，会丢掉后台经过的时间，进度停在退后台时附近；用固定的长周期定时器代替逐帧刷新，进度环与高精度时间文本会成段跳变。规格里“后台停摆”一类措辞容易被读成丢弃后台时间。帧时间差除以时长得到的只是时间分数：源端插值曲线（显式设置或框架默认）不套上去，动画就变成匀速，起止快慢与源端不同。

## 做法

1. 时间分数按绝对时间计算：f = min(1, (frameTime − startTime) / duration)，frameTime 取帧回调时间戳或单调时钟；进度 = 源端插值(f)。只有源端显式线性（Compose LinearEasing、Android LinearInterpolator 或 setInterpolator(null)）才省去插值；未写插值时取框架默认：Compose tween 为 FastOutSlowInEasing，Android ValueAnimator/ObjectAnimator 为 AccelerateDecelerateInterpolator，即 cos((f+1)π)/2 + 0.5（本机 SDK sources/android-*/android/animation/ValueAnimator.java 的 sDefaultInterpolator）。暂停与恢复只控制是否派帧，不逐 tick 累加增量，也不对单次增量设上限。
2. 刷新节奏对齐源端逐帧：用 displaySync（或下一帧回调）按 vsync 驱动，并随宿主可见性暂停、恢复帧回调；固定周期定时器只用于源端本就按固定周期 tick 的逻辑。
3. 规格描述前后台行为时把“后台期间不派帧、不推进显示”和“回前台按真实流逝时间追平”分开写，不只写“停摆”；转写源端 Animator 时连同时长写明生效的插值器及其来源（显式设置或框架默认）。改用 animateTo/曲线时注意 Curve.EaseInOut 是三次贝塞尔，与 AccelerateDecelerate 的余弦曲线不等价，要一比一时用 curves.customCurve 写入同一公式。

## 可选检查

- 对追平语义有疑问时，取一段 10s 的进度，运行 3s 后退后台 4s 再回前台：进度应约为 0.7，而不是停在 0.3 附近。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-34903093a988aad52061](../../../store/cases/case-34903093a988aad52061/e127c825ec9e70a3c6237159da0b285cf7d81483112e4a883a38d41762f5a5aa.json) · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`e127c825ec9e70a3c6237159da0b285cf7d81483112e4a883a38d41762f5a5aa`
- [case-cfbbc44d6d4ed0b9c289](../../../store/cases/case-cfbbc44d6d4ed0b9c289/1ebcd4d6ffa6d56157e44ef09303eb6db5a95869daf11f752647c11d085c7782.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`1ebcd4d6ffa6d56157e44ef09303eb6db5a95869daf11f752647c11d085c7782`
