# ui/layout

页面几何与层级：按约束定位、尺寸与边距、滚动区域、运行时覆盖层选择分支；通用页面结构与视觉修复依据留在本级。

[上一级](../index.md)

## 子主题

- [constraints](constraints/index.md) — ConstraintLayout/RelativeLayout的锚点、叠放与默认对齐，及ArkUI容器中的子项定位。
- [layers](layers/index.md) — 运行时addView挂载、全屏底层与状态覆盖层，以及动效/气泡锚点的坐标与取值时机。
- [scrolling](scrolling/index.md) — 滚动范围、连续折叠顶栏与滚动容器内的跟随等高。
- [sizing](sizing/index.md) — 宽高、比例、百分比与边距的组合，贴合内容的背景，以及横向滚动容器的交叉轴定高。

## 本级经验

- [视觉修复以源布局与源码分支为准：截图尺寸差先折算成 vp 对照，容器尺寸与自绘组件的绘制尺寸同源修改，截图里缺少的入口先查渠道与开关分支，文档截图与 @Preview 示例不当应用真值](lesson-8119d8bf0b58e4daac24.lesson.md)
  - 时机：视觉校验与修复阶段，根据截图差异撰写工单，决定修改固定尺寸、列数、背景，删减截图中没有出现的入口与区块，或按基线截图选定空态等文案与图标时；按差异单调整包裹自绘组件（Canvas 日历等）的容器高度与折叠范围时
  - 情境：源端基线截图与目标截图来自不同设备或屏幕密度，并排对比显示目标主内容“偏小”或“偏上”；目标页的主要区块已按源布局 dp 字面值写入固定高度与 marginTop，并与底部 Tab 共享有限的纵向空间。截图也可能只来自某个渠道、会员或开关变体，或只反映某一时刻的天气与昼夜状态；源 Fragment 中有按 getChannel()、开关对入口 setVisibility 的分支。也包括把源仓库 docs/assets 下的截图或 @Preview 预览当作基线，而其中的示例文案、图标与应用实际调用链不同的情形。也包括外层容器按“行数 × 行高”计算高度并 clip、同一行高还决定手势折叠范围，而行高实际由内部 Canvas 的常量绘制；差异单只有“行高更大”一类文字结论。
- [页面转换逐项落实源 XML 的 gone 节点、固定尺寸点击容器与 tools:listitem 行布局](lesson-f1a98587fe72ff68c5a8.lesson.md)
  - 时机：页面转换阶段，把 Android 页面 XML 翻译为 ArkUI 结构与几何时
  - 情境：源布局含 visibility=gone 的标题等节点、固定尺寸的点击容器（如 40×48dp 的返回 ImageView），列表 RecyclerView 用 tools:listitem 引用独立的 item 布局；迁移用的页面快照是合成的，可能把 gone 节点列为可见文本。
