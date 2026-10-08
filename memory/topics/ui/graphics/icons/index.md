# ui/graphics/icons

图标资源的选取与显示：原图复制不以近名替代、固有 dp 与触摸盒分离、场景变体映射、动画矢量帧与 Lottie 接入。

[上一级](../index.md)

## 本级经验

- [Lottie 动画层接 @ohos/lottie 不换静态图](lesson-ea55fe23fea47c1cfca3.lesson.md) · 阶段：execute · 信号：LottieAnimationView, @ohos/lottie, setAnimation, oh-package.json5
- [animated-vector 按状态给出起点帧和终点帧两图](lesson-e6b1f9094ec3b905cab5.lesson.md) · 阶段：execute · 信号：rememberAnimatedVectorPainter, AnimatedImageVector, animated-vector, atEnd
- [图标按资源固有 dp 显示，触摸盒放外层不设成盒尺寸](lesson-bdc493f5950835f9bfcc.lesson.md) · 阶段：execute · 信号：centerInside, ImageFit.Contain, wrap_content, drawableLeft
- [图标用源端原图，缺失从 drawable 密度目录复制不替代](lesson-943544ce27bf04f9faf8.lesson.md) · 阶段：execute/repair · 信号：does not have a base resource, drawable-xxhdpi, SymbolGlyph, $r('app.media
- [编码到资源的多变体映射按取值字段拆分不合一](lesson-c65e8e59008a5e31bcad.lesson.md) · 阶段：execute/repair · 信号：iconEx, bgEx, icon2Ex, setBackgroundResource
