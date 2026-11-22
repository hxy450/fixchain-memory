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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕Promise 和 async/await 是同一线程内的异步并发：异步代码在等待时挂起、操作完成后恢复，同一时间只有一段代码在运行；文档把它们定位于单次 I/O、轻量且无 CPU 阻塞的任务
- 〔做法第 1 步〕taskpool 的任务函数要用 @Concurrent 标注；入参须是序列化支持的类型（@State、@Prop、@Link 等装饰的复杂类型不支持）；ArrayBuffer 参数默认按转移传递，要多次调用使用同一 ArrayBuffer 参数的 task 时需用 setCloneList 改成拷贝传递
- 〔做法第 1 步〕taskpool 任务函数（LongTask 除外）的 CPU 执行时长不能超过 3 分钟；同步 I/O 的整个时长（含阻塞时间）都计入，异步 I/O 的等待时间不计入
