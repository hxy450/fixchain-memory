# 源端在 Room onCreate 里播种时，目标把播种放进建表分支的同一事务，不用表为空判断

审的是：代码
触发（任一种）：
- 读到：源端 RoomDatabase.Callback 的 onCreate(db) 里插入预置数据（首次建库才播种）；写错的样子：目标端初始化时每次打开都查 SELECT COUNT(*)，结果为 0 就调用播种函数
适用范围：源端只在首次建库时播种预置数据，目标端用 relationalStore 的 RdbStore 自行建表和播种时
做法：
- 播种放进建表分支（表都还不存在、要执行 CREATE TABLE 的那一支）的同一事务：beginTransaction() → executeSql(CREATE TABLE …) → insert 种子 → commit()
- 不用「表为空」（COUNT(*) === 0）判断代替「首次创建」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 播种移进「两表都不存在」的建表事务里，删光数据后重开不再重播种：首建播种的修法（出处：卡里修好并验证过）
- beginTransaction(): void；commit(): void：RdbStore 的事务开始和提交（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.beginTransaction、RdbStore.commit）
- executeSql(sql: string, bindArgs?: Array<ValueType>): Promise<void>：执行 CREATE TABLE 等语句（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.executeSql）
未核实：卡里的行为出自 HarmonyOS 6.0.1(21)，本机按 API 23 的声明核对
来源：1 张卡，1 个应用
- case-b2793695ef65617c820a（Cofi）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 1 ← 诊断
