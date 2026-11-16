# 前台引擎派工的 tick 周期和补偿方式取该 feature 规格的映射行，不搬台账里别的模块的参数

审的是：计划与派工
触发（任一种）：
- 读到：决策台账里有替代后台 Worker 的条目（如「500ms ticker + elapsedRealtime 补偿」）；该 feature 规格的映射行写 Animatable → 时间戳插值 + 高频 tick、行为等价；写错的样子：前台计时/动画引擎的派工写了「500ms ticker」「前台 ticker 模型」「ticker/elapsedRealtime 补偿」，与该 feature 规格的映射行不符；派工概括的源码锚点在所指文件里并不存在
适用范围：派工编排阶段，给某个 feature 的实现派工、写其中的技术参数和源码锚点时
做法：
- 派工里的 tick 周期、时间补偿方式照抄该 feature 规格的映射行；决策台账里属于其他模块（如后台 Worker 替代）的参数不写进这份派工
- 概括源码锚点（如「某文件：状态机/ticker/elapsedRealtime」）前先读该文件核对，内容不在这个文件里的不写
来源：1 张卡，1 个应用
- case-34903093a988aad52061（Cofi）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
