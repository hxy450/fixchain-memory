# 通知与后台任务

源端有 NotificationCompat.Builder、NotificationChannel、常驻通知、WorkManager / CoroutineWorker，目标端有 notificationManager.publish、NotificationRequest、SlotType 或后台计时时

## 触发族

- [WorkManager 后台计时 Worker](worker-timer/index.md)（3 条）：读到 WorkManager / CoroutineWorker 在后台逐拍刷新计时通知、跨多步推进计时；产物里改成应用内计时，退后台只记锚点、发静态通知或只做单步续跑
- [通知的正文和模板](notification-content/index.md)（4 条）：源端 NotificationCompat.Builder 的 setContentText / setProgress；产物里 NotificationRequest 的 normal.text 和通知模板
- [常驻通知的发布者和生命周期](ongoing-notification/index.md)（2 条）：源端通知帮助类按固定 ID notify / cancel 常驻通知、只在特定回调里调用；产物里 notificationManager.publish 写在哪个页面、ViewModel 或服务里，页面离开时是否停掉
- [通知渠道和通知槽（NotificationChannel、SlotType）](notification-channel-slot/index.md)（1 条）：读到源端 new NotificationChannel(id, name, NotificationManager.IMPORTANCE_*) 后 createNotificationChannel；产物里 addSlot 和 NotificationRequest 用的 SlotType，以及有没有源渠道 id、名称、重要度到目标槽的映射
- [AlarmManager 定时提醒和它的 BroadcastReceiver](alarm-reminder/index.md)（3 条）：读到源端 AlarmManager.setExact 到点由 BroadcastReceiver.onReceive 自绘通知（按钮各带 PendingIntent、Parcel 还原快照后写库、RRULE 重复提醒由应用链式重挂）；产物里 reminderAgentManager.publishReminder 的失败和上限回退、actionButton 和 subscribeReminderState，以及到点写回 DB 的逻辑
