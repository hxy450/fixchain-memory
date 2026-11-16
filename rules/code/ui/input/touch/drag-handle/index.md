# 拖拽柄上的 startDrag 和拖拽阴影

agent 会看到什么：读到拖拽柄的 OnTouchListener 在 ACTION_DOWN 里 startDrag(..., new View.DragShadowBuilder(v), ...)，拖拽阴影只在拖拽期间存在；产物里作拖拽柄的 Image 加 onTouch / PanGesture 自绘拖拽有没有 .draggable(false)，拖拽图层用 getOverlayManager().addComponentContent 挂在什么时段

## 规矩

- rule-81f3b488e2e6｜作拖拽柄或按钮的 Image 一律写 .draggable(false)｜读到：拖拽柄的 OnTouchListener 只在 ACTION_DOWN 里 startDrag，没有长按分支；写错：拖拽柄写成 Image($r(...)) 加 onTouch / priorityGesture(PanGesture) 自绘拖拽，没有 .draggable(false)；长按时系统图片拖拽接管，自绘拖拽收到 Cancel
- rule-3e75ede1e67a｜用 OverlayManager 挂窗口级图层时只在需要的时段挂载，常驻就用帧节点根并切换命中｜读到：源码在 ACTION_DOWN 里 startDrag(..., new View.DragShadowBuilder(v), ...)，拖拽阴影只在拖拽期间存在；写错：aboutToAppear 里 getOverlayManager().addComponentContent(content) 挂一个常驻图层，根是自定义组件、内层 Stack 写 HitTestMode.None，整页不响应触摸
