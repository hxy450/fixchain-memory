# ui/layout/sizing

宽高、比例、百分比与边距的组合，贴合内容的背景，以及横向滚动容器的交叉轴定高。

[上一级](../index.md)

## 本级经验

- [layout_marginStart/End 写成 margin 的 start/end 时同一对象各边都用 LengthMetrics；不需要随语言方向翻转时改用 left/right 数值](lesson-e3077bf60cfc3f34d0a2.lesson.md)
  - 时机：界面实现阶段，把 layout_marginStart/End 一类方向相关边距写成 ArkUI margin 时；维护映射参考的边距示例时
  - 情境：源布局用 marginEnd/marginStart（常与 marginBottom 等写在同一控件上）；映射参考把它对到 .margin({ end }) 并给出纯数字示例。
- [match_parent/0dp 加同轴 margin 表示“父尺寸减边距”：不写成百分比加 margin，等权重兄弟的间距改用 space](lesson-75f4743dff663f50966b.lesson.md)
  - 时机：界面实现阶段，把 match_parent 或两侧约束 0dp 且带同轴 margin 的视图、或带 margin 的等权重兄弟翻译成 ArkUI 尺寸与间距时；按要求调整左右边距时
  - 情境：源元素 match_parent（或约束到父两侧的 0dp）同时设 layout_marginHorizontal/Start/End 或 marginTop/Bottom；或水平 LinearLayout 中等权重（0dp + weight）的子项以 marginStart 作间距；目标用 width/height('100%') 或 layoutWeight。
- [并排 wrap_content 图片列不按固有 dp 写死宽度：按固有宽度比例分列，高度用 aspectRatio](lesson-0618cdf331560d389f0e.lesson.md)
  - 时机：界面实现阶段，把 match_parent 父行中并排的 wrap_content 图片列转换为 ArkUI Row/Column 并确定列宽时；修复“右侧顶满/被遮挡”时
  - 情境：源布局在 match_parent 的水平 LinearLayout 中并排放置 wrap_content 图片列，列宽来自 drawable 固有尺寸与左右、列间 margin，其总和接近或超过常见手机屏宽；目标要在宽度不同的设备上与源截图对齐。
- [横向滚动容器给交叉轴写数值高度，按内容算出，不写 'auto' 也不留空](lesson-2d7c6de68f604ae77caf.lesson.md)
  - 时机：界面实现阶段，把 Compose 可滚动 Tab 行、LazyRow、horizontalScroll 等按内容定高的横向滚动行翻译成 ArkUI 滚动容器时
  - 情境：源端横向滚动行的高度由子项固有高度决定；目标用 Scroll(ScrollDirection.Horizontal) 或横向 List/Grid 实现，所在父容器在纵向上还有剩余空间。
- [贴合内容的描边、选中背景画在由内容定尺寸的节点自身，不用 width/height('100%') 覆盖层](lesson-a58ebfe7a4c55b041b14.lesson.md)
  - 时机：界面实现阶段，翻译用 fillMaxSize()、matchContentSize 贴合内容的选中指示器、描边或背景时
  - 情境：源端指示器或背景层以 fillMaxSize、matchContentSize 贴合某个由内容定尺寸的格子；目标准备在 Stack/Row 里叠一层 width/height('100%') 的节点来画描边或背景。
  - 例外：父节点有确定的宽高（显式数值，或已被外层约束定死）时，百分比层按该尺寸解析，可以使用
