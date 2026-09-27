# 04 Cofi：session → memory

- 会话包：`C:\Users\hongy\projects\_sessions\_server-download-20260927\downloads\cbfc5590f07ce9b2\export.tar.gz`（run f0b2ddbc，host Codex 0.147.0，模型 glm-5.3；hmigbot-plus-1.6.0，runtime v1.4.8）
- 材料：`materials\`，原样解包，86 份转录的 sha256 与导出 manifest 全部一致
- 流程：migloop-session-to-memory 0.8.3（triage、build-cards、maintain 同版本），解释器 `py -3.13`
- 共享库：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\store`，沿用 03 轮 HEAD，snapshot 后续写，没有新建库

## 范围

- **会话构成**：一个迁移主会话 `main-01a0b85d`（09-19 06:32–12:01 UTC，含 34 个生成期子代理），两个 hmigbot 审阅会话，一次自动起跑的 ECAT refine（两轮：判官 7 个/轮、判别器、生成者会话 `main-01a0b99c` 及 11 个 worker），以及 13:56 起只有判官、没有生成者的第二次 ECAT。
- **用户调试**：没有人工消息。外部输入只有首条 /a2h-run、三次限流续跑提示和 hmigbot 注入的“验证闭包仍有阻塞项”。ECAT 由 hmigbot 自动起跑，其修改按修复纳入（与 02 轮口径一致）。
- **关键背景**：09:25 起子代理额度耗尽，主会话三次续跑后自己接手了 Base-6 平台端口和 Stage 2/3 接线，没有再派切片 worker。本轮大部分生成偏差都出在这一段。
- **生成结束 2026-09-19T10:26:37.280Z**：FV-2 终态全量编译的派发（主会话 L2134），此前最后一次应用写入在 10:21:29。
- **观察截止 2026-09-19T13:59:12.701Z**：材料中最后一条带时间戳的记录；最后一次应用写入是 ECAT 生成者 13:53:17。

## 问题清单（`repair-tasks.yaml`，20 项）

| # | 问题 | 最终卡 |
|---|---|---|
| 1 | 应用身份与版本元数据（bundleName/vendor 脚手架值、版本号字面量） | `cards/issue-f935850c669c48f05a00/case-1.json` |
| 2 | 路由名带参数、页面登记 | `cards/issue-17c8141513c5958bfbac/case-1.json` |
| 3 | 默认配方播种语义 | `cards/issue-b2793695ef65617c820a/case-1.json` |
| 4 | 开源许可页加载失败 | `cards/issue-ffdccd8c954d99b4c6d6/case-1.json` |
| 5 | 可折叠顶栏两态近似 | `cards/issue-66f3c1649b7b5c4f38b5/case-1.json` |
| 6 | 动画图标以待补资源占位 | `cards/issue-753b41488ff67ec1d068/case-1.json` |
| 7 | 步骤切换提示音与振动 | `cards/issue-290eac71ee43fe336138/case-1.json` |
| 8 | 外观设置（动态主题、波浪计时器）不生效 | `cards/issue-470d704a6ec794b4c3c9/case-1.json` |
| 9 | 后台计时、通知授权、画中画被桩化 | `cards/issue-f93a2f80bafd58105489/case-1.json` |
| 10 | ECAT 首轮新写计时代码的恢复与清理缺陷 | `cards/issue-e92bb15630afd5b03216/case-1.json` |
| 11 | 监听器匿名注册未移除 | `cards/issue-054901ca662ae6c66988/case-1.json` |
| 12 | 详情计时器行为 | `cards/issue-6da4fe27589af8c43f01/case-1.json` |
| 13 | 列表页源码常量与映射 | `cards/issue-37a2c6aacb67d1fc0aee/case-1.json` |
| 14 | 编辑页克隆/删除语义 | `cards/issue-ef4b9ae3acaea9323135/case-1.json` |
| 15 | 编辑页返回键不先关覆盖层 | `cards/issue-11d5804336d719cc070e/case-1.json` |
| 16 | 备份/恢复反馈 | `cards/issue-2f11f734c53d33bee770/case-1.json` |
| 17 | 数据库 schema 与迁移 | `cards/issue-a3f7f5fbc8635b723b96/case-1.json` |
| 18 | 描述链接未着色、不可点 | `cards/issue-8128c57ee5fb2e4f49d1/case-1.json` |
| 19 | 外部深链未声明 skills.uris | `cards/issue-6bc0c044e9bb2281aa01/case-1.json` |
| 20 | ECAT 非源端要求（全局异常观察、Wear 键、ArkTS 规范改写） | `cards/issue-98e7bd27bb334db83f51/case-2.json`（case-1 为前一稿，未入库） |

搁置项：UI 测试入口（route 参数、KNOWN_ROUTES、onPageShow 消费）与 ohosTest 归测试支撑；像素比对与 UI shell runner、结构闭包工具副本、把 Android 参照构建换成中文串归流水线工具；报告、判定、规格 AC03 纠错归产物。未实施：动态快捷方式（API 21 无接口，只登记决策缺口）、Wear 页面、RecipeAddPage 与详情页覆盖层的返回键、ECAT 清单里的孤儿 skill 文件。

## 制卡结果

20 个 job 各派一个独立子代理，同时最多 6 个，**20 张全部 `status: valid`，没有阻塞**。Codex 0.147 的 apply_patch（相对路径）能被索引解析成绝对路径并归属到正确 agent，写边都由检查器自动绑定；需要 force 的只有 shell 批量读取（每张卡 2–7 条），与 02 轮 Codex exec 全 force 的情况不同。逐卡的偏差定位、force 边与未决目标见 `dispatch-log.md`。

调查员核实后，有几项修复被判为判官或检查器的新要求，没有画生成期链：600vp 断点与 FAB 尺寸（源码是 `> 600` 和 padding，判官误读，修复后反而偏离源端）、重量公式去掉 timeMultiplier、recipe_new“缺表”（只是 Room 迁移临时表）、main_pages 登记与 @Entry、成功提示自动消失、全局异常观察、hilog 与注释卫生。

## 经验库变化

`c8107293…`（03 轮，15 卡 22 条）→ ingest `26efa475…`（+19 卡）→ apply `19dd9a4a…`（`proposals/plan-1.yaml`）→ ingest `2c5d1eb6…`（+1 卡）→ apply `37d28648…`（`proposals/plan-2.yaml`）。发布版 `37d28648907b93be2e9ec39005c0329cd34c0c811aa7ff056f556bac8092c29c`：35 卡，47 条 active，28 个主题目录。完整序列见 `revisions.json`。

**新增 25 条**，其中 6 条由多张卡归并而来：

1. **process/input-loading**（6 卡：后台计时、计时器、提示音、列表外链、克隆、深链）：编排者因子代理不可用而亲自实现切片时，先加载切片 worker 本应拿到的全部输入（切片计划、验收条目、决策正文、源码锚点），不凭占位登记表的一行触发文本写代码。
2. **process/task-handoff**（4 卡：外观、提示音、版本号、后台计时）：解决前向占位时按触发文本逐项兑现，只接一半、写常量或删标记都不算闭合。
3. **process/spec-handoff**（4 卡：播种、列表常量、克隆、描述链接）：写验收条目时实读所引源码，照抄比较符与边界样例；复制条目注明来源与变换；工具类按真实调用点归属。
4. **app/platform**（3 卡：外观、后台计时、ECAT 计时缺陷）：已批准等价实现的平台能力要真实现，判定“没有”前先查 SDK 声明，替代方案显式登记。
5. **app/settings**（2 卡：提示音、外观）：每个设置开关都要有运行期消费方。
6. **process/task-handoff**（2 卡：顶栏、动画图标）：“不确定/待补资源/延期”占位只登记输入确实缺值的情况。

其余 19 条各由一张卡支撑，按主题：app/platform（应用内计时替代后台 Worker 的恢复与退出清理）、app/entry（深链 skills.uris 与隐式 Want 验收）、app/identity（bundleName/vendor、运行时读版本号）、ui/navigation（固定目的地名加 param、popUpTo inclusive 映射为栈重建、页内覆盖层逐层处理返回、路由参数哨兵）、ui/state（监听回调存字段并移除）、ui/layout（连续折叠顶栏）、ui/graphics（动画矢量按状态选帧）、ui/feedback（单一 Snackbar 宿主与失败态渲染）、ui/text（链接富文本）、data/seeding、data/schema、data/parsing（org.json null 语义）、data/model（持久化枚举映射）、arkts/strict-mode（对象字面量类型与索引签名）、process/task-handoff（转述禁令带替代写法）。新开主题 app/settings、app/platform、ui/graphics、ui/feedback、ui/text、data/*。

**修订 6 条（补证并扩展）**：

- `lesson-42df1ac4…` 必读材料读全（v2→v3）：范围从 skill 扩到功能规格、参考文档与源码。本轮 4 张卡（播种、顶栏、计时器、schema）的截断正好落在要用的段落上。现由三个应用、两种宿主支撑。
- `lesson-7a065e8f…` 规格与源码冲突按源端（v1→v2）：01 轮留下的待查项“换 app 后是否仍有支持”，本轮有了新支持：规格作者把“列出全部默认项”写成“只列缺失的”，实现者读过源码仍照规格。另一例是转换者以“验收项没列”为由删掉源码里的链接，条目因此扩成“冲突或遗漏”。
- `lesson-e9c6e8ef…` 沿用兄弟页前核对源码（v1→v2）：两位设置页转换者读到正确源码，仍一个照抄兄弟页、一个再照抄前一个。
- `lesson-4f81eeea…` 移交登记（v1→v2）：新增“登记里写入源端确定值与出处”“只允许写本文件时在本文件实现或登记，不静默省略”。
- `lesson-c6132bf5…` 全局异常观察、`lesson-11e9d15d…` hilog（各 v1→v2）：第二个应用同样核为 ECAT 新要求，生成期输入里没有。

**只留在卡里、没写进经验的**：Cofi 专用的计时状态机清单（概览态 -1、完成态 progress=1 等）、各处具体数值与路由名、P-S*/D-00x 编号、历史 agent 与行号。

## 交付物

- 阅读入口：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\runs\04-cofi\memory\index.md`（revision `37d28648…`，47 条，28 个主题目录）
- 其他：`repair-tasks.yaml`、`metadata.json`（附 `server-metadata.json`）、`dispatch/`、`cards/`（各稿、回执）、`proposals/plan-1.yaml` 与 `plan-2.yaml`、`dispatch-log.md`、`revisions.json`

## 用时与 token

- 墙钟：2026-09-27 08:24–09:47（-04:00），约 83 分钟。
  - 解包、拆分、建索引：约 16 分钟（改动量大，ECAT 两轮约 160 次补丁）。
  - 20 个调查员：08:40 首批派出，最后一个 09:33 完成。
  - 归并与导出：先对 19 张卡归并（09:28），最后一张到齐后二轮归并并导出（09:44）。
- 子代理 token（完成通知）：20 个合计 5,581,801，单个 192,754–387,241，用时 422–1083 s。
- 编排主代理的 token 用量本地拿不到，未计入。

## 未完成与待复查

- **未决目标**（均在卡内写明原因）：修复期新建的文件（Haptics、WallpaperPaletteService、AnnotatedStringUtils、WearBridgeKeys）和生成期没有任何写入的 module.json5 画不出生成期写边；属于新要求或连带改动的文件（EntryAbility 的异常观察、DirectLinkDialog、LicensesPage 规范改写、RouteNames、main_pages 等）没有归因。
- **单应用支撑**：25 条新经验全部只来自 Cofi；其中 19 条只有一张卡，多卡归并的 6 条也集中在同一个接手的编排会话，同批卡不算独立验证。平台行为（org.json 的 null 语义、wallpaper.getColors、bundleManager 读版本、skills.uris 字段）取自卡里核过的 SDK 声明或源码，没有另做设备实测。
- **修复本身不完全符合源端**：动画图标修复后运行中的 FAB 仍是播放图形；顶栏背景色与阴影仍按 0.5 两态切换；判官要求的 600vp、FAB 尺寸改动与源码相反。这些写在对应卡的 summary 里，截至观察截止未改。
- **未实施**：动态快捷方式、Wear 页面、RecipeAddPage 与详情页覆盖层的返回键，截止时都没有修改，没有卡。
- **第二次 ECAT**（13:56 起）只有判官会话，判定没有进入本轮清单。
