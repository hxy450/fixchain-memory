# ui/layout/intrinsic

由内容、位图比例或库内部规则决定的尺寸：wrap_content、固有高度与宽高比不用百分比或估值代替。

[上一级](../index.md)

## 本级经验

- [IntrinsicSize.Min 行先算固有高度写显式值](lesson-cb1a12afca61db08ed9a.lesson.md) · 阶段：execute · 信号：IntrinsicSize.Min, fillMaxHeight, align(Top), padding(top)
- [Material 按钮区分布局占位、背景实绘与触控范围](lesson-b73a1ac8908f74856a02.lesson.md) · 阶段：spec/execute · 信号：minimumInteractiveComponentSize, IconButton, Surface, Box
- [图片盒尺寸与盒内缩放分开，高度用位图像素比](lesson-624248be2c5f81082268.lesson.md) · 阶段：execute · 信号：adjustViewBounds, layout_constrainedWidth, aspectRatio, constraintSize
- [并排图片列按固有宽比例分列高度用 aspectRatio](lesson-0618cdf331560d389f0e.lesson.md) · 阶段：execute/repair · 信号：aspectRatio, wrap_content, Blank().layoutWeight(1), layoutWeight
- [步进器居中子项组不给中间项 layoutWeight(1)](lesson-02b2fcd7d157d97f95c8.lesson.md) · 阶段：execute · 信号：gravity=center, FlexAlign.Center, wrap_content, justifyContent
- [贴合内容的描边背景写在内容节点不用 100% 覆盖层](lesson-a58ebfe7a4c55b041b14.lesson.md) · 阶段：spec/execute · 信号：matchContentSize, fillMaxSize, Modifier.border, HitTestMode.None
- [跨列卡片同行等高按列宽留边推 aspectRatio](lesson-4fc212d401ac7b2a4218.lesson.md) · 阶段：execute · 信号：aspectRatio, onAreaChange, GridItem, Grid
