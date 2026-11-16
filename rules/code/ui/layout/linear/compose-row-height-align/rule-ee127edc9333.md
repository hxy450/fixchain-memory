# Compose 横向滚动行译成 Scroll(Horizontal) 时，交叉轴写显式高度，不用 'auto' 也不留空

审的是：代码
触发（任一种）：
- 读到：Compose 里 PrimaryScrollableTabRow、ScrollableTabRow 或 Modifier.horizontalScroll 这类按内容定高的横向滚动行；写错的样子：目标 Scroll 配 .scrollable(ScrollDirection.Horizontal) 却没写 .height(...)，或写成 .height('auto')
适用范围：把源端按内容定高的横向滚动行（Tab 行、标签条）翻译成 ArkUI Scroll + Row 时
做法：
- 给 Scroll 写显式交叉轴尺寸 .height(行高 vp)，行高 = 文本样式的单行文本高 + 单元格上下内边距
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Scroll(Horizontal) 写 .height('auto') 或不写高度时，设备上行高被撑到父级高度；改成 .height(单行文本高 + 上下内边距) 后行高正确：卡里设备实测的行为（出处：卡里修好并验证过）
- width、height 设 auto 表示自适应子组件，只在 Row、Column、RelativeContainer 中成立：'auto' 对 Scroll 不是“随内容定高”（出处：ts-universal-attributes-size.md，height）
- height(value: Length): T，单位 vp：组件高度（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.height）
- scrollable(value: ScrollDirection): ScrollAttribute；ScrollDirection.Horizontal：Scroll 的滚动方向（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，ScrollAttribute.scrollable）
针对本应用要查的：
- 滚动行的高度：源工程里 Tab 文本用的 Compose TextStyle（fontSize、lineHeight）和 Tab 单元格的 Modifier.padding；单行文本高取 lineHeight（没写时按字号的行高），加上下内边距，sp/dp 数值照写成 vp；能上机时用一次布局检查核对
未核实：卡里的设备实测出自 API 12 工程，本机按 API 23 的声明和文档核对
来源：1 张卡，1 个应用
- case-2018daf21990f553ec22（JetLagged）：做法第 1 步 ← 建议 1、诊断；取值 1 ← 诊断
