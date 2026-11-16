# LinearLayout 迁成 Row/Column 时读出 gravity 两轴对齐并显式写出

审的是：代码
触发（任一种）：
- 读到：LinearLayout 没写或写了 android:gravity、子项写了 android:layout_gravity；写错的样子：Column / Row 没写 .alignItems(...) 或 .justifyContent(...)；或用子项 .layoutWeight(1)、Text 的 textAlign 代替容器对齐
适用范围：LinearLayout 迁成 Column / Row 时两轴上的子项对齐
做法：
- 在源布局 XML 读 android:orientation、android:gravity（没写按 START|TOP）和子项的 android:layout_gravity，分出主轴和交叉轴的对齐
- 纵向写 Column().alignItems(HorizontalAlign.…).justifyContent(FlexAlign.…)，横向写 Row().justifyContent(FlexAlign.…).alignItems(VerticalAlign.…)；个别子项不同的写 .alignSelf(ItemAlign.…)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- LinearLayout 的 mGravity 默认是 Gravity.START | Gravity.TOP：源端没写 gravity 时子项贴起始边（出处：android.widget.LinearLayout#mGravity）
- alignItems(value: HorizontalAlign): ColumnAttribute，默认值 HorizontalAlign.Center：Column 的交叉轴（水平）对齐，不写时居中（出处：鸿蒙 SDK 的 ets/component/column.d.ts，ColumnAttribute.alignItems；ts-container-column.md，alignItems）
- justifyContent(value: FlexAlign): RowAttribute，默认 FlexAlign.Start：Row 主轴（水平）对齐；不写时子项靠左（出处：鸿蒙 SDK 的 ets/component/row.d.ts，RowAttribute.justifyContent；ts-container-row.md，justifyContent）
- alignItems(value: VerticalAlign): RowAttribute，默认 VerticalAlign.Center：Row 交叉轴（竖直）对齐，默认已居中（出处：鸿蒙 SDK 的 ets/component/row.d.ts，RowAttribute.alignItems；ts-container-row.md，alignItems）
针对本应用要查的：
- 这个 LinearLayout 两个轴上的对齐：源工程 res/layout 下的布局 XML，按控件找 android:orientation、android:gravity 和各子项的 android:layout_gravity；没写 gravity 按 START|TOP 读；写了的按水平、竖直两部分分到主轴和交叉轴。例：横向 LinearLayout 写 gravity="center"、子项 wrap_content 时，Row 写 .justifyContent(FlexAlign.Center)，竖直方向 Row 默认已居中
未核实：Column 的 justifyContent 默认值，以及 gravity 各取值词（center_vertical、bottom、end 等）到 FlexAlign、VerticalAlign、HorizontalAlign 的逐项对应，族里规矩没有查实
来源：5 张卡，3 个应用
- case-440adef4b89e0a02222a（免费来电多多）：做法第 2 步 ← 建议 1
- case-6405389151d06d90f7cc（免费来电多多）：做法第 1 步 ← 建议 1
- case-6ba16d2344b52f8fca51（刺猬猫阅读）：做法第 2 步 ← 建议 2
- case-d54a9506e30031090325（Jetsnack）：做法第 1 步 ← 建议 1
- case-f749e3c70af1100c90d9（Jetsnack）：做法第 2 步 ← 诊断
