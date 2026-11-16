# 用 Scroll 承接 NestedScrollView 时显式写 .align(Alignment.Top)

审的是：代码
触发（任一种）：
- 读到：源布局用 NestedScrollView（或 ScrollView）承接页面内容，内容从顶部排起；写错的样子：目标 Scroll 没写 .align(Alignment.Top)；内容短于视口时整列下沉，头部脱离工具栏
适用范围：把 NestedScrollView / ScrollView 迁成 ArkUI Scroll，且内容可能短于视口时
做法：
- Scroll 显式写 .align(Alignment.Top)
- 做了可能让内容短于视口的改动（如收窄头部高度、去掉 height('100%')）后，复查 Scroll 子项的对齐
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- align(value: Alignment): T，默认 Alignment.Center：Scroll 不写 align 时内容在绘制区里居中（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.align）
- Scroll 的子节点矮于视口时默认居中；补上 .align(Alignment.Top) 后贴顶：上机看到的默认行为和修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-9058ac868b6feb3a04e0（AntennaPod）：做法第 1 步 ← 建议 5、诊断；做法第 2 步 ← 建议 5；取值 2 ← 诊断
