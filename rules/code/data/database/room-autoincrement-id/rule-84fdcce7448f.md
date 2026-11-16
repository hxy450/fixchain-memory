# Room 自增主键迁成手写 INSERT 时，列清单和参数省略 id，不把默认 0 写进去

审的是：代码
触发（任一种）：
- 读到：Room 实体 `@PrimaryKey(autoGenerate = true) val id: Int = 0`，行由映射函数新建、不设 id，经 `@Insert(onConflict = OnConflictStrategy.REPLACE)` 批量写入；写错的样子：ArkTS 手写 `INSERT OR REPLACE INTO t (id, …) VALUES (?, …)`，把行对象的 id（默认 0）照绑；行接口的 id 是必填 number，上层按 Room 习惯填 0
适用范围：把 Room 实体和 @Insert 方法翻成 relationalStore 手写 INSERT / INSERT OR REPLACE 时
做法：
- 列清单和参数都省略自增 id：`INSERT OR REPLACE INTO t (col1, col2, …) VALUES (?, ?, …)`，由数据库分配；确需保留时只在 id > 0 时绑定
- REPLACE 只作用于真实唯一键；行接口保留 id 时写成可选或在注释里注明「插入时忽略，由数据库分配」
- 写完用「同组插入两行再读回，行数应为 2」的最小用例自检
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- executeSql(sql: string, bindArgs?: Array<ValueType>): Promise<void>：手写 SQL 的执行接口，bindArgs 按 ? 的顺序绑定（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.executeSql）
- 显式给出主键值时 SQLite 不再自增；同组多行都写 0，第二行起按主键 0 REPLACE 前一行，只剩 1 行：Room「0 即未赋值」的语义在手写 SQL 里不存在（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-db65a2776f5a1a45dbe4（CleanSweep）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2、建议 3；做法第 3 步 ← 建议 2；取值 2 ← 诊断
