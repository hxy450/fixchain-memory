# ui/interaction/hit-testing

叠放层的命中测试与手势归属：全尺寸覆盖层透传、Block 只放遮罩、侧滑行按钮热区、滑删方向与触发瞬间的坐标取值。

[上一级](../index.md)

## 本级经验

- [Block 只放无子控件的遮罩层，面板根容器 Default](lesson-cf018b76af68b4c00895.lesson.md) · 阶段：execute · 信号：HitTestMode.Block, hitTestBehavior, HitTestMode.Default, showCustomDialog
- [SwipeToDismissBox 方向按手势与偏移符号写明](lesson-7f5eba1b969bddfb34dc.lesson.md) · 阶段：spec/execute · 信号：SwipeToDismissBox, enableDismissFromStartToEnd, EndToStart, StartToEnd
- [不处理点击的全尺寸覆盖层显式设 Transparent 命中](lesson-4a4f8d845a204ffa244b.lesson.md) · 阶段：execute/repair · 信号：hitTestBehavior, HitTestMode.Transparent, HitTestMode.None, FrameLayout
- [侧滑行按钮被拦截时只调按钮热区，不把内容层设 None](lesson-6677d286e690407d4af4.lesson.md) · 阶段：repair · 信号：HitTestMode.None, PanGesture, hitTestBehavior, Stack
- [锚点坐标在点击回调即时取，onAreaChange 只兜底](lesson-963bf871aa4e910a8fc8.lesson.md) · 阶段：execute/repair · 信号：getLocationInWindow, onAreaChange, GestureEvent.fingerList, globalX
