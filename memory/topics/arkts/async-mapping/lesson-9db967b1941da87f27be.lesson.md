# EventBus 迁移先核投递契约：emitter 异步且序列化 data，需同步按引用投递时自建订阅表，保留 priority 与嵌套 post 排队

ID：`lesson-9db967b1941da87f27be` · 版本：3 · 阶段：execute · 主题：[arkts/async-mapping](index.md)

概要：EventBus 需同步按引用投递时自建订阅表

信号：`EventBus`, `EventBus.getDefault`, `@ohos.events.emitter`, `eventHub`, `EventPriority`, `threadMode`, `POSTING`, `onEvent`, `instanceof`

## 何时使用

实现阶段把 greenrobot EventBus（register/post/onEvent）迁到目标端事件总线，在 @ohos.events.emitter、eventHub 与自建订阅表之间选择时

## 适用情境

源端 EventBus.getDefault().post(event) 携带实体对象（带方法的类实例、被 instanceof 判别），订阅方用 register(this, priority) 或依赖“post 返回前回调已执行”；派工只写“EventBus → emitter 或自研 typed pub/sub”；SDK d.ts 注明 EventPriority 对订阅不生效。

## 例外与边界

- 源事件只携带可序列化的纯数据，订阅方不依赖同步回调、优先级与投递顺序

## 原因

greenrobot EventBus 默认线程模式 POSTING 在 post 的线程内同步按引用回调，按 priority 降序、同级按注册序投递，投递中再 post 的事件排队到当前事件投递完。@ohos.events.emitter 异步投递并按跨线程传输规格序列化 data：类实例到达后丢原型，实例方法与 instanceof 失效，@State、@Observed 等装饰器修饰的复杂数据不支持传输（HarmonyOS 文档 js-apis-emitter，访问于 2026-10-17），post 返回时回调尚未执行；订阅接口也没有 priority 形参，订阅方之间的顺序依赖随之丢失。

## 做法

1. 先列源总线的投递契约：各订阅方法的 threadMode（默认 POSTING 即同步）、事件对象是否带方法或被 instanceof 判别、register 是否带 priority、post 中是否嵌套 post。
2. 需要同步按引用语义时自建进程内总线：订阅表按 priority 降序、同级按注册序；post 时对订阅表取快照后逐个同步回调；投递中再 post 的事件入队，当前事件投递完再处理。priority 作为 register 形参保留，订阅点照源端传入。
3. 只有纯数据事件、源端不依赖同步回调时才用 emitter；考虑 UIAbility 上下文的 eventHub 时，先核对其作用范围与投递方式再用。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [源端可观察缺陷照迁并核次数，修正走待批决策](../../process/unapproved-deviation/lesson-14411595fd9ac1e17683.lesson.md)（共享 1 张卡）
- [不补源端没有的元素；框架默认元素须保留](../../process/unapproved-deviation/lesson-352b96f599237cd27403.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-a293ed8cf3fa860f8330](../../../../store/cases/case-a293ed8cf3fa860f8330/5b59203d875d7187e99f77129cb00b802dad0c45e4571c82b666606995535ad5.json) · 结论：diagnosis, rec-8c042bae50, rec-73ad4a6e98
  卡片版本：`5b59203d875d7187e99f77129cb00b802dad0c45e4571c82b666606995535ad5`
