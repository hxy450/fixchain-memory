# 进程回收后重建任务栈的替代决策，触发条件只写系统回收且任务仍在

审的是：规格
触发（任一种）：
- 读到：源端用 `TaskStackBuilder.addNextIntentWithParentStack` 或 `PARENT_ACTIVITY` 组成任务栈、没有显式保存导航，靠框架在进程回收后重建；LAUNCHER 是按首启分流的 Splash；上游规格已把冷启动回起始页与回收后栈恢复分开写；写错的样子：规格或决策台账的 PD 写成「冷启动（含回收后重入）恢复至最后路由」，把冷启动和回收重建合成一条，没写按退出原因判定
适用范围：规格提取阶段为「进程回收后重建任务栈」这一平台行为写替代决策和目标端恢复契约时
做法：
- 触发条件写成「仅系统回收进程且任务仍在时恢复」；强停、从最近任务划掉、覆盖安装、崩溃后任务已清空，再启动走 LAUNCHER 的分流
- 写明目标端判定：EntryAbility.onCreate 里 launchParam.lastExitReason 为 AbilityConstant.LastExitReason.PERFORMANCE_CONTROL 或 RESOURCE_CONTROL 才恢复，其余进入口页
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 强停后退出原因是 NORMAL，覆盖安装后是 UPGRADE；只放行 PERFORMANCE_CONTROL / RESOURCE_CONTROL 后行为与源端一致：按退出原因区分回收重建与普通冷启动（出处：卡里修好并验证过）
- LastExitReason.NORMAL = 2（用户关闭）、PERFORMANCE_CONTROL = 6（系统性能问题，如内存不足）、RESOURCE_CONTROL = 7（不当使用系统资源）、UPGRADE = 8（更新）：退出原因枚举里与恢复判定有关的取值（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.AbilityConstant.d.ts，AbilityConstant.LastExitReason）
- lastExitReason: LastExitReason：LaunchParam 上的上次退出原因（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.AbilityConstant.d.ts，AbilityConstant.LaunchParam.lastExitReason）
来源：1 张卡，1 个应用
- case-a8413b6eae04f3be7d9d（Privacy Friendly 2048）：做法第 1 步 ← 建议 1、建议 3；做法第 2 步 ← 建议 1；取值 1 ← 诊断
