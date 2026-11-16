# M3 IconButton 的最小触控尺寸

agent 会看到什么：读到 M3 IconButton 外部 Modifier.size(...) 小于 48.dp（可带 CircleShape 背景）；产物里按字面尺寸写的 Button 宽高、borderRadius 和 margin

## 规矩

- rule-8feee787374a｜M3 IconButton 外部 size 小于 48dp 且带圆形背景时，按 48 圆实现、圆心不变｜读到：源码 IconButton(… modifier = Modifier….size(x.dp) …)，x < 48；规格写 .width(x).height(x)；写错：Button({ type: ButtonType.Circle }).width(36).height(36)，margin 仍按源码左上角的 16 / 10
