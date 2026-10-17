# app/capability/degradation

能力确实不可用时只降级做不到的一步，运行期显式提示

[上一级](../index.md)

## 本级经验

- [决策批准的平台能力要真实现，只在运行期按结果降级](lesson-efb94f2d70d4df1c65d7.lesson.md) · 阶段：execute · 信号：backgroundTaskManager.startBackgroundRunning, ohos.permission.KEEP_BACKGROUND_RUNNING, notificationManager.requestEnableNotification, WantAgent
- [后台计时降级只砍执行载体，保留逐拍刷新与回前台补算](lesson-30643cd3f209b896ffd1.lesson.md) · 阶段：spec/plan/execute · 信号：WorkManager, elapsedRealtime, PendingIntent.getBroadcast, backgroundTaskManager.requestSuspendDelay
- [平台差异只收敛做不到的一步，其余出口照源保留](lesson-9c973e50aaea054facdc.lesson.md) · 阶段：spec/plan/execute · 信号：HARD-DIV, startAbility, viewData, market://
- [应用内计时替代后台 Worker 时恢复入口共用扣减函数](lesson-35a684862ee500f08912.lesson.md) · 阶段：execute · 信号：WorkManager, backgroundTaskManager, keepScreenOn, WakeLock
- [激励广告不可用时显式提示并按台账放行，不伪造奖励](lesson-0f67121af7969203b76b.lesson.md) · 阶段：spec/execute/verify · 信号：showRewarded, onReward, RewardedAd, onUserEarnedReward
