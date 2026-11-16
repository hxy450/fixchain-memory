# 派工里带的领域技能（suggested_skills）

agent 会看到什么：可用技能清单或 skill 映射表里有对得上切片的领域技能（arkts-dark-mode、arkts-login、arkts-payment 等）；派工的 suggested_skills、派工技能里没带它，或把这个 SDK 判成三方 SDK 占位登记

## 规矩

- rule-db6fb8afcb91｜计划阶段每个 SDK 先查 skill 映射表，命中就派接入任务，不登记三方 SDK 占位｜读到：skill 映射表把某 SDK 绑定到领域 skill（如微信登录 → arkts-login，微信支付 → arkts-payment）；写错：派工内核或计划把它判成「鸿蒙版待入仓 → kind=thirdparty-sdk」，登记占位（P-S…），同时又列了 suggested_skills；oh-package 依赖、module.json5 querySchemes、EntryAbility 回调路由没有写者；返回信封报 kernel_conflicts: []
- rule-8d9550919fa1｜涉及主题切换、系统栏、Canvas/Web 取色的切片，派工技能里带上 arkts-dark-mode｜读到：可用技能清单里有 arkts-dark-mode（描述含状态栏 / 导航栏颜色错、ColorMode 切换后不刷新、Canvas/Web 未响应主题）；写错：主题切换、系统栏、Canvas/Web 自绘取色的切片，suggested_skills 和派工技能里没有 arkts-dark-mode
