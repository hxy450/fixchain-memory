# 源后台任务持久化、回前台读任务状态时，规格要求会话落盘并在进程重建后恢复

审的是：规格
触发（任一种）：
- 读到：源端任务由 WorkManager 持久化，回前台用 `getWorkInfosForUniqueWorkLiveData(...)` 按任务名读取进度；写错的样子：规格的会话状态只放 AppStorageV2 单一键，没写落盘，也没交代进程重建后怎么恢复；对接点同步读进程内全局态，不按任务标识查询
适用范围：规格阶段为持久化后台任务写状态管理和对接点时
做法：
- 规格要求会话记录落盘（如 preferences）并在进程重建后恢复；AppStorageV2 只在进程内存活，不作唯一载体
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- AppStorageV2 只在内存里保存；PersistenceV2 保存到磁盘：进程被回收后 AppStorageV2 的会话就没了（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.StateManagement.d.ts，AppStorageV2、PersistenceV2）
- function getPreferencesSync(context: Context, options: Options): Preferences；putSync(key: string, value: ValueType): void；flush(): Promise<void>：preferences 落盘的取实例、写值、刷盘（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，preferences.getPreferencesSync、Preferences.putSync、Preferences.flush）
- 会话记录经 preferences 持久化，进程重建后恢复；回前台按任务标识异步查询进度：修复后的做法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-ea77ad96a8fa0f09fbc8（Cofi）：做法第 1 步 ← 建议 3；取值 3 ← 诊断
