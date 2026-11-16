# Activity 的 NonConfigurationInstance 续存分支

agent 会看到什么：读到 Activity.onCreate 先取 getLastCustomNonConfigurationInstance() / getLastNonConfigurationInstance()，为 null 才按启动参数分支；规格或验收条目写成「已有实例时忽略启动参数」「单例天然续存」，没分配置重建和各入口

## 规矩

- rule-738888f400e0｜源端 getLast…NonConfigurationInstance 为空才读启动参数时，规格分写配置重建和正常进入｜读到：Activity.onCreate 先取 getLastCustomNonConfigurationInstance() 或 getLastNonConfigurationInstance()，只有为 null 时才按 Intent 的启动参数分支；同一 Activity 有 onRetainCustomNonConfigurationInstance / onRetainNonConfigurationInstance；写错：规格写成「已有实例时启动参数全部忽略、直接复用当前对象」，或映射行写「getLastCustomNonConfigurationInstance → 单例天然续存」，没有区分配置变化重建和正常启动
- rule-e1033d8e870f｜规格写「已有实例优先、忽略启动参数」的验收条目时，按入口×前置状态逐格列出｜读到：源端只在 getLastCustomNonConfigurationInstance() 为 null 时才按启动参数分支，页面有新建、继续等多个入口，状态对象同时是只在退出时销毁的静态单例；写错：验收条目写成「有实例时传入任意启动参数仍恢复原对象、不新建」，没有按入口和前置状态逐一列出，也没有「已有旧对象时走新建入口得到新状态」这一条
