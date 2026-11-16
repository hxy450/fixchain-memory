# onTouch 桥接源端 getX/getY 时，Move 取 touches[0]，Down/Up 多指时跳过

审的是：代码
触发（任一种）：
- 读到：源端 switch (event.getAction()) 只有 ACTION_DOWN / ACTION_MOVE / ACTION_UP，坐标用无索引的 getX() / getY()；写错的样子：.onTouch 回调里对所有 TouchType 统一取 event.changedTouches[0]，或 TouchType.Down / TouchType.Up 分支没有 event.touches.length > 1 的过滤
适用范围：源端只跟随首指（未掩码的 getAction、无索引的坐标），迁成 ArkUI .onTouch 的触控桥接代码
做法：
- TouchType.Down 和 TouchType.Up 时先判断 event.touches.length > 1，成立就直接 return，不把第二指按下当成新的 ACTION_DOWN、不把首指抬起当成 ACTION_UP
- TouchType.Move 取 event.touches[0].x / event.touches[0].y，对应源端的 getX() / getY()（指针索引 0）
- 首指 Down、末指 Up 和 TouchType.Cancel 取 event.changedTouches[0]；不要以单指为由对所有类型统一取 changedTouches[0]
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onTouch(event: (event: TouchEvent) => void): T：组件的触摸回调，每根手指的 Down/Move/Up 都会进来（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onTouch）
- touches: TouchObject[]（All finger information）：全部在屏触点；touches[0] 对应源端的指针索引 0（出处：鸿蒙 SDK 的 ets/component/common.d.ts，TouchEvent.touches）
- changedTouches: TouchObject[]（Finger information changed）：本次变化的触点；多指时 Move 的 changedTouches[0] 会在两指间换（出处：鸿蒙 SDK 的 ets/component/common.d.ts，TouchEvent.changedTouches）
- touches、changedTouches 在使用时都要校验是否为空：取 [0] 之前先判断长度（出处：ts-universal-events-touch.md，TouchEvent对象说明）
- getX()：The X coordinate of the first pointer index：源端无索引的 getX()/getY() 取指针索引 0（出处：android.view.MotionEvent#getX）
- Down/Up 时 touches.length > 1 忽略、Move 取 touches[0]、首指 Down / 末指 Up / Cancel 取 changedTouches[0]：两指同时下滑时不再把起点重置、不再误判方向（出处：卡里修好并验证过）
- onTouchIntercept(callback: Callback<TouchEvent, HitTestMode>): T：同族接口：CommonMethod 上同样拿 TouchEvent 的触摸拦截回调（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onTouchIntercept）
- setOnTouch(callback: Callback<TouchEvent> | undefined): void：同族接口：UICommonEvent 上设置触摸回调（出处：鸿蒙 SDK 的 ets/component/common.d.ts，UICommonEvent.setOnTouch）
未核实：Up 事件的 touches 是否还含正在抬起的那根手指，声明和文档都没写明；卡里只验证了两指同时同向滑动
来源：1 张卡，1 个应用
- case-e96028e4cc29cd5bd8eb（2048）：做法第 1 步 ← 诊断、建议 1；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2、诊断；取值 6 ← 诊断
