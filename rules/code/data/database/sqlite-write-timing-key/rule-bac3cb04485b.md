# 用缓存的 Promise 做 RdbStore 单例时，打开失败在 catch 里复位缓存，下次访问重试

审的是：代码
触发（任一种）：
- 读到：源端每次访问都调 getWritableDatabase() / getReadableDatabase()；写错的样子：目标端 init 把包着 relationalStore.getRdbStore 的 Promise 存进单例字段后永不清空，一次失败后每次 DAO 调用都拿到同一个 rejected Promise
适用范围：目标端用缓存 Promise 去重的数据库单例初始化（init、getStore 一类入口）
做法：
- 缓存为空时才发起打开：cached = open().catch((e) => { cached = undefined; throw e; })，返回 cached；失败时先复位再抛出，下一次访问重新调 getRdbStore
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getWritableDatabase 打开成功后缓存；因权限、磁盘满等失败的，问题修好后再次调用可能成功：源端基类的隐式契约：失败不钉死，每次访问都重新尝试打开（出处：android.database.sqlite.SQLiteOpenHelper#getWritableDatabase）
- function getRdbStore(context: Context, config: StoreConfig): Promise<RdbStore>：目标端打开库的接口，返回的 Promise 被缓存后失败就一直是 rejected（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，relationalStore.getRdbStore）
未核实：卡里的行为出自 HarmonyOS 6.1.1(24)，本机核实用的是 API 23 的声明
来源：1 张卡，1 个应用
- case-bbb6bcf0a09493406de9（omni-notes-hmos）：做法第 1 步 ← 建议 3、建议 1
