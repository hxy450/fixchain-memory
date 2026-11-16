# 远端行映射成本地行时按源端公式重建组合主键，再用 ON_CONFLICT_REPLACE 落库

审的是：代码
触发（任一种）：
- 读到：目标库 schema 里这张表的键列是 TEXT NOT NULL 并建了 CREATE UNIQUE INDEX；源端落库前用一个方法把几个字段（如记录 id、日期、用户 id）拼成组合主键；写错的样子：同步仓库把远端 payload 直接 fromJson 映射成实体，没有生成主键就用 ConflictResolution.ON_CONFLICT_REPLACE 批量插入；增量和全量两条路径有一条漏了也算
适用范围：目标端把远端拉到的记录批量写入本地 relationalStore 表，而这张表的唯一键由客户端按源端公式生成、远端 payload 不一定带时
做法：
- 在远端行映射成本地行的那一步，照源端生成主键的方法重建唯一键（字段顺序、分隔符照抄；子表按源端再拼上子项 id），增量和全量路径都调用同一个规范化函数
- 主键都生成之后，再用 ON_CONFLICT_REPLACE 批量插入（如 store.batchInsertWithConflictResolution(table, rows, relationalStore.ConflictResolution.ON_CONFLICT_REPLACE)）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ConflictResolution.ON_CONFLICT_REPLACE = 5：插入时遇到冲突就替换已有行；键为空或相同的多行会互相覆盖（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，ConflictResolution.ON_CONFLICT_REPLACE）
- batchInsertWithConflictResolution(table: string, values: Array<ValuesBucket>, conflict: ConflictResolution): Promise<number>：RdbStore 按冲突策略批量插入（@since 18，出自声明）（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.batchInsertWithConflictResolution）
- insert(table: string, values: ValuesBucket, conflict: ConflictResolution): Promise<number>：同族接口：RdbStore 单行按冲突策略插入（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.insert）
- batchInsertWithConflictResolution(table: string, values: Array<ValuesBucket>, conflict: ConflictResolution): Promise<number>（Transaction）：同族接口：事务里按冲突策略批量插入（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，Transaction.batchInsertWithConflictResolution）
- 增量和全量两条路径在映射远端行时都按源端公式重建主键后，多条状态不再落在同一个空键上互相覆盖：返修后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端组合主键的公式：源工程 Java/Kotlin 里写本地库之前给主键列赋值的方法（按表的主键列名搜赋值处）；照抄参与拼接的字段、顺序和分隔符；子表另拼的字段一并记下
来源：1 张卡，1 个应用
- case-9831097c34ea91e10955（记得日历）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断；取值 5 ← 诊断
