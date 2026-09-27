# ui/layout

容器选择、约束与定位（ConstraintLayout、RelativeContainer、Column 等），以及尺寸约束：滚动容器定高、百分比尺寸的解析

[上一级](../index.md)

## 本级经验

- [ConstraintLayout 中单视图对 parent 居中、兄弟单向悬挂时，用 RelativeContainer 复刻，不用 Column 整组居中](lesson-e607a28fcd91acd2b40f.lesson.md)
  - 时机：规格提取阶段把 ConstraintLayout 约束翻译成容器与定位决策，或页面实现阶段落定容器时
  - 情境：源 ConstraintLayout 中一个子视图以 start/end/top/bottom 四向锚定 parent 自身居中，另一个兄弟只以 constraintTop_toBottomOf 等单向约束挂在它下方，兄弟之间没有双向约束。
  - 例外：兄弟之间有双向约束构成 chain 时，按 chain 语义（chainStyle）另行转换，不适用本条
- [横向滚动容器给交叉轴写数值高度，按内容算出，不写 'auto' 也不留空](lesson-2d7c6de68f604ae77caf.lesson.md)
  - 时机：界面实现阶段，把 Compose 可滚动 Tab 行、LazyRow、horizontalScroll 等按内容定高的横向滚动行翻译成 ArkUI 滚动容器时
  - 情境：源端横向滚动行的高度由子项固有高度决定；目标用 Scroll(ScrollDirection.Horizontal) 或横向 List/Grid 实现，所在父容器在纵向上还有剩余空间。
- [贴合内容的描边、选中背景画在由内容定尺寸的节点自身，不用 width/height('100%') 覆盖层](lesson-a58ebfe7a4c55b041b14.lesson.md)
  - 时机：界面实现阶段，翻译用 fillMaxSize()、matchContentSize 贴合内容的选中指示器、描边或背景时
  - 情境：源端指示器或背景层以 fillMaxSize、matchContentSize 贴合某个由内容定尺寸的格子；目标准备在 Stack/Row 里叠一层 width/height('100%') 的节点来画描边或背景。
  - 例外：父节点有确定的宽高（显式数值，或已被外层约束定死）时，百分比层按该尺寸解析，可以使用
