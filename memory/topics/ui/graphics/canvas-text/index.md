# ui/graphics/canvas-text

Canvas 文字绘制：字体串与注册就绪、TextMetrics 度量字段选取、段落方向与基线取整

[上一级](../index.md)

## 本级经验

- [Paint 状态读回改为自记，不读 ctx 属性](lesson-c91afa108d966666d22b.lesson.md) · 阶段：spec/execute · 信号：Paint.getTextSize, getTextSize, getTextAlign, ctx.font
- [fillText 按串首强方向字符设 direction](lesson-68717b80482f4bd12825.lesson.md) · 阶段：spec/execute · 信号：Canvas.drawText, drawText, fillText, ctx.direction
- [字体串用注册名不加引号，测宽前等字体就绪](lesson-74295d12b4edc025569f.lesson.md) · 阶段：spec/execute · 信号：ctx.font, font.registerFont, registerFont, Typeface.createFromAsset
- [文字度量按源 API 分层选 TextMetrics 字段](lesson-f876887b216b6caf9f39.lesson.md) · 阶段：spec/execute · 信号：getTextBounds, Paint.ascent, getFontMetrics, measureText
