# 按偏好二选一的 Compose 进度组件

agent 会看到什么：读到 Compose 按布尔偏好在 CircularWavyProgressIndicator 和 CircularProgressIndicator 之间切换；产物里只写了一种 Progress({ type: ProgressType.Ring })，没有另一分支、占位登记或 decision_gaps

## 规矩

- rule-38490da6077e｜源 Compose 按偏好在两种进度组件间二选一时，两个分支都实现或登记占位，不静态选一个｜读到：源 Compose 代码按一个布尔偏好在 CircularWavyProgressIndicator 与 CircularProgressIndicator 之间二选一；写错：目标只写一种 Progress({ type: ProgressType.Ring })，没有偏好驱动的另一个分支，也没在这个位置登记 `P-S*` / forward-ref 占位
- rule-c47b790ba26a｜实现时发现 PD 只以成本为理由、源码有完整可绘分支，在回执 decision_gaps 上报｜读到：规格里的 PD 平台约束只写成本理由（「可移植但成本高」），源码里有完整的可绘制分支（如按偏好切到 CircularWavyProgressIndicator）；写错：目标只写 Progress({ type: ProgressType.Ring })，注释引 PD 说「不迁移」，回执的 `decision_gaps` 为空
