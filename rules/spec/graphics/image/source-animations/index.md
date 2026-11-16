# 源端动画（AnimatedImageVector 形变、多组 Animator 分支）

agent 会看到什么：读到 Compose 用 AnimatedImageVector.animatedVectorResource 加 rememberAnimatedVectorPainter(icon, atEnd) 做两态形变，或窗口类里定义多组 Animator、触摸回调里 cancel() 主动画改播另一个；规格写「图标态切换即可」，或行为笔记只记主时序、手势分支没有自己的时长

## 规矩

- rule-5c77c09e9017｜源端 AnimatedImageVector 两态形变，规格写成 parity 要求并给插值路线，不写图标态切换｜读到：源 Compose 用 AnimatedImageVector.animatedVectorResource(R.drawable.…) 加 rememberAnimatedVectorPainter(icon, atEnd)，atEnd 随状态变化；写错：转换决策表写「矢量动画无直接等价，图标态切换即可满足」「SymbolGlyph 切换或 ImageAnimator 序列帧」，没有决策 ID；结构段、映射表和 AC 对这个动画说法不一致
- rule-f00b3b2516f9｜行为提取时列出窗口类里每个 Animator 的触发分支和时长，不把手势分支概括成上滑收起｜读到：源窗口类 getView 里定义多组 Animator，各自 setDuration(...)；触摸回调里上滑超过阈值时 cancel() 主动画、只播另一个 Animator；写错：行为笔记只记主时序「入场 … ms、停留 … ms、出场 … ms」，手势分支只写「上滑超过 …dp 收起」，没有它自己的时长
- rule-6e9179f6dff2｜规格转写 Animator 时写明生效的插值器和来源，映射到 Curve 时注明是否等价｜读到：源码 ValueAnimator.ofFloat / ObjectAnimator 设了时长，没有 setInterpolator（或显式设了某个插值器）；写错：转换决策只写「ValueAnimator(0→1, 50ms) → animateTo 驱动」，没写插值器；或者写成「线性（默认插值器）」；或者把 AccelerateDecelerate 直接对成 Curve.EaseInOut 不加说明
- rule-2489789e879e｜应用侧 Configuration 常量引用库的动画资源时，映射行写出动画的时长和插值器｜读到：应用侧 Style / Configuration 常量类里有 Configuration.Builder().setInAnimation(R.animator.…).setOutAnimation(R.animator.…)；写错：映射行把常量类当作完整的样式锚点，只写配色和时长常量，没写进出动画资源的实际时长和插值器
