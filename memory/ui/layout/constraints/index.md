# ui/layout/constraints

ConstraintLayout/RelativeLayout的锚点、叠放与默认对齐，及ArkUI容器中的子项定位。

[上一级](../index.md)

## 本级经验

- [ConstraintLayout 中单视图对 parent 居中、兄弟单向悬挂时，用 RelativeContainer 复刻，不用 Column 整组居中](lesson-e607a28fcd91acd2b40f.lesson.md)
  - 时机：规格提取阶段把 ConstraintLayout 约束翻译成容器与定位决策，或页面实现阶段落定容器时
  - 情境：源 ConstraintLayout 中一个子视图以 start/end/top/bottom 四向锚定 parent 自身居中，另一个兄弟只以 constraintTop_toBottomOf 等单向约束挂在它下方，兄弟之间没有双向约束。
  - 例外：兄弟之间有双向约束构成 chain 时，按 chain 语义（chainStyle）另行转换，不适用本条
- [ConstraintLayout 改写成 Column 顺序流前先列出各子项锚点：锚父底、锚兄弟与双 0dp 比例子项都要保留语义](lesson-3fe0026df9abc72ff788.lesson.md)
  - 时机：界面实现阶段，把 ConstraintLayout 转成 Column/Row 顺序流或 Stack 层级，确定锚点边距与比例子项尺寸时
  - 情境：源 ConstraintLayout 中有多个子项 constraintBottom_toBottomOf=parent（含 invisible 仍占位的行）、按钮上方的文字以 constraintBottom_toTopOf 锚在兄弟上、0dp×0dp 加 dimensionRatio 的子项夹在上下锚点之间；目标用 Column 顺序流、layoutWeight、Visibility.Hidden 或父 Stack 的 BottomStart。
- [RelativeLayout 中没有相对规则的子 View 叠放在同一区域：用 Stack 或同一坐标定位，不改成 Column 顺序排列](lesson-7dcf2d92c689c96c190b.lesson.md)
  - 时机：界面实现与视觉返修阶段，把 RelativeLayout 或 FrameLayout 内的多个子 View（如两条曲线、图层）翻译成 ArkUI 容器时
  - 情境：源 item 在固定高度的 RelativeLayout 中放置多个子 View，它们没有 below/above/toEndOf 等相对规则，只有相同的 margin 或对齐，实际重叠绘制在同一区域；目标沿用了上一版的 Column 顺序结构。
  - 例外：子 View 之间写有 layout_below/above/toStartOf 等相对规则，此时按规则排布
- [Stack 中内容尺寸的子项按 alignContent 定位：子项自身的 .align() 不改变它在父容器中的位置，需要的对齐用满尺寸容器或显式 position](lesson-92aee54a305ea0bde363.lesson.md)
  - 时机：界面转换与巡检修复阶段，把 Compose 自定义 Layout 或 Box 中的文字改写为 ArkUI Stack 子节点并确定纵向位置时；修复或编译清理删除 height('100%')、.align() 等居中手段时；把 FrameLayout 中按 layout_gravity 叠放的角标、重叠头像翻译成 Stack 时
  - 情境：源端自定义 Layout 用 placeRelative(x, (maxHeight - height) / 2) 把定宽文字纵向居中，或 Box 中文字按居中对齐放置；目标用 Stack({ alignContent: Alignment.TopStart }) 同时容纳文字与图片等对齐需求不同的子项。也包括源端固定尺寸 FrameLayout 中的小角标以 layout_gravity=end|bottom 贴右下，目标写成 Stack({ alignContent: Alignment.TopStart }) 并只给角标加 .align(Alignment.BottomEnd)。
- [源端默认起始对齐和贴顶要显式写出：Android 与 Compose 的纵向容器默认贴起始边，ArkUI Column 交叉轴默认居中，Scroll 内不满一屏的内容默认居中](lesson-08b9064f678f1635e647.lesson.md)
  - 时机：界面实现阶段，把纵向 LinearLayout、带 constraintStart/Top 的 ConstraintLayout 或 ScrollView/NestedScrollView 转成 ArkUI Column 与 Scroll 时；以及把 Compose Column 中的文本块转成 ArkUI Column 子项时
  - 情境：源纵向 LinearLayout 没写 gravity（子项默认贴起始边），或 wrap_content 子项以 constraintStart_toStartOf=parent 靠起始边、卡片以 constraintTop_toTopOf=parent 贴顶；目标 Column 宽度撑满，子项为固定或内容宽度；滚动页内容常不满一屏。或显示卡片用 layoutWeight 分高，源端卡内内容 wrap_content 自上而下排列并带上内边距。也包括 Compose Column 未声明 horizontalAlignment（默认 Start），文本只带水平 padding 而无 fillMaxWidth，仅个别项以 fillMaxWidth + TextAlign.Center 居中。
