# 源 onCreateContextMenu 调 setHeaderTitle 时，目标菜单卡顶部显示被长按条目的标题

审的是：代码
触发（任一种）：
- 读到：onCreateContextMenu 里有 menu.setHeaderTitle(...)，参数是被长按条目的标题；写错的样子：目标菜单卡没有标题 Text，或宿主传给菜单卡的标题参数是空串 ''，注释称源端没有 setHeaderTitle
适用范围：源上下文菜单带标题（ContextMenu.setHeaderTitle），迁成 ArkUI 自绘菜单卡时，含子类调 super.onCreateContextMenu 继承来的标题
做法：
- 菜单卡顶部放一行标题 Text，内容取被长按条目的标题（对应 setHeaderTitle 的参数）；每个宿主（整页、区段）都把标题传进去，子类走 super.onCreateContextMenu 的也一样
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ContextMenu setHeaderTitle(CharSequence title)：设置上下文菜单头部的标题（出处：android.view.ContextMenu#setHeaderTitle）
- 菜单标题取条目标题，整页和区段宿主都补上：修复后保留的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-3ca3658855acd903c4ca（AntennaPod）：做法第 1 步 ← 建议 3、诊断；取值 2 ← 诊断
