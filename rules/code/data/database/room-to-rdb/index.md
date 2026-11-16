# Room 数据库迁成 relationalStore 的建表和版本

agent 会看到什么：源端 Room 的 @Database / @Entity / Migration、导出的 schema JSON 和 RoomDatabase.Callback；产物里 relationalStore 的 CREATE TABLE 字符串、StoreConfig 的 name、store.version 和升级分支

## 通用查法

### Room 库迁 relationalStore 时，建表和升级 SQL 照源 schema 与 Migration 写

审的是：代码
触发（任一种）：
- 读到：源端有 @Database(entities = …, version = N)、@Entity / @ColumnInfo、Room.databaseBuilder(…).addMigrations(…)，或模块下有 Room 导出的 schemas 目录；写错的样子：目标 executeSql 的 CREATE TABLE 按实体字段重拼（标识符裸写、多了 DEFAULT），StoreConfig 的 name、store.version 或升级分支和源端对不上
适用范围：把 Room 数据库落成 relationalStore 的建表 SQL、库名、版本和升级分支时
做法：
- 建表以最新版本 schema JSON 里每个实体的 createSql 为底稿（${TABLE_NAME} 换成表名，标识符保留引号），不按列清单重拼，不加源端没有的 DEFAULT 和约束
- StoreConfig 的 name 写 databaseBuilder 的第三个实参；store.version 写 @Database 的 version，各 Migration 的 migrate 方法体照写成对应的升级分支
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- version: number（设置时必须是大于 0 的整数）：RdbStore 的库版本，写源端 @Database 的 version（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.version）
- 新建的库 store.version 默认是 0：据此区分首次建库和旧库升级（出处：data-persistence-by-rdb-store.md，开发步骤）
针对本应用要查的：
- 最终 schema：每张表的 createSql 和字段的 notNull：源工程模块下 Room 导出的 schemas 目录（按 @Database 类全名分目录，每个版本一个 JSON）；取版本号最大的 JSON，读 database.entities 下每项的 createSql 和 fields 的 notNull
- 库名、版本号和迁移链：调用 Room.databaseBuilder 的地方、带 @Database 注解的类和 addMigrations 登记的各个 Migration 对象；库名读 databaseBuilder 的第三个实参，version 取注解里的值，每个 Migration 的 migrate 方法体是一条升级分支的 SQL
来源：2 张卡，2 个应用
- case-69e9fe864e45c19bce9d（Meshtastic）：做法第 1 步 ← 建议 2
- case-a3f7f5fbc8635b723b96（Cofi）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、建议 1

## 规矩

- rule-8e50ca2e4a49｜建表 SQL 照 Room 最终 schema 的 createSql 写、不加 DEFAULT，库名照源端｜读到：源工程有 Room 导出的 schemas/<Database 全名>/<version>.json，或 Room.databaseBuilder(context, X::class.java, "name.db")；写错：目标建表语句给可空列加了源 schema 没有的 DEFAULT、改了 NOT NULL，或 StoreConfig 的 name 和源端库名不一样
- rule-7c27f082e418｜把 Room 实体手写成 relationalStore 建表 SQL 时，表名和列名一律加双引号｜读到：源端 Room @Entity 里 @ColumnInfo(name = …) 的列名是 to、order、group、index、default、key 这类 SQL 关键字，或 Room 导出 schema 的 createSql 里标识符带反引号；写错：交给 executeSql 的 CREATE TABLE 字符串里标识符裸写，如 `to TEXT,`；注释还称列名与 Room @Entity 一致
- rule-3551876827dd｜Room @Database 带版本和迁移链时，RdbStore 设 store.version 并写升级分支｜读到：源端 @Database(entities = …, version = N)，Room.databaseBuilder(...).addMigrations(...) / AutoMigration，再加 .fallbackToDestructiveMigration()；或规格写 explicit versioned migration、retain source schema history；写错：目标 relationalStore.getRdbStore 之后只执行无版本的 CREATE TABLE IF NOT EXISTS，没有读写 store.version，也没有旧版本的升级分支
- rule-a6d03fc95a54｜源端 Room 有 ADD COLUMN 迁移时，基线建表只写 v1 的列，后加的列只由迁移添加｜读到：@Database(version = N) 大于 1，Migration(1, 2) 等的 migrate 里执行 ALTER TABLE … ADD COLUMN 或 CREATE TABLE；@Entity 实体类只给出最终版本的表结构；写错：store.version === 0 分支的基线 CREATE TABLE 按最终实体写进了某列，后面的升级分支又对同表同列 ALTER TABLE … ADD COLUMN，全新库依次执行两者，报 duplicate column
- rule-6e84c8e1ecad｜源端在 Room onCreate 里播种时，目标把播种放进建表分支的同一事务，不用表为空判断｜读到：源端 RoomDatabase.Callback 的 onCreate(db) 里插入预置数据（首次建库才播种）；写错：目标端初始化时每次打开都查 SELECT COUNT(*)，结果为 0 就调用播种函数
