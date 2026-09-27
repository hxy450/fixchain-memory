# 多应用迁移经验共享库

[当前分层经验入口](MEMORY.md)

本库继续沿用前五轮成果（Dice Roller、听音练习、JetLagged、Cofi、PolyPal），批量运行从 49 张卡、62 条经验开始。

每份迁移独立 Claude 会话，最多 6 个制卡子代理；迁移之间串行。正式卡检查、归并、发布完成后，由调度器提交一次 Git，再进入下一轮。无修复的轮次提交问题清单与结论；部分交付或失败明确标注，不作为完整成功。

- `store/`：版本化正式卡、经验及 snapshot。
- `runs/<任务>/`：已提交的问题清单、归并提案、报告和阅读包。
- `LATEST.json` / `MEMORY.md`：当前已验证发布的经验入口。
- `SEED.json`：本次批量运行的起点，不复制另一套库。
- `PIPELINE.json`：调度器与冻结 skill 的版本指纹。
- 本地 `STATUS.md`：运行状态，不纳入 Git。

原始转录、SQLite 索引、临时稿、检查日志和凭证不纳入仓库。当前仅本地自动 commit，不自动 push。

机械检查保证卡片格式和所画历史关系符合契约；不等于归因语义认证或泛化效果证明。泛化实验需冻结一个 Git commit / memory revision，在未入库应用上对照。

启动：

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\hongy\projects\_migloop-memory-batch-20260927\start.ps1"
```

运行时不要另开会话修改本共享库；每轮完成后 stdout 输出汇总与 commit 短号。
