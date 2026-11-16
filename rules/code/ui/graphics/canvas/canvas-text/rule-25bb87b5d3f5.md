# 代码按 getTextBounds 算文字高度时，写 actualBoundingBox 两项各自 Math.ceil

审的是：代码
触发（任一种）：
- 读到：源端 Paint.getTextBounds(text, start, end, rect) 后用 rect.height() 作文字高度；写错的样子：目标写成 Math.trunc(m.fontBoundingBoxAscent + m.fontBoundingBoxDescent)，或带着「需实测 hhea」注释保留 fontBoundingBox*
适用范围：渲染实现阶段用 CanvasRenderingContext2D.measureText 复刻源端文字行高、行距时，textBaseline 为默认 alphabetic
做法：
- const m = ctx.measureText(text.substring(start, end))；高度写 Math.ceil(m.actualBoundingBoxAscent) + Math.ceil(m.actualBoundingBoxDescent)
- 规格或经验只给「候选字段 + 待实测」时，按 d.ts 里各字段的注释和源 API 语义选字段，在交回报告里标注与规格的差异，不拿「待实测」当保留错误候选的理由
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- measureText(text: string): TextMetrics：CanvasRenderer 上的测量方法，CanvasRenderingContext2D、OffscreenCanvasRenderingContext2D 都继承（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderer.measureText）
- actualBoundingBoxAscent / actualBoundingBoxDescent：到渲染文字矩形边界顶部 / 底部的距离：墨迹级，对应 getTextBounds（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，TextMetrics.actualBoundingBoxAscent）
- textBaseline 默认 alphabetic：actualBoundingBox* 从这条基线量起，与 getTextBounds 以基线为原点一致（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderer.textBaseline）
- 改为 Math.ceil(actualBoundingBoxAscent) + Math.ceil(actualBoundingBoxDescent) 后，同字号下文字高度与安卓分组一致：修复后的观察（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-dcca102a6a4baff0e7a7（Blockinger）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
