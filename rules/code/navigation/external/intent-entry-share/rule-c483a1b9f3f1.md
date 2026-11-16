# 无 UI 的 trampoline Activity 接进入口时保留前后台状态和透明模态窗口，不只加一行分发

审的是：代码
触发（任一种）：
- 读到：源端通知按钮的 PendingIntent 指向一个无 UI、透明、独立任务的 trampoline Activity 来分派动作；写错的样子：EntryAbility.onCreate / onNewWant 只各加一行按 want 分发的调用，和主入口共用；没有前后台状态跟踪，也没有取消、过去时刻时的模态窗口
适用范围：实现阶段把源端无 UI 的透明 trampoline Activity 的动作分派接进目标入口 Ability 时
做法：
- 在 EntryAbility 里跟踪前后台：onForeground() 记为前台，onBackground() 记为后台并释放 trampoline 用到的窗口和资源
- 动作需要交互时（如取消、选的时间已过去），弹透明模态窗口拦截，前台和后台分别按源端 trampoline 的语义处理；onNewWant(want, launchParam) 和 onCreate 都走这条分派
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void：已启动的 UIAbility 再次被拉起时回调（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onNewWant）
- onForeground(): void；onBackground(): void：前后台切换回调，用来跟踪前台状态和释放（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onForeground、UIAbility.onBackground）
- 返修给动作处理和 EntryAbility 加前台状态跟踪，以及取消 / 过去时刻的透明模态窗口：trampoline 语义的落法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端 trampoline 的拦截和前后台语义：源工程 AndroidManifest 里该 Activity 的 theme、taskAffinity、excludeFromRecents，以及它的 onCreate / onResume / onPause；读出它在什么情况下弹窗、什么情况下直接 finish，前后台各自怎么处理，逐条对到 EntryAbility 的回调
来源：1 张卡，1 个应用
- case-97530cfa88ec30cb186c（omni-notes-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4、诊断；取值 3 ← 诊断
