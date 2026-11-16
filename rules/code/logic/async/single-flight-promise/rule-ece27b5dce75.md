# 单飞缓存 Promise 的入口方法不声明 async，直接返回缓存的同一 Promise 实例

审的是：代码
触发（任一种）：
- 读到：规格给出返回 `Promise<T>` 的一次性入口，AC 要求「防重守卫：连续两次调用仅执行一次、只写一次」；写错的样子：入口写成 `static async` 方法，方法体 `return` 缓存在字段里的 Promise，注释却写「重入共享同一 Promise」
适用范围：用字段缓存首次 Promise 做单飞防重的异步入口
做法：
- 入口方法去掉 async，直接返回已缓存的 Promise 实例；真正的异步工作放进被缓存的私有 async 函数（首次调用时 this.task = this.doWork()）
- 注释或契约写了「重复调用返回同一 Promise」的，写完核对签名：async 方法每次返回新的包装 Promise，只保证结果相同，需要实例相同就不能 async；做不到就不在注释里声称
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- async 方法里 `return cachedPromise` 每次调用都得到新的 Promise；去掉 async 后两次调用 `===` 成立：工作只执行一次两种写法都成立，差别在实例身份（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-8a7b85073af9754bb709（Countdate）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2、建议 3；取值 1 ← 诊断
