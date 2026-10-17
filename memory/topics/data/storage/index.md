# data/storage

本地持久化：relationalStore 建表与版本迁移、自增主键写入、预置数据内容与播种时机、fileIo 目录操作

[上一级](../index.md)

## 本级经验

- [Room 迁移保留库名、schema 版本与显式升级分支](lesson-a6f300f9295ba538f23b.lesson.md) · 阶段：execute/verify/repair · 信号：@Database(version, addMigrations, AutoMigration, fallbackToDestructiveMigration
- [SQLiteOpenHelper 首次取库才建库，启动不预建](lesson-519f6769ca714500d9c3.lesson.md) · 阶段：spec/execute · 信号：SQLiteOpenHelper, getReadableDatabase, getWritableDatabase, relationalStore
- [mkdirSync 对已存在目录抛错，先判存在再建](lesson-3f6b5d0b0ea6806a1b0c.lesson.md) · 阶段：execute · 信号：fileIo.mkdirSync, 13900015, fileIo.accessSync, @kit.CoreFileKit
- [单语句直接写，事务含 await 用独立事务](lesson-a078efd3361b4abe58e3.lesson.md) · 阶段：execute/verify · 信号：createTransaction, beginTransaction, beginTrans, rollBack
- [手写 INSERT 省略自增主键列，id=0 表示未赋值](lesson-5c101b4b3f08ab317202.lesson.md) · 阶段：execute · 信号：@PrimaryKey(autoGenerate = true), INSERT OR REPLACE, relationalStore, executeSql
- [手写建表 SQL 表名列名统一加引号，关键字不裸写](lesson-c55c56444f5271471a64.lesson.md) · 阶段：spec/execute · 信号：CREATE TABLE, createSql, relationalStore, executeSql
- [按 VERSION 分派建表升降级，打开失败可重试](lesson-7d8f649aa2713323e072.lesson.md) · 阶段：execute · 信号：SQLiteOpenHelper, onCreate, onUpgrade, onDowngrade
- [按日期实时计算的字段不改绑静态资产，先查内置能力](lesson-6d259db1ffd8927834a2.lesson.md) · 阶段：spec/execute · 信号：Lunar.fromDate, dayYi, dayJi, Intl.DateTimeFormat
- [演示预置数据逐字段取自源种子工厂与 assets 不自拟](lesson-1c513fdf2cf212354aa0.lesson.md) · 阶段：spec/execute · 信号：DemoDataFactory, rawfile, LocalDate.now(), plusDays
- [首次启动播种在启动路径落调用并保留标记门控](lesson-dc3f2589254d02893b0e.lesson.md) · 阶段：plan/execute/converge · 信号：Application.onCreate, seedDemoDataOnFirstLaunch, has_seeded_demo_data, EntryAbility.onCreate
- [首次建库播种放进建表分支同一事务，手动补充不带 id](lesson-488a3bd782acef92f5cf.lesson.md) · 阶段：execute · 信号：onCreate, RoomDatabase.Callback, copy(id = 0), ValuesBucket
