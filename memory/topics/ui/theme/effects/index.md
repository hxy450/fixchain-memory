# ui/theme/effects

渲染效果换算：阴影 px 单位、模糊边缘、blendMode 离屏范围、渐变端点几何与角度、渐变描边与背景分支。

[上一级](../index.md)

## 本级经验

- [Brush 渐变描边用外层渐变加内衬实底实现](lesson-5d56afe5595bb26eaf2f.lesson.md) · 阶段：execute · 信号：Modifier.border, Brush.linearGradient, Surface, linearGradient
- [Brush 渐变转 linearGradient 并解析色序](lesson-46805f8bf5da7b0c914b.lesson.md) · 阶段：execute · 信号：Brush.horizontalGradient, linearGradient, GradientDirection.Right, Surface
- [blendMode 着色把底色字形渐变放同一离屏组](lesson-3024193e4816229c5370.lesson.md) · 阶段：spec/execute/repair · 信号：blendMode, BlendApplyType, drawWithContent, BlendMode.Plus
- [blur 半径先确认 vp 单位，模糊层放大后裁边](lesson-6be3938453498c25e9a5.lesson.md) · 阶段：execute · 信号：Modifier.blur, BlurredEdgeTreatment, vp2px
- [elevation 阴影按 vp2px 换算并集中到共享函数](lesson-d0aad947e26220fb43fa.lesson.md) · 阶段：spec/execute/converge · 信号：ShadowOptions, Modifier.shadow, vp2px, .shadow(
- [渐变端点几何换算成 linearGradient 角度与色标](lesson-4ce3a1c186651285f362.lesson.md) · 阶段：execute · 信号：Brush.linearGradient, horizontalGradient, TileMode.Mirror, linearGradient
- [背景对象逐分支迁：url 用图片，否则按色数生成纯色或渐变](lesson-2dc88a09f6cfbbe3393c.lesson.md) · 阶段：execute · 信号：orientation, linearGradient, backgroundImage, backgroundColor
