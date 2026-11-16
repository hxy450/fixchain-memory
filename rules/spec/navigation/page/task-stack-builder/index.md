# TaskStackBuilder 父栈和回收后的任务栈

agent 会看到什么：读到 TaskStackBuilder.addNextIntentWithParentStack、android:parentActivityName / PARENT_ACTIVITY 组成的任务栈和 putExtra 的布尔参数；规格的实现映射、返回落点、恢复契约或 PD 写成 pushPathByName 带回栈、恢复至最后路由

## 规矩

- rule-7ebcd10b81fe｜源端用 TaskStackBuilder 带父栈跳转时，规格按 Manifest 父链写出完整栈和返回落点｜读到：源码 TaskStackBuilder.create(this).addNextIntentWithParentStack(intent).startActivities()，Manifest 为目标写了 android:parentActivityName 或 PARENT_ACTIVITY meta-data；写错：规格的实现映射写「pushPathByName 带回栈（Main 为根天然栈底）」，验收写「返回落回来源页」，副作用表没写清栈和按父链重建
- rule-3112b562d16e｜恢复契约按源端任务栈恢复整栈，每页参数保留入栈时的原值｜读到：源端 `TaskStackBuilder.addNextIntentWithParentStack` 建出「父页 + 当前页」的栈；跳转 Intent 用 `putExtra` 的布尔值区分新开和续接；写错：恢复契约写「恢复至最后路由」只恢复一页，或把恢复页的参数写死成续接值，没有对照已读的 putExtra 行
- rule-68fe33c4abba｜进程回收后重建任务栈的替代决策，触发条件只写系统回收且任务仍在｜读到：源端用 `TaskStackBuilder.addNextIntentWithParentStack` 或 `PARENT_ACTIVITY` 组成任务栈、没有显式保存导航，靠框架在进程回收后重建；LAUNCHER 是按首启分流的 Splash；上游规格已把冷启动回起始页与回收后栈恢复分开写；写错：规格或决策台账的 PD 写成「冷启动（含回收后重入）恢复至最后路由」，把冷启动和回收重建合成一条，没写按退出原因判定
