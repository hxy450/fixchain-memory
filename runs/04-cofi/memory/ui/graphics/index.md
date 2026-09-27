# ui/graphics

图标与图形资源：动画矢量的状态帧、系统符号替代、资源迁移中的静态化标注

[上一级](../index.md)

## 本级经验

- [AnimatedImageVector/animated-vector 按状态分别给出起点帧和终点帧；同名静态 SVG 只是起始帧](lesson-e6b1f9094ec3b905cab5.lesson.md)
  - 时机：界面实现阶段转换 AnimatedImageVector/animated-vector 图标、决定各状态显示哪一帧时；以及资源迁移阶段遇到 animated-vector 时
  - 情境：源码用 rememberAnimatedVectorPainter(icon, atEnd)，atEnd 由完成、运行等状态决定；目标资源目录里的同名媒体是资源迁移从 animated-vector 起始帧导出的静态 SVG；页面规格允许资源动画或等价符号，并要求保持可见的状态切换。
