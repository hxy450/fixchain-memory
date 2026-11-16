# 安卓触摸回调迁成 onTouch

agent 会看到什么：源端 OnTouchListener / onTouchEvent / dispatchTouchEvent / GestureDetector 按 MotionEvent 的 ACTION_* 处理触摸；产物里 .onTouch 按 TouchType 和 touches / changedTouches 做的判断

## 规矩

- rule-8aa53acf1eee｜onTouch 桥接源端 getX/getY 时，Move 取 touches[0]，Down/Up 多指时跳过｜读到：源端 switch (event.getAction()) 只有 ACTION_DOWN / ACTION_MOVE / ACTION_UP，坐标用无索引的 getX() / getY()；写错：.onTouch 回调里对所有 TouchType 统一取 event.changedTouches[0]，或 TouchType.Down / TouchType.Up 分支没有 event.touches.length > 1 的过滤
- rule-b7f19b46ddba｜ArkUI onTouch 判末指抬起写 type===Up 且 touches.length===1，不写 0｜读到：源端或规格要求在最后一根手指抬起（ACTION_UP，「非末指 Up 不进状态机」）时结算手势；写错：目标 .onTouch 的 Up 分支写成 event.touches.length === 0（或 touches 为空）才结算，滑动永远不触发
- rule-731231abd38b｜多按钮 onTouch 判首末指不用 touches.length，改用本控件的手指 id 集合｜读到：安卓源里多个兄弟 View 各自 setOnTouchListener，按 getAction() 的 ACTION_DOWN / ACTION_UP 驱动按住-释放（setPressed、开始或停止动作）；写错：目标里每个按钮的 .onTouch 用 event.touches.length === 1（或 > 1 就 return）作 TouchType.Down / TouchType.Up 的门，注释写着只跟首指、丢掉非首指 Down 和非末指 Up
- rule-8f1b69d8e08f｜GestureDetector 的 onFling 迁到 onTouch 时复刻触发路径，不用总位移除以总时长｜读到：onTouch 只 return gestureDetector.onTouchEvent(event)，SimpleOnGestureListener.onFling 里按 velocityX / velocityY 和位移判方向；写错：目标 .onTouch 的 Up 里用起点到抬起的总位移除以总时长当速度、只要求 > 0 就判方向，没有触摸容差、长按、双击和最小/最大抛掷速度
- rule-ea6fe14f3f01｜源基类 dispatchTouchEvent 带多项副作用时，目标基类逐项映射，不承接的列为裁剪项｜读到：源页面基类重写 dispatchTouchEvent，ACTION_DOWN 分支同时做几件事（刷新触摸时间、触摸计数上报、点外收键盘如 isShouldHideInput / hideKeyBoard）；规格里同一条也列出这些副作用；写错：目标基类写成 dispatchTouchEvent → onTouch() 的对等，onTouch 只承接其中一部分（如两行计数），收键盘等其余副作用既没有映射注释，也没在报告里列为裁剪项
- rule-7428dc095856｜预览 View 的 onTouchEvent 分派手势时，目标要接 .onTouch 和 PinchGesture｜读到：源端预览 View（SurfaceView 子类等）的 onTouchEvent 直接 return 给另一个类的触摸方法，再由 GestureDetector / ScaleGestureDetector 分派到单击对焦、onDoubleTap、ScaleGestureDetector 的 onScale；写错：目标只写了单击、缩放等内层处理函数，没有入口分派；预览宿主 XComponent 上只有 .onLoad / .onDestroy，没有 .onTouch 和 PinchGesture，这些处理函数在 UI 文件里没有调用方
- rule-c1620b7a59c8｜ArkUI 逐指触摸先折成 MotionEvent 序列，再按源端顺序先喂缩放检测器、后喂手势检测器｜读到：源端 onTouchEvent 里先 scaleGestureDetector.onTouchEvent(event)、再 gestureDetector.onTouchEvent(event)，之后才走自己的 ACTION_MOVE 分支；写错：目标 onTouch 里把 TouchEvent 直接分给各自的检测逻辑，没有折成 DOWN / POINTER_DOWN / MOVE / POINTER_UP / UP 序列，或喂检测器的顺序和源端不同
- rule-a69a4bca79f9｜移植 GestureDetector 时写全长按吞事件、平均焦点滚动和首击锚定的双击，不凭记忆自建｜读到：源端 new GestureDetector(…, SimpleOnGestureListener)，覆写 onScroll / onSingleTapUp / onDoubleTap，onTouchEvent 里调 gestureDetector.onTouchEvent(event)；写错：目标自建检测器没有长按超时（按住到期后仍回调滚动或单击）；onScroll 只跟首指（ptrIds[0]、touches[0]）；双击按「距上次抬起 300ms」判定并回调第二次按下的坐标
- rule-dffda54d41ff｜源端用 ScaleGestureDetector 缩放时，用 onTouch 逐事件移植 span 和门槛｜读到：源端（含三方库里的缩放图片控件）用 `ScaleGestureDetector` 的 `onScale` / `getScaleFactor` 缩放；写错：目标用 `PinchGesture` 按 `event.scale` 直接缩放、`PanGesture` 识别后再补偿位移，没有源端的 span slop 门槛
- rule-24ca79b8c74d｜三方手势控件没源码时，代码按 AAR 还原缩放双击，还原不了在回执登记缺口｜读到：源布局用三方库的缩放图片或画廊控件（如 `TouchImageView`、自定义 `ViewPager`）；写错：代码头注释写三方库无源码，画廊写成 `Swiper` + `Image`，没有任何缩放、双击实现，回执里也没登记缺口
- rule-a209dce5e1fd｜源端 MotionEvent 点击状态机用 onTouch 逐事件移植，Swiper 拖动时取消点击｜读到：源 `onTouch` 里 `ACTION_DOWN` 记坐标、`ACTION_MOVE` 位移 ≥ 阈值取消、`ACTION_UP` 仍按下才 click；父布局 `onInterceptTouchEvent` 把每个 MotionEvent 转给监听器后 return super；写错：目标页项只挂 `.onClick(...)`，没有 `onTouch`、阈值和拖动后取消；注释写点击与 `Swiper` 滑动内建分离、不迁移
