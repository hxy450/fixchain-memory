# 计划阶段每个 SDK 先查 skill 映射表，命中就派接入任务，不登记三方 SDK 占位

审的是：计划与派工
触发（任一种）：
- 读到：skill 映射表把某 SDK 绑定到领域 skill（如微信登录 → arkts-login，微信支付 → arkts-payment）；写错的样子：派工内核或计划把它判成「鸿蒙版待入仓 → kind=thirdparty-sdk」，登记占位（P-S…），同时又列了 suggested_skills；oh-package 依赖、module.json5 querySchemes、EntryAbility 回调路由没有写者；返回信封报 kernel_conflicts: []
适用范围：计划阶段按 SDK 逐个决定接入还是登记占位时
做法：
- 每个 SDK 都先查 skill-binding-rules；命中时追加 suggested_skills，不登记 thirdparty-sdk
- 把 oh-package 依赖、module.json5 的 querySchemes、EntryAbility onCreate / onNewWant 里的 handleWant 与回调分派列为有明确写者的切片任务
- 派工内核和规则冲突时在 kernel_conflicts 里报出来，不照抄内核
来源：1 张卡，1 个应用
- case-febf3c781ebde9778c30（DeepAI全能PPT）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2、诊断
