# 窗口常亮的验收只有进入页面不熄屏时，补一条离开页面后按系统超时熄屏

审的是：规格
触发（任一种）：
- 读到：源端 Activity 自身窗口上 getWindow().addFlags(FLAG_KEEP_SCREEN_ON)，没有清除代码；写错的样子：验收条目的设备判据只有「进入该页后屏幕不自动熄灭」，缺离开该页（返回主菜单、进设置等）之后的熄屏判据
适用范围：规格里为源端单个 Activity 窗口上的常亮写验收条目时
做法：
- 验收加一条：「离开该页（如返回主菜单）后按系统超时熄屏」，和「进入该页后不熄屏」配成一对
- 判据的查法写进条目：离开该页后用 hidumper -s PowerManagerService 看应用持有的 windowLock 已释放
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- hidumper -s PowerManagerService：查电源管理服务里应用持有的 windowLock；只开不关时回到上一页后仍持有（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-42fb1284b2edc857b78b（Privacy Friendly 2048）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；取值 1 ← 诊断、建议 2
