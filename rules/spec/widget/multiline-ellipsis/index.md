# 多行正文的末行省略（maxLines + Ellipsis）

agent 会看到什么：读到源码多行正文写 `maxLines = N, overflow = TextOverflow.Ellipsis` 或 `android:maxLines` 加 `android:ellipsize`；规格转换决策把 `.maxLines(N).textOverflow(...)` 写成「等价」，没写末行截断粒度的差异，也没有 PD 或差异 AC

## 规矩

- rule-908ae147e342｜多行省略的转换决策不写「等价」，写明末行截断粒度差异并登记 PD 或方案｜读到：源码多行正文写 `maxLines = N, overflow = TextOverflow.Ellipsis`（或 `android:maxLines` 加 `android:ellipsize`）；映射参考只记 `ellipsize → textOverflow` 的 API 对应；写错：规格「转换决策」表把 `.maxLines(N).textOverflow({ overflow: TextOverflow.Ellipsis })` 的理由写成「等价」，没写末行截断粒度的差异，也没有 PD 登记或差异 AC
