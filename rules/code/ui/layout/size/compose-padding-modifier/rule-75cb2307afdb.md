# Compose 占满父宽且背景外带水平 padding 时，不在同一节点写 '100%' 宽加左右 margin

审的是：代码
触发（任一种）：
- 读到：Compose 容器修饰链在 clip / background 之前有 padding(horizontal = N.dp)，自身 fillMaxWidth 或被 fillMaxWidth 的子项撑满；写错的样子：同一节点写 .width('100%') 加 .margin({ left: N, right: N })，卡片右移、右侧贴边或被裁
- 读到：Button(Modifier.fillMaxWidth().padding(horizontal = N.dp)) 这类包装组件的 modifier；写错的样子：只写了 .width('100%')（或只有 .margin({ top })），水平 N 的内缩整个丢了
适用范围：把 Compose 里水平占满父级、背景外侧带水平 padding 的容器或按钮翻译成 ArkUI 宽度和边距时
做法：
- 可见宽 = 父宽 − 两侧之和：写成外层容器 .padding({ left: N, right: N }) 加内层 .width('100%')，或在带 margin 的节点上写 .width('calc(100% - 2N vp)') 加 .margin({ left: N, right: N })（例：N = 10 时 'calc(100% - 20vp)'）
- 写完搜同一修饰链里 width('100%') 与 margin({ left / right }) 的组合，并对照源端逐个确认水平内缩都已写出
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- width(value: Length): T：组件宽度；宽度大于父容器时会画出父容器范围（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.width）
- width 从 API 10 起支持 calc，运算符与数值之间要用空格隔开：'calc(100% - 20vp)' 合法，'calc(100%-20vp)' 不行（出处：ts-universal-attributes-size.md，width 和页首说明）
- 在 Row、Column、Flex 交叉轴上布局时，子组件交叉轴的大小与 margin 的和为整体：margin 在百分比宽之外再占位，'100%' 加左右 margin 会溢出（出处：ts-universal-attributes-size.md，margin）
- margin(value: Margin | Length | LocalizedMargin): T，默认 0，单位 vp：外边距的签名（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.margin）
- 卡片改为 calc(100% - 20vp) 加 margin 左右 10，按钮改为 calc(100% - 40vp) 加 margin 左右 20 后，左右边距对称、不再溢出：修好后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-4b80089e571caa856066（GameOfLife）：做法第 1 步 ← 建议 1、建议 2；做法第 2 步 ← 建议 2；取值 5 ← 诊断、建议 2
