# Compose Animatable 改写成自驱计时时，进度按绝对帧时间算，不钳制、不累加增量

审的是：代码
触发（任一种）：
- 读到：Compose `Animatable(0f)` / `Animatable(Color)` 用 `animateTo(target, tween(durationMillis = …, easing = LinearEasing))` 推进进度；写错的样子：目标逐 tick 累加增量，并用 `Math.min(now - <上次时间>, <若干倍 tick>)` 给单次增量设上限；注释称「后台近似冻结」
适用范围：把 Compose Animatable 的定时动画改写成 ArkTS 自驱 ticker 时，前后台切换的时间推进
做法：
- 进度 = (frameTime − 首帧时间) / duration，钳到 [0, 1]；每帧按当前帧时间重算，不逐 tick 累加，也不给单次增量设上限
- 后台可以停止派帧，回前台第一帧按真实流逝时间追平，必要时一帧走完
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 按 frame − 首帧推进并删除钳制：修复后的计时方式（出处：卡里修好并验证过）
未核实：Compose 播放时间 = frameTime − startTime、帧时钟暂停后回前台按真实时间追平，出自卡，本机没有 Compose 源码可核
来源：1 张卡，1 个应用
- case-34903093a988aad52061（Cofi）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 1 ← 诊断
