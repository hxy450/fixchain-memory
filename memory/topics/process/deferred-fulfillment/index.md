# process/deferred-fulfillment

延后到别处兑现的占位、待裁决项与派发任务：登记边界、承接方与闭合是否真正落实

[上一级](../index.md)

## 本级经验

- [占位只登记输入缺值的情况，能实现的当场实现](lesson-a2f6a4ae9a72be740de6.lesson.md) · 阶段：plan/execute/verify/converge · 信号：forward-ref-uncertain, resource-pending-asset, .d.ts, getXxxProperties
- [子代理派发失败先修参数重试，再按降级条款补跑](lesson-ae78da6f1a3669f6ef59.lesson.md) · 阶段：plan/converge · 信号：spawn_agent, api-inventory
- [点击入口写具体导航契约，无兑现方不留 forward-ref](lesson-7f6b818559cfac767e4b.lesson.md) · 阶段：spec/plan · 信号：forward-ref, WebView, URL, Intent
- [规格留待裁决条目，决策轮逐条出题或关闭](lesson-35b9cdfd5d22ce53465e.lesson.md) · 阶段：spec/execute · 信号：待裁决, Kit, decision ledger, placeholder
- [解前向占位按触发文本逐项兑现，写常量不算闭合](lesson-eb4de4fd7452308a0483.lesson.md) · 阶段：execute/converge · 信号：FWD-REF, forward-ref-uncertain, TODO, return false
- [超时查 list_agents，running 就等待不代写](lesson-39e7e31b88e3d6176022.lesson.md) · 阶段：plan/converge · 信号：list_agents, agent_status, PASS
