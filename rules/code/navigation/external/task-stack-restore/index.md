# TaskStackBuilder 父栈和路由栈的恢复与再次拉起

agent 会看到什么：源端 TaskStackBuilder.addNextIntentWithParentStack、android:parentActivityName、LAUNCHER 跳板 Activity 的 FLAG_ACTIVITY_CLEAR_TOP，对应目标 NavPathStack 的入栈和整栈恢复、EntryAbility 的 onCreate(launchParam) 与 onNewWant

## 规矩

- rule-2a9108d2bb9e｜TaskStackBuilder 父栈跳转，代码写成 clear 后按父链依次 pushPathByName｜读到：源码 TaskStackBuilder.create(this).addNextIntentWithParentStack(intent).startActivities()，Manifest 有 android:parentActivityName；或规格把它映射成单次 pushPathByName；写错：目标只写 navPathStack.pushPathByName(name, param, false)，注释写「带父栈入栈」「返回落回来源页」
- rule-b33d36142b66｜源端重进会重跑跳板时，EntryAbility 加 onNewWant 经 eventHub 让入口页再分流｜读到：LAUNCHER 跳板 Activity 非首启分支 addFlags(FLAG_ACTIVITY_CLEAR_TOP) 后 finish；主页经 TaskStackBuilder.startActivities 成为任务根；写错：EntryAbility 只有 onCreate / onForeground，没有 onNewWant；入口页只在 aboutToAppear 里分流一次后 pushPathByName，没有处理再次拉起的事件
- rule-4e5c238fcf09｜路由恢复持久化整个 NavPathStack 并整栈重建，参数用入栈时的原值｜读到：规格或台账的 PD 要求进程回收后恢复路由栈；源端用 `TaskStackBuilder.addNextIntentWithParentStack` 组栈；写错：只存最后一个路由、恢复时只 `pushPathByName` 一页，并把恢复页参数写死成续接值；恢复后栈底没有父页，返回会露出空的 `Navigation` 宿主页
- rule-5e03ebe239f4｜EntryAbility.onCreate 把 lastExitReason 交给路由恢复，只在系统回收时恢复｜读到：规格或台账的 PD 要求进程回收后恢复路由栈；写错：`EntryAbility.onCreate(want, launchParam)` 没把 `launchParam` 交给恢复逻辑，恢复函数每次冷启动都无条件读上次路由
