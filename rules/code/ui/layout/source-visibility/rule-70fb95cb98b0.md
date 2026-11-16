# 源控件是 INVISIBLE 时，目标用 Visibility.Hidden 保留节点，不写条件渲染

审的是：代码
触发（任一种）：
- 读到：布局 XML 里控件写 `android:visibility="invisible"`；写错的样子：目标写成 `if (this.text !== '')` 一类的条件渲染，空时整个节点不出，注释还写「源 XML visibility=invisible」
- 读到：Adapter 里对控件 `setVisibility(View.INVISIBLE)`；写错的样子：目标在该状态下不渲染节点，而不是 `.visibility(Visibility.Hidden)`
适用范围：把安卓控件的显隐迁成 ArkUI 组件的渲染条件时
做法：
- INVISIBLE 写成保留节点加 `.visibility(Visibility.Hidden)`（显示时 `Visibility.Visible`），不写成 `if (...)` 条件渲染
- 只有 GONE 才对应不渲染（`if` 不出或 `Visibility.None`）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- View.INVISIBLE：不可见但仍占布局空间；View.GONE：不可见且不占布局空间：源端两种隐藏的区别（出处：android.view.View#INVISIBLE / android.view.View#GONE）
- visibility(value: Visibility): T：组件的显隐属性（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.visibility）
- Visibility.Hidden：隐藏但参与布局占位；Visibility.None：隐藏且不参与布局、不占位：INVISIBLE 对 Hidden，GONE 对 None（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，Visibility）
未核实：卡里的行为出自 HarmonyOS 6.1.1(24)，核对声明用的是本机 API 23
来源：1 张卡，1 个应用
- case-0a592ebcc5ad2dd158e6（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1
