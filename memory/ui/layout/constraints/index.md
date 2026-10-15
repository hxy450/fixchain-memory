# ui/layout/constraints

ConstraintLayout/RelativeLayout的锚点、叠放与默认对齐（含 Compose Column/Row 的默认对齐），Compose Box 子项在 Stack 中的定位，基线对齐与逐行内距的 Row 组，及ArkUI容器中的子项定位。

[上一级](../index.md)

## 本级经验

- [Compose Row 以 alignBy(LastBaseline) 对齐文本与自定义组件时，改用 Row 居中对齐，不用 Flex 基线对齐](lesson-c4990fef246323ffda03.lesson.md)
  - 时机：页面转换阶段，翻译 Compose Row 中以 alignBy(LastBaseline)/alignByBaseline 对齐的文本与自定义组件（数量选择器等）时
  - 情境：源 Row 的子项用 alignBy(LastBaseline) 对齐，其中一端是自定义组件或不含文本基线的控件；目标准备写 Flex/Row 的 ItemAlign.Baseline。
  - 例外：两端都是 Text（都有文本基线）时，可以用 Flex 的 ItemAlign.Baseline（enums.d.ts：Flex 容器内按文本基线对齐）
- [Compose weight(1f).wrapContentWidth(End) 靠尾端的文本，译为权重槽内尾端对齐，不只写 layoutWeight](lesson-71879b64fad065810c21.lesson.md)
  - 时机：页面转换阶段，翻译 Compose Row 中以 Modifier.weight(1f).wrapContentWidth(Alignment.End) 靠右（尾端）的标签、金额等文本时
  - 情境：源 Row 里某个文本以 weight(1f) 占剩余宽，再用 wrapContentWidth(Alignment.End) 让文本按自身宽度贴槽位尾端；目标准备写 layoutWeight(1) 或 flexGrow(1)。
- [ConstraintLayout 改写成 Column 顺序流前先列出各子项锚点：多个子项锚父底、元素锚在兄弟上方时保留原锚点距离](lesson-3fe0026df9abc72ff788.lesson.md)
  - 时机：界面实现阶段，把 ConstraintLayout 转成 Column/Row 顺序流或 Stack 层级，确定锚父底与锚兄弟子项的边距时
  - 情境：源 ConstraintLayout 中有多个子项 constraintBottom_toBottomOf=parent（含 invisible 仍占位的行），或按钮上方的文字以 constraintBottom_toTopOf 锚在兄弟上；目标用 Column 顺序流、Visibility.Hidden 或父 Stack 的 BottomStart。
  - 例外：0dp×0dp 加 dimensionRatio 的子项尺寸按比例盒的规则另行计算；单个子视图四向锚定 parent 自身居中、兄弟只单向悬挂在它下方时，按居中与单向悬挂的规则转换
- [ConstraintLayout 标题栏（返回贴 start、0dp 标题居中、操作贴 end）转成互斥三槽 Row 或 RelativeContainer](lesson-4d77f00fb4103d2f84f5.lesson.md)
  - 时机：界面实现阶段，把 ConstraintLayout 标题栏（左返回、居中标题、右侧操作）转换为 ArkUI，或抽取公共标题栏组件时
  - 情境：源标题栏中返回图标 constraintStart_toStartOf=parent，右侧文字或图标 constraintEnd_toEndOf=parent，标题宽 0dp、两端约束到 parent 并带左右 margin；工程里可能已有同类页面的标题栏代码可以照搬，或要按规格把该 include 布局抽成公共组件。
- [RelativeLayout 中没有相对规则的子 View 叠放在同一区域：用 Stack 或同一坐标定位，不改成 Column 顺序排列](lesson-7dcf2d92c689c96c190b.lesson.md)
  - 时机：界面实现与视觉返修阶段，把 RelativeLayout 内的多个子 View（如叠放的曲线、图层）翻译成 ArkUI 容器时
  - 情境：源 item 在固定高度的 RelativeLayout 中放置多个子 View，它们没有 below/above/toEndOf 等相对规则，只有相同或各自的 margin 与对齐，实际重叠绘制在同一区域；目标沿用了 Column 顺序结构。
  - 例外：子 View 之间写有 layout_below/above/toStartOf 等相对规则，此时按规则排布
- [RelativeLayout 设了 android:gravity 时整组非 GONE 子项按 gravity 平移，alignParentTop 子项也会居中](lesson-c7eccff80bac02281029.lesson.md)
  - 时机：界面实现阶段，把带 android:gravity 的 RelativeLayout 映射为 ArkUI 容器对齐时
  - 情境：源 RelativeLayout 设 gravity=center_vertical 等非 start|top 值，容器尺寸大于子项包围盒（match_parent 或固定尺寸），子项同时声明 alignParentTop/alignParentStart 等对齐规则，可能用 android:ignoreGravity 排除某个子项；映射参考只写“容器级 gravity 无直接对应”。
  - 例外：容器在该轴上为 wrap_content 时，子项包围盒与容器一样大，gravity 不产生偏移，按子项规则排布即可
- [Stack 子项位置由父 alignContent 决定、子项 .align() 只对齐自身内容：混合对齐用 layoutGravity 或 position](lesson-92aee54a305ea0bde363.lesson.md)
  - 时机：界面转换与巡检修复阶段，把 FrameLayout/CoordinatorLayout 的 layout_gravity、RelativeLayout 的 alignParent*/centerInParent、Compose Box 的 Modifier.align 或自定义 Layout 的 placeRelative 翻译为 ArkUI Stack 子项定位并确定叠层次序时；修复或编译清理删除 height('100%')、.align() 等定位手段时
  - 情境：目标用 Stack 同时容纳对齐需求不同的子项：贴右下的角标（layout_gravity=end|bottom）、贴底的购买栏（Modifier.align(BottomCenter)）、FAB、多选浮层、按 placeRelative(x, (maxHeight - height) / 2) 纵向居中的文字；Stack 设了统一的 alignContent（常为 TopStart 或默认 Center）。映射参考或兄弟页可能把 layout_gravity 写成 .align(Alignment.X)。
  - 例外：Stack 中只有一个需要定位的子项，或全部子项同向贴边时，直接改父 Stack 的 alignContent 即可
- [列表页空态按源布局定纵向位置：wrap_content 未居中的空态靠上，weight 剩余区里与列表叠放的空态在有界区域内居中](lesson-4d427dfb954940ff71d5.lesson.md)
  - 时机：界面实现阶段，为列表页或剩余区域的空态（无数据提示）确定在内容区中的纵向位置时；参照工程已有空态 Builder 写新页空态时
  - 情境：源空态容器可能是 layout_height=wrap_content 的 NestedScrollView/LinearLayout，在父 RelativeLayout 中未声明居中，内层 gravity=center；也可能是 layout_height=0dp + layout_weight=1 区域里与 RecyclerView 叠放、按数据显隐的 match_parent + gravity=center TextView。工程里可能已有全高居中的空态 Builder 可供参照。
- [单视图对父居中、兄弟单向悬挂时（单向约束、layout_below）用 RelativeContainer 或下挂层复刻，不用 Column 整组居中](lesson-e607a28fcd91acd2b40f.lesson.md)
  - 时机：规格提取阶段把 ConstraintLayout 约束翻译成容器与定位决策，或页面实现阶段落定容器时；转换 RelativeLayout 控件排（按钮 layout_centerVertical、标签 layout_below）时
  - 情境：源 ConstraintLayout 中一个子视图以 start/end/top/bottom 四向锚定 parent 自身居中，另一个兄弟只以 constraintTop_toBottomOf 等单向约束挂在它下方，兄弟之间没有双向约束。也包括 RelativeLayout 控件排：按钮 layout_centerVertical，标签以 layout_below 挂在各自按钮下方，兄弟之间有固定 margin。
  - 例外：兄弟之间有双向约束构成 chain 时，按 chain 语义（chainStyle）另行转换，不适用本条；子视图以 constraintBottom_toBottomOf=parent 贴底，或以 constraintBottom_toTopOf 锚在兄弟上方（不是居中）时，按锚点边距的规则转换
- [双 0dp 加 dimensionRatio 的子项按“满足比例且不越出约束的最大尺寸”定宽高，不只写 width('100%').aspectRatio](lesson-ccf0b3ab6ebd6dd7c2e6.lesson.md)
  - 时机：界面实现阶段，把 ConstraintLayout 中 0dp×0dp 加 layout_constraintDimensionRatio 的子项（封面、视频区等）转成 ArkUI 尺寸时
  - 情境：源子项 layout_width 与 layout_height 都是 0dp，带 layout_constraintDimensionRatio，上下或左右分别锚在相邻子项或 parent 上；目标用 Column 顺序流配 layoutWeight 或 Stack 承载，可用空间随屏幕变化。
  - 例外：只有一个方向为 0dp、另一方向已定尺寸时，按已定的边乘或除比例求另一边；dimensionRatio 带 W, 或 H, 前缀时本条未覆盖：来源为无前缀的双 0dp，本机只有 ConstraintLayout 字节码；先按所用 ConstraintLayout 版本的文档确认前缀指定哪一边，再决定是否套用下面的公式
- [源纵向容器或 Compose Row 未写交叉轴对齐时，ArkUI Column/Row 显式写起始或顶端对齐（ArkUI 默认居中）](lesson-08b9064f678f1635e647.lesson.md)
  - 时机：界面实现阶段，把未写 gravity 的纵向 LinearLayout、以 constraintStart_toStartOf=parent 靠起始边的 ConstraintLayout wrap_content 子项、未传 horizontalAlignment 的 Compose Column 或未传 verticalAlignment 的 Compose Row 转成 ArkUI Column/Row 时
  - 情境：源纵向 LinearLayout 没写 gravity（子项默认贴起始边），或 wrap_content 子项以 constraintStart_toStartOf=parent 靠起始边；Compose Column 未声明 horizontalAlignment（默认 Start），文本只带水平 padding 而无 fillMaxWidth，仅个别项以 fillMaxWidth + TextAlign.Center 居中；Compose Row 未写 verticalAlignment（默认 Top），子项高度不等。目标 Column 宽于子项（width('100%') 或约束宽），子项为固定或内容宽度。也包括容器被 layoutWeight 分到更高的高度，而源端卡内内容 wrap_content 自上而下排列。
  - 例外：源端写了 gravity=center/center_horizontal、Compose horizontalAlignment=CenterHorizontally，或子项 fillMaxWidth + TextAlign.Center：这些项按源端居中；Stack 子项在父容器中的位置、Scroll 内不满一屏的内容位置和空态的纵向位置是另外的决策，不由 Column 的 alignItems 决定
