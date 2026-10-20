# relationalStore 事务体含 await 时用 createTransaction，不用 beginTransaction；单语句直接 await

ID：`lesson-a078efd3361b4abe58e3` · 版本：2

[本主题](index.md)

## 何时使用

数据层实现阶段，为 relationalStore 的 DAO 共享写入口选择单语句执行或事务接口时

## 适用情境

ArkTS 用 @kit.ArkData relationalStore 普通（非向量）关系库，DAO 的单条 INSERT/DELETE 经共享写入口执行；规格要求“写完才返回、失败不留半条记录、异常回滚”；SDK d.ts 中同时有 beginTransaction()/commit()/rollBack() 与 beginTrans(): Promise<number>、execute(sql, txId, args)、commit(txId)、rollback(txId) 两套事务写法，后者列出 801（Capability not supported）；data-layer skill 参考只给出前一套（API 14+ 另有 createTransaction()）。也包括事务体内要多次 await 异步写接口（insert/update/delete 或其他 DAO 方法），而同一 store 上可能同时有其他异步库操作或同一流程的并发调用。

## 原因

单条 SQL 本身是原子语句，已满足“写完才返回、失败不留半条”，为它套事务只多出失败点。共享 store 上 beginTransaction 开启的事务不绑定调用方：事务体内每次 await 都会让出执行，其他经同一 store 的异步库操作会落进这个事务，同一流程并发进入时再次开启事务会造成嵌套错位；createTransaction()（API 14+）返回独立的 Transaction 对象，事务内语句经它执行并由它 commit/rollback。两套接口的 @since 相同，@since 只说明接口出现的版本，不说明当前库类型与设备支持：事务 ID 一套曾在 API 24 真机的普通库上调用 beginTrans() 即返回 801，所有保存都失败，而 unit 判定与签名比对都发现不了。该接口的官方适用库类型尚未核实，beginTransaction() 也未做真机验证。

## 做法

1. 单条 INSERT/DELETE/UPDATE 直接 await store.execute(sql, args) 或 insert/delete 等接口，失败按错误通道上抛；把“单语句即原子”的判断写进实现报告。
2. 多语句写入才包显式事务：事务体内需要 await（异步 insert/update/delete、调用其他 DAO 方法）时，用 store.createTransaction()（API 14+，写事务可传 { transactionType: relationalStore.TransactionType.IMMEDIATE }）取得 Transaction，语句都经它执行，成功 commit、异常 rollback；只有事务体全部是同步调用、没有 await 时才用 beginTransaction()/commit()/rollBack()。不因返回事务 ID 的 Promise 写法更顺手而换用参考未列出的接口。
3. 从 d.ts 选接口时，同类接口中只有一个声明 801 能力不支持，先确认它适用于当前 StoreConfig（是否向量库等）与目标设备，再用于共享写入口。

## 可选检查

- 共享写入口至少做一次真实 RdbStore 写入（真机或模拟器）；只有 unit 判定或签名比对时，在报告中标出设备能力未验证
- 检索 beginTransaction(：同一函数内在 commit 之前出现 await 的，逐个改为 Transaction 对象

来源支持：2 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

## 来源（按需复核）

- [case-8402e3a379e2a8d7f434](../../../store/cases/case-8402e3a379e2a8d7f434/ebdad535a42c01e6ce53368392b21e85f277e256da86944e0c7b0e2893b1d956.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`ebdad535a42c01e6ce53368392b21e85f277e256da86944e0c7b0e2893b1d956`
- [case-bbb6bcf0a09493406de9](../../../store/cases/case-bbb6bcf0a09493406de9/21a32e8e2f659dec5dc8a1982ba4cec150ff0dddab1577f972cec3d0a8b6d17a.json) · 结论：diagnosis, recommendation:2
  卡片版本：`21a32e8e2f659dec5dc8a1982ba4cec150ff0dddab1577f972cec3d0a8b6d17a`
