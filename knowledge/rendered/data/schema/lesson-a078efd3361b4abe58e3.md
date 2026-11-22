# relationalStore 事务体含 await 时用 createTransaction，不用 beginTransaction；单语句直接 await

## 何时使用

数据层实现阶段，为 relationalStore 的 DAO 共享写入口选择单语句执行或事务接口时

## 适用情境

ArkTS 用 @kit.ArkData relationalStore 普通（非向量）关系库，DAO 的单条 INSERT/DELETE 经共享写入口执行；规格要求“写完才返回、失败不留半条记录、异常回滚”；SDK d.ts 中同时有 beginTransaction()/commit()/rollBack() 与 beginTrans(): Promise<number>、execute(sql, txId, args)、commit(txId)、rollback(txId) 两套事务写法，后者列出 801（Capability not supported）；data-layer skill 参考只给出前一套（API 14+ 另有 createTransaction()）。也包括事务体内要多次 await 异步写接口（insert/update/delete 或其他 DAO 方法），而同一 store 上可能同时有其他异步库操作或同一流程的并发调用。

## 例外与边界

- 单语句直接 await 只针对写入口本身：源端用 Room @Transaction 方法或 runInTransaction 把多条写入包成一体的，外层事务照留（按第 2 步用事务对象执行），不因每条语句各自原子就拆掉。
- StoreConfig 配置 vector 为 true 的向量库上，beginTrans() 与带事务 ID 的 execute、commit、rollback 是文档支持的写法，不在这条的替换范围内。

## 原因

单条 SQL 本身是原子语句，已满足“写完才返回、失败不留半条”，为它套事务只多出失败点。共享 store 上 beginTransaction 开启的事务不绑定调用方：事务体内每次 await 都会让出执行，其他经同一 store 的异步库操作会落进这个事务，同一流程并发进入时再次开启事务会造成嵌套错位；createTransaction()（API 14+）返回独立的 Transaction 对象，事务内语句经它执行并由它 commit/rollback。两套接口的 @since 并不相同（beginTransaction 为 9，beginTrans 为 12），而且@since 只说明接口出现的版本，不说明当前库类型与设备支持：事务 ID 一套曾在 API 24 真机、API 26 模拟器的普通库上调用 beginTrans() 即返回 801，所有保存都失败，而 unit 判定与签名比对都发现不了。文档写明 beginTrans() 及带事务 ID 的 execute、commit、rollback 仅支持向量数据库（StoreConfig 配置 vector 为 true），普通库上调用即返回 801；beginTransaction() 未做真机验证。

## 做法

1. 单条 INSERT/DELETE/UPDATE 直接 await store.execute(sql, args) 或 insert/delete 等接口，失败按错误通道上抛；把“单语句即原子”的判断写进实现报告。
2. 多语句写入才包显式事务：事务体内需要 await（异步 insert/update/delete、调用其他 DAO 方法）时，用 store.createTransaction()（API 14+，写事务可传 { transactionType: relationalStore.TransactionType.IMMEDIATE }）取得 Transaction，语句都经它执行，成功 commit、异常 rollback；只有事务体全部是同步调用、没有 await 时才用 beginTransaction()/commit()/rollBack()。不因返回事务 ID 的 Promise 写法更顺手而换用参考未列出的接口。
3. 从 d.ts 选接口时，同类接口中只有一个声明 801 能力不支持，先确认它适用于当前 StoreConfig（是否向量库等）与目标设备，再用于共享写入口。

## 可选检查

- 共享写入口至少做一次真实 RdbStore 写入（真机或模拟器）；只有 unit 判定或签名比对时，在报告中标出设备能力未验证
- 检索 beginTransaction(：同一函数内在 commit 之前出现 await 的，逐个改为 Transaction 对象

来源支持：3 张卡 · 已知 2 次迁移（部分未记录） · 已知 2 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 原因 / 做法第 3 步〕RdbStore.beginTrans()（API 12 起）以及带 txId 的 execute(sql, txId, args)、commit(txId)、rollback(txId)，文档写明仅支持向量数据库（StoreConfig 配置 vector 为 true）；声明的 @throws 都列有 801
- 〔做法第 3 步〕StoreConfig.vector（API 18 起）没有设置时为 false，即普通关系型数据库
- 〔原因 / 做法第 3 步〕通用错误码 801 表示功能不支持，可能原因是硬件不支持、芯片不支持或依赖的业务特性不支持
- 〔原因〕普通（非向量）库上调用 beginTrans()，单元测试里一调用就抛 801
- 〔原因〕API 24 真机的普通库上，共享写入口调用 beginTrans() 返回 801，经它的保存全部失败
- 〔原因 / 做法第 2 步〕RdbStore.beginTransaction()、commit()、rollBack()（API 9 起）不带事务对象，文档写明不允许嵌套事务、不支持在多进程或多线程中使用
- 〔原因 / 做法第 2 步〕RdbStore.createTransaction（API 14 起）返回一个已开始的 Transaction 对象；不同事务对象之间相互隔离，经事务对象的写入不会被 on('dataChange') 监听到；一个 store 最多同时存在 4 个事务对象，超过返回 14800015；文档优先推荐 createTransaction，不再推荐 beginTransaction
- 〔做法第 1 步〕RdbStore.execute(sql, args)（API 12 起）支持增删改、PRAGMA 和建表、删表、改表语句，不支持查询、附加数据库和事务语句，也不支持分号分隔的多条语句和以注释开头的语句
