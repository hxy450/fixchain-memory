# ui/layout/layers

页面骨架与叠放层按运行时真实结构落定：运行时挂载、重叠子视图、gone 节点不按 XML 占位定几何。

[上一级](../index.md)

## 本级经验

- [RelativeLayout 无规则子项放同一 Stack](lesson-7dcf2d92c689c96c190b.lesson.md) · 阶段：execute/repair · 信号：RelativeLayout, layout_below, layout_above, layout_toEndOf
- [addView 挂根部的视图放 Stack 最底层铺满](lesson-c3dcc5a25a0ad59c53c1.lesson.md) · 阶段：execute · 信号：addView, removeView, LayoutParams, Stack
- [接线已转换页保留全屏底层加状态前景层骨架](lesson-4de4283ec625be7e976c.lesson.md) · 阶段：execute/repair · 信号：FEATURE_NO_TITLE, MapView, showRoute, tabData
- [新增可选背景层时上层不透明内容透明或合成](lesson-cba11443f9a59fdaf4f7.lesson.md) · 阶段：execute · 信号：BlendMode.DARKEN, blendMode, ImageFit.Contain, Drawable
- [源 XML 的 gone 节点不渲染，固定尺寸点击容器作热区](lesson-f1a98587fe72ff68c5a8.lesson.md) · 阶段：execute · 信号：tools:listitem, visibility="gone", setVisibility, findViewById
