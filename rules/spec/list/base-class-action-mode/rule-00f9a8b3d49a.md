# 覆盖 lint 报基类未锚定时读完整实现再写 AC，不并进无关组只写计数语义

审的是：规格
触发（任一种）：
- 读到：覆盖 lint 把共享基类文件报为未锚定；grep 它的声明已能看到 onDestroyActionMode(ActionMode) 等 ActionMode 信号；写错的样子：基类被并进无关的工具类组 AC，只写一句计数语义、判:unit，没有它的可见行为（操作栏、菜单、标题）
适用范围：规格阶段为消除覆盖 lint 给未锚定的基类文件补锚点时
做法：
- 先读基类完整实现；带 ActionMode、菜单或标题等可见行为的，按行为写成 UI AC 并锚到使用它的功能，不并进无关的工具类组，也不只写 unit 计数语义
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- public void onDestroyActionMode(ActionMode mode)：声明里出现它就说明基类会弹出上下文操作栏，有可见行为要写（出处：android.view.ActionMode.Callback#onDestroyActionMode）
来源：1 张卡，1 个应用
- case-997587966a65e79790b5（AntennaPod）：做法第 1 步 ← 建议 2、诊断
