# 移植 GestureDetector 时写全长按吞事件、平均焦点滚动和首击锚定的双击，不凭记忆自建

审的是：代码
触发（任一种）：
- 读到：源端 new GestureDetector(…, SimpleOnGestureListener)，覆写 onScroll / onSingleTapUp / onDoubleTap，onTouchEvent 里调 gestureDetector.onTouchEvent(event)；写错的样子：目标自建检测器没有长按超时（按住到期后仍回调滚动或单击）；onScroll 只跟首指（ptrIds[0]、touches[0]）；双击按「距上次抬起 300ms」判定并回调第二次按下的坐标
适用范围：界面实现阶段，在 ArkUI onTouch 上复刻安卓 GestureDetector 的回调时
做法：
- 打开 Android SDK sources/android-N 的 GestureDetector.java，按 onTouchEvent 逐段移植；Handler 的 TAP、SHOW_PRESS、LONG_PRESS 消息改用 setTimeout / clearTimeout，ViewConfiguration 尺寸按目标密度换算
- 长按定时器到期置 inLongPress，之后 MOVE 不回调 onScroll、UP 不回调 onSingleTapUp（监听没覆写 onLongPress 也照做）；onScroll 距离取全部未抬起手指平均焦点的差；第二次 DOWN 时首击的 TAP 定时器仍未到期且在双击范围内才算双击，onDoubleTap 传第一次按下的事件
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 返修照本机 SDK 的 GestureDetector 逐段移植后，按住约 0.7s 再拖动不平移、松手不走步，与安卓一致：长按吞事件要落成行为（出处：卡里修好并验证过）
- DOWN 时 hadTapMessage = mHandler.hasMessages(TAP)，为真且 isConsideredDoubleTap(...) 时调 mDoubleTapListener.onDoubleTap(mCurrentDownEvent)；否则 sendEmptyMessageDelayed(TAP, mDoubleTapTimeout)：双击以首击计时，回调的是第一次按下事件（出处：android.view.GestureDetector#onTouchEvent）
- dispatchLongPress()：removeMessages(TAP)；mInLongPress = true；mListener.onLongPress(mCurrentDownEvent)：长按到期的处理，之后 MOVE、UP 都看 mInLongPress（出处：android.view.GestureDetector#dispatchLongPress）
- focusX = sumX / div（div = pointerUp ? count - 1 : count）；scrollX = mLastFocusX - focusX：滚动按平均焦点（出处：android.view.GestureDetector#onTouchEvent）
- DEFAULT_LONG_PRESS_TIMEOUT = 400、TAP_TIMEOUT = 100、DOUBLE_TAP_TIMEOUT = 300、DOUBLE_TAP_MIN_TIME = 40（ms）；TOUCH_SLOP = 8、DOUBLE_TAP_SLOP = 100（dp）：检测器用到的框架默认参数（出处：android.view.ViewConfiguration）
针对本应用要查的：
- 移植哪一版 GestureDetector：源工程模块级 Gradle 构建脚本里的 compileSdk；Android SDK 的 sources/android-<N>/android/view/GestureDetector.java；取 compileSdk 对应版本的 onTouchEvent、isConsideredDoubleTap、dispatchLongPress 逐段移植
来源：1 张卡，1 个应用
- case-c576f74cc60bac7ba886（Sokoban）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 1、建议 2；取值 1 ← 诊断
