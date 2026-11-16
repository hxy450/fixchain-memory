# 单视图对 parent 居中、兄弟挂其下时，目标用 RelativeContainer 加 alignRules

审的是：代码
触发（任一种）：
- 读到：ConstraintLayout 子视图四向约束都是 parent，兄弟只有 layout_constraintTop_toBottomOf 指向它；写错的样子：目标用 Column().justifyContent(FlexAlign.Center) 包住两者整组居中，注释写“居中链”
适用范围：实现阶段落定 ConstraintLayout 迁移的容器时，包括规格已写成 Column 组居中的情形
做法：
- 被居中视图：RelativeContainer 内 .id('x').alignRules({ center: { anchor: '__container__', align: VerticalAlign.Center }, middle: { anchor: '__container__', align: HorizontalAlign.Center } })
- 兄弟视图：.alignRules({ top: { anchor: 'x', align: VerticalAlign.Bottom }, middle: { anchor: '__container__', align: HorizontalAlign.Center } })，源端 marginTop 写成 .margin({ top: 同值 vp })
- spec 把单视图居中写成组居中时，对照源 XML 的 constraint 属性按源约束实现，并在转换报告里标出与 spec 的冲突
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- alignRules(value: AlignRuleOption): T：RelativeContainer 子组件的对齐规则（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.alignRules）
- AlignRuleOption 的 center?: VerticalAlignParam、middle?: HorizontalAlignParam、top?: VerticalAlignParam：垂直居中、水平居中、顶部对齐各用一项，参数是 { anchor, align }（出处：鸿蒙 SDK 的 ets/component/common.d.ts，AlignRuleOption）
- RelativeContainer 的标识是 __container__；没设 id 的组件不能被其他组件引用为锚点：被兄弟引用的视图必须写 .id(...)（出处：arkts-layout-development-relative-layout.md，设置锚点）
- 改成 RelativeContainer 后被居中视图中心回到内容区 50%（Column 组居中时偏到约 44%）：卡里复测的结果（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-6448a485599bfc0740c6（Dice Roller）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 诊断；做法第 3 步 ← 建议 3；取值 4 ← 诊断
