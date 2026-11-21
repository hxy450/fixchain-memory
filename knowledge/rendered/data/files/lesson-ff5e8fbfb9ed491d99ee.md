# 源端在后台线程执行的文件拷贝与导入改用异步 IO 或 taskpool：async 函数里调用 *Sync 接口仍阻塞主线程

## 何时使用

服务层实现阶段，把源端 AsyncTask、线程池或后台线程里的文件拷贝、读写与批量导入翻译为 ArkTS，并核对规格要求的并发或后台执行时

## 适用情境

源端在 AsyncTask.doInBackground、executeOnExecutor(THREAD_POOL_EXECUTOR) 或 Executor 中拷贝附件、读写大文件，多个 URI 并行处理；规格或附录写明目标用 taskpool 并发、主线程只收束结果；实现者手里有 fileIo.copyFileSync、openSync/readSync 等同步接口。

## 原因

async 只改变函数的返回形态，函数体里的同步调用仍在调用线程（UI 主线程）上顺序执行；把 *Sync 拷贝链包进 async 方法，多文件导入期间界面被阻塞，也失去源端的并发。

## 做法

1. 源端在后台线程做的 IO，目标用 fileIo 的 Promise 接口（copyFile、read、write 等不带 Sync 后缀的版本）或交给 taskpool.execute 执行（任务函数加 @Concurrent，只传路径、fd 数值等可序列化参数），主线程只接收结果并更新状态；规格写了并发时多个文件分别发起，再按源端规则收束。
2. 写完检索该链路上的 *Sync 调用，逐个确认不在主线程的批量或大文件路径上；源端本就在主线程同步执行的小文件读写才保留同步接口。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕TaskPool 任务函数（LongTask 除外）在工作线程里的同步执行时长不能超过 3 分钟：同步接口的整个耗时（含磁盘 I/O 阻塞）都计入，Promise/async 的等待时长不计入；超时阻塞会让该线程无法再调度其他任务，长时间执行的任务可能导致进程被强制终止（TerminationError）。〔成立范围：对象：taskpool.execute 提交的普通 Task / TaskGroup。条件：任务里用 copyFileSync、readSync 等同步接口拷贝大文件或批量文件。不成立的情形：taskpool.LongTask；任务内改用 fileIo 的 Promise 接口时只计 CPU 处理时长。〕
- 〔做法第 1 步〕普通对象和普通类实例跨线程传给 TaskPool 时按序列化拷贝，只带数据、类方法丢失，任务里对它的修改不会回到宿主线程；只有 @Sendable 类的实例跨线程后能携带类方法。〔成立范围：对象：taskpool 任务函数的入参。条件：传入未加 @Sendable 的类实例（如带方法的导入器、服务对象）或简单对象。不成立的情形：@Sendable 类实例。〕
- 〔适用情境〕安卓 AsyncTask.execute() 交给进程内全局的 SERIAL_EXECUTOR，多个任务一个接一个顺序执行；只有 executeOnExecutor(THREAD_POOL_EXECUTOR, …) 才并行。〔成立范围：对象：源端 AsyncTask 的提交方式。条件：Android 3.0（HONEYCOMB）及以上、应用没有改默认执行器。不成立的情形：源端用 executeOnExecutor(THREAD_POOL_EXECUTOR) 或自建 Executor 时为并行。〕
- 〔做法第 1 步〕传给 TaskPool 的 ArrayBuffer 默认按转移传递，提交后宿主线程不能再使用这个 ArrayBuffer（任务返回的 ArrayBuffer 同样默认转移）；要多次执行或宿主侧继续使用，须用 setCloneList 把它改成拷贝，或调用 setTransferList 且不把它列入转移列表（传空数组时全部 ArrayBuffer 参数按拷贝）。〔成立范围：对象：taskpool Task 的 ArrayBuffer 参数与返回值。条件：没有调用 setTransferList/setCloneList 改传输方式。不成立的情形：已 setCloneList([buf])，或调用过 setTransferList 而 buf 不在列表里时，按拷贝传递。〕
- 〔做法第 1 步〕TaskPool 序列化传输的数据量上限为 16MB。〔成立范围：对象：taskpool 任务入参与返回值中走序列化的部分。条件：把整份文件内容作为字符串或对象传入、传出。不成立的情形：只传路径、fd 数值等小参数时不受影响。〕
- 〔做法第 1 步〕TaskPool/Worker 工作线程不能使用操作 UI 的模块和只支持在主线程使用的模块，文档点名的有 ApplicationContext。〔成立范围：对象：@Concurrent 任务函数体内调用的模块。条件：任务里要取 filesDir、cacheDir 等沙箱路径，或要弹 UI 提示。不成立的情形：hilog、TaskPool、Worker 等线程安全模块可在工作线程使用。〕
