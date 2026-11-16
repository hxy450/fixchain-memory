# ValueAnimator 没设插值器时，帧循环进度套 AccelerateDecelerate 公式

审的是：代码
触发（任一种）：
- 读到：ValueAnimator.ofFloat / ObjectAnimator 设了 setDuration、addUpdateListener，animatedValue 直接写进绘制用的进度字段，全文没有 setInterpolator；写错的样子：自驱帧循环里进度直接取 Math.min(1, (now - start) / duration) 这个时间分数，注释标「线性」，没有套插值函数
适用范围：安卓 ValueAnimator / ObjectAnimator 驱动的逐帧进度，迁成目标端自驱帧循环时
不适用的情形：源码显式用 LinearInterpolator 或 setInterpolator(null) 时才写成线性
做法：
- 进度写成 t = Math.min(1, (now - start) / duration)；progress = Math.cos((t + 1) * Math.PI) / 2 + 0.5，注释写明插值来自框架默认还是显式设置
- 源码里每个 ValueAnimator / ObjectAnimator 创建点都逐一对应到目标端的帧循环核对，共用同一个插值函数的都要真的接入
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- private static final TimeInterpolator sDefaultInterpolator = new AccelerateDecelerateInterpolator(); mInterpolator 初值就是它：不调 setInterpolator 时用 AccelerateDecelerate（出处：android.animation.ValueAnimator#sDefaultInterpolator）
- getInterpolation(input) = (float)(Math.cos((input + 1) * Math.PI) / 2.0f) + 0.5f：默认插值器的公式，目标端照写（出处：android.view.animation.AccelerateDecelerateInterpolator#getInterpolation）
- setInterpolator(null) 时 mInterpolator = new LinearInterpolator()：只有显式传 null 或 LinearInterpolator 才是线性（出处：android.animation.ValueAnimator#setInterpolator）
- progress = accelerateDecelerate(min(1, 经过时间 / 时长))，写成 Math.fround(Math.fround(Math.cos((t + 1) * Math.PI) / 2) + 0.5)：返修后采用的写法，fround 对齐 Java float 精度（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-cfbbc44d6d4ed0b9c289（Sokoban）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 3；例外 1 ← 建议 1；取值 4 ← 诊断
