# GestureDetector 的 onFling 迁到 onTouch 时复刻触发路径，不用总位移除以总时长

审的是：代码
触发（任一种）：
- 读到：onTouch 只 return gestureDetector.onTouchEvent(event)，SimpleOnGestureListener.onFling 里按 velocityX / velocityY 和位移判方向；写错的样子：目标 .onTouch 的 Up 里用起点到抬起的总位移除以总时长当速度、只要求 > 0 就判方向，没有触摸容差、长按、双击和最小/最大抛掷速度
适用范围：源端用 GestureDetector 识别滑动（onFling），目标在 ArkUI .onTouch 里自己判定滑动的代码
做法：
- 把每个 onTouch 事件都交给一个复刻 GestureDetector 的检测器：Down 记起点并开始跟踪速度；移出 8dp 触摸容差前不算滑动；按满 400ms 进入长按；抬起时若是双击第二击、长按中或仍在容差内，都不回调 onFling
- 抬起时按抬起前的速度估计（卡里复刻 VelocityTracker 的 LSQ2，上限 8000dp/s），|vx| 或 |vy| 超过 50dp/s 才走源端 onFling 的方向矩阵；不用总位移/总时长的平均速度代替
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 抬起时依次判：双击第二击 → 长按中 → 仍在触摸容差内（onSingleTapUp）→ 否则 computeCurrentVelocity(1000, 最大抛掷速度) 后 |vy| 或 |vx| > 最小抛掷速度才调 onFling：GestureDetector 在 ACTION_UP 上的分支顺序（出处：android.view.GestureDetector#onTouchEvent）
- config_viewMinFlingVelocity = 50dp，config_viewMaxFlingVelocity = 8000dp：最小、最大抛掷速度（每秒）（出处：Android SDK 平台资源 data/res/values/config.xml，config_viewMinFlingVelocity、config_viewMaxFlingVelocity（按应用的 compileSdk 取对应平台））
- config_viewConfigurationTouchSlop = 8dp：触摸容差（出处：Android SDK 平台资源 data/res/values/config.xml，config_viewConfigurationTouchSlop（按应用的 compileSdk 取对应平台）；android.view.ViewConfiguration 的 TOUCH_SLOP）
- DEFAULT_LONG_PRESS_TIMEOUT = 400（ms），DOUBLE_TAP_TIMEOUT = 300（ms）：长按时长、双击间隔（出处：android.view.ViewConfiguration 的 DEFAULT_LONG_PRESS_TIMEOUT、DOUBLE_TAP_TIMEOUT）
- onTouch 事件逐个交给复刻 8dp 容差、400ms 长按、双击、LSQ2 速度和最小/最大抛掷速度的检测器后，滑动按源端行为触发：卡里最终保留的改法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端是否关了长按或双击：源工程里构造 GestureDetector 的 Java/Kotlin 代码，找 setIsLongpressEnabled、setOnDoubleTapListener 的调用；setIsLongpressEnabled(false) 时检测器不做长按分支；setOnDoubleTapListener(null) 时不做双击分支；没调用就全做
未核实：设备的资源 overlay 可以改触摸容差和抛掷速度，这里写的是框架默认值；VelocityTracker 默认用 LSQ2 出自卡，本机只有 Java 源码，没核到原生实现
来源：1 张卡，1 个应用
- case-a1849836a1bfff3c265c（Privacy Friendly 2048）：做法第 1 步 ← 诊断、建议 1；做法第 2 步 ← 建议 2、诊断；取值 5 ← 诊断
