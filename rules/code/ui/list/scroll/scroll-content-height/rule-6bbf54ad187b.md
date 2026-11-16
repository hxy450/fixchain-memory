# 源空态是 wrap_content 且未在父布局居中的滚动容器时，目标靠上放，不写全高居中

审的是：代码
触发（任一种）：
- 读到：空态容器是 NestedScrollView / ScrollView，android:layout_height="wrap_content"，在 RelativeLayout 里没声明居中；内层 LinearLayout 写 android:gravity="center"；写错的样子：目标空态外层 Column 写 .height('100%') 加 .justifyContent(FlexAlign.Center)，内容在整个内容区垂直居中
适用范围：把源端列表页空态迁成 ArkUI 时确定空态在内容区里的纵向位置
做法：
- 先看空态容器自身的 layout_height 和它在父布局里的定位：wrap_content 且未居中就靠上放，改成 .justifyContent(FlexAlign.Start)，顶部偏移按源布局的边距取
- 内层 gravity="center" 只在包裹高度内排列子项；参照同工程已有空态 Builder 时只复用样式骨架，文案和位置按本页源布局定
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- gravity：Specifies how an object should position its content, on both the X and Y axes, within its own bounds.：gravity 只在控件自己的边界内排内容，不决定控件在父布局里的位置（出处：Android SDK 平台资源 data/res/values/attrs.xml，gravity（按应用的 compileSdk 取对应平台））
- justifyContent(value: FlexAlign): ColumnAttribute：Column 主轴（纵向）对齐（出处：鸿蒙 SDK 的 ets/component/column.d.ts，ColumnAttribute.justifyContent）
- FlexAlign.Start：元素在主轴起始端对齐，后续元素依次跟在前一个后面（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，FlexAlign.Start）
- FlexAlign.Start 加顶部内边距，空态靠上：修复后位置与源端一致的写法；偏移值按源布局或截图定（出处：卡里修好并验证过）
- justifyContent(value: FlexAlign): RowAttribute：同族接口：Row 的主轴（横向）对齐（出处：鸿蒙 SDK 的 ets/component/row.d.ts，RowAttribute.justifyContent）
针对本应用要查的：
- 空态在内容区里的纵向起点：源工程布局 XML 里空态容器的 layout_height、layout_marginTop / paddingTop，以及它在 RelativeLayout 里的定位规则（layout_below、layout_centerInParent 等）；没有居中规则时从父布局顶部（或所 below 的控件下方）开始，边距按源值换成 vp
来源：1 张卡，1 个应用
- case-a54f1d69801694c5b1bf（实时公交）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
