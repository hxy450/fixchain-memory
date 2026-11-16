# 源端 Float 相等比较和比值钳制

agent 会看到什么：读到源端 Kotlin 里用 == 比较 Float（toFloat() == value）、算比值时带零分母分支和 coerceIn(0f, 1f)，产物里是 TS 的比较表达式和进度计算

## 规矩

- rule-3215885f3b96｜源端进度比值带零分母分支和 coerceIn(0f, 1f) 时，目标写入前保留 total > 0 判断和钳制｜读到：源端辅助方法算进度：if (total == 0) … else (completed.toFloat() / total.toFloat()).coerceIn(0f, 1f)；写错：目标在进度回调里直接用 current / total 写进共享状态，写入前没有 total > 0 判断，也没有 Math.min / Math.max 钳制
- rule-2778c32634d8｜源码用 == 比较 Float 时目标保持精确相等，不自加容差，增删和选中用同一比较｜读到：源端 ToggleButton(checked = value == other.toFloat())，增删用 it.toFloat() == / != value；写错：目标写 Math.abs(parseFloat(v) - value) < 0.05 一类容差比较，源端和规格都没给容差
