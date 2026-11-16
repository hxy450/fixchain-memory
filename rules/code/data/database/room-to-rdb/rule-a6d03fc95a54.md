# 源端 Room 有 ADD COLUMN 迁移时，基线建表只写 v1 的列，后加的列只由迁移添加

审的是：代码
触发（任一种）：
- 读到：@Database(version = N) 大于 1，Migration(1, 2) 等的 migrate 里执行 ALTER TABLE … ADD COLUMN 或 CREATE TABLE；@Entity 实体类只给出最终版本的表结构；写错的样子：store.version === 0 分支的基线 CREATE TABLE 按最终实体写进了某列，后面的升级分支又对同表同列 ALTER TABLE … ADD COLUMN，全新库依次执行两者，报 duplicate column
适用范围：把 Room 实体和 Migration 转写成 relationalStore 建表 SQL 和 store.version 逐级升级分支时
做法：
- 以实体类为最终 schema，按各 Migration 逆推每一版的旧结构；store.version === 0 的基线 CREATE 只写 v1 已有的表和列，由后续迁移 ADD COLUMN 或 CREATE TABLE 的列、表不出现在基线里
- 写完逐条比对每个 ADD COLUMN 的列名是否已出现在同表的基线 CREATE 中，或在空库上从 version 0 逐级执行全部 DDL，确认全新安装和旧版本升级都走到目标版本
- 若全新库直接按最终 schema 建表，就在同一分支把 store.version 直接设为最终版本，只对旧库走增量迁移；不把最终 schema 基线和完整迁移重放混用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- version: number；设置时必须是大于 0 的整数：RdbStore 的版本号，升级分支据此判断（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.version）
- 新建的数据库版本默认为 0；官方示例在 version 为 0 的分支建表后直接把版本设为最终版本，版本为 1、2 的旧库才逐级 ALTER：两种合法做法之一：最终 schema 基线配直接设最终版本（出处：data-persistence-by-rdb-store.md，开发步骤）
- executeSql(sql: string, bindArgs?: Array<ValueType>): Promise<void>：执行建表和 ALTER 语句（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.executeSql）
- 从基线 CREATE 删除迁移才加的列、只由迁移添加后，全新库能逐级升到目标版本：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 每一版的表结构：源工程 @Database 类里的 version 和 addMigrations 登记的各个 Migration 对象的 migrate 方法，以及 @Entity 实体类；从实体（最终版）倒着减去每个迁移加的列和表，得到 v1 结构写进基线；每个迁移的 SQL 照写进对应的升级分支
未核实：卡里的环境是 HarmonyOS SDK 6.0.2(22)，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-648559f22685378197cb（CleanSweep）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 3；取值 4 ← 诊断
