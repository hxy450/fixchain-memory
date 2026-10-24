# 迁移记忆系统的代码仓整理方案

日期：2026-10-23　｜　状态：2026-10-23 已执行归位（§2–§4 为已定结果）；memory-engine 不在范围内　｜　范围：a2h 迁移记忆的制卡、经验库、召回、评测、录制五个部分

这一页只讲"哪个仓库管什么、怎么归位"。具体的迭代流程在 a2h-replay-bench 的 `skills/a2h-memory-iteration`（PR #1），经验候选清单在同一个 PR 的 `results/lesson-candidates.md`。

## 1. 现状（整理前）

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

## 2. 整理结果（已定，10-23）

代码仓五个，都在 fuxi-ailabs，经验库留在 hxy450：

```
录制 a2h-migration-recordings ──材料──→ 制卡 a2h-memory/distill ──卡──→ 经验库 hxy450/fixchain-memory ──导出包──→ 召回 a2h-memory/recall
        │                                                                          ↑                                      │
        └──切回放单元、取 execute-end──→ 评测 a2h-replay-bench ──钉版本、晋级──────────────────────────────────────────────┘
```

| 部分 | 仓库 | 装什么 | main |
|---|---|---|---|
| 制卡 + 召回 | **fuxi-ailabs/a2h-memory** | `recall/`、`retrieval/`、`library/`（原 v0.1）；`distill/` 制卡入口；`migloop/` 只放制卡要用的组件：`skills/`（五个 skill 源模板、memorylib、测试）和 `src/migloop/inquiry/`。以 subtree 从 migloop `dev/memory-skills` 7758b08 迁入，历史保留。`distill.py prepare` 用 `migloop/skills/.../build_bundle.py` 现场构建发布包，冻结副本已删 | 6d0a0dd(v0.1) → d1e6e62 → 543ba46 → a574d2b |
| migloop 全量 | **fuxi-ailabs/migloop** | hxy450/migloop 完整复制（10 条分支）：查看器、会话适配器、dist 等 | 原 `dev/memory-skills` 7758b08；旧 main 存为 `legacy/main-20260911` |
| 评测与迭代 | **fuxi-ailabs/a2h-replay-bench** | hxy450/a2h-replay-bench 完整复制（3 条分支）。回放、评测集、设备脚本、e2e 部署、结果；迭代 skill `skills/a2h-memory-iteration` 和 `results/lesson-candidates.md` 在 hxy450 PR #1 | 同 hxy450 main |
| 经验库 | **hxy450/fixchain-memory** | 不复制、不动（fengyis 10-23）。生产线 `memory/multi-app-20261012`，v2 线 `memory/structure-v2-20261017` | 不变 |
| 录制 | fuxi-ailabs/a2h-migration-recordings | 不变 | 不变 |

不在范围：memory-engine（fengyis：不要管）、a2h-recall-eval、migexp、memory-eval、migration-memory-eval 暂不动。

和第一版方案的差别：召回没有单独成仓，和制卡一起放在 a2h-memory（就是 hxy450 v0.1 的定位），分开只到目录级；仓库是完整复制而不是 GitHub 转移，hxy450 下的原仓仍在。

## 3. a2h-memory 里的边界

- `recall/`、`retrieval/`、`library/`：迁移时运行，带 bge-m3 等重依赖。
- `distill/` + `migloop/`：离线制卡，`migloop/` 部分只依赖标准库，构建发布包需要 PyYAML 6.0.3。
- 两边只靠导出包格式（`memory/` + `manifest.json`，`migloop-memory-files/2`）对接。
- 测试：`python3 -m pytest tests -q`（24 通过）；skill 测试 `python3 -m pytest migloop/skills/tests -q -o "pythonpath=migloop/src migloop"`（278 通过、1 个预存失败：`test_deveco_only_selected_descendants_and_model_not_message_id` 断言输出不含 `private`，在 macOS `/private/var` 临时路径下必失败，上游 migloop 同样失败）。

## 4. 待办

| 事项 | 说明 |
|---|---|
| 本地 remote 与链接 | bench `memory-refs.json`、README 和 a2h-memory `library/refs.json` 里的 `hxy450/migloop`、`hxy450/a2h-replay-bench` 改成 `fuxi-ailabs/...`；指向 fixchain-memory 的保持不变 |
| 契约 | 召回接口 schema（从 a2h-recall-eval `request-2` 起）；评测结果 `functional-*.json` schema；导出包 manifest 加格式版本 |
| 评测口径 | bench 做设备评测和迭代账本；a2h-recall-eval 做召回评测；memory-eval L1 并入制卡归并门禁，L2/L3 并入 bench |
| v2 结构线去留 | 先做 v1/v2 对照（同一留出 app、同一召回、各 ≥2 次、同一模拟器） |
| 原仓去向 | hxy450/migloop、hxy450/a2h-replay-bench 是否归档，由 hxy450 定 |

## 5. 相关记录

- fuxi-ailabs/a2h-memory README、`docs/distill.md`、`migloop/README.md`
- a2h-replay-bench PR #1：迭代 skill `skills/a2h-memory-iteration`、`results/lesson-candidates.md`
- fixchain-memory issue #1：ColorLines 评测暴露的经验问题
- migbot-documentation `hxy450/03-召回/经验召回降开销调研-20261020.md`
