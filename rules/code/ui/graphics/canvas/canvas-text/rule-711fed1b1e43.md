# Paint 状态读回迁到 ArkUI Canvas 时自己记字号和对齐，不读 ctx.font

审的是：代码
触发（任一种）：
- 读到：源端绘制函数从 Paint 读回状态：paint.getTextAlign()、paint.getTextSize()，再据此算文字底衬的位置和大小；写错的样子：目标端读取 ctx.font、ctx.textAlign（如从 ctx.font 解析字号的辅助函数、按 ctx.textAlign 分支）；运行时读到 undefined 抛 TypeError，编译照样通过
适用范围：把安卓 Paint 的有状态读写迁成 ArkUI CanvasRenderingContext2D 时
做法：
- 在组件里封装 setFont(px)、setTextAlign(align)：赋值 ctx.font / ctx.textAlign 的同时把当前字号和对齐存进自己的字段（如 curFontPx、curTextAlign），绘制逻辑只读这些字段
- 文字高度用 const m = ctx.measureText(text) 的 m.actualBoundingBoxAscent + m.actualBoundingBoxDescent
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- font：只写属性，可以赋值，读取返回 undefined：不能从上下文读回字号（出处：ts-canvasrenderingcontext2d.md，font）
- textAlign：只写属性，读取返回 undefined：不能从上下文读回对齐（出处：ts-canvasrenderingcontext2d.md，textAlign）
- textBaseline：只写属性，读取返回 undefined：同族：上下文的其他绘制状态（fillStyle、lineWidth、globalAlpha 等）文档也写明只写（出处：ts-canvasrenderingcontext2d.md，textBaseline）
- measureText(text: string): TextMetrics：测量文字（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderer.measureText）
- readonly actualBoundingBoxAscent: number；readonly actualBoundingBoxDescent: number：textBaseline 所指水平线到文字矩形上沿、下沿的距离（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，TextMetrics.actualBoundingBoxAscent / actualBoundingBoxDescent）
- 读回 ctx.font 得到 undefined，在模拟器上 jscrash；改成 setFont/setTextAlign 加 curFontPx/curTextAlign 后正常：验证过的写法（出处：卡里修好并验证过）
未核实：卡里的行为出自模拟器 6.1.0.126 和 HarmonyOS 6.1.1（API 24）环境，本机声明是 API 23
来源：1 张卡，1 个应用
- case-0543bbad1d6bc5c2cfde（opencamera-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 6 ← 诊断
