# 触摸、手势与按键

源端有 OnTouchListener / onTouchEvent、GestureDetector、跟手拖动、onKeyDown / dispatchKeyEvent，目标端有 .onTouch、PanGesture、parallelGesture、.onKeyEvent 时

## 触发族

- [安卓触摸回调迁成 onTouch](ontouch-pointers/index.md)（11 条）：源端 OnTouchListener / onTouchEvent / dispatchTouchEvent / GestureDetector 按 MotionEvent 的 ACTION_* 处理触摸；产物里 .onTouch 按 TouchType 和 touches / changedTouches 做的判断
- [Activity 的按键回调（onKeyDown、onKeyUp）](activity-key-events/index.md)（8 条）：读到 Activity 或 View 覆写 onKeyDown / onKeyUp / dispatchKeyEvent 处理 KEYCODE_*；交回的 .onKeyEvent 没判 KeyType、挂在要先获焦的子组件上、页内没有可获焦组件，或不放行输入框
- [绑了 PanGesture 的拖拽层（下拉关弹层、侧滑露按钮）](pan-gesture-drag-layer/index.md)（2 条）：读到旧代码里弹层或列表行用 PanGesture / parallelGesture 跟手拖动（在顶部才下拉关闭、横滑露出操作按钮），产物里是改成 bindSheet 后丢了顶部门禁，或给带收起手势的内容层设 HitTestMode.None
- [拖拽柄上的 startDrag 和拖拽阴影](drag-handle/index.md)（2 条）：读到拖拽柄的 OnTouchListener 在 ACTION_DOWN 里 startDrag(..., new View.DragShadowBuilder(v), ...)，拖拽阴影只在拖拽期间存在；产物里作拖拽柄的 Image 加 onTouch / PanGesture 自绘拖拽有没有 .draggable(false)，拖拽图层用 getOverlayManager().addComponentContent 挂在什么时段
- [长按监听（setOnLongClickListener）和松手回调](long-click-release/index.md)（1 条）：读到源端同一个 View 既有 setOnClickListener 又有 setOnLongClickListener，触摸监听在 MotionEvent.ACTION_UP 时停止长按动作；产物里组件只挂了 .onClick(...)，没有 LongPressGesture 和松手时的 onActionEnd
