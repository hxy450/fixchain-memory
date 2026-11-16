# Compose 状态迁 V2 与 @Trace 观察

源端有 Compose remember / mutableStateOf / derivedStateOf、LaunchedEffect(key) 这类按键值重跑的副作用、data class copy 更新，目标端有 @Local、@Computed、@ObservedV2 / @Trace 模型和数组、@Watch / @Monitor、UIUtils.getTarget 时

## 触发族

- [data class 用 copy 更新的列表项和模型字段](data-class-copy/index.md)（5 条）：读到 Kotlin data class 用 copy(...) 替换同 id 的列表项、ViewModel 改模型字段，交回的代码里模型写成 readonly、ForEach 的键只取 id，或用新对象替换元素而行组件 @Param 收整个元素
- [页面读 @ObservedV2 模型的 @Trace 状态](observedv2-in-page/index.md)（7 条）：读到 @ObservedV2 / @Trace 的模型或 store；产物里页面把它的字段拷进 @Local、靠 onPageShow 或手动 refresh 同步，或 VM 异步写 @Trace 列表
- [Compose remember 状态迁成 V2 状态后的重置时机](compose-remember-state/index.md)（4 条）：读到 Compose 的 remember / remember(key) / derivedStateOf / mutableStateOf，或对话框里 remember 的选择状态；产物里对应的 @Local / @State / @Computed 什么时候重置、重算，以及拿 === 判脏
- [Compose 按键值变化才重跑的副作用](compose-keyed-effect/index.md)（2 条）：读过的 Compose 源里有 LaunchedEffect(key…)、animateColorAsState(targetValue)、AnimatedContent(targetState) 这类键值或目标值变了才重跑的写法；交回的代码在 @Watch、@Monitor 或每次状态提交时都重评、都调回调
- [定时器里逐格计算的 @Trace 数组](trace-array-raw-target/index.md)（1 条）：读到源端在协程 delay 之后对普通 List 网格逐格计算、判定、计数再整体 copy 提交，目标网格是 @Trace 字段、tick 用 setTimeout；产物里回调把 @Trace 数组字段 this.… 直接交给逐格计算函数，没有 UIUtils.getTarget(...)
