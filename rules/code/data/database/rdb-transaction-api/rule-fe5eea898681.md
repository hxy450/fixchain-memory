# 普通 RDB 库的单条增删语句直接 await execute(sql, args)，不包 beginTrans

审的是：代码
触发（任一种）：
- 读到：规格或计划要求插入、删除「写完才返回、失败不留半条记录」，DAO 的单条 INSERT/DELETE 经共享写入口执行；写错的样子：共享写入口写成 await store.beginTrans() 取事务 ID → execute(sql, txId, args) → commit(txId)，失败 rollback(txId)；DAO 注释写 within a committed transaction
适用范围：@kit.ArkData relationalStore 的普通（StoreConfig 没有 vector: true）关系库，单条增删改语句的写入口
做法：
- 单条语句写成 await store.execute(sql, args)（或 store.insert / store.delete），单条语句本身原子，满足写完才返回、失败不留半条
- 只有多条语句要一起成败时才包显式事务（见普通库多语句事务的写法），注释写成单条原子语句，不写 committed transaction
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- execute(sql: string, args?: Array<ValueType>): Promise<ValueType>：RdbStore 执行带参数的单条 SQL，支持增删改（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.execute；arkts-apis-data-relationalStore-RdbStore.md，execute<sup>12+</sup>）
- execute(sql, args) 不支持查询、附加数据库和事务语句，也不支持分号分隔的多条语句；BEGIN/COMMIT 这类语句经它执行会抛 801：不要用 execute 跑 BEGIN/COMMIT 自己拼事务（出处：arkts-apis-data-relationalStore-RdbStore.md，execute<sup>12+</sup>；鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.execute）
- 共享写入口改为单条 await execute(sql, args) 后，真机保存成功（原 beginTrans() 处返回 801）：返修后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-8402e3a379e2a8d7f434（NFC）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 3 ← 诊断
