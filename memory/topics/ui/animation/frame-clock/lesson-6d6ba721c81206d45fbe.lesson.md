# 把 Compose Animatable 等帧时钟动画改成自驱 ticker 时，进度按“当前帧时间 − 起始时间”计算：后台可停帧，回前台首帧按真实流逝追平，不钳制单次增量

ID：`lesson-6d6ba721c81206d45fbe` · 版本：2 · 阶段：spec/execute · 主题：[ui/animation/frame-clock](index.md)

概要：自驱 ticker 进度按帧时间减起点，不钳增量

信号：`Animatable`, `animateTo`, `tween(`, `LinearEasing`, `displaySync`, `setInterval`, `ON_STOP`, `tickerFlow`, `elapsedRealtime`

## 何时使用

计时或动画引擎的规格与实现阶段，把 Animatable.animateTo(tween) 等由帧时钟驱动的进度改写为 setInterval、displaySync 等自驱 ticker，确定刷新周期与退后台、回前台的时间推进时

## 适用情境

源端进度由 Compose Animatable.animateTo(tween(duration, LinearEasing)) 一类帧时钟动画驱动，帧时钟随宿主 ON_STOP 暂停；目标没有可直接复用的同语义帧时钟，自写 ticker 复刻进度推进与前后台切换。同一应用可能另有后台 Worker 以固定周期（如 tickerFlow + elapsedRealtime）推进，其周期与补偿方式不属于前台动画。

## 原因

Compose 动画的播放时间等于帧时间减起始时间：后台不出帧只是暂停绘制，回前台首帧按真实流逝时间推进，必要时一帧结束。改成逐 tick 累加增量并给单次增量设上限，会丢掉后台经过的时间，进度停在退后台时附近；用固定的长周期定时器代替逐帧刷新，进度环与高精度时间文本会成段跳变。规格里“后台停摆”一类措辞容易被读成丢弃后台时间。

## 做法

1. 进度按绝对时间计算：progress = (frameTime − startTime) / duration，frameTime 取帧回调时间戳或单调时钟；暂停与恢复只控制是否派帧，不逐 tick 累加增量，也不对单次增量设上限。
2. 刷新节奏对齐源端逐帧：用 displaySync（或下一帧回调）按 vsync 驱动，并随宿主可见性暂停、恢复帧回调；固定周期定时器只用于源端本就按固定周期 tick 的逻辑。
3. 规格描述前后台行为时把“后台期间不派帧、不推进显示”和“回前台按真实流逝时间追平”分开写，不只写“停摆”。

## 可选检查

- 对追平语义有疑问时，取一段 10s 的进度，运行 3s 后退后台 4s 再回前台：进度应约为 0.7，而不是停在 0.3 附近。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [转述规则保留替代写法；禁并发构建的改动汇总后立即全量构建](../../../process/handoff-loss/lesson-73a7dd4f78cb747f7e7e.lesson.md)（共享 1 张卡）
- [规格与源码冲突按源实现，例外只认决策 ID](../../../process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-34903093a988aad52061](../../../../../store/cases/case-34903093a988aad52061/e127c825ec9e70a3c6237159da0b285cf7d81483112e4a883a38d41762f5a5aa.json) · 结论：diagnosis, rec-0b7441efd5, rec-fe3a273834
  卡片版本：`e127c825ec9e70a3c6237159da0b285cf7d81483112e4a883a38d41762f5a5aa`
