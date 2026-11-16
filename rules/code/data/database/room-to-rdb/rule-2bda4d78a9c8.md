# Room 库迁 relationalStore 时，建表和升级 SQL 照源 schema 与 Migration 写

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
