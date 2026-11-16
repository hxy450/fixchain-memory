# Paint.ascent/descent 算基线偏移时，目标取 emHeightAscent/Descent

审的是：代码
触发（任一种）：
- 读到：安卓自绘 View 用 `Paint.ascent()` / `Paint.descent()`（主字体的字体级上下伸，ascent 为负）算文字垂直居中的基线偏移，如 `(descent() + ascent()) / 2`；写错的样子：目标里写成 `fontBoundingBoxDescent - fontBoundingBoxAscent` 或用 actualBoundingBoxAscent/Descent 代替，注释称与源式同值
适用范围：安卓 Paint 字体度量做 Canvas 文字基线修正，迁成 ArkUI CanvasRenderingContext2D.measureText 时（卡里在注册了自定义 ttf 字体的情形下验证）
做法：
- const m = ctx.measureText(text)；偏移写成 (m.emHeightDescent - m.emHeightAscent) / 2，对应源端 (descent() + ascent()) / 2（emHeightAscent 是正的上方距离，所以相减）
- 不用 fontBoundingBoxAscent/Descent：卡里实测它的 descent 取的是字体外框 head.yMin，不是 hhea 下伸，偏移偏小、文字偏上；也不用 actualBoundingBox*（字形墨迹级）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- measureText(text: string): TextMetrics：画布上下文测文字度量，CanvasRenderingContext2D 和 OffscreenCanvasRenderingContext2D 都从 CanvasRenderer 继承（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderer.measureText）
- readonly emHeightAscent: number / readonly emHeightDescent: number：从 textBaseline 指示的线到 em 框顶 / 底的距离（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，TextMetrics.emHeightAscent、TextMetrics.emHeightDescent）
- readonly fontBoundingBoxDescent: number：按声明是到「所有字体渲染文字的矩形边界」底部的距离，即字体外框，不是 hhea 下伸（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，TextMetrics.fontBoundingBoxDescent）
- readonly actualBoundingBoxAscent: number：到实际渲染文字矩形边界顶部的距离，随字形墨迹变，不是字体级度量（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，TextMetrics.actualBoundingBoxAscent）
- public float ascent() / public float descent()：ascent 是基线上方的距离（负值），descent 是基线下方的距离（正值），都按主字体和字号算（出处：android.graphics.Paint#ascent、android.graphics.Paint#descent）
- emHeightAscent / emHeightDescent 等于字体 hhea ascender / descender × 字号 ÷ unitsPerEm；fontBoundingBoxDescent 等于 head.yMin × 字号 ÷ unitsPerEm：插桩实测的对应关系，换成 emHeight* 后文字墨迹中心与安卓一致（出处：卡里修好并验证过）
针对本应用要查的：
- 目标字体的 hhea ascender、descender 和 head.unitsPerEm：目标工程里注册给画布用的字体文件（.ttf/.otf）的 hhea 表和 head 表；ascender × 字号 ÷ unitsPerEm 应等于 emHeightAscent，descender 的绝对值同理；作为注释里写明的依据
未核实：只在一种注册的自定义字体上实测过；系统默认字体下 emHeight* 是否也等于 hhea 上下伸没有核实
来源：1 张卡，1 个应用
- case-5e1beaa11de7eb15fa6e（2048）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断、建议 1；取值 6 ← 诊断
