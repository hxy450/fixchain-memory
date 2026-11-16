# 数据库

源端有 Room 的 @Database / @Entity / @PrimaryKey / Migration、SQLiteOpenHelper，目标端有 relationalStore 的 getRdbStore、CREATE TABLE、insert、事务时

## 触发族

- [Room 数据库迁成 relationalStore 的建表和版本](room-to-rdb/index.md)（6 条）：源端 Room 的 @Database / @Entity / Migration、导出的 schema JSON 和 RoomDatabase.Callback；产物里 relationalStore 的 CREATE TABLE 字符串、StoreConfig 的 name、store.version 和升级分支
- [源端 SQLite 落库的主键、时机和建库](sqlite-write-timing-key/index.md)（5 条）：读到源端 SQLiteOpenHelper / SQLiteDatabase 落库（落库前拼组合主键、首次打开才建库、写完就发事件），产物里是 relationalStore 的 getRdbStore、insert / update / batchInsert 和写库后的事件发送
- [Room 自增主键 @PrimaryKey(autoGenerate = true) 的写入](room-autoincrement-id/index.md)（2 条）：读到 Room 实体 @PrimaryKey(autoGenerate = true) val id: Int = 0、种子数据显式传固定 id、补充路径 copy(id = 0)，产物里是 relationalStore 手写的 INSERT 列清单或 ValuesBucket 里的 'id'
- [RdbStore 的事务接口（beginTrans 与 beginTransaction）](rdb-transaction-api/index.md)（3 条）：读到 relationalStore.getRdbStore 的 StoreConfig 没有 vector: true、参考写法给的是 beginTransaction / createTransaction，或规格要求单条增删写完才返回，产物里是 beginTrans() 取 txId 再 execute(sql, txId, args) / commit(txId) 的写法
- [Room 的 UPDATE / DELETE 返回的受影响行数](rdb-affected-rows/index.md)（2 条）：读到源端 Room @Query 的 UPDATE / DELETE 方法返回 Int（可能带 COALESCE 或 WHERE id IN 子查询），或目标 DAO 签名承诺 Promise<number>；产物里行数是 store.update / delete 的返回值、按同一 WHERE 先计数，还是 executeSql 之后另查 SELECT changes()
- [Cursor 按文本读回的数值列](cursor-column-text/index.md)（1 条）：读到源端 cursor.getString(i) 读 REAL（浮点）列再交给 String 入口解析；产物里 relationalStore 的 ResultSet 同样用 rs.getString(idx) 读这一列
