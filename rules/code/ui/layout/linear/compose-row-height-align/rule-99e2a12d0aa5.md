# Compose Row 没写对齐时，目标 Row 显式写 alignItems(VerticalAlign.Top)

审的是：代码
触发（任一种）：
- 读到：Compose `Row(...)` 的构造参数里没有 `verticalAlignment`；写错的样子：对应的 ArkUI `Row()` 上没有 `.alignItems(...)`，沿用默认 VerticalAlign.Center，子组件被垂直居中
适用范围：Compose Row 迁成 ArkUI Row、源端没写 verticalAlignment 时
做法：
- 目标 Row 显式写 `.alignItems(VerticalAlign.Top)`
- 写完后搜本页全部 `Row(`，逐个对照源码的构造参数有没有写 verticalAlignment
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- alignItems(value: VerticalAlign): RowAttribute，默认 VerticalAlign.Center：ArkUI Row 的子项垂直对齐，不写时垂直居中（出处：鸿蒙 SDK 的 ets/component/row.d.ts，RowAttribute.alignItems；ts-container-row.md，alignItems）
- VerticalAlign.Top：顶部对齐：对应 Compose Row 不写对齐时的 Top（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，VerticalAlign.Top）
- Compose Row 的 verticalAlignment 默认 Top：两边默认不同，源端没写时目标要显式写 Top（出处：卡里修好并验证过）
未核实：case-d54a9506e30031090325 里 Row 这一项没有上机验证，出自建议
来源：2 张卡，1 个应用
- case-83dafcc0eaba740bd9c0（Jetsnack）：做法第 1 步 ← 建议 4、诊断；取值 3 ← 建议 4、诊断
- case-d54a9506e30031090325（Jetsnack）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
