# 账本批准等价实现的后台计时、通知授权和画中画回退，服务层要真实现，只在运行期降级

审的是：代码
触发（任一种）：
- 读到：决策账本里「经平台后台任务 / 通知抽象保留后台计时语义」「精确 PiP 不可用时用应用内紧凑回退」为 approved；源端用前台 Service、带动作的进度通知、POST_NOTIFICATIONS 或 enterPictureInPictureMode；写错的样子：平台服务的 getStatus 两个分支返回同一个值（`? X : X`）、persist 恒返回 false、没有通知和动作；requestNotificationPermission 直接置授权 false；后台开关打开即复位 false；hasPiPPermission 写死 false
适用范围：决策账本要求等价实现（非延期）的平台能力，在平台服务端口和页面接线里落地时
做法：
- 服务层写出能力检测（PiPWindow.isPiPEnabled()、notificationManager.isNotificationEnabled()）、权限请求（notificationManager.requestEnableNotification(context)）、后台长时任务（backgroundTaskManager.startBackgroundRunning）和带动作的进度通知，状态用 Preferences 持久化
- 只在运行期按实际结果降级，并暴露可观察的原因；「禁止伪造」只约束失败时如实上报，不代表可以不实现
- 自检：在本次解决的标记所在函数里搜恒 false、恒定枚举返回和「? X : X」，再与账本里 approved 的实现类决策逐条对照
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function startBackgroundRunning(context: Context, bgMode: BackgroundMode, wantAgent: WantAgent): Promise<void>（@permission ohos.permission.KEEP_BACKGROUND_RUNNING）：申请长时任务，系统会发一条与之关联的通知，wantAgent 是点通知时拉起的目标（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceschedule.backgroundTaskManager.d.ts，backgroundTaskManager.startBackgroundRunning）
- function startBackgroundRunning(context: Context, bgModes: string[], wantAgent: WantAgent): Promise<ContinuousTaskNotification>：同族接口：按多个后台模式字符串申请长时任务（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceschedule.backgroundTaskManager.d.ts，backgroundTaskManager.startBackgroundRunning）
- function requestEnableNotification(context: UIAbilityContext): Promise<void>：发通知前弹框请求用户允许通知（出处：鸿蒙 SDK 的 ets/api/@ohos.notificationManager.d.ts，notificationManager.requestEnableNotification）
- function isNotificationEnabled(): Promise<boolean>：检测通知是否已允许（出处：鸿蒙 SDK 的 ets/api/@ohos.notificationManager.d.ts，notificationManager.isNotificationEnabled）
- function isPiPEnabled(): boolean：当前系统是否支持画中画，不支持时走应用内紧凑回退（出处：鸿蒙 SDK 的 ets/api/@ohos.PiPWindow.d.ts，PiPWindow.isPiPEnabled）
- 用 backgroundTaskManager 长时任务、WantAgent 进度通知与动作、Preferences 持久化重写平台计时服务，页面改为消费真实能力和前后台状态：修复用的实现（出处：卡里修好并验证过）
针对本应用要查的：
- 长时任务要申请的后台模式：鸿蒙 SDK 的 ets/api/@ohos.resourceschedule.backgroundTaskManager.d.ts 里的 BackgroundMode 枚举，以及源工程 AndroidManifest 里 service 的 android:foregroundServiceType；按源端前台服务的类型选对应的 BackgroundMode，并在 module.json5 的 backgroundModes 和 requestPermissions 里声明
未核实：卡里的修复出自 API 21（6.0.1），本机声明是 API 23；卡里没写长时任务用的 BackgroundMode
来源：1 张卡，1 个应用
- case-f93a2f80bafd58105489（Cofi）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、建议 1；做法第 3 步 ← 建议 4；取值 6 ← 诊断
