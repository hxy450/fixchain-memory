# data/schema

Room 到 relationalStore 的库名、schema 版本、建表语句（含标识符加引号与关键字列名）与升级路径（基线建表与迁移重放一致），以及手写插入语句对自增主键的处理；relationalStore 共享写入口的单语句执行与事务接口选择

[上一级](../index.md)

## 本级经验

- [Room 数据库落成 relationalStore 时保留库名、schema 版本与显式升级路径；基线建表与版本重放方式一致，迁移代码里的 xxx_new 是临时表](lesson-a6f300f9295ba538f23b.lesson.md)
  - 时机：数据层实现阶段，把 Room 数据库落成 relationalStore，确定库名、schema 版本、建表语句与升级路径时；以及评审或修复分诊缺表、重复列问题时
  - 情境：源端 Room @Database 声明 version，配 addMigrations/AutoMigration 与 fallbackToDestructiveMigration，迁移代码可能 ALTER TABLE ADD COLUMN、CREATE TABLE 或用 xxx_new 临时表重建后 RENAME；实体类只给出最终版本的表结构；规格要求显式版本化迁移、保留源 schema 历史与字段可空性。
- [relationalStore 共享写入口：单条语句直接 await execute/insert/delete，多语句事务用 beginTransaction/commit/rollBack；不选 d.ts 声明 801 的 beginTrans()/execute(sql, txId) 事务 ID 接口](lesson-a078efd3361b4abe58e3.lesson.md)
  - 时机：数据层实现阶段，为 relationalStore 的 DAO 共享写入口选择单语句执行或事务接口时
  - 情境：ArkTS 用 @kit.ArkData relationalStore 普通（非向量）关系库，DAO 的单条 INSERT/DELETE 经共享写入口执行；规格要求“写完才返回、失败不留半条记录、异常回滚”；SDK d.ts 中同时有 beginTransaction()/commit()/rollBack() 与 beginTrans(): Promise&lt;number&gt;、execute(sql, txId, args)、commit(txId)、rollback(txId) 两套事务写法，后者列出 801（Capability not supported）；data-layer skill 参考只给出前一套（API 14+ 另有 createTransaction()）。
- [手写 relationalStore 建表 SQL 时给表名与列名统一加引号，关键字列名尤其不能裸写](lesson-c55c56444f5271471a64.lesson.md)
  - 时机：数据层实现阶段，把 Room 实体或列清单手写成 relationalStore 的建表与索引 SQL 字符串时；规格或侦察阶段为实现者整理表结构列清单时
  - 情境：源端表结构由 Room 注解生成，Room 导出的 createSql 会给表名、列名加反引号；目标端用字符串数组手写 DDL 并在 init 中顺序执行，实体列名可能是 to、order、group、index、default、key 一类 SQL 关键字；SQL 写在字符串里，ArkTS 编译不检查。
- [手写 relationalStore 插入语句时省略 Room autoGenerate 主键列：默认 0 表示未赋值，显式写入会让同批行按主键互相替换](lesson-5c101b4b3f08ab317202.lesson.md)
  - 时机：数据层实现阶段，把 Room 实体与 @Insert 方法翻译成 relationalStore 手写 INSERT/INSERT OR REPLACE SQL、决定自增主键列是否写入时
  - 情境：源 Room 实体用 @PrimaryKey(autoGenerate = true) val id = 0，行由映射函数新建且 id 保持默认 0，再经 @Insert(onConflict = REPLACE) 批量写入；目标用 executeSql 手写插入，行接口保留 id 字段。
  - 例外：源端确实为该行指定了非 0 的真实主键（如按固定 id 播种），此时照源端写入该值
