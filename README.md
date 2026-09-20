# Fixchain Memory

带来源情景卡的迁移经验开发仓库。按任务阶段、适用条件和技术机制归并与召回，不按 app 名或文件名匹配答案。

**阅读入口：[memory/index.md](memory/index.md)**。逐层选择相关主题和经验；每层只列直接子主题与本级经验预览，不必通读全库。

## 当前版本

| 项目 | 内容 |
| --- | --- |
| 来源 | Jetsnack915 迁移后的 15 张情景卡 |
| 经验 | 27 条：24 active、3 candidate |
| 阅读目录 | 24 条 active 经验、23 个主题；candidate 不发布到阅读目录 |
| Memory revision | `16e116f9809b6f1557e3f083436ef42d4b860da501387b52ae43073c6c6e9096` |
| 数据格式 | `migloop-memory/1`、精简的 `migloop-case/2`；维护脚本兼容旧卡 `/1` |
| 阅读包格式 / 发布器 | `migloop-memory-files/1` / `0.6.0` |

首次 Git 提交导入现有版本，保留原 store 的 3 个快照和全部卡片，未重做归并、修改结论或提升核验状态。Git 初始提交时间不是这些经验的形成时间。

2026-09-20 对卡片存储做了一次格式精简：15 张卡从 7,216,738 字节降至 626,471 字节（减少 91.3%）。其中原 10,050 行的卡片降至 731 行；调查员正文、全部声明树、已绑定证据引用、27 条经验及其状态均未改写。

卡片现在只保存正文、必要身份与相关来源指纹、关系的证据定位和简短核验结果。全会话逐转录统计、模型时间线、重复节点正文、完整校验回执不再逐卡保存，也没有另拆一批大文件入库。排查时可用制卡脚本的 `--debug-receipts .validation/receipts.json` 临时保存完整回执；该目录不提交。

本次格式迁移同步更新了 3 个快照中的卡片哈希、73 处经验来源绑定及阅读目录链接。原始大卡和旧快照仍可在 Git 提交 `486b377` 中恢复；历史归并提案保留当时的旧 revision，未伪装成新提案。后续新提案使用上表的新 revision。

## 目录与职责

```text
store/
  HEAD.json              当前 memory revision
  snapshots/             原有不可变经验库快照
  cases/<id>/<hash>.json  正文、证据引用、必要来源及简短核验状态
memory/
  index.md               分层阅读入口
  ui/                    组件、布局、渲染、文本、输入
  process/               规格、SDK 阅读、收敛、验收、修复
  manifest.json          阅读包文件校验和及来源绑定
proposals/
  2026-09-19-jetsnack915-v1/
    plan.yaml            原始归并提案
    notes.md             原始归并理由、未决项和审核记录
```

`store/` 是维护数据源；`memory/` 是从它生成的阅读视图，不单独手改。经验正文的来源链接指向本仓库 `store/cases/` 中的确切卡片版本，仓库整体移动后仍可使用。

Git 记录每次归并的文件变化；卡片 ID、claim 与 revision 记录结论的证据依赖。Git 提交不能代替来源撤回后的影响检查和重新审核。

## 后续归并与提交

使用外部安装的 `migloop-memory-maintain` skill，沿用其脚本，不在本仓库另维护一份内核或归并逻辑：

1. 在干净分支上读取当前 snapshot；导入新增/修订卡，或撤回失效卡/结论。
2. 比较阶段、情境、机制和动作，形成 `proposals/<批次>/` 下的新提案与说明。相同补证、不同分支、条件内冲突保留争议。
3. 用 skill 的 `apply` 发布新快照；查看 `impact`，处理受影响经验。
4. 用 `export --link-cards` 导出到全新的暂存目录，校验后整体替换 `memory/`；保留完整的 `store/` 来源历史。
5. 核对全部来源绑定、卡片/快照哈希、目录链接和敏感信息，然后把卡片、快照、阅读目录、提案和说明作为一次逻辑变更提交。

命令入口示例（`SKILL_DIR` 表示本机安装的维护 skill 路径）：

```text
python SKILL_DIR/scripts/memory.py snapshot --store store
python SKILL_DIR/scripts/memory.py apply --store store --plan proposals/<批次>/plan.yaml
python SKILL_DIR/scripts/memory.py export --store store --out .publish-staging/<新版目录> --link-cards
```

`apply` 要使用最新的 `base_revision`；`export` 拒绝覆盖已存在的目录。并行分支均改动 store 时，应在最新 HEAD 上重放提案，而非手工拼接快照 JSON。

## 给迁移模型使用

一次迁移固定一个 Git commit 与 memory revision，并记录在迁移产物中，不在迁移中途自动跟随 main 更新。

本仓库中的 `memory/` 是可追到卡片的开发阅读视图。实际接入迁移时，用同一版本重新 `export`（**不带 `--link-cards`**）生成独立阅读包，只分发这个包与 `migloop-memory-recall` skill；不把 `store/`、卡片、提案或完整转录放进模型默认上下文。这样阅读包只有来源标识，不会携带失效的本地卡片链接。

模型理解当前任务后，从根 index 按主题进入；文件名/API 可以辅助定位，经验是否适用取决于 when、description、unless，而非是否来自同一个 app。

## 证据与核验边界

- `active` 表示当前维护流程认为可供召回，不代表已完成跨 app 泛化验证。原有卡片的语义核验、链路完整性和 unknown 状态均保留，没有在本次导入中转正。
- 卡片包含证据坐标、引用和历史 provenance；原始转录、SQLite 索引、截图、安装包不在此仓库。卡片中的本地材料路径仅作历史来源记录，不能保证另一台机器可直接打开，也不代表单独 clone 本仓库就能重建完整调查 UI。
- [原始归并说明](proposals/2026-09-19-jetsnack915-v1/notes.md) 保留了当时工作目录、脚本和日志的名称；这些是来源记录，未全部复制到本仓库。对应归并提案在本批次的 `plan.yaml`。
- 仓库保持私有。卡片含源码片段、会话标识和原始路径；推送前检查凭证，未经审查不改为公开。
