# 决策台账与决策缺口

读到的决策台账、PD 决策卡、规格里的条件或作用域限定和源码、派工对不上，交回的 decision_gaps、handback、巡检问题单里要记分歧或延后裁决时

## 触发族

- [规格里的多腿条件在目标端无等价](condition-leg-gap/index.md)（1 条）：规格或已批准决策写了「DEBUG 构建 || X」这类多腿条件，交回的代码注释说某一腿无等价就省掉，决策台账和移交项里没有缺口
- [派工、台账和源端行为不一致处](spec-source-divergence/index.md)（6 条）：派工或规格的要求（如 setInterval 单句柄）和读到的源码不一致，或台账里有与安卓行为不一致的安全隐私约束，交回的 handback、审计结论没有把分歧写进 decision_gaps 或单列待审批
- [decision_gaps 里的缓存或重绘选型](cache-strategy-gap/index.md)（1 条）：规格的跨栈映射允许「OffscreenCanvas 缓存或每帧矢量重绘」二选一，worker 交回的 decision_gaps 只报选型，没写取值时机和源端的差异
- [台账决策里的作用域限定](decision-scope-limit/index.md)（1 条）：读到决策台账写「作用域限定：本决策不得改变其他功能的页面与导航行为」，替代页目前没有调用方；巡检问题单的修法写「在合适的现有页面加可见入口」，转述决策时漏了限定，也没标为决策冲突
- [PD 决策卡里「由 grill #N 裁决」的延后条目](deferred-grill-items/index.md)（1 条）：读到 PD 决策卡里写着「由 grill #N 裁决」「形态未定」的条目；grill 的预知清单没列出它，HARD-GATE 自检按编号把另一通道的 registry 行对到这张 PD 上，这项延后裁决既没出题也没关闭
