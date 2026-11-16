# WorkManager 后台计时 Worker

agent 会看到什么：读到 WorkManager / CoroutineWorker 在后台逐拍刷新计时通知、跨多步推进计时；产物里改成应用内计时，退后台只记锚点、发静态通知或只做单步续跑

## 规矩

- rule-00074ff48838｜源端 Worker 逐拍刷新后台计时通知时，目标在短时任务窗口内照刷，到期转代理提醒｜读到：WorkManager Worker 里 tickerFlow 每 500ms 刷新进度通知、步终切下一步、最后发完成通知；写错：ArkTS 退后台只记锚点，notificationManager.publish 一条静态常驻通知，不启动 `countdown`，后台不推进
- rule-e0ed1ba927f4｜实现时发现规格降级未覆盖源端行为、又能纯计算复现时，按源语义实现或登记疑点｜读到：源 Worker 在后台跨多步推进，规格降级只写了单步续跑；写错：实现以「规格已接受降级」为由只做单步：剩余时长 ≤ 0 就返回完成，只在当前步内插值，用 `Date.now()` 作锚点
- rule-2211ef4f3cf0｜用应用内计时替代后台 Worker 时，持久化恢复和后台 tick 共用按步骤扣减的函数｜读到：源端后台 Worker（WorkManager）跨步骤推进计时，回到前台时按 Worker 进度里的步骤 id 直接设当前步；写错：持久化恢复另写一支：把全部停机时长加到当前步，满一步只前进一次、余量丢弃（源端 Worker 会连续推进多步），没有复用后台 tick 的跨步扣减函数
