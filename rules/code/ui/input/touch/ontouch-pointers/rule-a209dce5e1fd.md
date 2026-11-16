# 源端 MotionEvent 点击状态机用 onTouch 逐事件移植，Swiper 拖动时取消点击

审的是：代码
触发（任一种）：
- 读到：源 `onTouch` 里 `ACTION_DOWN` 记坐标、`ACTION_MOVE` 位移 ≥ 阈值取消、`ACTION_UP` 仍按下才 click；父布局 `onInterceptTouchEvent` 把每个 MotionEvent 转给监听器后 return super；写错的样子：目标页项只挂 `.onClick(...)`，没有 `onTouch`、阈值和拖动后取消；注释写点击与 `Swiper` 滑动内建分离、不迁移
适用范围：源端在 View 层用 MotionEvent 自判点击和滑动，目标是含 Swiper 等可拖动容器的 ArkUI 页面时
做法：
- 在承接源端监听器的根容器上写 .onTouch((e: TouchEvent) => {…})：TouchType.Down 记 e.touches[0] 的 x、y 并置按下；TouchType.Move 位移 ≥ 阈值时置未按下；TouchType.Up 时仍按下才执行点击；TouchType.Cancel 置未按下
- 子 Swiper 的 .onGestureSwipe(...) 回调里置未按下，拖动一开始就取消点击
- 对照源方法逐项列出跟手位移、阈值、速度、取消各由目标哪一行承接，缺一项就补
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onTouch(event: (event: TouchEvent) => void): T：逐事件接收触摸（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onTouch）
- TouchType.Down / Move / Up / Cancel：对应源端 ACTION_DOWN / ACTION_MOVE / ACTION_UP / ACTION_CANCEL（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，TouchType）
- TouchObject.x、y 的单位是 vp：源端阈值按 px 写时，比较前换算到同一单位（出处：ts-universal-events-touch.md，TouchObject）
- onGestureSwipe(event: OnSwiperGestureSwipeCallback): SwiperAttribute：Swiper 被手势拖动翻页时逐帧触发，用来取消点击（出处：鸿蒙 SDK 的 ets/component/swiper.d.ts，SwiperAttribute.onGestureSwipe）
- 根布局加 DOWN / MOVE≥阈值 / UP 状态机，并在 Swiper.onGestureSwipe 时置未按下后，拖动不再误触发点击：改法出自返修（出处：卡里修好并验证过）
- onGestureSwipe(handler: OnTabsGestureSwipeCallback): TabsAttribute：同族接口：Tabs 被手势拖动时的逐帧回调（出处：鸿蒙 SDK 的 ets/component/tabs.d.ts，TabsAttribute.onGestureSwipe）
未核实：卡里环境是 API 24，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-1a09dd649093f650a6fc（omni-notes-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 诊断、建议 2；做法第 3 步 ← 建议 2；取值 5 ← 诊断
