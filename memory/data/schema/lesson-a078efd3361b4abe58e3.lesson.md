# relationalStore 共享写入口：单条语句直接 await execute/insert/delete，多语句事务用 beginTransaction/commit/rollBack；不选 d.ts 声明 801 的 beginTrans()/execute(sql, txId) 事务 ID 接口

ID：`lesson-a078efd3361b4abe58e3` · 版本：1

[本主题](index.md)

## 何时使用

数据层实现阶段，为 relationalStore 的 DAO 共享写入口选择单语句执行或事务接口时

## 适用情境

ArkTS 用 @kit.ArkData relationalStore 普通（非向量）关系库，DAO 的单条 INSERT/DELETE 经共享写入口执行；规格要求“写完才返回、失败不留半条记录、异常回滚”；SDK d.ts 中同时有 beginTransaction()/commit()/rollBack() 与 beginTrans(): Promise<number>、execute(sql, txId, args)、commit(txId)、rollback(txId) 两套事务写法，后者列出 801（Capability not supported）；data-layer skill 参考只给出前一套（API 14+ 另有 createTransaction()）。

## 原因

单条 SQL 本身是原子语句，已满足“写完才返回、失败不留半条”，为它套事务只多出失败点。两套事务接口 @since 相同，@since 只说明接口出现的版本，不说明当前库类型与设备支持；来源中事务 ID 一套在 API 24 真机的普通库上调用 beginTrans() 即返回 801，所有保存都失败，而 unit 判定与签名比对都发现不了。该接口的官方适用库类型未在来源中核实，参考写法 beginTransaction() 也未在来源中做真机验证。

## 做法

1. 单条 INSERT/DELETE/UPDATE 直接 await store.execute(sql, args) 或 insert/delete 等接口，失败按错误通道上抛；把“单语句即原子”的判断写进实现报告。
2. 多语句写入才包显式事务，沿用 skill 参考的 beginTransaction()/commit()/失败 rollBack()，或在满足 API 级别时用 createTransaction()；不因返回事务 ID 的 Promise 写法更顺手而换用参考未列出的接口。
3. 从 d.ts 选接口时，同类接口中只有一个声明 801 能力不支持，先确认它适用于当前 StoreConfig（是否向量库等）与目标设备，再用于共享写入口。

## 可选检查

- 共享写入口至少做一次真实 RdbStore 写入（真机或模拟器）；只有 unit 判定或签名比对时，在报告中标出设备能力未验证

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-8402e3a379e2a8d7f434](../../../store/cases/case-8402e3a379e2a8d7f434/ebdad535a42c01e6ce53368392b21e85f277e256da86944e0c7b0e2893b1d956.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`ebdad535a42c01e6ce53368392b21e85f277e256da86944e0c7b0e2893b1d956`
