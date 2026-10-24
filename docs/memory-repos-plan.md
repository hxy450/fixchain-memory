# 迁移记忆系统的代码仓整理方案

日期：2026-10-23　｜　状态：已决定全部仓库放在 fuxi-ailabs；其余待对齐（hxy450、夏仲天、fengyis）　｜　范围：a2h 迁移记忆的制卡、经验库、召回、评测、录制五个部分

这一页只讲"哪个仓库管什么、怎么归位"。具体的迭代流程在 a2h-replay-bench 的 `skills/a2h-memory-iteration`（PR #1），经验候选清单在同一个 PR 的 `results/lesson-candidates.md`。

## 1. 现状

| 仓库 | 维护者 | 现在装了什么 | 问题 |
|---|---|---|---|
| hxy450/fixchain-memory | hxy450、fengyis | 经验库本体：`store/` 和阅读包 `memory/`，每个提交一版 | main 只有最早的 15 张卡。生产线在分支 `memory/multi-app-20261012`（最新 bcdc3ed0，560 条），v2 结构在 `memory/structure-v2-20261017`（56fcfe88），两条线没有对照过 |
| hxy450/migloop | hxy450 | 轨迹查看器、会话适配器、制卡/归并/召回 skill | main 停在 09-11，没有 `skills/`。在用的在 `dev/memory-skills`（maintain 0.10.9）和 `feat/memory-structure-0.10.10`（0.11.1，v2 结构） |
| hxy450/a2h-replay-bench | hxy450、fengyis | 回放评测、e2e 部署、召回实现（sweep3、k20c3、粗筛，约 6000 行）、设备评测脚本、结果、`memory-refs.json` | 召回实现和 a2h-memory 重复；`apps/game2048/` 复制了一份录制材料；路径写死 Windows 机器 |
| fuxi-ailabs/a2h-memory（v0.1 分支，10-22） | hxy450 | `recall/`（部署、hook、k20c3、sweep3）、`retrieval/`（bge-m3 粗筛）、`library/`（refs.json、发布、检索资产）、`distill/`（无头制卡，内嵌 migloop skill 0.10.5 / 0.10.9 冻结包） | main 只有 README。召回和制卡打包在一起 |
| fuxi-ailabs/a2h-recall-eval（v0.1 分支，10-22） | hxy450 | 召回评测集：ColorLines 3 个 agent、19 条历史缺陷，接任意召回命令，续跑、盲评、计分 | main 只有 README。和 bench 的回放评测口径相近，分在两处 |
| fuxi-ailabs/memory-engine（10-23） | 夏仲天 | 10-10 从 migloop `dev/memory-skills`（edaf3cb）整体迁入的 `distillation/`，加 EngramForge 的 contracts / runtime / center，目标是部署到 FunctionGraph 的通用记忆引擎 | `MIGRATION-FROM.json` 写明"迁移后在本仓维护，migloop 不再双维护"，但 migloop 在那之后又有 24 个提交（maintain 0.10.9 三层归因、0.11.1 v2 结构），memory-engine 里的是旧快照 |
| fuxi-ailabs/a2h-migration-recordings | hxy450 | 9 次迁移的录制包（agent-replay），含返修检查点 | 我这边用 migexp 跑的 ColorLines v2mem / v2docs、Breezy 两段会话还没进去 |
| fuxi-ailabs/migexp | fengyis | 迁移实验框架：影子快照、转录同步、finalize、distill 材料池 | 和 a2h-memory `recall/run.py`（原 bench `e2e/run.py`）功能重叠 |
| fuxi-ailabs/memory-eval、migration-memory-eval | fengyis | 三级评测（L1 语义 / L2 任务 / L3 回放）；JetNews 评测 | 和 bench、a2h-recall-eval 是三套评测口径 |

另外，MigBotMemory、AgentLineage 是不同路线的记忆或溯源系统，不在本方案范围内。

## 2. 目标分工

```
录制 a2h-migration-recordings ──材料──→ 制卡 ──卡──→ 经验库 fixchain-memory ──导出包──→ 召回 a2h-recall
        │                                                        ↑                              │
        └──切回放单元、取 execute-end──→ 评测 a2h-replay-bench ──钉版本、晋级───────────────────────┘
```

| 部分 | 仓库 | 只管什么 | main 分支是什么 |
|---|---|---|---|
| 录制 | a2h-migration-recordings | 每次迁移和返修的完整会话、检查点、召回记录。只追加 | 全部 run |
| 制卡 | **待定**：migloop 或 memory-engine（见 §4） | 会话适配、拆分、制卡、归并、导出 | 发布版，带版本号 |
| 经验库 | fixchain-memory | 卡片、经验、各 revision；改经验的提案；经验候选清单 | 生产库。每个 revision 打 tag |
| 召回 | **a2h-recall（独立仓）** | 召回方法、检索索引、Claude Code hook、Codex MCP 适配、召回时的文档核对 | 发布版，带版本号 |
| 评测与迭代 | a2h-replay-bench | 回放、评测集、设备脚本、e2e 部署、结果、迭代 skill、生产组合清单和晋级记录 | 当前评测方法 |

**三条原则**

- 召回和制卡分开。召回在迁移时运行，带 bge-m3、torch 这类重依赖；制卡是离线维护工具，零依赖。两边只靠导出包的格式对接。
- 各仓库的 main 就是现在在用的版本，不把生产版本挂在功能分支上。
- 迭代不单独建仓库。流程和账本放在评测仓库，"现在生产用哪个组合"写回各组件仓库。

**五个接口**（格式定下来后，各仓库内部各自改）

1. 会话录制包：agent-replay 的 `recording.zip`。已有。
2. 卡片 schema。已有。
3. 导出包：`memory/` + `manifest.json`，`migloop-memory-files/2`。已有，缺格式版本号的契约测试。
4. 召回接口：输入将要写的内容和上下文，输出注入的提醒行。a2h-recall-eval 的 `request-2` JSON 可以直接作为起点。
5. 评测结果 `functional-*.json`。有事实格式，没有 schema。

## 3. 召回独立仓 a2h-recall 怎么落

已定：召回单独一个仓库。a2h-memory 已经包含了召回的全部代码，所以不是从零新建，而是二选一：

| 方案 | 做法 | 代价 |
|---|---|---|
| A. a2h-memory 改名为 a2h-recall | `v0.1` 合到 main；`distill/` 移出，归到制卡那一侧 | 改动最小，但仓库名和描述要改 |
| B. 新建 a2h-recall | 从 a2h-memory 拆出 `recall/`、`retrieval/`、`library/`，保留历史；a2h-memory 退役或只剩 `distill/` | 边界最干净，但要重排 hxy450 上周的打包 |

两种都要先和 hxy450 对齐。拆分后：

- bench 的 `e2e/recall_*.py`、`tools/memory_retrieve*.py`、`bench.py` 里的 `RECALL_STEPS` / `recall()`、`assets/k20c3/` 删除，改成按版本号调用 a2h-recall。
- 验证：在 2048 回放和 a2h-recall-eval 的 3 个单元上各跑一次，召回结果与拆分前一致，再删旧代码。
- migloop 里的 `migloop-memory-recall` skill 改成调用 a2h-recall 的薄入口，或退役。
- `library/refs.json` 和 bench 的 `memory-refs.json` 合成一份，放在 a2h-recall 还是 bench，随第 5 步"生产组合清单"一起定。

## 4. 待裁定

| 决策 | 选项 | 建议 |
|---|---|---|
| 制卡的归属 | A. memory-engine 同步到 migloop 最新（24 个提交 + 0.11.1），之后只在 memory-engine 维护；B. 制卡继续在 migloop，memory-engine 只做通用引擎，定期从 migloop 取发布包 | 先问清 memory-engine 的时间表。它的目标是 FunctionGraph 上的通用引擎，a2h 制卡现在每周都在改；短期按 B，等 memory-engine 能跑通一次完整 a2h 制卡再切 A |
| a2h-recall 的来源 | §3 的 A 或 B | B |
| fixchain-memory、a2h-replay-bench、migloop 转到 fuxi-ailabs | **已定（fengyis，10-23）：全部仓库放在 fuxi-ailabs。** 用 GitHub 的仓库转移，不建镜像：转移保留 issue、PR、star 和旧地址的自动跳转，镜像会多出一份要同步的副本。转移要由仓库所有者 hxy450 操作（fengyis 只有 push 权限）；hxy450 是 fuxi-ailabs 成员且有建仓权限，可直接在 Settings → Danger Zone → Transfer 里选 fuxi-ailabs，每个仓一次 | 转移后把本地 remote 改到新地址；`memory-refs.json`、`library/refs.json`、各 README 里的 `hxy450/...` 链接改成 `fuxi-ailabs/...` |
| 评测三套口径 | bench 回放 + 设备评测、a2h-recall-eval、memory-eval L1–L3 | bench 做设备评测和迭代账本；a2h-recall-eval 做召回评测；memory-eval 的 L1 语义检查并入制卡的归并门禁，L2/L3 并入 bench。各自保留结果，不重跑 |
| v2 结构线去留 | 合入生产线、或关闭 | 先做 v1/v2 对照（同一留出 app、同一召回、各 ≥2 次、同一模拟器），不和整理一起做 |

## 5. 归位步骤

| 步 | 做什么 | 验证 | 动代码 |
|---|---|---|---|
| 0 对齐 | 本页过一遍，填 §4 | — | 否 |
| 1 main 归位 | fixchain-memory：main 快进到生产线，给 `memory-refs.json` 里每个 revision 补 tag。a2h-memory、a2h-recall-eval：`v0.1` 合到 main。migloop：`dev/memory-skills` 合入 main，打版本 tag | `memory-refs.json` / `library/refs.json` 里每条仍能按 commit 取到 | 否 |
| 2 定契约 | 召回接口 schema（从 a2h-recall-eval `request-2` 起）；评测结果 schema；导出包 manifest 加格式版本 | 用现有导出包、结果文件跑校验 | 少量 |
| 3 召回成包 | 按 §3 落 a2h-recall；bench 改成调用 | 2048 回放 + a2h-recall-eval 结果不变 | 是，最大的一步 |
| 4 运行框架合一 | migexp 的影子快照、转录同步并入 a2h-recall 的 `run.py`（或反过来），收尾时自动打录制包归档到 a2h-migration-recordings | ColorLines 复跑一次 setup / finish | 是 |
| 5 清理 | 经验候选清单从 bench 搬到 fixchain-memory `proposals/`；两份 refs 合成生产组合清单；bench 的 2048 材料改成引用录制包（先确认两边"首写前"切点定义一致）；写死路径改环境变量；各 README 放同一张分工图 | bench validate 全部通过 | 少量 |

每一步先在本地做完验证，推送、改默认库、晋级之前先征得同意。

## 6. 相关记录

- a2h-replay-bench PR #1：迭代 skill `skills/a2h-memory-iteration`、`results/lesson-candidates.md`
- fixchain-memory issue #1：ColorLines 评测暴露的经验问题
- memory-engine `docs/design/单仓归位执行方案.md`、`MIGRATION-FROM.json`
- migbot-documentation `hxy450/03-召回/经验召回降开销调研-20261020.md`
