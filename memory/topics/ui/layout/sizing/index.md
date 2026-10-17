# ui/layout/sizing

满铺、剩余空间与边距内距的尺寸公式及单位域：百分比、layoutWeight、calc 与 px/vp 取舍。

[上一级](../index.md)

## 本级经验

- [fillMaxWidth 先占满剩余宽，后续兄弟按实得宽判断](lesson-45f77b3088fa69398f9e.lesson.md) · 阶段：spec/execute · 信号：fillMaxWidth, requiredWidth, Visibility.Hidden, layoutWeight(1)
- [fragment 根 padding 只由宿主或组件一方实现](lesson-8a7d25959b954ffb9215.lesson.md) · 阶段：execute · 信号：LinearLayout, TabContent, ViewPager
- [weightSum 与权重和不等时按源算法分余量](lesson-adad817f2c3c8f1eaa09.lesson.md) · 阶段：spec/execute · 信号：weightSum, layout_weight, layoutWeight, flexGrow
- [定宽兄弟后的多行 Text 加 flexShrink(1)](lesson-8566839cffc9e9e7fa30.lesson.md) · 阶段：execute · 信号：flexShrink(1), layoutWeight(1), layout-land, wrap_content
- [带同轴 margin 的 100% 改容器 padding](lesson-75f4743dff663f50966b.lesson.md) · 阶段：execute · 信号：layout_marginHorizontal, showAsDropDown, PopupWindow, calc(100%
- [整数 px 公式在 px 域取整再 px2vp 写入属性](lesson-0ef2cd00e1a91491b350.lesson.md) · 阶段：spec/execute · 信号：px2vp, vp2px, measureText, onAreaChange
- [方向边距用 end 时各边统一 LengthMetrics](lesson-e3077bf60cfc3f34d0a2.lesson.md) · 阶段：execute · 信号：LengthMetrics, layout_marginStart, layout_marginEnd, @kit.ArkUI
- [权重槽可能小于 padding 时不放在 Image 上](lesson-8c5e3ea6e2c4ff7e8478.lesson.md) · 阶段：execute · 信号：layout_weight, ImageView, FIT_CENTER, layoutWeight
- [槽位子项搬进 Row 改等分权重，不留 100%](lesson-c572346f0be19acf5579.lesson.md) · 阶段：execute · 信号：layoutWeight(1), width('100%'), BarMode.Fixed, LayoutParams
- [移进 Refresh 的内容根节点改用显式高度居中](lesson-1c3d6367be48f70bb001.lesson.md) · 阶段：execute · 信号：@BuilderParam, Refresh, layoutWeight(1), height('100%')
- [背景之前的 padding 放外层，背景圆角裁剪放内层](lesson-5c6217b05bb4c266f254.lesson.md) · 阶段：spec/execute · 信号：statusBarsPadding, navigationBarsPadding, Surface, borderRadius
- [随选中进度收放的间距按同一选中条件归零](lesson-c39245065cc26d8c9f64.lesson.md) · 阶段：execute · 信号：animationProgress, constraintSize, Layout
