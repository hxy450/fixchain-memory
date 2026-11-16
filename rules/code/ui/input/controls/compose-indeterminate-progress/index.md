# Compose 的不定进度条

agent 会看到什么：读到 Compose 里没传 progress 的 LinearProgressIndicator()（不定进度、持续动画），可能带 Modifier.zIndex 叠在内容上；产物里定值的 Progress({ value, type: ProgressType.Linear })、圆形 LoadingProgress，或放进 Column 流里把内容往下推的进度条

## 规矩

- rule-0288f1feadc6｜不传 progress 的 LinearProgressIndicator，用 Canvas 逐帧复刻并叠放｜读到：Compose 里 `LinearProgressIndicator()` 没传 progress（不定进度，持续动画），可能带 `Modifier.zIndex` 叠在内容上；写错：目标写成 `Progress({ value: 0 / 30 / 50, type: ProgressType.Linear })` 一类定值静止条，或换成圆形 `LoadingProgress`，或放进 Column 流里把列表往下推
