---
name: lesson-knowledge-attach
description: 给安卓 → 鸿蒙（ArkTS）迁移经验配「已核实的平台事实」（每条经验一个知识文件，放 knowledge/lessons/），核对时顺带改正经验正文里说错或缺条件的句子。两种时候用：归并把新卡并成新经验或改了旧经验之后（apply、lint 之后、export 之前）；给库里现有的经验分批补知识。
---

# 给经验配已核实的平台事实

## 做什么、交出什么

- 每条经验一个 `lesson-<id>.json`：`entries` 是这条经验做法要用到的平台事实（每条在声明、文档、源码、平台资源、依赖库或卡里核过），`changes` 是对正文的改句，另有 `sdk`（核实环境）、`device_todo`（要上机才能定的，只给维护的人）、`dropped_notes`，没有条目时 `note`。格式见 `references/knowledge-format.md`。
- 知识文件放经验库的 `knowledge/lessons/`，**不写进经验正文**。改句在知识文件里，渲染时套到正文上；要让改句真正进正文，走库的提案流程（下面「改句进正文」）。
- 交给模型的那一段由渲染脚本生成：正文（套上改句）后面接「已核实的平台事实（核实时用的是 …）：」和「- 〔step〕fact」各行，不带出处和链接（`references/rules.md` P1、P2）。用知识的提示词模板里要有和它配套的两句（P3）。
- 不调模型 API，不上机。

先读 `references/rules.md`（规则 C、V、U、T、P、Q、N），再读 `references/sources.md`（去哪查、出处、版本）、`references/knowledge-format.md`、`references/examples.md`；工具的用法和已知限制在 `references/tools.md`。

## 两个入口

### ① 新卡归并之后：给新增和改动的经验配知识

**由归并维护 skill（migloop-memory-maintain）第 4 步调用：** 它在第 4 步「校验并发布」的 `apply`、`lint` 之后、第 5 步 `export` 之前把这一步列为必做。本次提案 `upsert` 里新增或改动了哪几条经验，就对这几条做；没动的、退役的经验不做。检查 0 错、抽查过线，才回到它的第 5 步。不放在 apply 之前的原因（新经验 ID 在 apply 时才定、提案里放不下条目、apply 之前没有正文文件可核、改旧经验有门槛）见 `references/tools.md` 第 7 节。

**谁做：** 做归并的人协调，自己不写知识：同步文档（第 0 步）、取正文、分类分组、填任务书派人、收件、跑检查、并入。写的人、专门复核的人、抽查的人是另外三拨人（子代理，或互不共享上下文的会话），由做归并的人派，各自只读任务书给的材料；抽查的人不看写的人的工作稿和复核日志。

**归并时写新句的人要做的（归并维护 skill 第 3 步）：** 新卡要并进已有知识文件的经验，先读这条经验渲染后的知识段（`scripts/render.py <知识目录>/lesson-<id>.json --memory <归并前的阅读包>`），再写新句；新句里的具体值、接口照 `references/rules.md` T4b–T4d 写。新句和已核实的事实对不上的，记进归并的 REPORT.md「交知识裁决」（经验号、新句、对不上的那条事实），不凭记忆改。这几条交给写这条经验的人，当 doubts（V10）照 U1 裁决成改句（任务书 `briefs/write-new-cards.md` 的 `{交知识裁决}`）。新建的经验没有知识，照常写。

**取正文：** 用作者脚本把刚 apply 的版本开发版导出到一个新的临时目录：`python scripts/memory.py export --store <store> --out <临时目录>/memory --link-cards`（作者 skill 的脚本；export 只读 store，输出目录必须是新的）。下面的 `<memory>` 都指这个临时目录下的 `memory/`；`<归并前的阅读包>` 是归并开工前库里现成的 `memory/`（或 ingest 之前先 `export --link-cards` 一份）。

**一次归并里三种经验怎么做。** 先分类：`scripts/gate.py plan --store <store> --base <归并开始时的版本> --knowledge <知识目录的上一级，即仓库的 knowledge/>` 对照两个版本的 store 快照，列出新增、正文改了、只补来源、退役四类和每条现有知识文件的格式；正文改了哪几部分，再用 `scripts/candidates.py --from-case-files links --memory <memory> --base-memory <归并前的阅读包> lesson-<id>` 看「改动的部分」。

1. **新增：全做。** 下面「共用步骤」全走一遍；候选从卡收，卡全算新卡。
2. **加了句子：**
   - 知识目录里还没有这条，或只有旧格式（`sdk` 里没有 `docs_commit`）：和新增一样全做。
   - 已有新格式的知识文件：不整条重做，只做三件事。
     a. `scripts/check.py <知识目录>/lesson-<id>.json --memory <memory> --require-new --docs <文档同步目录> --sources …`：正文改了以后旧改句还套不套得上、旧出处在今天的文档 master 里还在不在；报出来的逐条重裁。
     b. `scripts/candidates.py --from-case-files links --memory <memory> --base-memory <归并前的阅读包> --new-cards-only lesson-<id>`：只核新卡的候选，再照 C6 读新卡另列；「改动的部分」列出的那几部分逐句过（新句要用的平台事实补查，step 落在这几部分的旧条目复核），其余旧条目不动。整条正文仍要读一遍，看新句有没有让旧条目的成立条件不够。
     c. `sdk` 换成这次的核实日期和文档提交（旧条目只在 a 里核了出处还在，值没有重核；a 报出来的那几条要重核）；`changes` 只追加，旧的不删（a 里套不上的除外）。和旧文件逐条比（Q4）。
   理由：归并的增量只追加句子或步骤、不动标题和原有第一步，没改的部分要用的平台事实没变；整条重做的工作量和新增一样，还会把已核过的条目措辞改来改去。
3. **只补来源：正文没变，默认不动知识文件，没有的也不为这次新建。** 只跑 `--new-cards-only` 看新卡的行：和已有条目说法冲突、或给已有条目补出成立条件的，那几条按 2 的 b、c 处理；否则不动。还没有知识文件的经验，留给入口 ② 统一做。理由：知识跟着做法走，做法没变；这类经验数量多（一次归并常是新增的两倍），新卡多半只是同一机制再出现一次。

**任务书和份量：** 写的人用 `briefs/write-new-cards.md`（一人一组 3–6 条，按候选行数配平）；专门复核用 `briefs/review.md`（每人不超过约 60 条要复核的条目）；每批抽查用 `briefs/audit.md`（一批一人，没参与这批的写和复核）。

**门槛：** 全部知识文件过检查脚本、错误为 0，抽查过线（安卓平台和依赖库两类里中等以上的有出入不超过一成，没有和出处相反的），才照下面「并入经验库」把知识文件拷进 `knowledge/lessons/`、把改句发布进正文，再跑 `scripts/gate.py check`，退出码 0 才回到归并维护 skill 第 5 步 export。不过线的这批不进第 5 步：按抽查报出的毛病类型返工，换一个没参与过的人重抽。

### ② 给库里现有的经验补知识

- **分批：** 按经验的使用频次排先后（用得多的先做），一批若干组，一组几条经验交给一个写的人。流程类经验（做法不依赖平台事实）给空条目加 `note`。
- **正文：** 直接读库里的 `memory/<主题>/lesson-<id>.lesson.md`（开发版导出，带「## 来源」），不用另外 export。
- **候选：** `scripts/candidates.py --from-case-files <库>/store/cases --memory <库>/memory lesson-<id>`（或 `links`）；有现成候选表时可用 `--from-json`。再照 C6 读来源卡另列。
- **已有旧格式知识文件的**（第三版、第七版规则写的）：照这套规则整条重写成新格式，并入时替换旧文件；旧文件带过、已发布进正文的改句仍在正文里，新文件不用再记。
- **任务书：** 写的人用 `briefs/write-backfill.md`，复核和抽查同入口 ①。

## 共用步骤

两个入口用同一套步骤。工具都在 `scripts/`，命令写全见 `references/tools.md` 第 1 节；Python 用 3.10 以上（例：`py -3.12 -B -X utf8 scripts/…`）。

| # | 步骤 | 做什么 | 工具 / 任务书 | 规则 |
|---|---|---|---|---|
| 0 | 同步文档 | 把 OpenHarmony 文档最新 master 同步到本机目录；打印的提交号和日期填进这一批文件的 `sdk.docs_commit`、`sdk.docs_date`。几个人共用一个同步目录时，协调的人开工前拉一次，写的人只跑 `--show` | `sync_ohdocs.py <文档同步目录>` | N1 |
| 1 | 读正文 | 读这条经验的正文（入口 ① 读临时导出，入口 ② 读库里的 `memory/`）；改句的原句从这份文件里逐字取 | — | V1 |
| 2 | 收候选 | 脚本从来源卡收；打印的编号就是「用到的候选」的下标。再读来源卡被引的结论，另列脚本收不到的平台事实（「卡补」） | `candidates.py` | C1–C7 |
| 3 | 逐条核实并补查 | 逐步过正文，列出要用的平台事实；用得上的候选回来源重核（沿用并复核），缺的自己查（新查）；核不到的进 unverified，和正文对不上的进 doubts。读全用工具：文档取整节，安卓资源查全部限定目录和整条 parent 链、库比最旧最新两版，鸿蒙声明列出同名的每一处 | `ohdocs_section.py`、`android_res.py`、`dts_lookup.py`、`ohdocs_link.py` | V0–V11、N2、N3 |
| 4 | 统一写法 | doubts 裁决成改句（原句逐字、恰好一处）；unverified 四种去向；正文不写要上机的话；逐个核对能机械做的写成脚本做法 | — | U1–U9 |
| 5 | 清理 | 卡里验证条目分甲乙；默认值加成立条件、写最常见的覆写；颜色尺寸写主题和深浅两值、目标侧用跟主题走的资源；具体值和接口带条件、写全另一支和可见效果；一个限定语只管一个后果；版本条件按两层写；去掉做法尾巴；文档出处换成链接 | `ohdocs_link.py` | T1–T7（含 T4a–T4d）、N4、N5 |
| 6 | 检查 | 错误改到 0；「要人看的」逐条看；卡里验证条目逐条读 | `check.py … --require-new --docs … --app-name … --sources …` | Q1–Q3 |
| 7 | 渲染 | 出预览，看改句套上、没有残留的「待核」「有出入」 | `render.py <知识目录> --memory <memory> --out <目录>` | P1–P2、Q5 |
| 8 | 专门复核 | **安卓平台和依赖库两类条目，加上全部正文改句，交给另一个人专门复核**：回出处重核、就地改、记日志 | `briefs/review.md` | V6b、Q6 |
| 9 | 每批抽查 | 一批复核完，再由另一个人按类别抽 40 条左右加 8 处改句逐条核，只查不改；过线才并入 | `briefs/audit.md` | Q7 |

第 3–7 步是一个写的人对自己那几条经验做完；第 8、9 步换人。

**花费：** 一条经验写下来（第 1–7 步）大约 8–12 万 token，一个写的人一组 3–6 条约 15–20 分钟；专门复核再加三到四成 token，每人一份约 20–30 分钟；抽查一批一次，约 25 万 token、10 分钟。几组并行时，写、复核、抽查三段依次做，一次归并约多一小时。只补来源的经验默认不做，花费跟着新增和加了句子的条数走。

## 并入经验库

1. 知识文件拷进 `knowledge/lessons/`；已有同名文件的（旧格式）替换。
2. **改句进正文（默认全部发布）：** `scripts/publish_plan.py --store <store> --knowledge <仓库的 knowledge/> --out <提案.json>` 取 store 里有未发布改句的经验的全部字段，把改句套进对应字段（每处 `before` 在这条经验的各字段里合起来恰好一处，否则报出、不生成提案），`evidence`、`requires`、`topic`、`status` 原样；再 `apply`、`lint`、`export --link-cards`（`references/tools.md` 第 7 节的注意事项）。发布以后知识文件里的改句原样留着，渲染和检查脚本认它「已发布」，不再套、不报错。默认全部发布的理由：交出去的经验只有一个说法，直接读阅读包的人和下一次归并看到的也是改过的正文。要上机才能定的不写成改句（进 `device_todo`）。
3. 跑 `scripts/gate.py check`（入口 ① 必跑；入口 ② 用 `--lessons` 给这批的经验号），再跑仓库的 `knowledge/check.py`（不加 `--legacy-ok`，留作评测的应用名用 `--app-name` 传）和 `knowledge/render.py`（重渲染 `knowledge/rendered/`）；`knowledge/README.md` 的覆盖表用 `scripts/gate.py readme --repo <仓库>` 重生成，并入记录加一行。

**两套脚本的分工：** `knowledge/skill/scripts/check.py`、`render.py` 是写知识的人用的，`check.py` 带 `--sources`、`--docs` 等核对本机出处的选项；`knowledge/check.py`、`knowledge/render.py` 是仓库一侧的检查和渲染，同一套新格式规则外加两种旧格式，只对仓库里的 `memory/` 核改句，不核本机出处。两个渲染脚本对新格式文件的输出逐字节相同。详见 `references/tools.md` 第 2 节。

## 不做的

- 不在写知识时改经验库、store 和作者的文件；改句只在知识文件里，进正文另走提案。
- 不上机；要上机才能定的只进 `device_todo`，不交给模型。
- 不用博客、问答、第三方教程；不用旧的本机文档副本作出处。
- 不看评测用的工程和评测结果，不按评测结果加减条目；不设条数上限。
