# 靠 layoutWeight 填满居中的根节点移进 Refresh 后，改成 height('100%')

审的是：代码
触发（任一种）：
- 读到：空态或引导 builder 的根 Column 用 .layoutWeight(1) + .justifyContent(FlexAlign.Center) 在 Column 父级里填满剩余空间并居中，现在要放进 Refresh 的内容；写错的样子：移进 Refresh { ... } 后根 Column 仍是 .layoutWeight(1)，没有 .height('100%') 之类的显式高度
- 读到：封装刷新组件的 build() 是 Refresh(...) { this.content() }，内容经 @BuilderParam content 注入；写错的样子：传给 content 的 builder 根节点用 .layoutWeight(1) 撑高
适用范围：把已有内容 builder 移进非 Row/Column/Flex 的父级（Refresh、Scroll、Stack、List 等封装组件）时，内容根节点的高度约束
做法：
- 先看封装组件 build() 里 content 的直接父组件；不是 Row/Column/Flex 时，把根节点的 .layoutWeight(1) 换成 .height('100%')，居中仍交给 .justifyContent(FlexAlign.Center)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- layoutWeight(value: number | string): T，仅在 Row / Column / Flex 布局中生效：父级是 Refresh 时 layoutWeight 不起作用，根节点高度缩成内容高度（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.layoutWeight；ts-universal-attributes-size.md，layoutWeight）
- Refresh 支持单个子组件：注入的 builder 根节点就是 Refresh 的直接子组件（出处：ts-container-refresh.md，子组件）
- 根 Column 由 .layoutWeight(1) 改成 .height('100%')、保留 .justifyContent(FlexAlign.Center) 后，空态在 Refresh 内恢复垂直居中：修好后的写法和行为（出处：卡里修好并验证过）
未核实：卡里的行为出自 HarmonyOS 5.0.4(16)，本机按 API 23 声明核实
来源：1 张卡，1 个应用
- case-a79794249bd5f8bd96fa（五星智投）：做法第 1 步 ← 建议 1、诊断；取值 3 ← 诊断
