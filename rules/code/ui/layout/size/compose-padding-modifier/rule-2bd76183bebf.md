# Compose 内距修饰符在 heightIn(min) 之前时，minHeight 要加上这段内距

审的是：代码
触发（任一种）：
- 读到：Row(modifier = Modifier.navigationBarsPadding().then(…).heightIn(min = N.dp))：navigationBarsPadding() 在 heightIn 之前，最小高度作用在内距之内；写错的样子：.constraintSize({ minHeight: N }).padding({ bottom: 导航条避让值 })，minHeight 没加上底部 padding，内容区不足 N
适用范围：Compose 修饰符链里内距（navigationBarsPadding、padding）先于 heightIn / sizeIn 的组件迁成 ArkUI 时
做法：
- 写成 .constraintSize({ minHeight: N + 底部 padding }).padding({ bottom: 底部 padding })：ArkUI 的尺寸含 padding，最小高度要把内距加进去
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 设置了固定的 width 和 height 时，组件内容的大小就是 width 和 height 减去 padding 和 border：ArkUI 组件尺寸包含 padding，constraintSize 的 minHeight 同样含内距（出处：arkts-layout-development-overview.md，布局元素的组成）
- constraintSize(value: ConstraintSizeOptions): T：组件布局时的尺寸范围（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.constraintSize）
- minHeight 改成 底栏高度 + 底部避让值 后与安卓一致：修好后的写法（出处：卡里修好并验证过）
- constraintSize(value: ConstraintSizeOptions): T：同族接口：安全控件（SecurityComponentMethod）的尺寸约束（出处：鸿蒙 SDK 的 ets/component/security_component.d.ts，SecurityComponentMethod.constraintSize）
- itemConstraintSize(value: ConstraintSizeOptions): WaterFlowAttribute：同族接口：WaterFlow 子项的尺寸约束（出处：鸿蒙 SDK 的 ets/component/water_flow.d.ts，WaterFlowAttribute.itemConstraintSize）
未核实：heightIn 和内距修饰符的先后语义出自 Compose 库代码，本机没有源码，按卡写
来源：1 张卡，1 个应用
- case-cfab70f115f2d290e44a（Jetsnack）：做法第 1 步 ← 诊断；取值 3 ← 诊断
