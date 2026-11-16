# ConstraintLayout 子项的约束和锚点

agent 会看到什么：读到 ConstraintLayout 子项的 app:layout_constraint*_to*Of="parent" 或指向兄弟、0dp 加 dimensionRatio；产物里换成了 Stack 加 .align()、带 Blank() 的 Row、百分比 position、整组居中的 Column 或照抄 margin 的顺序流

## 规矩

- rule-da5f717e6731｜ConstraintLayout 标题栏左右入口约束到 start/end 时，用 Row 三段槽位，不用 Stack｜读到：ConstraintLayout 标题栏：返回入口 app:layout_constraintStart_toStartOf="parent"，右侧文字或图标 app:layout_constraintEnd_toEndOf="parent"，标题 android:layout_width="0dp" 两端约束到 parent 并带 android:layout_marginStart / layout_marginEnd；写错：写成 Stack({ alignContent: Alignment.Center })，返回 Image 只加 .align(Alignment.Start)、右侧加 .align(Alignment.End)，标题 Text 用 .width('100%') 加左右 padding
- rule-671a9126246c｜Stack 里要贴边的子组件不靠自身 .align()，改放 Row 槽位或用 position/offset｜读到：源布局里子控件约束到父容器的一边（app:layout_constraintStart_toStartOf / layout_constraintEnd_toEndOf / layout_constraintBottom_toBottomOf="parent"）；写错：Stack 的子组件上写 .align(Alignment.Start)、.align(Alignment.End) 或 .align(Alignment.Bottom)，想让它贴左、贴右或贴底
- rule-64df7d04369a｜贴末端加 marginEnd 的约束改用 Row + Blank，不用百分比 position x｜读到：ConstraintLayout 里的控件 app:layout_constraintEnd_toEndOf="parent" 加 android:layout_marginEnd；写错：目标写成 .position({ x: '72%', y: … }) 这类按宽度百分比算的横坐标
- rule-539aa2e63775｜ConstraintLayout 子块约束到 parent 首尾时，目标居中叠放，不放进带 Blank() 的 Row｜读到：ConstraintLayout 里一个子 View 同时写 app:layout_constraintStart_toStartOf="parent" 和 app:layout_constraintEnd_toEndOf="parent"，在整卡中水平居中，另有元素贴 parent 末端；写错：目标把这个块放进横向 Row，排在 Blank() 之后、紧挨贴末端的元素，块被推到右侧
- rule-e4c9f0de7070｜单视图对 parent 居中、兄弟挂其下时，目标用 RelativeContainer 加 alignRules｜读到：ConstraintLayout 子视图四向约束都是 parent，兄弟只有 layout_constraintTop_toBottomOf 指向它；写错：目标用 Column().justifyContent(FlexAlign.Center) 包住两者整组居中，注释写“居中链”
- rule-6df2657f3ad2｜多个子项都锚 parent 底的 ConstraintLayout 改 Column 流式时，重算底边距或改贴底定位｜读到：ConstraintLayout 里两个及以上子项都写 app:layout_constraintBottom_toBottomOf="parent"，各带 android:layout_marginBottom，其中有 android:visibility="invisible" 仍占位的行；写错：目标写成 Column 顺序流，每个子项照抄源端 .margin({ bottom: <源值> })，排在后面的兄弟写 .visibility(Visibility.Hidden) 仍占位，于是前一个子项的底边距从这个兄弟之上算起
- rule-83eaa3fe7833｜0dp×0dp 加 dimensionRatio 夹在上下锚点间时，边长取可用宽高的较小者｜读到：ConstraintLayout 子项 android:layout_width="0dp"、android:layout_height="0dp"，带 app:layout_constraintDimensionRatio，上下分别锚在相邻子项上（layout_constraintTop_toBottomOf / layout_constraintBottom_toTopOf）；写错：目标在 .layoutWeight(1) 的 Row / Column 里写 Image(...).width('100%').aspectRatio(1)，没有高度上限，源端的上下 margin 留在 Image 上
