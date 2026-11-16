# 前台计时或动画引擎派工里的 tick 参数

agent 会看到什么：决策台账里有替代后台 Worker 的条目（如「500ms ticker + elapsedRealtime 补偿」），前台计时、动画引擎的派工照搬了这组参数，和该 feature 规格的映射行不符

## 规矩

- rule-77f4fde5facc｜前台引擎派工的 tick 周期和补偿方式取该 feature 规格的映射行，不搬台账里别的模块的参数｜读到：决策台账里有替代后台 Worker 的条目（如「500ms ticker + elapsedRealtime 补偿」）；该 feature 规格的映射行写 Animatable → 时间戳插值 + 高频 tick、行为等价；写错：前台计时/动画引擎的派工写了「500ms ticker」「前台 ticker 模型」「ticker/elapsedRealtime 补偿」，与该 feature 规格的映射行不符；派工概括的源码锚点在所指文件里并不存在
