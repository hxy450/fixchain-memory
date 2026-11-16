# Stack 里可点击控件之后有盖住它的全屏同级节点时，壳设 Transparent 或控件提高 zIndex

审的是：代码
触发（任一种）：
- 读到：Compose Box 里返回按钮（IconButton 一类）和后面的子项叠放，后面的子项只占自己的区域、不和按钮重叠；写错的样子：目标 Stack 里返回按钮之后声明了 width('100%').height('100%') 的同级容器，没有 hitTestBehavior(HitTestMode.Transparent)，按钮也没有更高的 zIndex
适用范围：重排 ArkUI Stack 叠放层、可点击覆盖控件之后还有同级节点时
做法：
- 按声明顺序检查每个可点击覆盖控件之后的同级节点，区域覆盖到它的就处理
- 全屏壳确实要留时给壳写 .hitTestBehavior(HitTestMode.Transparent)；或者让返回按钮最后声明，或写 .zIndex(<大于壳的值>)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- hitTestBehavior(value: HitTestMode): T，默认 HitTestMode.Default：默认时自己和子节点响应触摸，被它遮住的兄弟节点收不到（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.hitTestBehavior）
- HitTestMode.Transparent：自己和子节点响应，同时放行被它遮住的其他节点（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，HitTestMode.Transparent）
- HitTestMode.None：自己不响应、子节点响应（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，HitTestMode.None）
- zIndex(value: number): T：同一容器里兄弟组件的层级，值大的在上（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.zIndex）
- 给返回按钮加 .zIndex(3) 后顶部返回可点：返修的写法（出处：卡里修好并验证过）
未核实：hitTestBehavior(HitTestMode.Transparent) 卡里没有上机验证，返修用的是 zIndex
来源：1 张卡，1 个应用
- case-7d423b2bf98cdaabda82（Jetsnack）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 2、诊断；取值 5 ← 诊断
