# Compose Modifier.blur 的模糊

agent 会看到什么：读到 Compose Modifier.blur(N.dp)（edgeTreatment 写没写）；产物里组件上的 .blur(…) 半径和外层 .clip

## 规矩

- rule-23a332b18efb｜Modifier.blur(N.dp) 译成 ArkUI blur 时，半径写成 vp2px(N)，不照搬数字｜读到：Modifier.blur(40.dp) 这类带 dp 单位的模糊半径（含图片 Modifier 链调用的自定义 Modifier 扩展函数里的）；写错：.blur(40) 直接照搬数字，没换单位；或者图片上没有 .clip(true)
- rule-17063a01ea40｜Modifier.blur 没写 edgeTreatment 时，模糊层大于显示区并由外层 clip 裁掉｜读到：Modifier.blur(…) 没写 edgeTreatment（默认 BlurredEdgeTreatment.Rectangle，边缘不淡出）；写错：被 .blur(…) 的组件和显示区一样大，外层容器没有 .clip(true)
