# 自绘画布的规格只写一份单位契约，写明上下文构造和各量的单位

审的是：规格
触发（任一种）：
- 读到：安卓自定义 View 在 onSizeChanged 的 int px 尺寸上推导布局，Paint.setTextSize / measureText 按 px 算字号和间距；写错的样子：规格里画布单位的说法不止一处且互相矛盾（字体串写 px、坐标映射写 vp），或者没写 CanvasRenderingContext2D 用哪个构造、默认按什么单位
适用范围：把安卓自绘 View 迁成 ArkUI Canvas 时，规格里写画布单位的那一节
做法：
- 规格里只写一份画布单位契约：上下文怎么构造（new CanvasRenderingContext2D(settings) 按默认 vp，或 new CanvasRenderingContext2D(settings, LengthMetricsUnit.PX) 按 px），以及字体串后缀、measureText 结果、ctx.width、触点坐标、窗口避让值和 dp 常量各自的单位
- 各功能的映射表都引用这一份契约，不各写各的单位
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- constructor(settings?: RenderingContextSettings, unit?: LengthMetricsUnit)：CanvasRenderingContext2D 的构造，第二个参数定单位（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderingContext2D.constructor）
- LengthMetricsUnit.DEFAULT = 0（vp）、LengthMetricsUnit.PX = 1：单位模式的两个取值，DEFAULT 是 vp（出处：鸿蒙 SDK 的 ets/api/arkui/Graphics.d.ts，LengthMetricsUnit）
- 默认构造的上下文按 vp 解释字号和坐标；改成 LengthMetricsUnit.PX 构造后字号、测宽、几何、触点与安卓 View/Paint 同为 px：契约里写哪种构造，决定了其余各量要不要换算（出处：卡里修好并验证过）
- constructor(width: number, height: number, settings?: RenderingContextSettings, unit?: LengthMetricsUnit)：同族接口：OffscreenCanvasRenderingContext2D 的构造，同样用 unit 定单位（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，OffscreenCanvasRenderingContext2D.constructor）
- constructor(width: number, height: number, unit: LengthMetricsUnit)：同族接口：OffscreenCanvas 的构造（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，OffscreenCanvas.constructor）
- constructor(unit?: LengthMetricsUnit)：同族接口：DrawingRenderingContext 的构造（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，DrawingRenderingContext.constructor）
来源：1 张卡，1 个应用
- case-caa0a4c6289286b0e6ba（2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 3 ← 诊断
