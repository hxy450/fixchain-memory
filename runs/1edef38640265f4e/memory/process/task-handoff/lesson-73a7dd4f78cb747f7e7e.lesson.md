# 派工转述编码禁令时连同原文里的替代写法一起下发；禁止并发构建的 worker 改动，汇总后立即全量构建

ID：`lesson-73a7dd4f78cb747f7e7e` · 版本：1

[本主题](index.md)

## 何时使用

编排或返修阶段，把规则清单转述进 worker 派工，并决定 worker 能否自行构建时

## 适用情境

编排者收到的规则原文带有替代写法（例如“禁止 Record，改用具名字段或 HashMap”），派给多个并发 worker 时压缩成一句禁令，并要求 worker 不跑全量构建。

## 原因

只转述禁令不转述替代写法，worker 会各自找一种看似合规的写法，可能同样被禁止；又因为不能构建，错误要到汇总后才暴露。来源中返修派工把“No Record<K,V> — use explicit typed fields or HashMap”截成“No Record<K,V>”，两个 worker 都改成了索引签名。

## 做法

1. 转述规则时保留原文的替代写法或示例，不只写禁令。
2. 禁止 worker 并发构建时，收齐改动后立即全量构建，并逐一核对 worker 新引入的类型声明。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-98e7bd27bb334db83f51 · 结论：diagnosis, recommendation:4
  卡片版本：`e3b34e5cf0141bbd33b2ff873f7e69123a2b872c4526854af2ba0acb5724774e`
