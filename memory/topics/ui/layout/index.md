# ui/layout

页面几何：子项如何定位、取尺寸、滚动与叠放，以及全屏窗口下安全区的测量与避让归属。

[上一级](../index.md)

## 子主题

- [constraints](constraints/index.md) — 锚点与对齐语义的转换：源端默认对齐与锚点落到 Column/Row/Stack/RelativeContainer。（5 条）
- [intrinsic](intrinsic/index.md) — 由内容、位图比例或库内部规则决定的尺寸：wrap_content、固有高度与宽高比不用百分比或估值代替。（7 条）
- [layers](layers/index.md) — 页面骨架与叠放层按运行时真实结构落定：运行时挂载、重叠子视图、gone 节点不按 XML 占位定几何。（5 条）
- [safearea](safearea/index.md) — 全屏窗口安全区：避让值单位、expandSafeArea 与前景 padding 之别、inset 只消费一次及承载层（9 条）
- [scrolling](scrolling/index.md) — 滚动容器的包含范围、交叉轴尺寸、首尾留白与高度上限，以及 Scroll 内嵌套内容的测高与滚动归属。（7 条）
- [sizing](sizing/index.md) — 满铺、剩余空间与边距内距的尺寸公式及单位域：百分比、layoutWeight、calc 与 px/vp 取舍。（7 条）
