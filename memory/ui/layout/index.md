# ui/layout

页面几何与层级：按约束定位、尺寸与边距、滚动区域、运行时覆盖层选择分支；通用页面结构与视觉修复依据留在本级。

[上一级](../index.md)

## 子主题

- [constraints](constraints/index.md) — ConstraintLayout/RelativeLayout的锚点、叠放与默认对齐（含 Compose Column/Row 的默认对齐），Compose Box 子项在 Stack 中的定位，基线对齐与逐行内距的 Row 组，及ArkUI容器中的子项定位。
- [layers](layers/index.md) — 运行时addView、全屏底层与状态覆盖层：确定视图挂在哪里、如何叠放及几何范围；点击命中与事件时坐标属于ui/interaction。
- [scrolling](scrolling/index.md) — ScrollView/NestedScrollView的滚动范围、LazyRow/横向滚动行的交叉轴尺寸、Lazy 列表 contentPadding 的内容偏移、带高度上限的滚动卡片、连续折叠顶栏与滚动区内跟随等高。
- [sizing](sizing/index.md) — 宽高、比例、百分比与边距的组合（父尺寸减边距、占剩余空间），Compose 修饰符链顺序与 Row 的测量顺序、固有高度，Material 按钮的布局占位与实绘尺寸，px 域整数布局公式与随进度收放的间距，以及随内容定尺寸的图片、背景和描边。

## 本级经验

- [视觉修复以源布局与源码分支为准：截图尺寸差先折算成 vp 对照，容器尺寸与自绘组件的绘制尺寸同源修改，截图里缺少的入口先查渠道与开关分支，文档截图与 @Preview 示例不当应用真值](lesson-8119d8bf0b58e4daac24.lesson.md)
  - 时机：视觉校验与修复阶段，根据截图差异撰写工单，决定修改固定尺寸、列数、背景，删减截图中没有出现的入口与区块，或按基线截图选定空态等文案与图标时；按差异单调整包裹自绘组件（Canvas 日历等）的容器高度与折叠范围时
  - 情境：依据截图或视觉差异单修改页面尺寸、可见入口、文案或图标；基线可能跨设备密度、渠道或运行状态，也可能来自docs/assets或@Preview。页面含Canvas自绘组件时，外层高度、clip和折叠范围还可能依赖绘制端的行高等尺寸。
- [页面转换逐项落实源 XML 的 gone 节点、固定尺寸点击容器与 tools:listitem 行布局](lesson-f1a98587fe72ff68c5a8.lesson.md)
  - 时机：页面转换阶段，把 Android 页面 XML 翻译为 ArkUI 结构与几何时
  - 情境：源布局含 visibility=gone 的标题等节点、固定尺寸的点击容器（如 40×48dp 的返回 ImageView），列表 RecyclerView 用 tools:listitem 引用独立的 item 布局；迁移用的页面快照是合成的，可能把 gone 节点列为可见文本。
