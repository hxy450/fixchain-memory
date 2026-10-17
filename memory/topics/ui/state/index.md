# ui/state

状态驱动刷新：可观察模型与变更信号、状态到控件的绑定、生命周期触发的加载，以及操作结果反馈。

[上一级](../index.md)

## 子主题

- [binding](binding/index.md) — 状态到控件的绑定与刷新：随状态变的参数不作 @Builder 值参、事件给出的目标值直写、按状态显隐、乐观更新。（8 条）
- [feedback](feedback/index.md) — 操作结果反馈：异步结果各分支的副作用、失败隔离与降级语义、loading 收口、提示浮层的承载与队列。（10 条）
- [lifecycle](lifecycle/index.md) — 生命周期触发的加载与复位：返回不再走 aboutToAppear、加载入口单飞、监听成对释放、框架会恢复的焦点与状态。（8 条）
- [observation](observation/index.md) — 共享可观察模型的订阅：@Trace 字段判定与直读、新数组赋值发变更、ForEach 键与原位更新、实例拆分。（9 条）
