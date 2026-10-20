# 源端在后台线程执行的文件拷贝与导入改用异步 IO 或 taskpool：async 函数里调用 *Sync 接口仍阻塞主线程

ID：`lesson-ff5e8fbfb9ed491d99ee` · 版本：1

[本主题](index.md)

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

## 来源（按需复核）

- [case-29db923e9cadbe8ce53c](../../../store/cases/case-29db923e9cadbe8ce53c/aa92466b00c3c3bc5eadb4e83e006fcff79e7f08502b0bb49fa74f7777666761.json) · 结论：diagnosis, recommendation:2
  卡片版本：`aa92466b00c3c3bc5eadb4e83e006fcff79e7f08502b0bb49fa74f7777666761`
