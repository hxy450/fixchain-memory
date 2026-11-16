# gravity=center 的行里 wrap_content 子项保留居中，不加 layoutWeight(1)

审的是：代码
触发（任一种）：
- 读到：横向 LinearLayout 带 android:gravity="center"，子项（含 EditText）都是 android:layout_width="wrap_content"；写错的样子：Row 没写 .justifyContent(FlexAlign.Center)，中间的 TextInput 写了 .layoutWeight(1) 拉满剩余宽度，两侧按钮被推到容器边缘
适用范围：安卓 gravity=center 的横向 LinearLayout、子项按内容定宽，迁成 ArkUI Row 时
做法：
- Row 写 .justifyContent(FlexAlign.Center)；竖直方向 Row 默认就是 VerticalAlign.Center
- 中间输入框去掉 .layoutWeight(1)，按内容定宽（例如按数量的位数给 .width）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- justifyContent(value: FlexAlign): RowAttribute，默认 FlexAlign.Start：Row 主轴（水平）对齐；不写时子项靠左（出处：鸿蒙 SDK 的 ets/component/row.d.ts，RowAttribute.justifyContent；ts-container-row.md，justifyContent）
- alignItems(value: VerticalAlign): RowAttribute，默认 VerticalAlign.Center：Row 交叉轴（竖直）对齐，默认已居中（出处：鸿蒙 SDK 的 ets/component/row.d.ts，RowAttribute.alignItems；ts-container-row.md，alignItems）
- 数量框按位数定宽、Row 居中后，加减按钮回到源端位置：按此改后多种位数下都不再被推到边缘（出处：卡里修好并验证过）
- justifyContent(value: FlexAlign): ColumnAttribute：同族接口：Column 主轴（竖直）对齐（出处：鸿蒙 SDK 的 ets/component/column.d.ts，ColumnAttribute.justifyContent）
- FlexOptions.justifyContent?: FlexAlign（默认 FlexAlign.Start）：同族接口：Flex 容器的主轴对齐（出处：鸿蒙 SDK 的 ets/component/flex.d.ts，FlexOptions.justifyContent）
来源：1 张卡，1 个应用
- case-6ba16d2344b52f8fca51（刺猬猫阅读）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；取值 3 ← 诊断
