# ui/graphics/drawing

Canvas 自绘的移植：坐标原点共用、自适应公式的参照常量、共享绘制分支的统一规则与被注释绑定的静态化。

[上一级](../index.md)

## 本级经验

- [Adapter 注释掉的绑定按未启用，只按 XML 静态属性](lesson-cd87ec49e06af8e6459a.lesson.md) · 阶段：execute · 信号：Adapter, onBindViewHolder, maxTop, minTop
- [共享绘制分支按源端通用规则统一修，不写单 key 特判](lesson-17d6e4c04764983be25a.lesson.md) · 阶段：repair · 信号：drawBars, STROKE, FILL_AND_STROKE, strokeWidth
- [反复 render 的画布每帧先清屏](lesson-351ce34d3ebe51b8ff8e.lesson.md) · 阶段：execute · 信号：clearRect, onDraw, render(), CanvasRenderingContext2D
- [折线点与标签共用原点，点坐标含留白时不再加 position](lesson-dca31bed776aaf7cb328.lesson.md) · 阶段：execute · 信号：valToY, ItemDecoration, Polyline, paddingTop
- [按 px 公式移植画布时用 PX 构造上下文](lesson-7083c6ad69ab19ad17dd.lesson.md) · 阶段：spec/execute · 信号：LengthMetricsUnit.PX, CanvasRenderingContext2D, measureText, Paint.setTextSize
- [烘焙位图改每帧绘制时状态留快照、按比例缩放](lesson-046c8bbb304684669060.lesson.md) · 阶段：execute · 信号：onSizeChanged, Bitmap, onDraw, setBounds
- [自绘红点按实际分支取尺寸，半径换直径](lesson-99fe69fc59afa886750d.lesson.md) · 阶段：execute/repair · 信号：BadgeView, setBadgeCount, drawCircle, Circle
- [自适应尺寸公式的参照基数写成独立常量不替换](lesson-f395cbdf6742a7f4c761.lesson.md) · 阶段：execute · 信号：referenceCellHeight, contentHeight / 6, Canvas, onDraw
- [预缩放位图在 PixelMap 上按同一采样缩放](lesson-c3bd9c8b2f24c209a659.lesson.md) · 阶段：spec/execute · 信号：BitmapFactory.decodeResource, createScaledBitmap, drawBitmap, drawImage
