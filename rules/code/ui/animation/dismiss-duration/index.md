# 浮层出场动画的时长

agent 会看到什么：读到源端上滑超过阈值时 cancel() 主动画、改播另一个 setDuration 不同的 Animator；产物里 dismiss() 固定 animateTo({ duration: 300 })，PanGesture 收起和定时自动出场共用它

## 规矩

- rule-9b3da61a6d33｜浮层关闭动画按触发源传时长，手势收起和自动出场不共用一个硬编码时长｜读到：源端上滑超过阈值时 cancel() 主动画，改播另一个 setDuration(...) 不同的 Animator；写错：dismiss() 里固定 animateTo({ duration: 300 }, …)，PanGesture 上滑和定时自动出场都调它
