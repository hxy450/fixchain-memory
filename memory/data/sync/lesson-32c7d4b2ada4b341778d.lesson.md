# greenrobot EventBus 迁移先核投递契约：需同步按引用、priority 与嵌套 post 排队时自建进程内总线，不直接用 emitter

ID：`lesson-32c7d4b2ada4b341778d` · 版本：1

[本主题](index.md)

## 何时使用

基础层实现阶段，为源端事件总线选择目标投递模型、订阅优先级与事件载荷形态时

## 适用情境

源端用 greenrobot EventBus（默认线程模式在 post 线程同步回调订阅者、事件对象按引用传递、register(this, priority)、订阅回调中嵌套 post 会排队）发布实体对象事件；目标候选是 @ohos.events.emitter、eventHub 或自建订阅表。

## 原因

EventBus 默认线程模式下 post 返回时订阅方已处理完，高 priority 订阅者先收到，分发中再 post 的事件排在当前分发之后。emitter 异步投递（post 返回后才回调），data 按跨线程方式序列化传递（类实例丢失原型与方法，instanceof 失效），订阅侧的 EventPriority 不生效（@ohos.events.emitter.d.ts 注释）；照搬会改变事件到达时机、顺序与载荷类型。

## 做法

1. 逐条列出源端投递契约：同步还是异步、按引用还是拷贝、priority 与同级注册序、嵌套 post 是否排队，以及订阅者是否依赖在 post 返回前处理完。
2. 需要同步按引用语义时自建进程内总线：订阅表按 priority 降序、同级按注册序，post 时对订阅表取快照逐个同步调用，分发中再 post 的事件入队、当前分发结束后处理；register 保留 priority 形参，订阅点照源传入。
3. 只有契约允许异步投递与可序列化载荷时才用 emitter；载荷是带方法的实体类时不直接经 emitter 传递。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-a293ed8cf3fa860f8330](../../../store/cases/case-a293ed8cf3fa860f8330/5b59203d875d7187e99f77129cb00b802dad0c45e4571c82b666606995535ad5.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`5b59203d875d7187e99f77129cb00b802dad0c45e4571c82b666606995535ad5`
