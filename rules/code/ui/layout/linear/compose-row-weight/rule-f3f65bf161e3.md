# Row 里无 weight 的 fillMaxWidth 占满剩余宽，不写成 layoutWeight(1)

审的是：代码
触发（任一种）：
- 读到：Compose Row 中某子项 Modifier.fillMaxWidth() 没有 weight，后面还有兄弟（如 IconButton）；写错的样子：目标把这个子项写成 .layoutWeight(1)，后续兄弟给了固定宽，兄弟变得可见
适用范围：Compose Row 的子项按顺序测量、有无 weight 的 fillMaxWidth 子项时
做法：
- 按顺序测量推算每个子项实得宽度：无 weight 的 fillMaxWidth 先占满剩余宽，后续兄弟实得 0；忠实复刻时后续兄弟写 .width(0).clip(true)
- 规格描述的可见结果和这个推算不同时，在规格或转换报告里明写为有意偏离
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 不设 layoutWeight 的子元素先占位，设了 layoutWeight > 0 的从剩余空间按权重分配，并忽略自身尺寸：ArkUI 先扣除兄弟再分配，和 Compose 的顺序测量相反，所以 layoutWeight(1) 会让后续兄弟可见（出处：ts-universal-attributes-size.md，layoutWeight）
- clip(value: boolean): T：裁掉超出自身的内容，配 width(0) 让兄弟不可见（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.clip）
- 后续兄弟改成 width(0) + clip 后，和源端一样不可见：修复时用的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-83dafcc0eaba740bd9c0（Jetsnack）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 3 ← 诊断
