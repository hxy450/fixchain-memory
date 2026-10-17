# ui/interaction/gestures

触摸与手势移植：逐指派发过滤、自写状态机阈值、识别器默认参数、系统拖拽与长按触感

[上一级](../index.md)

## 本级经验

- [onTouch 逐指派发按源端接收方式过滤](lesson-68023ac5f088c72a775a.lesson.md) · 阶段：spec/execute · 信号：onTouch, getAction, getActionMasked, ACTION_POINTER_DOWN
- [手势起点 Image 写 draggable(false)](lesson-b30da57443f68ab9046a.lesson.md) · 阶段：execute · 信号：.draggable(false), Image, onTouch, PanGesture
- [自写触摸状态机按源阈值复刻，不换识别器](lesson-b9f5cb5d3ae174e5bf70.lesson.md) · 阶段：spec/execute · 信号：onTouch, dispatchTouchEvent, ItemTouchHelper, ScaleGestureDetector
- [长按手势显式补系统长按触感](lesson-8a752faf9f5dff52e3ff.lesson.md) · 阶段：execute · 信号：combinedClickable, onLongClick, hapticFeedbackEnabled, LongPressGesture
