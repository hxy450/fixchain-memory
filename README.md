# ColorLines 留出评测库

[从 memory/index.md 开始阅读](memory/index.md)

ColorLines（[SergeyChelak/ColorLines](https://github.com/SergeyChelak/ColorLines)）用 a2h 流水线（GLM 5.3）迁移后，经一比一返修，从返修中保留的应用修改制卡得到的独立经验库：23 张卡、30 条经验，知识版本 `ebbab6cc8c6559e5818730a1ddc3196c85c119500ae409003cbaad48323fcd0c`。

## 用途

ColorLines 是多应用经验库的留出 app。这个分支只用作评测判据：

- [a2h-replay-bench](https://github.com/hxy450/a2h-replay-bench) 的 `apps/colorlines` 用它的经验喂 oracle 组，用它的卡定回放单元和检查项；
- 不并入 `memory/multi-app-*`，不作为召回池，也不拿它的证据修订多应用库的经验。在多应用库上跑 ColorLines 的 memory 组，才算泛化测试。

## 来源

- 生成：a2h 主会话 aacaafce 与 32 个子代理，生成结束 2026-10-11T20:20:17Z；
- 返修：会话 fb3def7c，观察截止 2026-10-12T12:03:59Z（FINAL 检查点）；保留修改以影子仓 f758d61 → d5dedf3 为准；
- 制卡与归并：migloop-session-to-memory 0.10.5（triage → build-cards → memory-maintain），新建独立库，没有以多应用库为起点。

## 目录

与多应用库相同：`memory/` 是带来源的开发版阅读包，链接到 `store/` 中确切版本的卡；`store/HEAD.json` 记当前知识版本，`memory/manifest.json` 记文件校验和与来源绑定。
