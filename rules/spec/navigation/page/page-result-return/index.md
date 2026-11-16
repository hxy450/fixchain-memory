# 页面之间回传结果的通道（savedStateHandle 回传）

agent 会看到什么：读到安卓源用 savedStateHandle 回传：子页写结果后 navigateUp()，来源页回来后读取；规格的实现映射只写「NavPathStack param + onResult 回调 / emitter 事件」或「addReturn 后 pop」，没写载荷类型、生产端用哪个出栈调用、消费端在哪个时机读取

## 规矩

- rule-c4acf08b9ec9｜规格里每条回传通道写清载荷类型、生产端出栈调用和消费端触发点｜读到：安卓源用 savedStateHandle 回传：子页写结果后 navigateUp()，来源页回来后读取；写错：实现映射只写「NavPathStack param + onResult 回调 / emitter 事件」或「addReturn 后 pop」，没写载荷类型、生产端用哪个出栈调用、消费端在哪个时机读取
