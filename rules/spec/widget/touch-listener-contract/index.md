# 安卓触摸监听（onTouch、GestureDetector）的触控契约

agent 会看到什么：读到源端 onTouch 里 switch (event.getAction()) 分 ACTION_DOWN / MOVE / UP、多个兄弟 View 各自 setOnTouchListener，或 onTouch 只转交 GestureDetector、方向写在 onFling；规格把它逐一对成 TouchType 或只抄阈值，没写附加手指、分指和触发条件

## 规矩

- rule-856116cb7b36｜MotionEvent 动作分支映射到 TouchType 时，规格写明附加手指怎么处理、怎么过滤｜读到：源端 onTouch 里 switch (event.getAction())（未掩码）只列 ACTION_DOWN / ACTION_MOVE / ACTION_UP，坐标用无索引的 getX() / getY()；写错：实现映射把 ACTION_DOWN/MOVE/UP 逐一写成 TouchType.Down/Move/Up 或写「行为等价」一句带过；没写用的是 getAction 还是 getActionMasked、ACTION_POINTER_DOWN/UP 是否参与，没写 ArkUI 逐指派发 Down/Up 和过滤规则
- rule-8f825c311573｜多个兄弟控件各自监听触摸时，触控契约写明分指、按控件内手指集合判首末指｜读到：安卓源里多个兄弟 View（按钮等）各自 setOnTouchListener，监听里用未掩码的 getAction() 只认 ACTION_DOWN / ACTION_UP 驱动按住-释放；targetSdkVersion ≥ 11，且没写 android:splitMotionEvents="false"；写错：规格的触控契约写成「touches.length>1 时非首指的 Down/Up 不进状态机」这类按全屏手指数过滤的说法，或者没写安卓按控件分指、每个控件只收落在自己身上的手指
- rule-aead3d22acee｜源端 onTouch 只转交 GestureDetector、方向写在 onFling 时，契约写明它的触发条件｜读到：安卓源里 OnTouchListener 的 onTouch 只 return gestureDetector.onTouchEvent(event)，监听 extends SimpleOnGestureListener，方向判定写在 onFling 里；写错：规格的手势行只转写 onFling 里的位移/速度阈值（如「位移>阈值且速度>0」），没写抬起速度要超过最小抛掷速度、未移出触摸容差、长按、双击第二击都不回调 onFling；或者把它写成「非首指 Down、非末指 Up 不进状态机」这种原始触摸过滤
- rule-8f792a2bf4a0｜源码有显式触摸状态机时，规格写成行为 AC，不以平台内建为由登记无需迁移｜读到：源 `onTouch` / `onInterceptTouchEvent` 里 `MotionEvent.ACTION_DOWN` 记坐标置按下、`ACTION_MOVE` 位移超过阈值取消、`ACTION_UP` 仍按下才 click；写错：规格写「ArkUI 原生点击/滑动天然分离，无需自判阈值」，转换决策表把这段触摸拦截登记为「无需迁移」，和同一规格里保留阈值的 AC 矛盾
- rule-de1fca5ce9e4｜源端触摸交给 GestureDetector/ScaleGestureDetector 时，规格写按框架源码逐段移植｜读到：源端自定义 View 的 onTouchEvent 把每个 MotionEvent 先交 ScaleGestureDetector.onTouchEvent、再交 GestureDetector.onTouchEvent，监听只覆写 onSingleTapUp / onDoubleTap / onScroll / onScale 等回调；写错：规格映射写「等价检测器按触发路径复刻（非逐事件直译）」「PinchGesture/等效捏合检测」；长按超时只出现在备注、没写成行为；没读框架源码就声明「行为等价、无 HARD-DIV」
- rule-5f3858741c27｜预览表面有手势入口或跨 feature 读面时，规格对接点段要把它们列出来｜读到：源端预览 View 的 onTouchEvent 直接转给别的类，再经 GestureDetector / ScaleGestureDetector 分派；别的组件调用源类的公开读方法；写错：规格「对接点」段只列按钮、滑条回调，没列预览表面的手势入口和被其他 feature 读的读面；验收里有「源:…touchEvent → 标:…touchEvent」式入口，对接点里却没有对应项
