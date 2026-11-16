# 源端 WindowInsets.navigationBars 的顶部分量迁成 0，不用窗口顶部安全区

审的是：代码
触发（任一种）：
- 读到：源端内边距工具把 WindowInsets.navigationBars 的 calculateTopPadding() 加进顶部内边距；写错的样子：目标把这一项写成窗口顶部避让值（如 windowTopPadding），使用它的页面顶部多算一份避让
适用范围：迁移源端按 WindowInsets.navigationBars 求内边距的工具函数时
做法：
- navigationBars 的顶部分量在手机上没有值，目标写 0，各页按源端的式子把其余项内联求和
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- navTop = 0：修好后设置页顶部不再多一份避让（出处：卡里修好并验证过）
未核实：手机上 navigationBars 没有顶部分量出自卡的修复判断，本机没有 Compose 源码核对
来源：1 张卡，1 个应用
- case-036361d8949e7daf5247（Cofi）：做法第 1 步 ← 诊断；取值 1 ← 诊断
