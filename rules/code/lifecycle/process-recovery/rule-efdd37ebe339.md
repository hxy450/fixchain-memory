# 要恢复页面栈时，UIAbility 开启备份恢复并在 APP_RECOVERY 时恢复窗口舞台

审的是：代码
触发（任一种）：
- 读到：规格要求进程回收后恢复页面栈，或源宿主用 rememberNavController + NavHost / onCreate(savedInstanceState)；写错的样子：EntryAbility 的 onCreate 里没有 this.context.setRestoreEnabled(true)；launchReason 为 APP_RECOVERY 时没有 restoreWindowStage，也没有 onWindowStageRestore，onWindowStageCreate 每次都直接 loadContent
适用范围：实现阶段装配 UIAbility，需要进程被系统回收后恢复页面栈时（setRestoreEnabled 声明 @since 14）
做法：
- onCreate 里调用 this.context.setRestoreEnabled(true)，在 onForeground 之前
- launchParam.launchReason === AbilityConstant.LaunchReason.APP_RECOVERY 时调用 this.context.restoreWindowStage(new LocalStorage())，并实现 onWindowStageRestore(windowStage)；只开 setRestoreEnabled 加 recoverable 不够
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setRestoreEnabled(enabled: boolean): void：UIAbilityContext 上设置是否启用后台回收后的恢复（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.setRestoreEnabled）
- setRestoreEnabled 要在应用初始化阶段（onForeground 之前）调用，比如 UIAbility 的 onCreate：调用时机（出处：ability-recover-guideline.md，接口说明）
- AbilityConstant.LaunchReason.APP_RECOVERY = 4：应用从故障中恢复时自动拉起的启动原因（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.AbilityConstant.d.ts，LaunchReason.APP_RECOVERY）
- restoreWindowStage(localStorage: LocalStorage): void：UIAbilityContext 上恢复窗口舞台数据（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.restoreWindowStage）
- onWindowStageRestore(windowStage: window.WindowStage): void：UIAbility 上窗口舞台恢复时的回调（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onWindowStageRestore）
- removeMissionAfterTerminate 为 true，或设备不支持任务保留（如 PC/2in1）时，备份恢复不生效：机制的前提（出处：ability-recover-guideline.md，约束限制）
- 只开 setRestoreEnabled 加 recoverable 时，APP_RECOVERY 拉起后仍不恢复；加上 restoreWindowStage(new LocalStorage()) 和 onWindowStageRestore 后恢复：修好的做法（出处：卡里修好并验证过）
未核实：卡里环境是 6.1.1(24)，本机按 API 23 的声明核对
来源：1 张卡，1 个应用
- case-30dbf63ea8a03d315607（Cofi）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 7 ← 诊断
