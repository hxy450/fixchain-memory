# 铸后台执行或通知控制类 HARD-DIV 决策前，逐条在 d.ts 里查证所称平台约束

审的是：规格
触发（任一种）：
- 读到：源端 WorkManager Worker 逐拍刷新进度通知（setProgress）、步间切换、发完成通知；通知按钮是 PendingIntent.getBroadcast 交给 BroadcastReceiver，应用不被拉起；写错的样子：规格铸 `HARD-DIV` / `PD-` 决策，写「HMOS 无应用级广播对等通道」「第三方通知无进度条字段」「无长驻 Worker」等约束，契约列标了 d.ts 依据却没有对应的查询
适用范围：规格阶段为后台计时、进度通知、通知按钮判定平台差异时
做法：
- 逐条查证再定案：wantAgent 的 OperationType（含 SEND_COMMON_EVENT）与 commonEventManager 订阅、backgroundTaskManager 短时任务与长时任务模式、reminderAgentManager 代理提醒、NotificationRequest 的模板进度能力
- 契约列的「依据」只引用本次实际查到的条款原文，查到有对等能力的不写成 HARD-DIV
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- wantAgent.OperationType：UNKNOWN_TYPE = 0、START_ABILITY、START_ABILITIES、START_SERVICE、SEND_COMMON_EVENT（Sends a common event）：通知按钮可以发公共事件，不必拉起应用（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.wantAgent.d.ts，wantAgent.OperationType）
- NotificationRequest.template?: NotificationTemplate；name 只支持 downloadTemplate，data 含 title、fileName、progressValue：第三方通知有带进度的模板（出处：鸿蒙 SDK 的 ets/api/notification/notificationRequest.d.ts，NotificationRequest.template；ets/api/notification/notificationTemplate.d.ts，NotificationTemplate）
- function requestSuspendDelay(reason: string, callback: Callback<void>): DelaySuspendInfo：短时任务：申请延迟挂起，到期回调（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceschedule.backgroundTaskManager.d.ts，backgroundTaskManager.requestSuspendDelay）
- function publishReminder(reminderReq: ReminderRequest): Promise<number>（需 ohos.permission.PUBLISH_AGENT_REMINDER）：代理提醒：进程挂起后由系统按时提醒（出处：鸿蒙 SDK 的 ets/api/@ohos.reminderAgentManager.d.ts，reminderAgentManager.publishReminder）
来源：1 张卡，1 个应用
- case-f4fef12b5d994df457b2（Cofi）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
