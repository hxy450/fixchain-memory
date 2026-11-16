# RdbStore 要返回受影响行数时用 update/delete 的返回值，不另查 SELECT changes()

审的是：代码
触发（任一种）：
- 读到：源端 Room @Query 的 UPDATE / DELETE 方法返回 Int，或目标 DAO 签名承诺返回 Promise<number> 受影响行数；写错的样子：写成 store.executeSql(...) 后另起 store.querySql('SELECT changes() AS value') 读行数，或 return 一个这样实现的共享 helper
- 读到：下游读到的共享 helper 是 executeSql 加 querySql('SELECT changes()')；写错的样子：下游 DAO / Repository 直接 return 这个 helper 的结果当行数
- 写错的样子：交回报告的风险里写 helper「依赖 RdbStore 单连接语义，可能不准」，代码没改
适用范围：数据层用 relationalStore 写 UPDATE / DELETE 并要返回受影响行数时
做法：
- UPDATE 写成 return await store.update(valuesBucket, new relationalStore.RdbPredicates(表名).equalTo(列, 值))，DELETE 写成 return await store.delete(predicates)，直接用它们返回的 number
- 共享 helper 的返回值依赖 SELECT changes() 这类连接级状态时，交付前换成 update / delete 的实现，或让 helper 不再承诺返回行数；下游复用前先看它的返回值从哪来
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- update(values: ValuesBucket, predicates: RdbPredicates): Promise<number>：RdbStore 的更新，Promise 返回受影响的行数（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.update；arkts-apis-data-relationalStore-RdbStore.md，update）
- delete(predicates: RdbPredicates): Promise<number>：RdbStore 的删除，Promise 返回受影响的行数（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.delete；arkts-apis-data-relationalStore-RdbStore.md，delete）
- executeSql(sql: string, bindArgs?: Array<ValueType>): Promise<void>：RdbStore 执行 SQL，不返回行数（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.executeSql）
- updateSync(values: ValuesBucket, predicates: RdbPredicates, conflict?: ConflictResolution): number：同族接口：RdbStore 的同步更新，返回受影响的行数（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.updateSync）
- deleteSync(predicates: RdbPredicates): number：同族接口：RdbStore 的同步删除，返回受影响的行数（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，RdbStore.deleteSync）
- update(values: ValuesBucket, predicates: RdbPredicates, conflict?: ConflictResolution): Promise<number>：同族接口：Transaction 里的更新，在事务内写时用（出处：鸿蒙 SDK 的 ets/api/@ohos.data.relationalStore.d.ts，Transaction.update）
- 改用 RdbPredicates + store.update / store.delete 的返回值后，断言行数的用例通过：原先数据已写入、返回值却是 0（出处：卡里修好并验证过）
未核实：「executeSql 和 querySql 落在不同连接」是生成者和修复者的判断，卡里没有 RdbStore 内部实现的证据；能确认的是改用 update / delete 返回值后用例通过
来源：1 张卡，1 个应用
- case-e6ec1491a065e800a4f8（com.nononsenseapps.feeder）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 3、建议 5；取值 7 ← 诊断
