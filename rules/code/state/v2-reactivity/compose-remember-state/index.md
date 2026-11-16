# Compose remember 状态迁成 V2 状态后的重置时机

agent 会看到什么：读到 Compose 的 remember / remember(key) / derivedStateOf / mutableStateOf，或对话框里 remember 的选择状态；产物里对应的 @Local / @State / @Computed 什么时候重置、重算，以及拿 === 判脏

## 规矩

- rule-0e8bd133adbd｜条件挂载对话框里的 remember 状态提到页级时，每次打开都重置并重跑初始化｜读到：源端对话框 Composable 内用 remember 保存选择状态（每次打开都是新状态）；写错：目标端选择状态放在页面级 @State / @Local，打开对话框时不清空上次的选择
- rule-5709926d599c｜源端 remember(key) 派生输入状态时，目标只在 key 真正变化时重置，同值赋值不动｜读到：Compose 里名称输入用 `remember(…, 类型名) { mutableStateOf(…) }` 派生：只有类型名变化才重置名称；写错：目标的类型选择 onClick 每次都给 @Local 名称字段重新赋值，没有比较新旧类型，重选当前类型也会清掉用户已改的名称
- rule-3217751a2810｜源端无键 remember 只在首次组合求值，目标按条目缓存一次，不写成每次重算的 @Computed｜读到：val x by remember { derivedStateOf { … } } 没有 key，只在首次组合时求值（如是否显示小数位）；写错：目标写成 @Computed getter 或每次调用都重新判断的方法，依赖变化（如倍率变化）时结果跟着变
- rule-f00ad41fa89c｜源端靠引用比较判脏时，V2 里不拿 @Local 数组和另存数组做 ===，改用已替换标志｜读到：Compose 里 `remember(x) { mutableStateOf(x) }` 取初值，退出前的未保存判断用 state !== x 引用比较（未改动时两侧是同一对象）；写错：目标新建两个独立数组 `@Local steps = []` 与另存的初始数组，判脏写成 this.steps === this.initial…，新增模式两个 [] 恒不等，编辑模式 @Local 代理与原数组也不等
