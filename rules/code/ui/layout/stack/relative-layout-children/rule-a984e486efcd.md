# Stack 叠层按源布局声明顺序排 z 序，排不了时补 zIndex

审的是：代码
触发（任一种）：
- 读到：RelativeLayout 里半透明按钮条先声明，圆角装饰和封面卡后声明（后声明的画在上面）；写错的样子：Stack 里把按钮条放到最后声明，压住封面下沿和圆角装饰，也没有 zIndex
适用范围：把 RelativeLayout / FrameLayout 的叠放子 View 迁成 ArkUI Stack 子组件时
做法：
- 按源布局的声明顺序复核 Stack 子组件顺序（后声明者在上）；无法按序排列时，给应在上层的子组件加 .zIndex(1)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Stack 的子元素依次入栈，后一个子元素覆盖前一个：声明顺序就是 z 序，和 RelativeLayout 相同（出处：arkts-layout-development-stack-layout.md，概述）
- zIndex(value: number): T；值越大显示层级越高：改不了顺序时用它把子组件提到上层（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.zIndex；arkts-layout-development-stack-layout.md，Z序控制）
来源：1 张卡，1 个应用
- case-4f627840679361f165a3（AntennaPod）：做法第 1 步 ← 建议 2、诊断
