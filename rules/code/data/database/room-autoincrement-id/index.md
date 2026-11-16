# Room 自增主键 @PrimaryKey(autoGenerate = true) 的写入

agent 会看到什么：读到 Room 实体 @PrimaryKey(autoGenerate = true) val id: Int = 0、种子数据显式传固定 id、补充路径 copy(id = 0)，产物里是 relationalStore 手写的 INSERT 列清单或 ValuesBucket 里的 'id'

## 规矩

- rule-84fdcce7448f｜Room 自增主键迁成手写 INSERT 时，列清单和参数省略 id，不把默认 0 写进去｜读到：Room 实体 `@PrimaryKey(autoGenerate = true) val id: Int = 0`，行由映射函数新建、不设 id，经 `@Insert(onConflict = OnConflictStrategy.REPLACE)` 批量写入；写错：ArkTS 手写 `INSERT OR REPLACE INTO t (id, …) VALUES (?, …)`，把行对象的 id（默认 0）照绑；行接口的 id 是必填 number，上层按 Room 习惯填 0
- rule-d37858351a5e｜种子带固定主键时首建写入该 id，补充路径按 copy(id = 0) 插新行，两条路径分开构造｜读到：源端种子数据的 Room 实体构造里显式传 id = <常量>（固定主键）；手动补充或复制路径用 copy(id = 0) 插入；写错：首建播种的 ValuesBucket 不写 id、由自增主键重新编号；或补充路径复用首建的构造函数也写入固定 id
