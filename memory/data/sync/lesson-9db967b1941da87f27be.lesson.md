# EventBus 迁移先核投递契约：emitter 异步且序列化 data，需同步按引用投递时自建订阅表，保留 priority 与嵌套 post 排队

ID：`lesson-9db967b1941da87f27be` · 版本：1

[本主题](index.md)

## 何时使用

实现阶段把 greenrobot EventBus（register/post/onEvent）迁到目标端事件总线，在 @ohos.events.emitter、eventHub 与自建订阅表之间选择时

## 适用情境

源端 EventBus.getDefault().post(event) 携带实体对象（带方法的类实例、被 instanceof 判别），订阅方用 register(this, priority) 或依赖“post 返回前回调已执行”；派工只写“EventBus → emitter 或自研 typed pub/sub”；SDK d.ts 注明 EventPriority 对订阅不生效。

## 例外与边界

- 源事件只携带可序列化的纯数据，订阅方不依赖同步回调、优先级与投递顺序

## 原因

greenrobot EventBus 默认线程模式 POSTING 在 post 的线程内同步按引用回调，按 priority 降序、同级按注册序投递，投递中再 post 的事件排队到当前事件投递完。@ohos.events.emitter 异步投递并序列化 data：类实例到达后丢原型，实例方法与 instanceof 失效，post 返回时回调尚未执行；订阅接口也没有 priority 形参，订阅方之间的顺序依赖随之丢失。

## 做法

1. 先列源总线的投递契约：各订阅方法的 threadMode（默认 POSTING 即同步）、事件对象是否带方法或被 instanceof 判别、register 是否带 priority、post 中是否嵌套 post。
2. 需要同步按引用语义时自建进程内总线：订阅表按 priority 降序、同级按注册序；post 时对订阅表取快照后逐个同步回调；投递中再 post 的事件入队，当前事件投递完再处理。priority 作为 register 形参保留，订阅点照源端传入。
3. 只有纯数据事件、源端不依赖同步回调时才用 emitter；考虑 UIAbility 上下文的 eventHub 时，先核对其作用范围与投递方式再用。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-a293ed8cf3fa860f8330](../../../store/cases/case-a293ed8cf3fa860f8330/5b59203d875d7187e99f77129cb00b802dad0c45e4571c82b666606995535ad5.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`5b59203d875d7187e99f77129cb00b802dad0c45e4571c82b666606995535ad5`
