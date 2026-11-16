# 返修派工里转述的上游禁令

agent 会看到什么：上游规则原文带替代写法（如「No Record<K,V> indexed signatures — use explicit typed fields or HashMap」），派给 worker 的限制只剩「No Record<K,V>」，要求「Do not run the full build」却没写汇总后的全量构建

## 规矩

- rule-41e81eeb11da｜返修派工把禁令原文的替代写法一起写进 worker 任务，禁并发构建时汇总后立即全量构建｜读到：上游规则原文带替代写法，如「No Record<K,V> indexed signatures — use explicit typed fields or HashMap」；写错：派给 worker 的限制只剩「No Record<K,V>」，丢了 indexed signatures 和替代写法；要求「Do not run the full build」却没写汇总后的全量构建和类型声明核对
