# LAUNCHER 入口是路由跳板且任务根被改写时，进程存活后从桌面图标重进要在 onNewWant 按同一条件再分流

ID：`lesson-16375a31f9d9cfe6cd55` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段把 LAUNCHER 路由跳板 Activity 映射为入口分流时；入口装配阶段接线 EntryAbility.onNewWant 与入口页时

## 适用情境

源端 LAUNCHER Activity 是按条件 startActivity 后 finish 的无界面跳板（未声明 launchMode 即 standard），跳往主页时带 FLAG_ACTIVITY_CLEAR_TOP；应用内跳转用 TaskStackBuilder.startActivities 或 NEW_TASK|CLEAR_TASK 重建任务，使任务根变为主页。目标为单例 UIAbility 加单个 Navigation，进程存活时再次从桌面拉起只回调 onNewWant/onForeground，页面栈原样保留。

## 原因

进程存活时从桌面图标再次进入，源端在任务顶新建跳板并重跑分流（如首启进引导，否则经 CLEAR_TOP 清掉主页之上的页面回主页），从最近任务切回才保持原页；目标单例 UIAbility 只回到原页面栈。入口分流只接在冷启路径时，CLEAR_TOP 被“冷启时根页天然唯一”消解，热重入停在原页。

## 做法

1. 规格对跳板的每个 Intent flag 写出可观察后果与对应的进入场景，入口分流按“冷启 / 进程回收后重入 / 进程存活时从桌面图标再次拉起 / 从最近任务切回”逐种写验收。
2. 结合跳板的 launchMode 与任务根是否被 TaskStackBuilder.startActivities、NEW_TASK|CLEAR_TASK 改写，判断源端重进时是否重跑跳板；需要重跑时在 EntryAbility.onNewWant 经事件通知入口页，按与冷启相同的条件再分流（如首启压引导，否则回主页并清掉其上的页面）。

## 可选检查

- 有设备时，在内页按 Home 再点桌面图标，两端都回到分流目标；从最近任务切回则保持原页。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-41dfb6f341d11578323a](../../../../store/cases/case-41dfb6f341d11578323a/aa2a6135acd04efeada2bfe65f91f40ffa852968432c2f5b3c9fd6c53b53fef7.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`aa2a6135acd04efeada2bfe65f91f40ffa852968432c2f5b3c9fd6c53b53fef7`
