# relationalStore 写操作返回受影响行数时取 update/delete 的返回值，不在 executeSql 后另查 changes()

ID：`lesson-4ada94833c1fdf169dfe` · 版本：1

[本主题](index.md)

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

## 来源（按需复核）

- [case-e6ec1491a065e800a4f8](../../../store/cases/case-e6ec1491a065e800a4f8/866b6acfa73b2e7b45da07fdac76965935188499ebe4dcb405fc45af12241fed.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`866b6acfa73b2e7b45da07fdac76965935188499ebe4dcb405fc45af12241fed`
