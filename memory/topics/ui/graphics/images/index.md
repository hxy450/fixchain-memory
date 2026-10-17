# ui/graphics/images

背景图与图片组件的缩放、形状裁剪与分层落地：layer-list 逐层、整屏位图拉伸、自定义图片组件与兜底预览。

[上一级](../index.md)

## 本级经验

- [layer-list 背景按生效 flavor 逐层落组件](lesson-0da8733ee0a6c52924da.lesson.md) · 阶段：execute · 信号：layer-list, sourceSet, ImageFit.Fill, $r
- [整屏背景位图用 ImageFit.Fill 不默认裁切](lesson-7708f650eb4b55dce045.lesson.md) · 阶段：spec/execute · 信号：android:background, ImageFit.Fill, ImageFit.Cover, scaleType
- [无来源兜底预览不加源端没有的边框选中态装饰](lesson-c8909c3cb5f925913407.lesson.md) · 阶段：execute/repair · 信号：borderWidth, FrameLayout, placeholder
- [自定义图片组件先读定义：圆形裁剪译 Cover 加圆角](lesson-9dcd69d2824702310959.lesson.md) · 阶段：execute/repair · 信号：CircleShape, ContentScale.Crop, ImageFit.Cover, borderRadius
