# 规格转写 Animator 时写明生效的插值器和来源，映射到 Curve 时注明是否等价

审的是：规格
触发（任一种）：
- 读到：源码 ValueAnimator.ofFloat / ObjectAnimator 设了时长，没有 setInterpolator（或显式设了某个插值器）；写错的样子：转换决策只写「ValueAnimator(0→1, 50ms) → animateTo 驱动」，没写插值器；或者写成「线性（默认插值器）」；或者把 AccelerateDecelerate 直接对成 Curve.EaseInOut 不加说明
适用范围：规格里转写源端 ValueAnimator / ObjectAnimator 的转换决策那一项
做法：
- 转换决策写成「时长 N ms；插值器 AccelerateDecelerateInterpolator（框架默认，源码未调 setInterpolator）」，显式设置的写类名并注明「显式设置」
- 映射到 animateTo / Curve 时注明：Curve.EaseInOut 是三次贝塞尔，和 AccelerateDecelerate 的余弦曲线不等价；要求一比一时写出公式 cos((t+1)π)/2 + 0.5
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- sDefaultInterpolator = new AccelerateDecelerateInterpolator()：源端不调 setInterpolator 时生效的插值器（出处：android.animation.ValueAnimator#sDefaultInterpolator）
- getInterpolation(input) = cos((input + 1)π) / 2 + 0.5：规格里要一比一时写的公式（出处：android.view.animation.AccelerateDecelerateInterpolator#getInterpolation）
- Curve.EaseInOut：CubicBezier(0.42, 0.0, 0.78, 1.0)：声明写的贝塞尔参数，不是余弦曲线（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，Curve.EaseInOut）
来源：1 张卡，1 个应用
- case-cfbbc44d6d4ed0b9c289（Sokoban）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
