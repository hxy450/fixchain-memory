# Compose 的 CircularProgressIndicator

agent 会看到什么：读过的 Compose 源里有 CircularProgressIndicator()（传不传 progress，带 Modifier.size、strokeWidth、color）；交回的代码里写成 LoadingProgress、Progress({ type: ProgressType.Ring }) 还是自绘，尺寸、描边和颜色是否照源端

## 规矩

- rule-30d190ac23d8｜CircularProgressIndicator() 不定进度要自绘复刻，不换成 LoadingProgress｜读到：Compose 里 `CircularProgressIndicator()` 没传 progress，可能带 `Modifier.size(…)`、`strokeWidth`、`color`；不写 color 时是默认 primary；写错：目标换成 `LoadingProgress()`（系统加载动效）或定值 `Progress({ type: ProgressType.Ring })`，尺寸、描边、颜色和源端不同（如写死白色）
