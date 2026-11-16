# 源方法里对框架对象的调用逐条落到目标，缺一条在报告列明，不以「AC 已覆盖」代替

审的是：代码
触发（任一种）：
- 读到：源方法里调了抽屉开关：getDrawerToggle().setDrawerIndicatorEnabled(false)，或重建菜单的方法末尾调 syncState()；写错的样子：目标方法里没有对应调用，注释写「…由 AC 验收覆盖」或只留 FWD-REF 记号；重建菜单的方法末尾缺 syncState，指示器从没被禁用
- 读到：源 onBackPressed 有多个分支：开关抽屉、关 FAB（为假时）、复位标志、super.onBackPressed()；写错的样子：目标 onBackPress() 只处理抽屉开关两个分支，其余直接 return false，关 FAB 和标志复位用注释推给别处
适用范围：实现阶段把源端 Activity / Fragment 里调用框架对象的方法迁到目标页面或外壳时
做法：
- 源方法里每个框架调用逐条落到目标：setDrawerIndicatorEnabled(false) 落成外壳上的指示器启用态（如 drawerIndicatorEnabled = false，导航位按它渲染），syncState() 落成按当前开合态同步指示器（如 syncState(opened)）
- onBackPressed 的每个分支（关 FAB、复位标志、交给上一级）都在 onBackPress() 里照顺序写出，返回 true 表示页面自己处理
- 有一条落不了的在报告里列明，不用「AC 的验收描述已覆盖」代替源调用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onBackPress?(): void | boolean：@Entry 组件的返回键回调；true 表示页面自己处理，false 或不返回走默认返回逻辑（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.onBackPress）
- onBackPressed(callback: () => boolean): NavDestinationAttribute：同族接口：Navigation 子页的返回回调（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onBackPressed）
- 返修加外壳的 drawerIndicatorEnabled 与 controller.syncState(opened)，列表导航位按指示器态渲染：两个抽屉开关调用的落法（出处：卡里修好并验证过）
未核实：AppCompatDelegate 返回链的内部顺序属库内行为，卡里没核到，本机也只有编译产物
来源：1 张卡，1 个应用
- case-aa81c21ff3eaca257ba4（omni-notes-hmos）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；做法第 3 步 ← 建议 3；取值 3 ← 诊断
