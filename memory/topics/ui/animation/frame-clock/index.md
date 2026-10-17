# ui/animation/frame-clock

帧驱动与计时：invalidate、自建渲染线程与帧时钟动画迁成 vsync 帧回调，请求合并、实例数与前后台时间推进

[上一级](../index.md)

## 本级经验

- [SurfaceView 线程循环按实例迁，vsync 驱动](lesson-4da9eabca745b3b2be91.lesson.md) · 阶段：spec/plan/execute · 信号：SurfaceView, SurfaceHolder.Callback, lockCanvas, unlockCanvasAndPost
- [invalidate 迁成单一下一帧入口，待决标志合并](lesson-27d9e16a099c2fb437eb.lesson.md) · 阶段：execute · 信号：View.invalidate, invalidate(), onDraw, UIContext.postFrameCallback
- [自驱 ticker 进度按帧时间减起点，不钳增量](lesson-6d6ba721c81206d45fbe.lesson.md) · 阶段：spec/execute · 信号：Animatable, animateTo, tween(, LinearEasing
