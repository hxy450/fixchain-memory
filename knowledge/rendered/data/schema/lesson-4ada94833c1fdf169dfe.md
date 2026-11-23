# relationalStore 写操作返回受影响行数时取 update/delete 的返回值，不在 executeSql 后另查 changes()

## 何时使用

数据层实现阶段，为 UPDATE/DELETE 编写 DAO 方法或共享写入 helper，并决定受影响行数从哪里取时

## 适用情境

源端 Room @Query UPDATE/DELETE 返回 Int，或目标 DAO 签名承诺 Promise<number> 受影响行数；目标 relationalStore 的 executeSql 返回 Promise<void>，update(values, predicates) 与 delete(predicates) 返回 Promise<number>。

## 原因

executeSql 不给出行数，另起 querySql('SELECT changes()') 读的是连接级状态：已观察到数据已写入、方法却恒返回 0（成因按生成者与修复者判断为两次调用不在同一连接，未见内部实现证据）。依赖返回值的单调更新判定、清理计数与验收断言随之失效。

## 做法

1. 需要行数时直接用 store.update(values, predicates) / store.delete(predicates) 的返回值，不在 executeSql 之后读取 changes()。
2. SQL 带 COALESCE、子查询等无法写成 ValuesBucket 的表达式时，先按同一 WHERE 查出 id 或 count(*)（需保留原值的先读后写），再用 predicates 更新并返回该数量。
3. 共享写入 helper 自检发现返回值依赖未验证的平台假设、且有可用替代 API 时，交付前换成替代实现或不再承诺该返回值；下游复用前先看返回值来源。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕RdbStore.update(values, predicates) 和 RdbStore.delete(predicates) 的 Promise 兑现值是受影响的行数；executeSql 的 Promise 不带返回值
- 〔原因〕单测中用 RdbStore.executeSql 执行 UPDATE，随后用 querySql('SELECT changes()') 读行数，数据已经写入，读到的行数却是 0
