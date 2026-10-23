# 多应用迁移经验库

[从 memory/index.md 开始阅读](memory/index.md)

## 两层产物

- `memory/`：开发维护用的阅读包，按三个检索轴组织：`stage`（阶段字段）、`topic`（领域/主题[/子主题]，按技术机制划分）、`signals`（输入里可 grep 的符号）。根 `index.md` 给出三步召回协议、领域与阶段入口；`catalog.jsonl` 每行一条经验，`signals.json` 是符号到经验 id 的倒排表，`by-stage/` 按阶段分组，`topics/` 每级只列直接子项，`topics/<主题>/<id>.lesson.md` 是正文（与主题索引同目录，末尾自动附同源经验和来源段，可点击到 `store/` 中对应版本的卡片）。
- `store/`：正式情景卡、经验数据及格式需要的版本快照。经验通过 case、claim、revision 关联具体来源卡。

正式卡使用自包含的 `migloop-case/4`，保存模型总结、建议、归因图及必要身份与环境信息。迁移模型通常只阅读经验，证据卡用于按需复核；图的 UI 结合原始迁移转录重新生成，不把检查回执和展示缓存存成知识。

当前知识版本以 `store/HEAD.json` 为准；`memory/manifest.json` 记录对应 revision、文件校验和与来源绑定。[MEMORY.md](MEMORY.md) 保留为兼容入口。

## 用这个库跑迁移实验

一条命令起一组端到端迁移（无 memory / 有 memory 两种条件，建好目标工程、装好我们的 `.claude`、影子 git 记录和首写召回）在 [a2h-replay-bench](https://github.com/hxy450/a2h-replay-bench) 的 `e2e/`。bench 不保存经验库副本，只在 `memory-refs.json` 里按名字固定本库的 commit 与 revision，用到时取出该 commit 的 `memory/` 并核对 revision；经验库的更新都提交到本仓库。

## 更新与历史

每次迁移的调查任务收尾后统一归并，通过机械检查，再更新根目录的 `store/` 与带来源的 `memory/`，由调度器 commit 并 push 一次。推送失败保留本地提交，续跑只补推送，不重跑分析或强推远端。

只有部署给迁移 agent 时，才从同一 store 另行导出不带完整来源列表的精简阅读包；不拿部署包替换本仓库的 `memory/`。相对卡片链接按最终目录位置生成，仓库移动或克隆后仍可用。

两种阅读版均保留一行“来源支持：N 张卡 · M 次迁移 · K 个应用”。计数从当前绑定卡片自动计算：同卡的多个 claim 只算一张；迁移按记录的 server_session_id（本地记录可用 migration.id）去重；应用按 project 标识去重，不把同应用的多次迁移当成多个应用。缺失项标为未记录，不从子代理、材料池或分析会话推断。计数仅是历史样本覆盖，可辅助理解佐证强度，不是正确概率或成功复用次数；适用条件仍优先。开发版在计数之后继续保留全部来源链接。

旧版阅读包由 Git 历史保留，不按迁移复制多份。此前的 `runs/` 已退出当前 Git 树，本地的材料、稿件、报告与断点仍保留；原有提交没有改写。此次目录调整不改变卡片内容、经验语义或知识 revision。

当前发布分支：`memory/multi-app-20261017`（旧目录结构，知识版本 `212330c6…`）。`memory/structure-v2-20261017` 是同一批 715 张卡、550 条经验的 v2 结构版本（知识版本 `9f396e97…`），对照评测后再定是否作为发布分支。本分支 `memory/opencamera-20261023` 在其上归并 OpenCamera（见下），待审核后合并。留出 app ColorLines 的独立评测库在 `memory/colorlines-holdout`，不并入本分支。工作目录、转录、SQLite、模型日志、提案及本机调度信息不进入正式发布树。

机械检查保证格式、引用及所画历史关系符合契约，不等于归因语义认证或泛化效果证明。评测应冻结一个 Git commit / memory revision，在未入库应用上对照。

## 2026-10-23：OpenCamera 归并（分支 memory/opencamera-20261023）

起点 `56fcfe88…`（memory/structure-v2-20261017）。来源是 OpenCamera 的 a2h 迁移（GLM-5.3，hmigbot 1.7.0 claude_sdk，无 memory），以及两轮返修（Claude Opus 一处、Codex 其余）。迁移期原生转录从 OBS 原始切片按字节偏移重组，92 份与上传方 watermark 的长度和前缀 sha256 一致。发布器 0.11.1。

- **入卡**（`50c978289b637ed98f68c2cf4e26271ec12f637c9af32acb7573a38226a992ea`）：101 个返修问题合成 44 个制卡任务，入卡 43 张（715 → 758）。job41（21 个语言目录未迁移）的目标文件只由返修脚本写出，索引没有记录、目标校验无 force 通道，没有正式卡，归因稿留在本地工作目录。
- **归并**（`e548ed0ba4c7bf875453e5e0bf29f777d3d31d6de51465de52bc98e58aa50095`）：active 经验 550 → 586；新增 36、修订 17（增量，其中 1 条兼呈现）、只补证 10、退役 0；新增经验与新卡之比 0.84。新开 `app/camera/{session, parameters, orientation, capture, recording}` 与 `app/media-library`；改写 app/entry、app/media、app/recreation、data/storage、process/lossy-transcription 的主题描述。迁移会话没有加载经验，没有召回或使用失败记录。
- **主题描述**（`276c45d921fb516691f9f45b45803e79886abb4bb9e1569dd57b2bb699fda6ed`）：补 app/camera/capture 与 app/camera/session 的描述，经验正文不变。
- **校验**：lint 命中 72 处，均在原有文本中，本次新增与修改的句子零命中。

## 2026-10-17：按 v2 结构重建（分支 memory/structure-v2-20261017）

起点 `212330c6…`（memory/multi-app-20261017）。知识版本 `9f396e9797c18686ee288022550338c72218bc5d5ded0c29f3fd10ad48283072`（序号 88：87 为 migrate，88 为补字段与重划主题），发布器 0.11.1（migloop `feat/memory-structure-0.10.10`：把 0.11.0 移到 0.10.10 之上）。保留 **715 张卡、550 条 active 经验**，没有重新调查，没有改写任何经验的 title、when、description、why、how、check、依赖或来源绑定；每条经验版本号加一，因为补了字段、移动了主题。

- **claim ID 稳定化**：`memory.py migrate` 在快照内把 715 张卡的 2,628 条建议绑定从 `recommendation:N` 改为 `rec-<文本哈希>`，卡片文件未改。
- **检索字段**：2026-10-07 v2 已定过且正文此后未改的 284 条沿用当时的 topic、stage、summary、signals；正文改过的 82 条沿用 v2 主题，按新正文重核 summary 与 signals；v2 之后新增的 184 条由分类子任务逐条补全。阶段分布：execute 513、spec 194、repair 92、plan 42、verify 42、converge 27；2,601 个不同符号。
- **主题树**：在 v2 树上扩展为 5 个领域 105 个主题路径、89 个叶子（最大 12 条）。新开的叶子有 app/playback、app/recreation、app/nfc、app/notification、app/window、data/preferences、arkts/java-stdlib、arkts/async-mapping、process/unapproved-deviation、process/lossy-transcription、ui/animation/*、ui/web、ui/accessibility、ui/interaction 下的 focus-ime、gestures、press-states、app-bar，以及 ui/dialog/frame、ui/graphics/canvas-text、ui/layout/variants。超限的 app/capability（15 条）拆为 sdk-lookup、degradation、launch，ui/layout/safearea 拆为 immersion 与 insets（软键盘避让并入 insets），页面转场并入 ui/animation/transitions。
- **校验**：apply 前后逐条比对，经验正文、来源绑定与状态无变化；从 store 重新导出与提交的 `memory/` 一致；lint 文风提示 690 条，与起点相同。

### 没有做的

- export 给出 23 条非阻断整理提示：14 个叶子少于 4 条（如 ui/libraries、ui/interaction/app-bar 各 1 条），9 个叶子多于 9 条（ui/layout/sizing 12 条，app/resources、data/storage、ui/theme/effects 各 11 条）。子任务建议的进一步拆分（app/resources 分 identity 与 conversion，back-stack、feedback、input 按子机制拆）没有做。
- 子任务提出的跨领域与跨叶子调整（如 SwipeToDismissBox 移到 gestures、runtime-semantics 两条移到 async-mapping）没有采纳；changed 经验的 topic 全部沿用 v2。
- lesson-6b2879705254045a49c5 正文没有任何代码符号，signals 暂用“同一项即忽略”这句守卫描述，不是 grep 符号。
- 召回方要用 0.11.1 的 recall skill 才能按三步协议读这个布局；没有做召回或迁移评测。

## 2026-10-17：omni-notes 归并（分支 memory/omni-notes-20261017）

起点 `e613047f…`（memory/multi-app-20261012）。来源是 omni-notes（Omni-Notes）的 a2h 迁移（GLM 5.3，hmigbot，无 memory）与一比一返修（Opus 5.5）。迁移期原生转录从 a2h 运行时上传的 OBS 切片取回拼接。

- **归并**（`ace057cc5e202b60bdf117b28276aff3b4a687e7cdfe4db7977883f64ac41bc5`）：入卡 46 张（669 → 715），active 经验 521 → 550；新增 29、修订 27（纠错 2、增量 25，其中 8 条兼呈现）、只补证 26、退役 0。两次会话都没有加载经验，没有召回或使用失败记录。
- **官方文档纠错**（`e8c7b39b112a0f2f8acff7bfdea743cf6d5977d195ee6f30342409e7b95ccb0c`）：用鸿蒙开发者知识 MCP 核对本次新增与修订的 82 条经验中的 192 条平台断言，查出 13 处错误（11 条经验：4 处在本次新增经验、2 处在本次修订句、7 处是起点版本已有文本），全部按纠错修改并在句旁注明文档出处；42 条经验改动。卡片、经验 ID、evidence 不变。
- **修订后复核与第二轮纠错**（`212330c62ac0d763caeb25e4d181395c0f03c4642c8756ada2eb7450bb9d5e55`）：对 42 条修订经验重新核对，13 处纠错中 12 处与文档一致、1 处部分解决；修订新增约 64 处出处中查出 2 处新错误（ArkWeb「默认视口 980px」、Swiper 弹簧曲线下 duration 不生效）与 4 处出处精度问题，改动 6 条经验。

三个状态各是一个提交，可分别检出对照。评测规则、任务集与结果见 [fuxi-ailabs/memory-eval](https://github.com/fuxi-ailabs/memory-eval) 的 `runs/omni-notes-20261017`。这三个提交原在 `memory/omni-notes-20261017` 上；`memory/multi-app-20261017` 从那里开出，作为合并后的完整多应用库，`memory/multi-app-20261012` 保持原样。

## 2026-09-30：阅读减负与制卡模型来源

本次维护后的知识版本为 `01caa432ff663246c58f608b99f0f32bae12111a1f17d324962f708d0a58bd5d`，保留 **276 张卡、256 条经验**。没有重新调查或全库重新归并，也没有改变卡片的正文、归因图、修复判断或迁移环境信息。

### 模型来源

当前 276 张卡的制卡分析模型均有 `claude-opus-5-5` 记录。原先 51 张已有记录；其余 225 张依据分析会话及调查员转录的实际模型记录补齐，而非仅按启动命令推断。

`metadata.analysis` 表示制卡分析的模型、客户端与根会话；`metadata.migration` 及已有环境观察表示被调查迁移的信息。两者不混用，也不把缺失的迁移模型填成 Opus。补录只更新卡片来源元数据和相应版本绑定，不改变经验语义版本或状态。

本地批处理已使用 0.10.1 运行包：宿主从实际运行事件采集分析模型，封装时自动附入卡片，调查员无需填写。直接在其他宿主使用 skill 时需由宿主提供同样的运行上下文；没有观察到的信息不猜测。

[查看带模型来源的完整卡片](store/cases/case-6b781bb8b1a4eb80b808/24d878a8aaa32c3bdfd97e6c38e9535508127e0644d3461891a191099f6f7298.json)

### 阅读上的变化

- 部署阅读包不再显示来源列表；开发仓库的 `memory/` 保留完整来源及卡片链接。完整 case / claim / revision 绑定同时保存在 `store/` 和 `memory/manifest.json`。
- 精简两条长期累加案例的 `why`，保留机制与适用边界；标题、时机、情境、动作、例外和可选检查未改。
- 将 layout、navigation 下的 34 条经验按机制移入子主题，ID 与来源关系保留。索引仍使用原来的标题、时机和情境，不截断内容。
- 维护 skill 增加“同机制仅补来源，不重复追加案例”的正向示例，约束同时适用于 `why`、时机和情境。一个索引的直接入口超过 20 个时，导出给出非阻断提示，由维护者按语义判断如何细分，不按数量机械分桶。

| 示例 | 维护前字符数 | 0.10.1 部署版字符数（不含来源段） |
|---|---:|---:|
| [规格与源码冲突](memory/process/spec-handoff/lesson-7a065e8fe384b8c462cc.lesson.md) | 2,974 | 967 |
| [目标代码先例](memory/process/spec-handoff/lesson-e9c6e8ef1b29a6fe9c26.lesson.md) | 3,247 | 928 |
| [layout 父索引](memory/ui/layout/index.md) | 7,167 | 1,299 |
| [navigation 父索引](memory/ui/navigation/index.md) | 6,963 | 307 |

前两条的缩短包括移除部署包来源段与精简 `why`，不是只改 `why` 的收益，也不是当前带来源的开发版文件长度。父索引变短也不等于整个任务同比例节省：按文件选择模拟，只读 layout 的约束分支时，父子索引合计为 3,855 字符；约束、尺寸、滚动三支都读为 6,604；全部分支都读为 7,611，比原来多约 6%。navigation 只读参数分支为 3,090，全部分支为 7,293，比原来多约 5%。这些是字符测量，不是模型实际召回或质量评测。

### 校验与边界

逐张核对了 276 张卡的正文、图和迁移信息未丢失，所有经验来源仍可解析。仅因目录移动或正文改写而更新的经验按正常提案增加版本；未改写的经验不因来源元数据补录而失效。

本地 skill 回归 274 项通过、1 项跳过；批处理回归 65 项通过、1 项跳过。包来自干净提交 `27ced0f95005063fa9d610a39b7e1e80668c0d94`，归因内核与此前运行包一致。本次未修改 Server，未恢复批量模型分析。

后续展示修正：上一提交把仓库 `memory/` 也误导出成了部署版，现恢复来源段与可点击卡片链接。0.10.2 指令明确区分开发交付和部署导出，调度器每轮重新生成带来源的仓库视图；卡片、经验内容、ID、版本与知识 revision 均不因本次展示修正改变。

0.10.3 增加上述自动来源计数，部署版每条只多这一行，不恢复来源清单；未修改分类、卡片或经验正文，未增加模型必填项及评分机制。

[维护前的阅读入口](https://github.com/hxy450/fixchain-memory/blob/f6c57898066f8abd5c37e6a12d48815ae3509896/memory/index.md)

## 2026-10-01：触发目录小修与完整版本冻结

冻结标签：`memory-full-20261001`。知识 revision：`d7f8451f268e6beb805c73be4ccb6702c9de33203a3e214a37a1777d2a2af934`。完整保留 **276 张卡、256 条 active 经验**，不排除任何项目、不做应用留出；AntennaPod 的来源与相关经验均保留。因此，用这份库在 AntennaPod 上实验应解释为包含同应用历史经验的复用实验，而非严格的跨应用留出验证。本次没有运行迁移或恢复批量分析。

本轮只更新三条经验与五处目录介绍：

- [横向滚动容器交叉轴定高](memory/ui/layout/scrolling/lesson-2d7c6de68f604ae77caf.lesson.md)：由 sizing 移到 scrolling；保留 API 12 模拟器约 597vp 的观察、陷阱表依据和“已有设备测量值时以测量值为准”。how 留直接实现动作，全量 grep／设备必验要求改为有条件的局部可选检查。
- [点击时读取锚点坐标](memory/ui/interaction/lesson-963bf871aa4e910a8fc8.lesson.md)：由 layers 移到 interaction，正文与来源不变。
- [视觉修复依据](memory/ui/layout/lesson-8119d8bf0b58e4daac24.lesson.md)：情境 340 → 116 字符，why 541 → 161 字符；保留跨设备、渠道/运行状态、文档预览和 Canvas 内外尺寸一致的条件，动作、例外和来源未改。
- layers 保留运行时挂载、叠放与几何职责；interaction 介绍聚焦点击命中、手势、事件时坐标，不再把挂载位置作为入口。parameters 介绍以“跳转契约”开头，路径不改。

三条经验沿用 ID、正常版本 +1；其余 253 条经验不变，全部卡片文件及来源绑定未变。skill 0.10.4 增加按事前已知任务归类的原则、LazyRow 与点击锚点的正向示例，以及少量代表任务的选路检查；没有新增必填字段、查询工具或审核步骤。

人工目录走查以来源经验记录的真实任务情境为输入：横向标签行 → ui/layout/scrolling；点击触发动效/气泡 → ui/interaction；点击接页面跳转 → ui/navigation/parameters。检查的是目录介绍与链接是否提供自然入口，并非独立模型召回率评测。278 项 skill 回归通过，1 项跳过。

维护源码已发布到 [migloop 的工作分支](https://github.com/hxy450/migloop/tree/feat/memory-reading-ergonomics)，冻结源码提交为 `97e9c211b8eee754a34cde926901c60ebba94911`；本地包来自干净源码，Server 未改。开发版保留完整来源；从本标签对应 store 用 0.10.4 的默认 export 可重建带计数、不带来源清单的完整部署包。该部署包 `manifest.json` 的 SHA-256 为 `4561e7f307226ce858b1b2265a1e3b8389f229f00a3c8de17c34a86d7b63725c`。冻结后不自动跟随后续批次更新。
