# Compose AnimatedVisibility 的显隐动画

agent 会看到什么：读到 Compose 的 AnimatedVisibility(visible, enter = fadeIn() / expandVertically(), exit = …) 包住部分兄弟节点、没传 animationSpec；产物里折叠容器（.width(cond ? N : 0) 加 .clip(true)）或 if 分支里放了哪些节点、有没有 .transition(TransitionEffect.OPACITY…)、动画曲线是定时长还是 springMotion

## 规矩

- rule-0f7df866232f｜AnimatedVisibility 转成折叠容器时只放 lambda 内的节点，lambda 外的兄弟留在容器外常驻｜读到：Compose 同一 Row 里既有常驻节点，又有 AnimatedVisibility(visible) { … } 或条件块只包住其中一部分兄弟（连同它前面的 Spacer）；写错：目标的折叠容器（.width(cond ? N : 0) 加 .clip(true)，或 if 分支）里放进了源端在 AnimatedVisibility lambda 外的常驻节点，容器外没有它
- rule-9056069e0bd0｜fadeIn / fadeOut 包住的块要加 OPACITY 弹簧转场，不用 if 瞬显｜读到：AnimatedVisibility(enter = fadeIn(), exit = fadeOut()) 包住徽标等小块；写错：目标对应块只用 if 条件渲染，没有 .transition(TransitionEffect.OPACITY…)
- rule-df098705851e｜可见性动画没写 animationSpec 时用 springMotion(2π/√400, 1.0)｜读到：AnimatedVisibility 的 expandVertically()、shrinkVertically()、fadeIn()、fadeOut() 都没传 animationSpec（沿用 Compose 默认 spring）；写错：目标转场或 animateTo 写 .animation({ duration: 200 }) 之类的定时长 tween
