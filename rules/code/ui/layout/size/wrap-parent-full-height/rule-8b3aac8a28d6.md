# 被嵌入子组件的源布局根和状态容器是 wrap_content 时，根和各状态视图不写 height('100%')

审的是：代码
触发（任一种）：
- 读到：将被宿主嵌入的子组件（规格写 `page_type=sub_component`，源端是 Fragment 布局）：根节点、内层容器和空态容器都是 android:layout_height="wrap_content"；写错的样子：@ComponentV2 / @Component 的 build() 根 Column，以及 loading / empty / error / 列表态的外层写了 .height('100%')
适用范围：把将被宿主页面嵌入的子组件转成自定义组件时，根节点和各状态视图的高度约束（源端对应节点是 wrap_content）
做法：
- 源端 wrap_content 的根节点和 loading / empty / error 态，目标不写 .height(...)，让根 Column 和各状态视图按内容取高
- 空态要居中时，用图片固有尺寸（或源端写死的 dp 尺寸）加文字撑出内容高度，或写 .constraintSize({ minHeight: <源端最小高度> })，不用百分比高度
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- height(heightValue: Length | LayoutPolicy): T：不写时组件取装下内容所需的高度，比父容器高时画出父容器范围（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.height）
- 百分比尺寸参考最近设置了固定大小的祖先节点的尺寸：子组件放进 Scroll 里无高度的 Column 时，100% 高度会落到更上层定了高的祖先（如视口）上（出处：ts-universal-attributes-size.md，尺寸设置（开头的说明））
- constraintSize(value: ConstraintSizeOptions): T，默认 {minWidth: 0, maxWidth: Infinity, minHeight: 0, maxHeight: Infinity}：空态需要最小高度时用 minHeight，不用百分比（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.constraintSize）
- 嵌进 Scroll → 无高度 Column 的子组件根节点 height('100%') 解析成视口高度，空态卡几乎占满内容区、后续区块被挤出首屏：出错时看到的样子（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-821ade66a5ad47cdea22（实时公交）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 4 ← 诊断
