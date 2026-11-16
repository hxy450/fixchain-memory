# 从顶部排的可变长度纵向列表用 List；Scroll 包 Column 时设 .align(TopStart)

审的是：代码
触发（任一种）：
- 读到：Compose LazyColumn(Modifier.fillMaxSize(), verticalArrangement = Arrangement.spacedBy(...)) 从顶部排列，项数可能不足一屏；写错的样子：写成 Scroll() { Column() { ForEach(...) }.width('100%') }.layoutWeight(1)，Scroll 没设 .align，Column 也没撑满高度
- 读到：RecyclerView 纵向列表，项数可能不足一屏；写错的样子：用 Scroll() 包 Column() + ForEach，Scroll 占满剩余空间（layoutWeight(1) 或固定高度）却没设 .align
适用范围：目标滚动容器占满剩余空间、列表项数量可能不足一屏的纵向列表
做法：
- 按源列表语义优先写成 List() { ForEach / LazyForEach(… ListItem …) }，列表项默认从顶部排列
- 若用 Scroll 包 Column，给 Scroll 显式加 .align(Alignment.TopStart)（或 Alignment.Top）；只给 Column 加 justifyContent(FlexAlign.Start) 不够，Column 没设高度时主轴对齐不起作用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- align(value: Alignment): T，默认值 Alignment.Center，在 Scroll 等组件上生效：Scroll 不设 align 时，比视口短的子内容居中显示（出处：ts-universal-attributes-location.md，align；鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.align）
- Scroll 加 .align(Alignment.TopStart) 后内容从顶部排列：起作用的是 Scroll 的对齐设置，Column 的 justifyContent 不起作用（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-918a52ecd2f381adbd7d（青商城）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 2 ← 诊断
