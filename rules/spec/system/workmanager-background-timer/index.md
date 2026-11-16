# 源端 WorkManager Worker 的后台计时和进度通知

agent 会看到什么：源端用 WorkManager Worker 在后台跨步推进计时、逐拍刷新进度通知、按钮经 PendingIntent.getBroadcast 静默投递、回前台按任务名读 WorkInfo，规格里铸成整体降级的 HARD-DIV / PD 决策、只锚定单步剩余时长或只放进程内状态

## 规矩

- rule-bd34b6fd4d66｜铸后台执行或通知控制类 HARD-DIV 决策前，逐条在 d.ts 里查证所称平台约束｜读到：源端 WorkManager Worker 逐拍刷新进度通知（setProgress）、步间切换、发完成通知；通知按钮是 PendingIntent.getBroadcast 交给 BroadcastReceiver，应用不被拉起；写错：规格铸 `HARD-DIV` / `PD-` 决策，写「HMOS 无应用级广播对等通道」「第三方通知无进度条字段」「无长驻 Worker」等约束，契约列标了 d.ts 依据却没有对应的查询
- rule-bf319f7f3840｜后台计时类降级只覆盖确实不可用的那段，进程存活期保留逐拍刷新和静默按钮｜读到：源端 Worker 每 500ms 逐拍刷新通知、步间切换、发完成通知，按钮静默投递不拉起应用；写错：PD 决策整体降级成「退后台 ticker 停摆 + 单条静态常驻通知」「按钮 wantAgent(StartAbility) 拉起应用」「进度转文本」
- rule-a12f756a1aea｜后台计时降级只降执行载体，回前台的跨步推进、需输入停顿和完成判定写进替代路径和 AC｜读到：源端 WorkManager `Worker` 在后台跨步推进计时：一步到时递归启动下一步、需用户输入的步发通知后停住、末步发完成通知，用 `SystemClock.elapsedRealtime()` 计偏移；写错：规格的降级替代路径和 AC 只锚定 {当前步, 剩余时长, 锚点时间}，回前台「从剩余时长续跑」，没规定后台时长越过当前步时如何跨步、停在需输入步、判完成
- rule-e97d29523531｜降级差异 AC 的验证场景覆盖后台越过当前步、跨多步、停在需输入步和已完成｜读到：源端后台任务会跨步推进（到时启动下一步、需输入步停住、末步完成）；写错：降级差异 AC 只测几秒到 30 秒的单步内恢复
- rule-d7748a37e4dc｜源后台任务持久化、回前台读任务状态时，规格要求会话落盘并在进程重建后恢复｜读到：源端任务由 WorkManager 持久化，回前台用 `getWorkInfosForUniqueWorkLiveData(...)` 按任务名读取进度；写错：规格的会话状态只放 AppStorageV2 单一键，没写落盘，也没交代进程重建后怎么恢复；对接点同步读进程内全局态，不按任务标识查询
