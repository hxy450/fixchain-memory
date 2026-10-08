# ui/graphics/drawing

Canvas 自绘的移植：坐标原点共用、自适应公式的参照常量、共享绘制分支的统一规则与被注释绑定的静态化。

[上一级](../index.md)

## 本级经验

- [Adapter 注释掉的绑定按未启用，只按 XML 静态属性](lesson-cd87ec49e06af8e6459a.lesson.md) · 阶段：execute · 信号：Adapter, onBindViewHolder, maxTop, minTop
- [共享绘制分支按源端通用规则统一修，不写单 key 特判](lesson-17d6e4c04764983be25a.lesson.md) · 阶段：repair · 信号：drawBars, STROKE, FILL_AND_STROKE, strokeWidth
- [折线点与标签共用原点，点坐标含留白时不再加 position](lesson-dca31bed776aaf7cb328.lesson.md) · 阶段：execute · 信号：valToY, ItemDecoration, Polyline, paddingTop
- [自适应尺寸公式的参照基数写成独立常量不替换](lesson-f395cbdf6742a7f4c761.lesson.md) · 阶段：execute · 信号：referenceCellHeight, contentHeight / 6, Canvas, onDraw
