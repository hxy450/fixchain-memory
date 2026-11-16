# 源端在 onActionItemClicked 入口统一门控时，目标在分发入口统一接门控，不只接个别分支

审的是：代码
触发（任一种）：
- 读到：源端 ActionMode.Callback.onActionItemClicked 入口对除一个例外列表外的所有动作，先调同一个门控方法（如密码校验），通过后再分发；写错的样子：目标的批量动作分发函数（switch / case）只在删除、清空等个别 case 里调门控，其余动作直接执行；或照页面 FWD-REF 占位注释列出的局部分支接线
适用范围：收口接线阶段，源端在 ActionMode 或基类回调入口统一做门控、目标按切片分开实现分发时
做法：
- 对照源回调函数逐个动作核对目标分发表：在分发函数入口统一调门控，例外列表照抄源端（源端免门控的动作才跳过），通过后再进各 case
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- boolean onActionItemClicked(ActionMode mode, MenuItem item)：用户点了上下文操作栏上的动作时回调：源端所有批量动作都经过这个入口，门控放在这里就覆盖全部动作（出处：android.view.ActionMode.Callback#onActionItemClicked）
- 在分发入口统一接门控后，原来不过门的归档、移入回收站、改分类等批量动作都要先过门控：返修后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端门控的适用范围和例外动作：源工程 Java/Kotlin 里 ActionMode.Callback 的 onActionItemClicked 实现（常在 Fragment 或基类里）；看门控调用之前的判断：列出被排除的菜单 id，其余全部动作都要过门控
未核实：卡里的环境是 HarmonyOS 6.1.1（API 24）
来源：1 张卡，1 个应用
- case-3ceab2782faa0c414d88（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；取值 2 ← 诊断
