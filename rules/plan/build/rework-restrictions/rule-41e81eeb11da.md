# 返修派工把禁令原文的替代写法一起写进 worker 任务，禁并发构建时汇总后立即全量构建

审的是：计划与派工
触发（任一种）：
- 读到：上游规则原文带替代写法，如「No Record<K,V> indexed signatures — use explicit typed fields or HashMap」；写错的样子：派给 worker 的限制只剩「No Record<K,V>」，丢了 indexed signatures 和替代写法；要求「Do not run the full build」却没写汇总后的全量构建和类型声明核对
适用范围：返修阶段把编码规范、禁令转派给并发 worker 时
做法：
- worker 任务里照抄禁令原文，连同替代写法（typed fields 或 HashMap）
- 禁止并发构建时，派工里写明：汇总后立即全量构建，并逐一核对 worker 新引入的类型声明
来源：1 张卡，1 个应用
- case-98e7bd27bb334db83f51（Cofi）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4
