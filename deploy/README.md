# 部署：用本仓库的 memory 和目前最好的召回方式跑一次迁移

给任意一个 a2h 目标工程装上两样东西：

- **迁移记录**：每个 agent 在派发、首次显式写入前、结束时的工程快照（影子 git）与转录，供复盘、做 replay、切返修检查点；
- **memory 召回**：每个 agent（含主会话）第一次写文件前，从它自己的上下文出发查本仓库的经验库，把相关经验以一行一条的提醒注入给它。

不绑定任何 app，Windows、macOS、Linux 通用，只用 Python 标准库；部署和收尾不调用模型。

## 最简起跑：只需要目标工程

前提：目标工程已经按平时的方式准备好（DevEco 模板 + a2h 的 `.claude`，agents、skills 都装配好），还没发第一条消息。
本机有 Python 3.9+、git 2.28+、Claude Code（实测 2.1.296）。下面的 `python3` 在 Windows 上换成 `py`。

```
git clone -b memory/multi-app-20261011 https://github.com/hxy450/fixchain-memory.git
python3 fixchain-memory/deploy/deploy.py install --project <目标工程>
# 照常在目标工程里启动 Claude Code、发迁移 prompt，跑到 a2h-execute 结束
python3 fixchain-memory/deploy/deploy.py finish  --project <目标工程>
```

不加参数时的取值，就是目前评测下来最好的组合：

| 项 | 默认 | 依据 |
|---|---|---|
| 经验库 | 本分支的 `memory/`，复制一份给召回用；版本号和 commit 记进部署记录 | `memory/multi-app-20261011` 是目前最新的合并库（429 条，含 2048 与 AntennaPod）；`memory/multi-app-20260929` 是此前的多应用库（367 条） |
| 召回时机 | 每个 agent 第一次显式写文件前，召回一次 | 在 2048 上逐个 agent 复现：不给经验时 52 次判定犯 44 次，首写时给对口经验 48 次改好 |
| 召回方式 | sweep3：从 agent 自己的上下文 fork 出只读 worker，从源端视角盘点任务，把库的子主题清单当检查表逐个判断，打开的主题下级全开，不设返回上限 | 难单元覆盖从 24/38（按任务盘点、8 条上限）提到 37/38 |
| 注入方式 | 摘要：拒绝那次写入一次，每条一行「经验标题 → 对这次任务的提醒（正文路径）」 | 续跑 45 次判定避开 43 次，与直接给全文持平，agent 侧开销更小；2048 整条流水线端到端 26 条历史错误避开 25 条 |
| worker 的模型和凭据 | 继承迁移会话自己的：同一个端点、同一组凭据（含存在 `CLAUDE_CONFIG_DIR` 里的登录）、同一个模型（取该 agent 最近一条回复的模型，加 `[1m]`） | 召回要用和被召回 agent 相同的模型 |

评测细节见 a2h-replay-bench 的 `EXPERIMENTS.md`。

## 可选参数

```
python3 deploy/deploy.py install --project <工程> [--no-recall] [--memory <经验库>] [--method sweep3]
                                 [--recall-slot glm-03[,glm-0x] --keys <key 表.csv>] [--shadow <目录>] [--recall-root <目录>]
python3 deploy/deploy.py status  --project <工程>
python3 deploy/deploy.py finish  --project <工程> [--forbid <不该被读的目录 ...>] [--notes <备注.txt>] [--archive <zip>] [--force]
```

- `--no-recall`：只装迁移记录，不召回（做无 memory 基线时用）。
- `--memory`：换一个经验库目录（需有 `index.md`）。
- `--recall-slot` + `--keys`：召回 worker 用单独的 key 槽（csv 列 `slot,api_key,base_url`，也可用环境变量 `RECALL_KEYS`），
  和迁移不共用额度。GLM 有账户级限流（1302），迁移和召回挤在同一个 key 上时召回容易失败；能拿到第二个 key 就建议用。
  给多个槽时，前一个额度用尽会自动换下一个。
- 默认位置：影子仓 `<工程上级>/_shadow/<工程名>`，召回目录 `<工程上级>/_recall/<工程名>`，
  归档 `<工程上级>/a2h-migration-archive/<工程名>-execute-YYYYMMDD.zip`。

## install 做什么

1. 在工程的 `.claude/settings.local.json` 写 hook（设 `autoMemoryEnabled: false`，其余已有设置保留）：
   - 影子快照 `shadow_snapshot.py`：SubagentStart、UserPromptSubmit（主会话派发）、
     PreToolUse（Write/Edit/MultiEdit/NotebookEdit/Bash/PowerShell，判定首次显式写入）、SubagentStop、Stop。
     只记录、从不拦截，出错写 `hook-errors.log`，超时 60 秒。
   - 召回 `recall_hook.py`（PreToolUse，超时 3720 秒）：agent 第一次显式写文件时 fork 出 worker（只开 Read/Glob/Grep，
     设置只取 project/local，关掉 CLAUDE.md 和自动记忆，空的工作目录），按 sweep3 查库，拒绝那次写入一次并注入摘要。
     worker 失败就放行，迁移照常进行；召回期间同一 agent 的其他写入会等结果并收到同一份摘要。
     判定「首次显式写入」的规则和影子快照是同一份代码。
2. 把经验库复制到召回目录的 `library/memory`，worker 只读这份副本。本仓库的 `memory/` 是开发版，来源段会一起复制，
   其中指向 `store/` 的链接在副本里打不开，不影响召回（2048 端到端用的库同样带来源段）。
3. 初始化影子仓（工程外的 git-dir，work-tree 指向工程；不碰工程自己的 git），把当前工程（含上面的 hook 配置）提交为基线，
   打 `scaffold` 标签；写 `deploy.json`（含经验库版本）。已经装过的工程会被拒绝。

hook 命令里写的是执行 install 的那个 Python 解释器和本目录的绝对路径；换了 Python 或挪了本仓库，要重新 install。
继承凭据时，worker fork 出来的会话文件写在迁移会话的 `CLAUDE_CONFIG_DIR/projects/` 下，每次召回一个目录，可以随时删。

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
- 限流（GLM 1302）时 worker 失败、按设计放行，hook 还没有重试；那次端到端唯一没避开的错误就漏在这里。
- 跑之前把同一 app 的旧工程、旧归档、验收清单挪开；finish 的扫描只是事后检查。
- 实测环境：Claude Code 2.1.296，`auto` 权限模式，GLM 5.3。Windows 上跑过完整迁移；Linux（WSL）上做过全流程自测，
  含一次真实召回；macOS 未实机跑过。继承凭据的模式只用回放 stub 测过参数和环境，没有真实调用过。
