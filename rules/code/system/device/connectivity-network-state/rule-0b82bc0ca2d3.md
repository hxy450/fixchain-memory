# 初始化链注册网络切换接收器时，目标用 createNetConnection 实现等价监听

审的是：代码
触发（任一种）：
- 读到：源端 Application 初始化链调用 register…Receiver() 注册 CONNECTIVITY_ACTION 接收器，注册前给“上次网络类型”赋初值，onReceive 里按前后网络类型调用业务检测；写错的样子：目标只声明了对应的来源常量，没有任何调用方，也没有 createNetConnection 监听；或逐项迁移 init 链时静默略过这个接收器，没有占位也没有决策记录
适用范围：实现阶段迁移初始化链里的网络切换监听，以及 AC 列出多个触发来源时
做法：
- 写服务前对照源码找出每个触发来源的调用点，读被注册的接收器本体
- 用 connection.createNetConnection() 得到 conn，conn.on('netAvailable' / 'netCapabilitiesChange' / 'netLost', …) 后 conn.register(cb)；注册时记下当前网络类型，回调里按 netCap.bearerTypes 判断，仅上次为 BEARER_CELLULAR、本次为 BEARER_WIFI 时调用业务检测并传对应来源常量
- 暂不实现时登记占位或决策，不静默略过
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function createNetConnection(netSpecifier?: NetSpecifier, timeout?: number): NetConnection：创建网络监听对象（出处：鸿蒙 SDK 的 ets/api/@ohos.net.connection.d.ts，connection.createNetConnection）
- on(type: 'netCapabilitiesChange', callback: Callback<NetCapabilityInfo>): void；NetCapabilityInfo.netCap.bearerTypes: Array<NetBearType>：网络能力变化回调，从 bearerTypes 读当前网络类型（出处：鸿蒙 SDK 的 ets/api/@ohos.net.connection.d.ts，NetConnection.on、NetCapabilities.bearerTypes）
- NetBearType.BEARER_CELLULAR = 0、NetBearType.BEARER_WIFI = 1：蜂窝和 Wi‑Fi 的取值（出处：鸿蒙 SDK 的 ets/api/@ohos.net.connection.d.ts，NetBearType）
- register(callback: AsyncCallback<void>): void，需要 ohos.permission.GET_NETWORK_INFO：开始接收通知；GET_NETWORK_INFO 是 system_grant，在 module.json5 声明即可（出处：鸿蒙 SDK 的 ets/api/@ohos.net.connection.d.ts，NetConnection.register；permissions-for-all.md，ohos.permission.GET_NETWORK_INFO）
- createNetConnection 注册 netAvailable/netCapabilitiesChange/netLost，注册时赋初值，仅蜂窝→Wi‑Fi 时触发检测：卡里修好的做法（出处：卡里修好并验证过）
针对本应用要查的：
- 触发条件和传入的来源常量：源工程里被注册的接收器类的 onReceive，以及注册前赋初值的代码；照它的前后类型比较写目标端条件；源端“蜂窝族”包含哪些网络类型照源端判断写
来源：1 张卡，1 个应用
- case-c234d95411230bdbffda（DeepAI全能PPT）：做法第 1 步 ← 建议 4；做法第 2 步 ← 诊断、建议 4；做法第 3 步 ← 建议 4；取值 5 ← 诊断
