# 源端 onTouch 只转交 GestureDetector、方向写在 onFling 时，契约写明它的触发条件

审的是：规格
触发（任一种）：
- 读到：安卓源里 OnTouchListener 的 onTouch 只 return gestureDetector.onTouchEvent(event)，监听 extends SimpleOnGestureListener，方向判定写在 onFling 里；写错的样子：规格的手势行只转写 onFling 里的位移/速度阈值（如「位移>阈值且速度>0」），没写抬起速度要超过最小抛掷速度、未移出触摸容差、长按、双击第二击都不回调 onFling；或者把它写成「非首指 Down、非末指 Up 不进状态机」这种原始触摸过滤
适用范围：安卓 GestureDetector 驱动的滑动（onFling 回调）迁到 ArkUI 时，规格里写手势契约的那一行或那一节
做法：
- 手势契约写明 onFling 的触发条件：抬起时 VelocityTracker 速度（上限 8000dp/s）的 |vx| 或 |vy| 超过最小抛掷速度 50dp/s 才回调；手指没移出 8dp 触摸容差时走单击、按满 400ms 进入长按后抬起、双击的第二击，都不回调 onFling
- onFling 里的位移/速度方向矩阵照源码另写一行，并注明它只在上面的条件满足后才判定
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 抬起时依次判：双击第二击（交给 onDoubleTapEvent）→ 长按中（不回调）→ 仍在触摸容差内（onSingleTapUp）→ 否则 computeCurrentVelocity(1000, 最大抛掷速度) 后 |vy| 或 |vx| > 最小抛掷速度才调 onFling：GestureDetector 在 ACTION_UP 上的分支顺序，速度单位是每秒（出处：android.view.GestureDetector#onTouchEvent）
- config_viewMinFlingVelocity = 50dp，config_viewMaxFlingVelocity = 8000dp：最小、最大抛掷速度（每秒）（出处：Android SDK 平台资源 data/res/values/config.xml，config_viewMinFlingVelocity、config_viewMaxFlingVelocity（按应用的 compileSdk 取对应平台）；android.view.ViewConfiguration 的 MINIMUM_FLING_VELOCITY）
- config_viewConfigurationTouchSlop = 8dp：触摸容差：移出前抬起算单击，不算抛掷（出处：Android SDK 平台资源 data/res/values/config.xml，config_viewConfigurationTouchSlop（按应用的 compileSdk 取对应平台）；android.view.ViewConfiguration 的 TOUCH_SLOP）
- DEFAULT_LONG_PRESS_TIMEOUT = 400（ms）：按住不动满这么久进入长按，之后抬起不回调 onFling（出处：android.view.ViewConfiguration 的 DEFAULT_LONG_PRESS_TIMEOUT）
- DOUBLE_TAP_TIMEOUT = 300（ms）：第一击抬起到第二击按下在这个间隔内算双击（出处：android.view.ViewConfiguration 的 DOUBLE_TAP_TIMEOUT）
- SimpleOnGestureListener 同时实现 OnDoubleTapListener，GestureDetector 构造时自动把它设为双击监听：继承 SimpleOnGestureListener 时双击路径默认生效（出处：android.view.GestureDetector.SimpleOnGestureListener；android.view.GestureDetector 构造方法）
针对本应用要查的：
- 源端是否改过 GestureDetector 的默认路径：源工程里构造 GestureDetector 的 Java/Kotlin 代码，找 setIsLongpressEnabled、setOnDoubleTapListener 的调用；setIsLongpressEnabled(false) 时契约里去掉长按条件；setOnDoubleTapListener(null) 时去掉双击条件；没调用就按默认全写
未核实：设备的资源 overlay 可以改触摸容差和抛掷速度，这里写的是框架默认值
来源：1 张卡，1 个应用
- case-a1849836a1bfff3c265c（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
