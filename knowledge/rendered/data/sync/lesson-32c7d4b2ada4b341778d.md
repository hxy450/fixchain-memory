# greenrobot EventBus 迁移先核投递契约：需同步按引用、priority 与嵌套 post 排队时自建进程内总线，不直接用 emitter

## 何时使用

基础层实现阶段，为源端事件总线选择目标投递模型、订阅优先级与事件载荷形态时

## 适用情境

源端用 greenrobot EventBus（默认线程模式在 post 线程同步回调订阅者、事件对象按引用传递、register(this, priority)、订阅回调中嵌套 post 会排队）发布实体对象事件；目标候选是 @ohos.events.emitter、eventHub 或自建订阅表。

## 例外与边界

- 同步回调只是默认 POSTING 模式的语义：订阅方法在 @Subscribe 里写了 threadMode = MAIN、MAIN_ORDERED、BACKGROUND 或 ASYNC 的（MAIN 在非主线程 post 时、MAIN_ORDERED 与 ASYNC 总是经队列投递），post 返回时这些订阅不一定已处理完，按各自的线程模式迁，不一律改成同步调用。
- 源端用了 postSticky 或 @Subscribe(sticky = true) 的，自建总线要保留粘性事件：按事件类型记住最近一次，粘性订阅者注册时立即收到，并提供对应的取出与移除。

## 原因

EventBus 默认线程模式下 post 返回时订阅方已处理完，高 priority 订阅者先收到，分发中再 post 的事件排在当前分发之后。emitter 异步投递（post 返回后才回调），data 按跨线程方式序列化传递（类实例丢失原型与方法，instanceof 失效），订阅侧的 EventPriority 不生效（@ohos.events.emitter.d.ts 注释）；照搬会改变事件到达时机、顺序与载荷类型。

## 做法

1. 逐条列出源端投递契约：同步还是异步、按引用还是拷贝、priority 与同级注册序、嵌套 post 是否排队，以及订阅者是否依赖在 post 返回前处理完。
2. 需要同步按引用语义时自建进程内总线：订阅表按 priority 降序、同级按注册序，post 时对订阅表取快照逐个同步调用，分发中再 post 的事件入队、当前分发结束后处理；register 保留 priority 形参，订阅点照源传入。
3. 只有契约允许异步投递与可序列化载荷时才用 emitter；载荷是带方法的实体类时不直接经 emitter 传递。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 org.greenrobot:eventbus 3.1.1（字节码）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 原因 / 做法第 2 步〕greenrobot EventBus 3.1.1：订阅方法没有在 @Subscribe 里另写 threadMode、priority 时，threadMode 为 POSTING（在 post 所在线程直接同步调用订阅方法）、priority 为 0；同一事件类型的订阅按 priority 从高到低排列，同级按注册先后；post 先把事件放进当前线程的队列，当前线程正在分发时直接返回，嵌套 post 的事件在当前分发结束后才处理
- 〔原因 / 做法第 3 步〕Emitter 事件异步执行：发布后插入内部事件队列，队列串行执行到它时才调用订阅回调，emit 返回时回调还没有执行
- 〔原因 / 做法第 3 步〕Emitter 的 EventData.data 支持的数据类型是 Array、ArrayBuffer、Boolean、DataView、Date、Error、Map、Number、Object、Primitive（除 symbol）、RegExp、Set、String、TypedArray
- 〔原因〕emitter.InnerEvent 的 priority（EventPriority）只在发布时生效，订阅时设置不起作用
