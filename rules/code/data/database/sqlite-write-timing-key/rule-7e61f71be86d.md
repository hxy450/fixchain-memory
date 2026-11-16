# SQLiteOpenHelper 子类迁成 RdbStore 时按 store.version 分派建表、升级、降级报错

审的是：代码
触发（任一种）：
- 读到：源端类 extends SQLiteOpenHelper，构造里 super(context, name, factory, VERSION)，重写 onCreate / onUpgrade；写错的样子：目标端 getRdbStore 打开后直接调建表，或写成 store.version >= VERSION 就 return、否则建表并写 version；没有 version === 0 建表、小于 VERSION 走 onUpgrade、大于 VERSION 抛错的分派
- 读到：规格或决策台账写「升级路径不迁移」「onCreate 即唯一入口」；写错的样子：目标端把 onUpgrade 分派骨架连同 store.version 写回一起删掉，只剩建表
适用范围：安卓 SQLiteOpenHelper 子类的打开与建表逻辑迁成 @ohos.data.relationalStore 的 RdbStore 时
做法：
- 打开后读 const v = store.version：v === 0 执行 onCreate（建表脚本）；0 < v < VERSION 执行 onUpgrade(store, v, VERSION)；v > VERSION 直接 throw（对应 onDowngrade 默认报错）；v 不等于 VERSION 时分派完写 store.version = VERSION。VERSION 取源端传给 super(...) 的第 4 个参数
- 规格写「升级路径不迁移」时只免去 onUpgrade 的函数体，分派骨架、降级报错和 store.version 写回照样保留
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- version: number：RdbStore 的版本属性，可读可写；写入的值必须是大于 0 的整数（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.version）
- 新建的数据库 version 为 0：v === 0 就是首次创建，对应源端 onCreate（出处：data-persistence-by-rdb-store.md，开发步骤）
- version == 0 → onCreate(db)；version > mNewVersion → onDowngrade；否则 onUpgrade(db, version, mNewVersion)；之后 db.setVersion(mNewVersion)：源端基类在 version 不等于构造传入的版本时做的分派（出处：android.database.sqlite.SQLiteOpenHelper#getDatabaseLocked）
- onDowngrade 默认 throw new SQLiteException("Can't downgrade database from version " + oldVersion + " to " + newVersion)：子类没重写 onDowngrade 时，库版本高于代码版本就报错，目标端对应写 throw（出处：android.database.sqlite.SQLiteOpenHelper#onDowngrade）
针对本应用要查的：
- VERSION 的值和 onUpgrade 里各版本区间要执行的脚本：源工程里继承 SQLiteOpenHelper 的类：构造里 super(...) 的第 4 个参数、onUpgrade 按 oldVersion 的分支；assets 或 res/raw 下的升级 SQL 文件；VERSION 原样写成目标端常量；onUpgrade 的各分支按 oldVersion 区间搬成目标端 onUpgrade 里的分支
未核实：卡里的行为出自 HarmonyOS 6.1.1(24)，本机核实用的是 API 23 的声明
来源：1 张卡，1 个应用
- case-bbb6bcf0a09493406de9（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1
