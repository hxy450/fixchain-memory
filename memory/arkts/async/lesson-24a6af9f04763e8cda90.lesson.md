# 缓存 Promise 做单飞的入口方法不声明 async，直接返回缓存的实例：async 每次返回新的包装 Promise，只保证结果相同、不保证实例相同

ID：`lesson-24a6af9f04763e8cda90` · 版本：2

[本主题](index.md)

## 何时使用

服务层或 ViewModel 实现阶段，为一次性异步入口（启动恢复、首次加载）写单飞防重并确定方法签名、且契约或注释要求重复调用返回同一 Promise 实例时

## 适用情境

规格要求返回 Promise 的入口重复调用只执行一次；实现用静态或成员字段缓存首次的 Promise，并在注释或契约里声称重入共享同一 Promise；同类其他方法多写成 async。

## 例外与边界

- 契约和测试只要求工作只执行一次、不要求同一实例时，已写成 async 的入口不算错，不为此改签名。
- 去掉 async 后，入口里在返回缓存之前同步抛出的异常会直接抛给调用方，不再变成被拒绝的 Promise；入口只做取缓存和存缓存，可能抛错的逻辑全部放进被缓存的私有 async 工作函数。

## 原因

async 函数会把 return 的 Promise 再包一层，每次调用拿到不同实例：工作仍只执行一次，但“返回同一 Promise”的自述契约不成立，按该契约断言实例相等的测试会失败。

## 做法

1. 单飞入口写成普通方法：首次调用把私有 async 工作函数的 Promise 存入字段并返回，之后直接返回该字段；不给入口加 async。
2. 注释或契约写了“重复调用返回同一 Promise”时，写完核对签名；只需工作去重时只声明“只执行一次”，不声称同一实例。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-8a7b85073af9754bb709](../../../store/cases/case-8a7b85073af9754bb709/dff920cdea61a277387d761edd55f1da2b2f61bc8fadd6862aa49173b7451f4a.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`dff920cdea61a277387d761edd55f1da2b2f61bc8fadd6862aa49173b7451f4a`
