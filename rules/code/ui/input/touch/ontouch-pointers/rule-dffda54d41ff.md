# 源端用 ScaleGestureDetector 缩放时，用 onTouch 逐事件移植 span 和门槛

审的是：代码
触发（任一种）：
- 读到：源端（含三方库里的缩放图片控件）用 `ScaleGestureDetector` 的 `onScale` / `getScaleFactor` 缩放；写错的样子：目标用 `PinchGesture` 按 `event.scale` 直接缩放、`PanGesture` 识别后再补偿位移，没有源端的 span slop 门槛
- 读到：源端 new ScaleGestureDetector(…, OnScaleGestureListener)，覆写 onScaleBegin / onScale；写错的样子：目标捏合状态机只在指针按下、抬起时推进，MOVE 里要缩放已开始才算比例，两指按下后移动永远进不了缩放；没有最小跨度，没有 quick scale
适用范围：把带缩放的图片或画廊控件迁到 ArkUI、要求缩放行为和源端一致时
做法：
- 用 .onTouch 按 ScaleGestureDetector#onTouchEvent 逐段移植：每个事件都算焦点和两指到中心的平均距离 span；未开始且 span >= minSpan 且 |span − initialSpan| > spanSlop 时（在 MOVE 中判断）调 onScaleBegin，之后每帧缩放比 = 当前 span / 上一帧 span；进行中 span < minSpan 或指针增减时 onScaleEnd
- 映射参考里「ScaleGestureDetector → PinchGesture」只当组件候选，不按 event.scale 直接缩放
- 源端 targetSdk > 18 时开 quick scale：双击后按住拖动，以第一次按下点为焦点、按 Y 方向跨度缩放，期间不平移
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- spanSlop = ViewConfiguration.getScaledTouchSlop() * 2；minSpan = getScaledMinimumScalingSpan()：ScaleGestureDetector 公开构造时的两个门槛（出处：android.view.ScaleGestureDetector#ScaleGestureDetector(Context, OnScaleGestureListener, Handler)）
- if (!mInProgress && span >= minSpan && (wasInProgress || Math.abs(span - mInitialSpan) > mSpanSlop)) mInProgress = mListener.onScaleBegin(this)：源端开始缩放的条件（出处：android.view.ScaleGestureDetector#onTouchEvent）
- if (!inAnchoredScaleMode() && mInProgress && (span < mMinSpan || configChanged)) onScaleEnd：跨度小于最小跨度或指针增减时结束（出处：android.view.ScaleGestureDetector#onTouchEvent）
- config_viewConfigurationTouchSlop = 8dp；config_minScalingSpan = 27mm：两个阈值的平台默认尺寸，按目标密度换算（出处：Android SDK 平台资源 data/res/values/config.xml，config_viewConfigurationTouchSlop、config_minScalingSpan（按应用的 compileSdk 取对应平台））
- targetSdkVersion > Build.VERSION_CODES.JELLY_BEAN_MR2 时 setQuickScaleEnabled(true)；锚定模式下焦点固定在双击开始处、span 取 spanY：quick scale 的开启条件和焦点（出处：android.view.ScaleGestureDetector#ScaleGestureDetector；android.view.ScaleGestureDetector#onTouchEvent）
- PinchGesture 的 distance 是最小识别距离，单位 vp，默认 5：识别器的门槛和源端 span slop 定义、取值都不同（出处：ts-basic-gestures-pinchgesture.md，PinchGesture）
- TouchEvent.touches：全部屏幕触点，每个元素是一个触点：两指 span 从这里算（出处：ts-universal-events-touch.md，TouchEvent）
针对本应用要查的：
- quick scale 是否默认开：源工程模块级 Gradle 构建脚本（或 AndroidManifest）里的 targetSdk；大于 18 就开
未核实：case-1a09dd649093f650a6fc 只记了返修第 2 轮改为逐事件移植，没写上机对比结果；case-1a09dd649093f650a6fc 的环境是 API 24，本机按 API 23 的文档核实
来源：2 张卡，2 个应用
- case-1a09dd649093f650a6fc（omni-notes-hmos）：做法第 1 步 ← 诊断、建议 2；做法第 2 步 ← 建议 3、诊断
- case-c576f74cc60bac7ba886（Sokoban）：做法第 1 步 ← 建议 1、建议 2；做法第 3 步 ← 建议 1、建议 2
