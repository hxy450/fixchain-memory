# Room 的 UPDATE / DELETE 返回的受影响行数

agent 会看到什么：读到源端 Room @Query 的 UPDATE / DELETE 方法返回 Int（可能带 COALESCE 或 WHERE id IN 子查询），或目标 DAO 签名承诺 Promise<number>；产物里行数是 store.update / delete 的返回值、按同一 WHERE 先计数，还是 executeSql 之后另查 SELECT changes()

## 规矩

- rule-40b1415faaeb｜RdbStore 要返回受影响行数时用 update/delete 的返回值，不另查 SELECT changes()｜读到：源端 Room @Query 的 UPDATE / DELETE 方法返回 Int，或目标 DAO 签名承诺返回 Promise<number> 受影响行数；写错：写成 store.executeSql(...) 后另起 store.querySql('SELECT changes() AS value') 读行数，或 return 一个这样实现的共享 helper
- rule-6a0d85dd5761｜带 COALESCE 或子查询的 UPDATE 要返回行数时，先按同一 WHERE 计数再更新｜读到：源端 Room @Query 的 UPDATE 带 COALESCE(...) 等表达式或 WHERE id IN (子查询)，写不成 ValuesBucket，方法返回 Int；写错：整条 SQL 交给 executeSql，再用 SELECT changes() 或依赖它的 helper 取行数
