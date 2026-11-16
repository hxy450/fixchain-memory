# Box 子项有 Modifier.align 非默认位置时，Stack 子项写 .position 实际定位

审的是：代码
触发（任一种）：
- 读到：源 Compose Box 里子项写 Modifier.align(Alignment.BottomCenter) 等非左上位置；规格写「底部居中」「Stack 底部对齐」；写错的样子：目标 Stack({ alignContent: Alignment.TopStart }) 里这个子项只有 width / zIndex，没有 .position / .align / .markAnchor，底部定位只留在注释或转换报告里
适用范围：把 Compose Box 叠层迁成 ArkUI Stack、子项靠 Modifier.align 定位时
做法：
- 逐个核对源 Box 子项的 Modifier.align，非默认位置的子项写成实际属性（.position / .align / .markAnchor），如底部通栏写 .position({ left: 0, bottom: 0 })
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- position(value: Position | Edges | LocalizedEdges): T：相对父组件的绝对定位；传 Edges 时按 top / left / bottom / right 定位（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.position）
- Edges { top?, left?, bottom?, right?: Dimension }（@since 12）：写 { left: 0, bottom: 0 } 即贴父容器左下（出处：鸿蒙 SDK 的 ets/component/units.d.ts，Edges）
- StackOptions.alignContent 默认 Alignment.Center：Stack 只给所有子项一个统一对齐，单个子项要另写定位（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackOptions.alignContent）
- markAnchor(value: Position | LocalizedPosition): T：同族接口：定位锚点，配合 position 使用（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.markAnchor）
- 底部栏 Column 加 .position({ left: 0, bottom: 0 }) 后贴底：修复时用的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-83dafcc0eaba740bd9c0（Jetsnack）：做法第 1 步 ← 建议 1、诊断；取值 5 ← 诊断
