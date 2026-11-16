# 源端 SQLite 落库的主键、时机和建库

agent 会看到什么：读到源端 SQLiteOpenHelper / SQLiteDatabase 落库（落库前拼组合主键、首次打开才建库、写完就发事件），产物里是 relationalStore 的 getRdbStore、insert / update / batchInsert 和写库后的事件发送

## 规矩

- rule-93a9fea29ec2｜远端行映射成本地行时按源端公式重建组合主键，再用 ON_CONFLICT_REPLACE 落库｜读到：目标库 schema 里这张表的键列是 TEXT NOT NULL 并建了 CREATE UNIQUE INDEX；源端落库前用一个方法把几个字段（如记录 id、日期、用户 id）拼成组合主键；写错：同步仓库把远端 payload 直接 fromJson 映射成实体，没有生成主键就用 ConflictResolution.ON_CONFLICT_REPLACE 批量插入；增量和全量两条路径有一条漏了也算
- rule-7907d243f848｜源端不等落库就发事件、目标改成异步 RDB 写时，等写完再发或补发一次事件｜写错：目标的写库函数用 `relationalStore` 的异步 `update` / `insert`，返回的 Promise 没被 await 或没被返回，就接着发状态事件，订阅页重查读到旧值
- rule-dad17b0e7483｜源端库只在首次打开时创建，目标不在启动 init 里 getRdbStore 预建库｜读到：数据库 helper extends SQLiteOpenHelper，构造只调 super(...)，正常路径上没有 getWritableDatabase 调用；写错：目标启动服务或备份服务构造里 fire-and-forget 调 init() → relationalStore.getRdbStore(...) 建库，备份前先 await 这个建库任务
- rule-7e61f71be86d｜SQLiteOpenHelper 子类迁成 RdbStore 时按 store.version 分派建表、升级、降级报错｜读到：源端类 extends SQLiteOpenHelper，构造里 super(context, name, factory, VERSION)，重写 onCreate / onUpgrade；写错：目标端 getRdbStore 打开后直接调建表，或写成 store.version >= VERSION 就 return、否则建表并写 version；没有 version === 0 建表、小于 VERSION 走 onUpgrade、大于 VERSION 抛错的分派
- rule-bac3cb04485b｜用缓存的 Promise 做 RdbStore 单例时，打开失败在 catch 里复位缓存，下次访问重试｜读到：源端每次访问都调 getWritableDatabase() / getReadableDatabase()；写错：目标端 init 把包着 relationalStore.getRdbStore 的 Promise 存进单例字段后永不清空，一次失败后每次 DAO 调用都拿到同一个 rejected Promise
