# 源端触摸交给 GestureDetector/ScaleGestureDetector 时，规格写按框架源码逐段移植

审的是：规格
触发（任一种）：
- 读到：源端自定义 View 的 onTouchEvent 把每个 MotionEvent 先交 ScaleGestureDetector.onTouchEvent、再交 GestureDetector.onTouchEvent，监听只覆写 onSingleTapUp / onDoubleTap / onScroll / onScale 等回调；写错的样子：规格映射写「等价检测器按触发路径复刻（非逐事件直译）」「PinchGesture/等效捏合检测」；长按超时只出现在备注、没写成行为；没读框架源码就声明「行为等价、无 HARD-DIV」
适用范围：规格提取阶段，源端触摸由 Android 框架手势检测器处理、目标 ArkUI 要在 onTouch 上自做同等检测时
做法：
- 映射契约写成「按 Android SDK sources/android-N 中 GestureDetector（及 ScaleGestureDetector）的 onTouchEvent 逐段移植」
- 列出回调依赖的框架行为：长按到期后不再回调 onScroll / onSingleTapUp（onLongPress 空实现也一样）；onScroll 按全部未抬起手指的平均焦点算；双击要第二次按下时首击的 TAP 消息未到期，onDoubleTap 收到第一次按下事件；缩放在每个 MOVE 判断开始，跨度变化超过 spanSlop 且不小于 minSpan，targetSdk>18 时 quick scale 默认开
- 没读框架源码前不写「行为等价、无 HARD-DIV」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ACTION_MOVE 分支开头 if (mInLongPress || mInContextClick) { break; }；ACTION_UP 里 mInLongPress 为真时不调 onSingleTapUp：长按到期后吞掉滚动和单击（出处：android.view.GestureDetector#onTouchEvent）
- 焦点 focusX = sumX / div（跳过正在抬起的指针）；scrollX = mLastFocusX - focusX：onScroll 的距离按全部手指平均焦点算，不是首指（出处：android.view.GestureDetector#onTouchEvent）
- if (!mInProgress && span >= minSpan && (wasInProgress || Math.abs(span - mInitialSpan) > mSpanSlop)) 调 onScaleBegin：缩放开始条件，每个事件都判断（出处：android.view.ScaleGestureDetector#onTouchEvent）
- targetSdkVersion > Build.VERSION_CODES.JELLY_BEAN_MR2 时 setQuickScaleEnabled(true)：targetSdk 19 起 quick scale 默认开（出处：android.view.ScaleGestureDetector#ScaleGestureDetector）
针对本应用要查的：
- 按哪一版框架源码移植、quick scale 是否默认开：源工程模块级 Gradle 构建脚本里的 compileSdk、targetSdk；Android SDK 的 sources/android-<N>/android/view/ 下 GestureDetector.java、ScaleGestureDetector.java；取 compileSdk 对应版本的源码；targetSdk 大于 18 时规格写 quick scale 默认开
来源：1 张卡，1 个应用
- case-c576f74cc60bac7ba886（Sokoban）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1
