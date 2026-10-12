# 部署：迁移记录（影子 git + hook）与 memory 召回

给任意一个 a2h 目标工程装上两样东西：迁移记录（每个 agent 在派发、首次显式写入前、结束时的工程快照与转录），
和可选的 memory 首写召回（agent 第一次写文件前，从它自己的上下文出发查经验库并提醒它）。跑完再收尾打包。

不绑定任何 app：工程怎么建、迁哪个 app、prompt 怎么写、模型怎么启动，都照平时的做法。Windows、macOS、Linux 都能用；
部署和收尾是纯机械操作，只有迁移本身和召回 worker 调用模型。

## 要求

- Python 3.9+（只用标准库），git 2.28+，Claude Code（实测 2.1.296）。
- 带 memory 时：一个 key 表 csv，列 `slot,api_key,base_url`（可有别的列），用 `--keys` 或环境变量 `RECALL_KEYS` 指定；
  install 会把它的绝对路径记进召回配置，hook 运行时不依赖环境变量。召回用的槽不要和迁移用同一个，额度是共用的。

下面的 `python3` 在 Windows 上换成 `py`。

## 用法

```
# 1. 照常准备目标工程（DevEco 模板 + a2h 的 .claude），先别发第一条消息
# 2. 装记录；要带 memory 就加 --memory、--recall-slot、--keys
python3 deploy/deploy.py install --project <工程>
python3 deploy/deploy.py install --project <工程> --memory <经验库目录> --recall-slot glm-03[,glm-0x] --keys <key 表.csv>
# 3. 照常在工程目录启动 Claude Code、发 prompt，跑到 a2h-execute 结束
python3 deploy/deploy.py status  --project <工程>          # 过程中随时看
# 4. 交付最终报告之后
python3 deploy/deploy.py finish  --project <工程> --forbid <不该被读的目录 ...> --notes <备注.txt>
```

默认位置（都可以用参数改）：影子仓 `<工程上级>/_shadow/<工程名>`，召回目录 `<工程上级>/_recall/<工程名>`，
归档 `<工程上级>/a2h-migration-archive/<工程名>-execute-YYYYMMDD.zip`。

**经验库用哪一版**：本仓库的 `memory/` 是开发版，每条经验带指向 `store/` 的来源段。部署给迁移 agent 时，
按根 README 的约定从同一 store 导出不带完整来源列表的精简阅读包，把那个目录传给 `--memory`。直接传 `memory/` 也能跑，
只是 worker 会读到来源段，而且复制出去的来源链接是断的。

## install 做什么

1. 在工程的 `.claude/settings.local.json` 写 hook（并设 `autoMemoryEnabled: false`，其余已有设置保留）：
   - 影子快照 `shadow_snapshot.py`：SubagentStart、UserPromptSubmit（主会话派发）、
     PreToolUse（Write/Edit/MultiEdit/NotebookEdit/Bash/PowerShell，判定首次显式写入）、SubagentStop、Stop。
     只记录、从不拦截，出错写 `hook-errors.log`，超时 60 秒。
   - 带 memory 时，再追加召回 hook `recall_hook.py`（PreToolUse，超时 3720 秒）。每个 agent（含主会话）第一次显式写文件时，
     从它自己的转录 fork 出一个只读召回 worker（同模型，只开 Read/Glob/Grep，独立的配置目录，碰不到迁移的 hook、skills 和会话），
     按 `--method`（默认 sweep3）查库，把那次写入拒绝一次并注入摘要：每条一行「经验标题 → 对这次任务的提醒（正文路径）」。
     worker 失败就放行；召回期间同一 agent 的其他写入会等结果并收到同一份摘要。
     判定「首次显式写入」的规则和影子快照是同一份代码。
2. 带 memory 时，把经验库复制到召回目录的 `library/memory`，worker 只读这份副本。
3. 初始化影子仓（工程外的 git-dir，work-tree 指向工程；不碰工程自己的 git），把当前工程（含上面的 hook 配置）提交为基线，打 `scaffold` 标签。
4. 写 `deploy.json`。已经装过的工程会被拒绝。

hook 命令里写的是执行 install 的那个 Python 解释器和本目录的绝对路径；换了 Python 或挪了本仓库，要重新 install。

## finish 做什么

主会话转录最近 10 分钟内还在变会拒绝（`--force` 跳过）。

1. 补拷转录（最后一次 Stop 时主转录的尾巴可能还没落盘），写 `index.clean.jsonl`；
2. 工程如有最后一次结束之后的改动，补一个提交；打 `execute-end` 标签；
3. 防抄扫描：所有迁移 agent 和召回 worker 的工具调用里，有没有碰 `--forbid` 给的路径（同一 app 的旧工程、旧归档、验收清单等）；
   迁移 agent 碰自己的影子仓也算。按路径边界匹配，明细写进影子目录的 `finish.json`；
4. 统计：用时、子 agent 数、API 调用、token（按消息去重，输入含缓存读取）、召回次数与失败放行；
5. 打包 zip：`project/`（不含 build、oh_modules 等）、`sessions/`、`shadow/`、`recall/`（配置、索引、每次召回的 prompt 和结果）、
   `hap/`（如果编出来了）、`README.md`（`--notes` 的内容放在「已知」一节）。

## 产物怎么用

| 位置 | 内容 |
|---|---|
| `<影子>/repo.git` | 每个 agent 在派发、首次显式写入前、结束各一次提交，`refs/agents/<agent>/<事件>`；标签 `scaffold`、`execute-end` |
| `<影子>/index.jsonl` | 每次提交一行：事件、agent、类型、转录路径、首写目标 |
| `<影子>/transcripts/` | 结束时归档的转录 |
| `<召回>/recall-index.jsonl` | 每次首写召回一行：返回的经验、耗时、token、成败 |
| `<召回>/forks/` | 每次召回的 worker 会话、prompt、stream、result |

- 还原某个 agent 首写前的工程：`git --git-dir <影子>/repo.git --work-tree <空目录> checkout refs/agents/<agent>/first-write -- .`
- 返修时一处一提交：`python3 deploy/shadow_snapshot.py mark --root <影子> --project <工程> --id FIX-03 --title "..."`，
  ref 是 `refs/fixes/<id>`，制卡时用它切返修检查点。

## 文件

| 文件 | 作用 |
|---|---|
| `deploy.py` | install / status / finish |
| `shadow_snapshot.py` | 影子快照 hook，以及 init / log / resync / mark |
| `recall_hook.py` | 首写召回 hook，以及 install / test / log |
| `recall_core.py` | 召回 worker 的提示词、答案解析、key 槽环境。与 a2h-replay-bench `harness/bench.py` 里评测用的召回逐字相同，改召回方法时两边一起改 |

## 已知问题（2048 端到端实测）

- 召回同步阻塞写入：一次召回平均约 5 分钟（约 13 次串行调用，每次带着 fork 来的整段转录），总耗时因此多 46–78 分钟。
- GLM 1302（请求频率过高）时 worker 失败、按设计放行，hook 还没有重试；`--recall-slot` 给多个槽目前只在额度用尽时换槽。
- 跑之前把同一 app 的旧工程、旧归档、验收清单挪开；finish 的扫描只是事后检查。
- 实测环境：Claude Code 2.1.296，`auto` 权限模式，GLM 5.3。macOS 上未实机跑过；Linux（WSL）上做过包括一次真实召回在内的全流程自测。
