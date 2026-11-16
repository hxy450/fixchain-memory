# 源码 register(this, priority) 时，目标总线订阅接口保留 priority 形参并在订阅点传入

审的是：代码
触发（任一种）：
- 读到：源码 `EventBus.getDefault().register(this, 1)` 这类带 priority 的注册；写错的样子：目标总线的订阅 API（如包着 `emitter.on` 的 subscribe）没有 priority 形参，头注写 priority「对本工程订阅方无行为差异，不迁移」，订阅点无优先级可传
适用范围：迁移带订阅优先级的 EventBus 注册
做法：
- 订阅 API 带 priority 形参（不传为 0），投递时按 priority 降序、同级按注册序调用
- 源端带 priority 的订阅点照源值传入，不以「订阅方互不依赖顺序」的推断去掉它
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- InnerEvent：The EventPriority settings do not take effect under event subscription：emitter 的 EventPriority 只作用于发布，订阅侧没有优先级，承载不了 register 的 priority（出处：鸿蒙 SDK 的 ets/api/@ohos.events.emitter.d.ts，emitter.InnerEvent）
- 总线按 priority 降序 / 注册序投递，订阅点补传源端优先级：返修后保留的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-a293ed8cf3fa860f8330（omni-notes-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 2 ← 诊断
