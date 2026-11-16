# EntryAbility.onCreate 把 lastExitReason 交给路由恢复，只在系统回收时恢复

审的是：代码
触发（任一种）：
- 读到：规格或台账的 PD 要求进程回收后恢复路由栈；写错的样子：`EntryAbility.onCreate(want, launchParam)` 没把 `launchParam` 交给恢复逻辑，恢复函数每次冷启动都无条件读上次路由
适用范围：入口装配阶段按进程回收恢复的决策实现冷启动路由恢复时
做法：
- onCreate 里把 launchParam.lastExitReason 交给恢复逻辑；只有 reason === AbilityConstant.LastExitReason.PERFORMANCE_CONTROL 或 RESOURCE_CONTROL 时恢复，其余进入口页
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void：UIAbility 创建时拿到启动参数（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onCreate）
- LastExitReason.NORMAL = 2、PERFORMANCE_CONTROL = 6、RESOURCE_CONTROL = 7、UPGRADE = 8：强停是 NORMAL、覆盖安装是 UPGRADE，都不恢复（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.AbilityConstant.d.ts，AbilityConstant.LastExitReason）
- onCreate 传入 launchParam.lastExitReason，只有 PERFORMANCE_CONTROL / RESOURCE_CONTROL 允许恢复：修好的入口写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-a8413b6eae04f3be7d9d（Privacy Friendly 2048）：做法第 1 步 ← 建议 1、建议 4、诊断；取值 3 ← 诊断
