# ui/layout

页面几何：子项如何定位、取尺寸、滚动与叠放，以及全屏窗口下安全区的测量与避让归属。

[上一级](../index.md)

## 子主题

- [constraints](constraints/index.md) — 锚点与对齐语义的转换：源端默认对齐与锚点落到 Column/Row/Stack/RelativeContainer。（6 条）
- [immersion](immersion/index.md) — 安全区沉浸：是否全屏、系统栏底色与避让带由哪一层承担（5 条）
- [insets](insets/index.md) — 系统栏与软键盘避让值的取值、单位与只消费一次（7 条）
- [intrinsic](intrinsic/index.md) — 由内容、位图比例或库内部规则决定的尺寸：wrap_content、固有高度与宽高比不用百分比或估值代替。（9 条）
- [layers](layers/index.md) — 页面骨架与叠放层按运行时真实结构落定：运行时挂载、重叠子视图、gone 节点不按 XML 占位定几何。（7 条）
- [scrolling](scrolling/index.md) — 滚动容器的包含范围、交叉轴尺寸、首尾留白与高度上限，以及 Scroll 内嵌套内容的测高与滚动归属。（10 条）
- [sizing](sizing/index.md) — 满铺、剩余空间与边距内距的尺寸公式及单位域：百分比、layoutWeight、calc 与 px/vp 取舍。（12 条）
- [variants](variants/index.md) — 布局方向与限定词变体：supportsRtl、land、swNdp 按窗口条件分支（3 条）
