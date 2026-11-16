# 靠右的 weight 标签写成 layoutWeight 加 textAlign(End)

审的是：代码
触发（任一种）：
- 读到：Compose Text 写 Modifier.weight(1f).wrapContentWidth(Alignment.End)；写错的样子：目标 Text 只有 .layoutWeight(1) 或 .flexGrow(1)，没有 .textAlign(TextAlign.End)，文字靠左
适用范围：Compose 行内用 weight 占满剩余宽、再把内容推到右端的文本
做法：
- 写成 Text(…).layoutWeight(1).textAlign(TextAlign.End)（Flex 里用 .flexGrow(1)），源端的 padding(end) 照写
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- textAlign(value: TextAlign): TextAttribute，默认 TextAlign.Start：文本段落的水平对齐，要靠右得显式写 End（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.textAlign；ts-basic-components-text.md，textAlign）
- flexGrow(value: number): T：Flex 里分配剩余空间，作用同 layoutWeight（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.flexGrow）
来源：1 张卡，1 个应用
- case-83dafcc0eaba740bd9c0（Jetsnack）：做法第 1 步 ← 建议 6、诊断
