# FlowRow 套 FlowRow 再跟尾随元素时，不用嵌套 wrap Flex，改用贪心换行自定义布局

审的是：代码
触发（任一种）：
- 读到：Compose 的 FlowRow(SpaceBetween) { FlowRow(spacedBy 间距){ 左组 } ; 尾随元素 }，放得下时左组和尾随元素同一行两端对齐；写错的样子：写成外层 Flex({ wrap: FlexWrap.Wrap, justifyContent: FlexAlign.SpaceBetween }) 套内层 wrap Flex，内层再加 .flexGrow(1)；尾随元素总是独占一行
适用范围：Compose FlowRow 两端对齐、里面嵌一个 FlowRow 再跟一个尾随元素，迁成 ArkUI 时
做法：
- 新建自定义布局组件：在 onMeasureSize 里用 child.measure(constraint) 按各子项内容宽度测量，在 onPlaceChildren 里从左往右贪心排放、放不下才换行；尾随元素与左组放得下时同一行并靠右
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onMeasureSize?(selfLayoutInfo: GeometryInfo, children: Array<Measurable>, constraint: ConstraintSizeOptions): SizeResult：自定义组件测量子项并返回自身尺寸的回调（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.onMeasureSize；ts-custom-component-layout.md，onMeasureSize）
- onPlaceChildren?(selfLayoutInfo: GeometryInfo, children: Array<Layoutable>, constraint: ConstraintSizeOptions): void：自定义组件给每个子项定位置的回调（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.onPlaceChildren；ts-custom-component-layout.md，onPlaceChildren）
- measure(constraint: ConstraintSizeOptions): MeasureResult；layout(position: Position): void：Measurable 测量子项、Layoutable 摆放子项（出处：鸿蒙 SDK 的 ets/component/common.d.ts，Measurable.measure / Layoutable.layout）
- 嵌套 wrap Flex + 内层 flexGrow(1) 让尾随元素总是独占一行；改成贪心换行布局后恢复：错误写法的表现和修法（出处：卡里修好并验证过）
未核实：卡里没写自定义布局用的是哪组接口，onMeasureSize/onPlaceChildren 是按 ArkUI 自定义布局的声明写的；嵌套 wrap Flex 在 ArkUI 中具体的测量原因（容器默认撑满主轴还是 flexGrow）卡里没复现
来源：1 张卡，1 个应用
- case-bcc79fa7d3d15ef4a8b2（jerboa）：做法第 1 步 ← 建议 3、诊断；取值 4 ← 诊断
