# 从自绘角标推导无数字红点尺寸时，按实际计数分支的绘制半径求直径

审的是：代码
触发（任一种）：
- 读到：源端自定义 View 用计数切换无数字红点和带数字角标（计数为 0 是红点），尺寸由 dp 半径基数、计数分支和 DisplayMetrics.density 分支算出，onDraw 里 canvas.drawCircle(cx, cy, radius, paint)；写错的样子：目标端红点写成 Circle().width(16).height(16) 这类：把半径基数乘 2、或带数字角标分支的高度当成无数字红点的直径，和承载它的入口相比明显过大
适用范围：把安卓自定义角标 / 红点 View 迁成 ArkUI 固定尺寸的 Circle 等组件时
做法：
- 先看调用处传的计数确定走哪个分支（计数为 0 即无数字），再找该分支的尺寸函数和 drawCircle 实际用的半径（如 半径 = 宽 / 2），直径 = 2 × 该半径
- 有屏幕密度分支时取对应分支的 dp 值，dp 数值照写成 vp：Circle().width(D).height(D)；写完和承载入口的尺寸对照，明显过大时回头查分支
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- drawCircle(float cx, float cy, float radius, Paint paint)：radius 是半径，直径是它的两倍（出处：android.graphics.Canvas#drawCircle）
- DisplayMetrics.density：dp 的缩放系数，约 160dpi 屏上为 1：源端 dp × density 得到 px；目标端 vp 与 dp 同为密度无关单位（出处：android.util.DisplayMetrics#density）
- CircleOptions 的 width、height 类型 Length，默认 0，默认单位 vp：Circle 的宽高直接写 vp 数值（出处：鸿蒙 SDK 的 ets/component/circle.d.ts，CircleOptions；ts-drawing-components-circle.md，CircleOptions）
- Circle 宽高设置不一致时以短边为直径：红点宽高写成同一个直径（出处：ts-drawing-components-circle.md，示例）
- 按半径基数 ×2 写出的红点约为无数字分支直径的两倍，用户截图反馈过大：要用无数字分支的实际绘制半径（出处：卡里修好并验证过）
针对本应用要查的：
- 无数字红点的直径：源工程里角标 View 类：计数为 0 时调用的尺寸函数、其中按 DisplayMetrics.density 区分的分支，以及 onDraw 里 drawCircle 的半径参数；读出该分支的半径 dp 值，×2 为直径 dp，照写成 vp；有密度分支时写明取的是哪一支
来源：1 张卡，1 个应用
- case-3ed128d1dc80288ed29a（两步路）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2；取值 5 ← 诊断
