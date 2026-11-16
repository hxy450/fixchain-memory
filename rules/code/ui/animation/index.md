# 动效

源端有 Animator 和它的 setDuration、动效起点的锚点位置、Compose 的 animateItem / animateContentSize / AnimatedContent、AnimatedVectorDrawable、LottieAnimationView，目标端有 animateTo、.animation、.transition 或 lottie 时

## 触发族

- [动效起点的锚点窗口位置](anim-anchor/index.md)（3 条）：读到源端动效触发时对锚点 View（可能是按钮或列表行里的子 View）调 getLocationInWindow 再加半宽半高求起点；产物里点击时拿 onAreaChange 缓存的 globalPosition 当起点，或量的是外层 Button / Row
- [Compose 的尺寸、内容切换和列表项动画](compose-animation/index.md)（6 条）：读到 Compose 的 Modifier.animateItem()、animateContentSize()、AnimatedContent 的 transitionSpec / SizeTransform，交回的代码在 ListItem、ForEach 或切换容器上没写对应的 animateTo、transition、animation
- [Compose 的 AnimatedVectorDrawable 动画图标](animated-vector-painter/index.md)（2 条）：读到 Compose 用 AnimatedImageVector.animatedVectorResource(R.drawable.…) 加 rememberAnimatedVectorPainter(icon, atEnd)，产物里是 Image($r('app.media.…')) 静态图、SymbolGlyph 按状态切换或 Path / Canvas 的 pathData 插值
- [浮层出场动画的时长](dismiss-duration/index.md)（1 条）：读到源端上滑超过阈值时 cancel() 主动画、改播另一个 setDuration 不同的 Animator；产物里 dismiss() 固定 animateTo({ duration: 300 })，PanGesture 收起和定时自动出场共用它
- [LottieAnimationView 动画层](lottie-view/index.md)（1 条）：读到布局里的 com.airbnb.lottie.LottieAnimationView、代码 setAnimation("json/...") 或按数据状态切动画；产物里只有一张静态 Image($r('app.media.…'))，没有 @ohos/lottie 依赖、迁过来的 json 文件和占位登记
- [显隐切换带的淡入淡出动画](fade-visibility/index.md)（1 条）：读到源码在 setVisibility(View.VISIBLE / View.GONE) 前后调淡入淡出（fade 辅助方法、startAnimation、res/anim 的 <alpha>），动画结束才切显隐；产物里直接改 if 条件渲染依赖的状态让节点瞬显瞬隐，没有 animateTo
- [共享元素转场的 geometryTransition](geometry-transition/index.md)（2 条）：读到 Compose SharedTransitionLayout 里 Modifier.sharedBounds 包住 Modifier.sharedElement，或已写好的对端文件里的 .geometryTransition；产物里同一配对子树外层和内层各挂一个 .geometryTransition
- [Compose AnimatedVisibility 的显隐动画](compose-animated-visibility/index.md)（3 条）：读到 Compose 的 AnimatedVisibility(visible, enter = fadeIn() / expandVertically(), exit = …) 包住部分兄弟节点、没传 animationSpec；产物里折叠容器（.width(cond ? N : 0) 加 .clip(true)）或 if 分支里放了哪些节点、有没有 .transition(TransitionEffect.OPACITY…)、动画曲线是定时长还是 springMotion
- [ValueAnimator 改写成的自驱帧循环](valueanimator-frame-loop/index.md)（2 条）：读到 ValueAnimator.ofFloat / ObjectAnimator 设 setDuration、addUpdateListener 逐帧写进度并 invalidate()，有没有 setInterpolator；产物里 postFrameCallback 的 FrameCallback 和 pending 去重标志、进度是不是直接取 (now - start) / duration
