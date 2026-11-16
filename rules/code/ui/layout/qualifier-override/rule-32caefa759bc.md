# 合并 layout 与 layout-land 时逐控件逐属性比两份 XML，每个差异都有方向分支或覆盖说明

审的是：代码
触发（任一种）：
- 读到：源 res/layout/ 和 res/layout-land/ 下有同名布局，同一 android:id 的 background、textSize、margin、layout_weight 不同；写错的样子：目标组件对 layoutWeight、margin、fontSize 做了 isLandscape 分支，背景形状（borderRadius / backgroundColor）却没有分支，转换报告也没说明被哪段运行时代码覆盖
适用范围：目标端用一个组件按方向条件合并源端多个布局变体时
做法：
- 按 android:id 逐控件 diff 两份 XML 的每个属性（background、textSize、margin、layout_weight 等）
- 每个差异要么写成方向条件分支（如 .borderRadius(this.isLandscape ? 0 : <半径>)、.backgroundColor(…)），要么在转换报告里注明被哪段运行时代码覆盖
针对本应用要查的：
- 两个布局变体的属性差异：源工程 res/layout/ 与 res/layout-land/（及其他限定词变体）下的同名布局 XML；按 android:id 配对控件，逐属性比较，列出每个不同的属性及两边的值
来源：1 张卡，1 个应用
- case-14fd5b307673d523bead（Privacy Friendly 2048）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
