# Compose 按键值变化才重跑的副作用

agent 会看到什么：读过的 Compose 源里有 LaunchedEffect(key…)、animateColorAsState(targetValue)、AnimatedContent(targetState) 这类键值或目标值变了才重跑的写法；交回的代码在 @Watch、@Monitor 或每次状态提交时都重评、都调回调

## 规矩

- rule-0b8485aa9890｜LaunchedEffect(key1, key2) 驱动的弹窗调度，目标只在键值变化时重评｜读到：LaunchedEffect(key1, key2) { … } 里按两个布尔键决定是否弹出启动弹窗；写错：目标的调度函数在每次设置或其它状态变化（如 @Watch、aboutToAppear 之后的回调）时都重评，关闭后因无关状态更新再次弹出
- rule-98a1b7c21d8e｜把 @Monitor 改成生产方回调时，回调入口比较监听字段上次值，未变就返回｜读到：源端视觉效果按目标值变化触发：LaunchedEffect(key)、animateColorAsState(targetValue)、AnimatedContent(targetState)；原目标代码用 @Monitor 只监听运行态和结果字段；写错：删掉 @Monitor 后在每次状态提交（每代 tick）尾部都调页面回调，回调里的 animateTo、getColorSync、getStringSync 没有任何变化判断
