# RdbStore 的事务接口（beginTrans 与 beginTransaction）

agent 会看到什么：读到 relationalStore.getRdbStore 的 StoreConfig 没有 vector: true、参考写法给的是 beginTransaction / createTransaction，或规格要求单条增删写完才返回，产物里是 beginTrans() 取 txId 再 execute(sql, txId, args) / commit(txId) 的写法

## 规矩

- rule-865ae2712fd3｜普通 RDB 库的多语句事务用 beginTransaction 系列，不用 beginTrans｜读到：relationalStore.getRdbStore 的 StoreConfig 里没有 vector: true；参考给的是 beginTransaction() 或 createTransaction()；写错：代码用 beginTrans() 取事务 ID，再 execute(sql, txId, args)、commit(txId)、rollback(txId)
- rule-fe5eea898681｜普通 RDB 库的单条增删语句直接 await execute(sql, args)，不包 beginTrans｜读到：规格或计划要求插入、删除「写完才返回、失败不留半条记录」，DAO 的单条 INSERT/DELETE 经共享写入口执行；写错：共享写入口写成 await store.beginTrans() 取事务 ID → execute(sql, txId, args) → commit(txId)，失败 rollback(txId)；DAO 注释写 within a committed transaction
- rule-1e258117560c｜源端事务迁到 RdbStore 后体内要 await 的，改用 createTransaction 返回的事务对象｜读到：源端 db.beginTransaction() … setTransactionSuccessful() / endTransaction() 包着多步写入；写错：目标端在共享的 store 上 store.beginTransaction() 后，同一函数里 await store.insert / store.update / store.delete 再 store.commit()
