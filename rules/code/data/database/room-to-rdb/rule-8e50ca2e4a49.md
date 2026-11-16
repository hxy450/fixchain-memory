# 建表 SQL 照 Room 最终 schema 的 createSql 写、不加 DEFAULT，库名照源端

审的是：代码
触发（任一种）：
- 读到：源工程有 Room 导出的 schemas/<Database 全名>/<version>.json，或 Room.databaseBuilder(context, X::class.java, "name.db")；写错的样子：目标建表语句给可空列加了源 schema 没有的 DEFAULT、改了 NOT NULL，或 StoreConfig 的 name 和源端库名不一样
适用范围：把 Room 实体落成 relationalStore 建表 SQL、并定库名时
做法：
- 建表 SQL 用最新版本 schema JSON 里各实体的 createSql 和字段的 notNull，不添加源端没有的 DEFAULT 和约束
- StoreConfig 的 name 写 Room.databaseBuilder 的第三个参数
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 库名改成源端 databaseBuilder 的库名、建表按最终 schema 去掉 DEFAULT 后，和源 schema 对齐：返修的做法（出处：卡里修好并验证过）
针对本应用要查的：
- 最终 schema 和库名：源工程模块下 Room 导出的 schemas 目录（按 @Database 类的全名分目录，每个版本一个 JSON），以及调用 Room.databaseBuilder 的地方；取版本号最大的 JSON，读 database.entities 里每个实体的 createSql 和 fields 的 notNull；库名读 databaseBuilder 的第三个实参
来源：1 张卡，1 个应用
- case-a3f7f5fbc8635b723b96（Cofi）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 1 ← 诊断
