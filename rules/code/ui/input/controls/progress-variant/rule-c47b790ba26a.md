# 实现时发现 PD 只以成本为理由、源码有完整可绘分支，在回执 decision_gaps 上报

审的是：代码
触发（任一种）：
- 读到：规格里的 PD 平台约束只写成本理由（「可移植但成本高」），源码里有完整的可绘制分支（如按偏好切到 CircularWavyProgressIndicator）；写错的样子：目标只写 Progress({ type: ProgressType.Ring })，注释引 PD 说「不迁移」，回执的 `decision_gaps` 为空
适用范围：实现阶段照着带降级 PD 的规格写组件时
做法：
- 在回执的 decision_gaps 里上报：哪条 PD 只以成本为理由、源码哪个分支可完整绘制；不把这条决策短路当作复刻依据
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ProgressType.Ring = 1：原生环形进度条，只能画普通环（出处：鸿蒙 SDK 的 ets/component/progress.d.ts，ProgressType.Ring）
来源：1 张卡，1 个应用
- case-8e426a5be8a17ead231c（Cofi）：做法第 1 步 ← 建议 4
