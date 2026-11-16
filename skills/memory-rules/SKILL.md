---
name: memory-rules
description: 从卡库（store/）重建或增量归并「规矩库」：把每张卡提炼成窄的候选规矩（一个触发对一个做法，带查好的知识），检查、合并、归族，导出 rules/ 目录树和召回索引，并按子代理的视野粗筛召回。用于新卡进库后的归并，或从头重建。
---

# memory-rules：从卡片到规矩

依据是 `docs/rules-v2-design.md`（为什么重建、三条原则、格式、流程、检查项都以它为准）。这里写怎么用这个 skill。

## 它做什么

卡（`store/cases/`）是一次迁移里某个错的调查记录。这个 skill 把卡变成**规矩**：一条规矩只讲一个触发、一个做法；触发写子代理的视野（读过的东西里看得到什么、交回的产物里写错成什么样）；做法带着查实的写法和取值，查不实的写怎么查。规矩按产物（规格、计划与派工、代码、资源）→ 主题 → 触发族组织，给「任务刚做完、在审」的 agent 用。

## 五步流程和召回

| 步 | 做什么 | 谁做 | 输入 | 输出 |
|---|---|---|---|---|
| 1 准备 | 每张卡渲染成一个工作包，分批 | 脚本 `prepare_cards.py` | `store/`（HEAD 那一版） | `work/cards/<卡号>.md`、`work/cards_index.json`、`work/batches/extract-NNN.txt`、`pilot.txt` |
| 2 提炼 | 一张卡写成若干条候选规矩，写完自检 | 子代理照 `references/extract-brief.md`；`check_rules.py` 检查 | 一批卡文件 | `store/candidates/<卡号>.json` |
| 2b 复核 | 对着卡把候选规矩再核一遍，原地改掉（查什么、怎么改以 `references/review-brief.md` 为准） | 子代理照 `references/review-brief.md`；`check_rules.py` 检查；`review_stats.py` 统计 | 一批卡文件和它们的候选 | 改过的 `store/candidates/<卡号>.json`、复核记录 `store/reviews/<卡号>.json` |
| 3 合并 | 相近的候选聚成组；子代理判断哪些是同一个触发、同一个做法，相同的并成一条；落盘成规矩 | `cluster.py` 聚类 → 子代理照 `references/merge-brief.md` → `apply_merge.py` | `store/candidates/` | `store/merge/`（组、决定、映射、理由）、`store/rules/<规矩号>.json` |
| 4 归族、建主题 | 同一产物下按触发聚成族的提案；子代理起族名、写族的一行、补通用查法、建议主题、排顺序、标出像是同一条的规矩（`same`）；落盘。第一次建库时再「理主题」和「补并」（两件可以并行） | `families.py propose` → 子代理照 `references/family-brief.md` → `families.py apply`；理主题：`families.py topics-list` → 子代理照 `references/topic-brief.md`；补并：`families.py same-groups` → 子代理照 `references/merge-brief.md` → `apply_merge.py --prefix same`；最后 `families.py apply --fresh` | `store/rules/` | `store/families/`（提案、决定、`topic_lists/`、`topic_decisions/`、`families.json`、`topics.json`），通用查法写进 `store/rules/`，补并改 `store/rules/` 和 `store/merge/` |
| 5 导出、检查 | 写四层目录树、每个产物的一页地图、召回索引和清单；全量检查 | `build_index.py`、`check_rules.py --rules` | `store/rules/`、`store/families/` | `rules/`（各级 `index.md`、`<产物>/map.md`、`<规矩号>.md`、`keys.jsonl`、`manifest.json`） |
| 召回 | 粗筛：按子代理读过和交回的文件给同一产物的规矩（或族）打分取前 K；精选：审的 agent 先看一页地图，再用短号打开族、读正文 | `recall.py coarse / lines / body / show` | `rules/` 和子代理的视野 | 候选规矩或族的得分、命中的词、probe 命中；地图；族；正文 |

读卡、写规矩的活（第 2–4 步）由子代理做，它们不知道任何评测；脚本负责准备、检查、聚类和落盘。每个子代理只拿任务书、格式说明、知识来源说明、检查脚本、批次清单和清单里的文件。

## 怎么跑（都在分支根目录下）

**第 1 步 准备**

```
py -3 -X utf8 skills/memory-rules/scripts/prepare_cards.py
```

读 `store/HEAD.json` 指的快照，把每张卡写成 `work/cards/<卡号>.md`；`work/cards_index.json` 记每张卡的应用（没记的从卡里路径认，标 `app_basis`）、在快照 e613047f 里有没有、建议条数，以及应用清单；`work/batches/extract-NNN.txt` 每批不超过 12 张（种子 1115），`pilot.txt` 是 12 张的试跑小样；`work/lists/in-e613047f.txt`、`not-in-e613047f.txt` 是按卡在不在快照 e613047f 里分开的卡号清单（分两期建库用；只要清单时跑 `prepare_cards.py --lists-only`，不动卡文件和批次）。`work/` 不进版本库。

OpenHarmony 文档的本地副本（提炼、合并、归族的子代理都只读它，不联网）放在 `work/ohdocs/`，只取 `zh-cn/application-dev/` 下的 .md。没有时这样建（只取公开仓库，请求里不带本机路径和个人信息），建好后把 `git -C work/ohdocs log -1` 的提交号和日期更新到 `references/knowledge-sources.md`：

```
git clone --filter=blob:none --sparse --depth 1 https://gitcode.com/openharmony/docs.git work/ohdocs
git -C work/ohdocs sparse-checkout set --no-cone "/zh-cn/application-dev/**/*.md"
```

GitHub 镜像（`https://github.com/openharmony/docs`）停在 2026-05-26，现有副本就是从它取的提交 f41b9345，现有引文都是对着这一版核的。换成 gitcode 的新版本之后，要对 `store/candidates/` 和 `store/rules/` 全部重跑 `check_rules.py`，引文对不上的重新核对，`version` 的写法跟着改。

**知识库来源在本机的根目录。** 规矩的 `refs.where` 只写来源里的相对路径（写法见 `references/knowledge-sources.md`），检查脚本按这台机器的根目录找文件核对引文。把 `skills/memory-rules/sources.example.json` 复制成 `work/sources.local.json`（不进版本库），填上鸿蒙 SDK（DevEco Studio 的 `sdk/default`）、Android SDK、Gradle 缓存（可以几个）和文档副本的目录；没填的按惯例找（环境变量 `DEVECO_SDK_HOME`、`ANDROID_HOME`、`GRADLE_USER_HOME`，以及常见的安装位置）。`py -3 skills/memory-rules/scripts/check_rules.py --roots` 打印用的是哪几个目录。本机没有某个来源、或 Gradle 缓存里没有某个库时，那些出处记作「没能核对」单列，不算违反。

**第 2 步 提炼**

每批起一个子代理，给它 `references/extract-brief.md` 和一个批次清单（先用 `pilot.txt` 试一轮）。子代理每写完一张卡跑：

```
py -3 skills/memory-rules/scripts/check_rules.py <卡号前 8 位>      查一张；不带参数查 store/candidates/ 全部
```

**第 2b 步 复核**

提炼完的卡，每批起一个子代理，给它 `references/review-brief.md` 和一个批次清单；查哪几类、怎么改、复核记录怎么写，都以那份任务书为准，这里不重复。产出是改过的 `store/candidates/<卡号>.json` 和每张卡一份复核记录 `store/reviews/<卡号>.json`。进度和改动统计：

```
py -3 -X utf8 skills/memory-rules/scripts/review_stats.py [--all]
```

报复核了多少张卡、规矩从几条到几条、按复核记录里的 `check` 各改了多少处、拆了多少条、挪进 left_out 多少条、`unsure` 多少项，列出有候选但没有复核记录的卡。第 3 步在复核做完之后开始。

**分两期建库**

卡库里在快照 e613047f 里的卡（`work/lists/in-e613047f.txt`）先完整走一遍第 3–5 步，得到「基础库」（评测用它，和以前几组对照用的是同一批卡）；其余较新应用的卡（`work/lists/not-in-e613047f.txt`）再按下面「增量归并」加进去。基础库的第 3 步就是下面的命令加 `--only-file work/lists/in-e613047f.txt`。

**第 3 步 合并**

```
py -3 -X utf8 skills/memory-rules/scripts/cluster.py --only-file work/lists/in-e613047f.txt [--threshold 0.35] [--max-size 10] [--per-batch 40]
```

同一 product 内按 `keys` 两栏和标题的 IDF 余弦相似度连成组（同一张卡的候选不连边），超过 10 条的组提高阈值再拆；阈值默认 0.35，每批不超过 40 条候选；写 `store/merge/groups/<组号>.json`（带候选全文）、`singles.json`（单独成组的，不交给子代理）、`batches/merge-NNN.txt`、`cluster_report.json`（相似度和组大小的分布，调阈值看它）。每批起一个子代理照 `references/merge-brief.md` 写 `store/merge/decisions/<组号>.json`，它用 `apply_merge.py --check --groups <组号>` 自检。全部写完后：

```
py -3 -X utf8 skills/memory-rules/scripts/apply_merge.py --fresh
```

检查每条候选恰好被处理一次（并进某条或单独保留），编号（`rule-` + sha1(product + 换行 + title) 前 12 位，撞号的把 sources 也算进去），补 `sources`、`status`、`general`，写进 `store/rules/`，再跑 `check_rules.py` 查这些规矩；另写 `merge_map.json`（临时号 → 规矩号）和 `origins.json`（每条规矩出自哪些候选、理由）。

**第 4 步 归族和建主题**

```
py -3 -X utf8 skills/memory-rules/scripts/families.py propose [--threshold 0.3] [--max-size 20]
```

同一产物内按 `keys.read` 的相似度聚成族的提案（每族不超过 20 条，落单的并到最近的族或自成一族），写 `store/families/proposals/`、`batches/family-NNN.txt`、`propose_report.json`。每批起一个子代理照 `references/family-brief.md` 写 `store/families/decisions/<提案号>.json`，它用 `families.py apply --check --proposals <提案号>` 自检。全部写完后：

```
py -3 -X utf8 skills/memory-rules/scripts/families.py apply --fresh
```

检查每条规矩恰好进了一个族（或列进 `move_out`）、目录名合法、`same` 的每组合乎要求，通用查法过检查后写进 `store/rules/`；写 `families.json`（每个族带标识「提案号#序号」和短号 `f001`…）、`topics.json`。同产物、同主题、同目录名的族并进排在前面的那个。有 `move_out` 的写进 `unplaced.json`、退出码为 1：对它们再出一轮（第一次建库也一样）：

```
py -3 -X utf8 skills/memory-rules/scripts/families.py apply --fresh --no-topic-decisions     先把这一轮落成 families.json
py -3 -X utf8 skills/memory-rules/scripts/families.py propose --new-only [--per-batch 70]
```

`--new-only` 只给还没进族的规矩出提案，提案号、批次号接在已有的后面（`round` 记第几轮），已有的提案、批次和决定都不动；还有提案没写决定时拒绝。从头 `propose` 时 `decisions/` 里已有决定就拒绝。下一轮的子代理照同一份任务书写决定（提案附了已有族，归进已有族就写成同一主题、同一目录名），全部写完再 `apply --fresh --no-topic-decisions`：各轮的提案和决定一起读，前一轮 `move_out`、后一轮放进了族的不算待挪，归进已有族的并进去。`unplaced.json` 空了再往下走。第一次建库时归族子代理写的主题只当建议（中文名不一、族目录重名只报提示），接着并行做理主题和补并，都写完了再 `apply --fresh`：

```
py -3 -X utf8 skills/memory-rules/scripts/families.py topics-list                                   理主题：出清单
py -3 skills/memory-rules/scripts/families.py topics-check --product <spec|plan|code|resource>    理主题的子代理自检
py -3 -X utf8 skills/memory-rules/scripts/families.py same-groups                                   补并：把 same 组做成 store/merge/groups/same-*.json
py -3 -X utf8 skills/memory-rules/scripts/apply_merge.py --prefix same                              补并：合并的子代理写完决定后落盘
py -3 -X utf8 skills/memory-rules/scripts/families.py apply --fresh
```

补并是为了并掉词面相似度抓不到的重复：归族的子代理把族里从标题和触发看是同一条的规矩列进 `same`，`same-groups` 把它们做成合并组（成员都是已有规矩，带全文，标 `existing`，批次清单 `store/merge/batches/same-NNN.txt`；重跑时已出过的组号和组文件不动，新标出的往后排，新批次只列还没有合并决定的新组），合并的子代理照 `references/merge-brief.md` 判断、写 `store/merge/decisions/same-NNNN.json`、用 `apply_merge.py --check --groups same-NNNN` 自检；`apply_merge.py --prefix same` 落盘时并出来的规矩沿用组里排在前面那条的规矩号，其余成员的文件删掉，`merge_map.json`、`origins.json` 跟着更新；最后的 `apply --fresh` 按 `merge_map.json` 把归族决定里被并掉的规矩号换成留下的那条（去重）。

`topics-list` 给每个产物写一份清单 `store/families/topic_lists/<产物目录>.json`（族的标识、族名、族的一行、规矩条数、有没有通用查法、建议的主题）。每个产物起一个子代理照 `references/topic-brief.md` 写 `store/families/topic_decisions/<产物目录>.json`：主题树（按任务对象分，第一次 1–2 级、以后超限时按需加深，每个节点的直接子项不超过 20 个，每个主题有中文名和一行「agent 手里有什么东西时该进来看」），每个族恰好归一个主题，族名和一行说的是同一类写法的族标出来合并（两个都带通用查法的列进 review 给人看）。再跑一次 `apply --fresh`：同一套检查过了，就用这份决定覆盖各族的主题、合并标出的族，`topics.json` 写成「目录 → 中文名和一行」，并要求同一主题下族目录不重名。增量归并时不理主题，照旧优先用已有主题。

**第 5 步 导出和检查**

```
py -3 -X utf8 skills/memory-rules/scripts/build_index.py
py -3 skills/memory-rules/scripts/check_rules.py --rules
```

写 `rules/index.md`（各产物下的一级主题，每个主题一行，带主题的一行）、`rules/<产物>/map.md`（一页地图：每个主题一行中文名加它的一行，下面是这个主题的族，每个族只写「短号 族名（条数）」，用「；」隔开）、`rules/<产物>/<主题>/index.md`（主题的一行、子主题和触发族）、`rules/<产物>/<主题>/<族>/index.md`（族的一行、通用查法全文、每条规矩一行）、`<规矩号>.md`（正文）、`keys.jsonl`（每条规矩一行，召回用，带族的路径、短号、族名和族的一行）、`manifest.json`（条数、卡库版本、构建时间、分支提交、应用清单、短号 → 族的路径；输入目录写相对路径）、`rules/<产物>/index.md`（这个产物的一级主题，指向同目录的 `map.md`）、`rules/cards.md`（卡和规矩的对照：按应用分节，每张卡一行，卡号、卡的标题、它支持的规矩；没有产出规矩的卡注明原因）。规矩页和通用查法在「来源：N 张卡，M 个应用」下面逐张列出卡号、应用和各项出自哪条结论（如「做法第 1 步 ← 建议 2、诊断」）。规矩的应用从 `work/cards_index.json` 取。同一主题下族目录重名时停下。

给 agent 的部署包（评测时拷进试验目录的就是它）：

```
py -3 -X utf8 skills/memory-rules/scripts/build_index.py --no-library --deploy-out <目录> [--products 代码,资源] [--exclude-apps A,B] [--cases-in 前缀]
```

同一棵树，规矩页只留来源的计数一行，不带对照表和 `manifest.json`，`keys.jsonl` 不带 `sources`、`apps`，另带 `scripts/recall.py`、`rulelib.py` 和一页 `README.md`（在部署包里跑 `python scripts/recall.py …` 不用写 `--rules`）。部署包里没有来源，`--exclude-apps`、`--cases-in` 要在建部署包时给。

**召回**

```
py -3 -X utf8 skills/memory-rules/scripts/recall.py coarse --product 代码 --read <读过的文件或目录…> --wrote <交回的文件或目录…> [--k 30] [--fields keys|keys+text] [--query read|read+wrote] [--level rule|family]
py -3 -X utf8 skills/memory-rules/scripts/recall.py lines <规矩号…>
py -3 -X utf8 skills/memory-rules/scripts/recall.py body <规矩号…>
py -3 -X utf8 skills/memory-rules/scripts/recall.py show map [--products 代码,资源]
py -3 -X utf8 skills/memory-rules/scripts/recall.py show f017 f123 <规矩号…>
py -3 -X utf8 skills/memory-rules/scripts/recall.py coarse --level family --k 12 --as-tree [--with-lines] [--products 代码,资源] --read <…> --wrote <…>
```

给审的 agent 的路线是两步：先 `show map` 看一页地图（几百个族也在几千字以内），再 `show <短号…> <规矩号…>` 一次取几个族（族的一行、通用查法全文、每条规矩一行）和几条正文；都不带链接和多余修饰。`show` 也认 `index`、主题和族的路径。`body`、`show` 取规矩正文时默认去掉来源明细（只留计数一行），给人看时加 `--with-sources`。

先粗筛再挑时用 `coarse --as-tree`：按族打分取前 K 个族，排成和地图一样紧凑的小树（只含入选的族和它们所在的主题，开头写明是粗筛出的一部分，不带得分）；加 `--with-lines` 时每个族下面直接带族的一行和每条规矩的一行（通用查法只写规矩号和标题），一次调用就拿到小树和可挑的行。`--products` 写几个产物时合在一起按得分取前 K，不是各取 K。

粗筛从读过和交回的文件里抽标识符（整体和拆开的部分都算）当 query，对同一产物的规矩按 IDF 余弦打分（`keys` 两栏，或加上标题和触发全文），`probe` 在交回的文件里搜到的加分并列出文件和行；输出每条的得分和命中的词。`--level family` 按族打分（族的一行加族里所有规矩的 keys），输出带短号，只当排序提示。精选时只把候选的那一行（`lines`）给审的 agent，命中的族的通用查法一并给，它判断触发在的再读正文（`body`）；`show` 一次打印多个索引节点（顶层、主题、族）或规矩正文，`--products` 只列这些产物。四个子命令都可以用 `--rules <目录>` 指到别处的一份导出（评测时拷进试验目录的那一份）。视图：`--exclude-apps A,B` 去掉只出自这些应用的规矩；`--cases-in <快照号前缀>` 只用该快照里已有的卡产出的规矩（`--cases-mode all` 要求 sources 全在，`any` 要求有一张在）。

**自测**（改了脚本之后跑）

```
py -3 -X utf8 skills/memory-rules/scripts/selftest.py            检查和渲染：两个样例通过，改坏的各处都查出，format.md 和样例一致
py -3 -X utf8 skills/memory-rules/scripts/selftest_pipeline.py   合并、归族、理主题、导出、召回走一遍，故意做错的几处被拒
```

## 增量归并（新卡进库之后，或分两期建库的第二期）

1. `prepare_cards.py` 重新渲染（新卡的卡文件会出现在 `work/cards/`），只把新卡列成批次交给提炼的子代理。
每一期起一个名字（第二期用 `p2`，以后 `p3`…），这一期的组、批次、单独成组的清单都带这个前缀，不碰基础库和别的期的文件。

2. 合并：
   ```
   py -3 -X utf8 skills/memory-rules/scripts/cluster.py --only-file work/lists/not-in-e613047f.txt --existing store/rules --phase p2
   ```
   新候选和库里已有的规矩（不含通用查法）一起聚，已有规矩用规矩号当临时号、标 `existing`；只算新候选之间、新候选和已有规矩之间的相似度，已有规矩彼此不连边；只含已有规矩的组不出。写 `store/merge/groups/p2-NNNN.json`、`batches/p2-NNN.txt`、`singles-p2.json`、`cluster_report-p2.json`；这一期已有合并决定时拒绝重聚。每批起一个合并的子代理（同一份 `merge-brief.md`，自检 `apply_merge.py --check --groups <组号>`），写完后：
   ```
   py -3 -X utf8 skills/memory-rules/scripts/apply_merge.py --prefix p2
   ```
   只落这一期的组和 `singles-p2.json`；并进已有规矩时沿用它的规矩号，被并掉的已有规矩文件删除，单独保留的已有规矩不动；`merge_map.json`、`origins.json` 接着更新；重跑结果不变。基础库的组只能连同 `--fresh` 落，`--prefix p2` 不能加 `--fresh`。
3. 归族：`families.py propose --new-only` 只给还没进族的规矩（新规矩，以及合并时变了号的）出提案（新的一轮，编号接着排），每个提案附同一产物下最相近的 8 个已有族（带主题的中文名）；子代理可以把规矩归进已有的族（写成同一主题、同一目录名），新起主题时带上主题的一行。`families.py apply`（不加 `--fresh`）只落还没落过的轮（`apply_state.json` 记着），把它们接在已有族后面，其余作为新族加上；已有的族和理过、拆过的主题原样留着，不用 `topic_decisions/`。有 `move_out` 的再 `propose --new-only` 一轮。基础库建成后加过增量或拆过节点时，`apply --fresh` 会拒绝。
4. 补并（可选）：`families.py same-groups` 只出新标的组（组号往后排），合并的子代理判断后 `apply_merge.py --prefix same`，再 `families.py apply`。
5. 超限的节点就地拆（树按需加深；每期增量落完都做）：
   ```
   py -3 -X utf8 skills/memory-rules/scripts/families.py oversize                 列出规矩超过 20 条的族、直接子项超过 20 个的主题节点（含产物根）
   py -3 -X utf8 skills/memory-rules/scripts/families.py split-families           有超限的族：每个出一个拆分提案（新的一轮）和批次
   py -3 -X utf8 skills/memory-rules/scripts/families.py apply                    拆族的子代理（family-brief.md「拆一个超限的族」）写完后
   py -3 -X utf8 skills/memory-rules/scripts/families.py topic-split-lists        有超限的主题节点：每个出一份清单和批次 batches/topic-split-NNN.txt
   py -3 -X utf8 skills/memory-rules/scripts/families.py topic-split-apply        拆节点的子代理（topic-brief.md「拆一个超限的主题节点」，自检 topic-split-check）写完后
   ```
   先拆族（拆完主题下的子项会变多），再拆主题节点；`topic-split-apply` 之后还超限的再出一轮清单，直到 `oversize` 退出码为 0。拆出来的族留在原主题下，原族被替换；拆主题节点是在这个节点下加一层新主题，族和子主题整棵挪下去，主题层数不限。
6. `build_index.py` 全量重写 `rules/`，`check_rules.py --rules` 全量检查。

## 文件

```
skills/memory-rules/
  SKILL.md                      本文
  references/
    extract-brief.md            提炼任务书（第 2 步的子代理）
    review-brief.md             复核任务书（第 2b 步的子代理）
    merge-brief.md              合并任务书（第 3 步和第 4 步补并的子代理）
    family-brief.md             归族任务书（第 4 步的子代理）
    topic-brief.md              理主题任务书（第一次建库时第 4 步末尾，每个产物一个子代理）
    format.md                   规矩的格式，带两条完整例子
    knowledge-sources.md        三类知识库来源怎么找、出处怎么写成可移植的样子
    examples/                   两条例子的候选文件（代码类、规格类），都过检查
  scripts/
    rulelib.py                  共用：路径、规矩号、词的切分、IDF 余弦、按阈值连成组
    prepare_cards.py            第 1 步
    check_rules.py              检查候选（store/candidates/）和规矩（store/rules/）；--format-only 只查格式
    review_stats.py             第 2b 步的统计
    cluster.py                  第 3 步的聚类
    apply_merge.py              第 3 步和补并的落盘（--check 给子代理自检；--prefix <期名> 落增量这一期，--prefix same 落补并的组）
    families.py                 第 4 步：propose / apply（--check 给子代理自检）/ topics-list / topics-check / same-groups；
                                超限拆分：oversize / split-families / topic-split-lists / topic-split-check / topic-split-apply
    build_index.py              第 5 步的导出（含每个产物的 map.md）
    recall.py                   召回：coarse（--level rule|family，--as-tree、--with-lines）/ lines / body / show（map、短号、路径、规矩号）
    render.py                   规矩 → 呈现的正文（含来源明细）、第三层索引的一行
    sources.py                  知识库来源在本机的根目录（work/sources.local.json），refs 的定位解析成本机文件
    migrate_refs.py             一次性：把 refs 的本机绝对路径改写成可移植的定位
    selftest.py、selftest_pipeline.py   自测
  sources.example.json          本机根目录配置的样例（复制成 work/sources.local.json）
```

## 做的时候的规矩

- 读卡、写规矩的子代理不读任何评测材料，也不去找任何具体应用的源码；它们的任务书里只有白名单上的文件。
- 只在本分支的工作目录里写；不改已有的 `memory/`、`store/cases/`、`store/snapshots/`、`store/HEAD.json`；不推送。
- 库里（候选、规矩、导出、部署包、文档和样例）不写任何本机路径；`refs` 只写来源里的相对路径。
- 不打开凭据文件。子代理不联网，文档读 `work/ohdocs/` 的本地副本；建副本时只取公开仓库，请求里不带本机路径和个人信息。
- 脚本都设 `sys.dont_write_bytecode = True`；中间产物放 `work/`，命令记在 `work/commands.log`。
- `.gitignore` 已经放开 `docs/`、`skills/`、`rules/`、`store/candidates/`、`store/reviews/`、`store/merge/`、`store/rules/`、`store/families/`。
