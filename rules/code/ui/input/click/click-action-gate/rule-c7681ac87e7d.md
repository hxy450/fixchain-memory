# 源码在确认对话框 onPositive 后才执行的破坏性操作，目标也先弹确认再执行

审的是：代码
触发（任一种）：
- 读到：源码分支里 MaterialDialog.Builder(...).onPositive(...) 或 setPositiveButton 的回调里才执行删除、清空等操作；写错的样子：目标的动作分支直接把数据清空（如赋值 `= []`），没有先弹确认弹窗
适用范围：迁移源端带确认的破坏性动作（删除、清空、重置）时
做法：
- 读到源码里这个分支的对话框构造再实现：先弹确认弹窗，确认按钮（对应 onPositive / setPositiveButton）的回调里才执行操作，按钮集合照源码
针对本应用要查的：
- 动作分支有没有确认对话框：源工程里处理该菜单项或动作的 Java / Kotlin 分支，按 onPositive、setPositiveButton 找；回调里执行的操作就是确认后才做的那一步
来源：1 张卡，1 个应用
- case-ac1b65b76f72e7be3fa6（omni-notes-hmos）：做法第 1 步 ← 建议 5、诊断
