# 02 听音练习：session → memory

- 会话包：`C:\Users\hongy\projects\_sessions\_server-download-20260927\downloads\96ed3b1920f46d74\export.tar.gz`（run 5e3fe706，host codex 0.157.0，模型 gpt-6-sol；hmigbot-plus-1.6.0，runtime v1.5.2）
- 材料：`materials\`，原样解包，238 份转录 sha256 与导出 manifest 全部一致
- 流程：migloop-session-to-memory 0.8.3（triage、build-cards、maintain 同为 0.8.3），解释器 `py -3.13`
- 共享库：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\store`，沿用 01 轮 HEAD，snapshot 后续写，没有新建库

## 范围

这个 run 分三段，全部纳入材料池：

1. 迁移主会话（09-25 19:04–22:54 UTC），含 hmigbot 自动注入的验证闭包循环；
2. 用户启动的两轮 ECAT refine（09-26 05:08–05:35、06:13–06:36）；
3. 用户启动的 dt-verifier TDD 验证（06:53–07:40）。

第 2、3 段运行在副本 `eartraining-ecat` 上。副本在转录外从迁移终态复制而来，本身是 git 仓，转录里没有复制记录。用户直接消息只有 gate 选择，以及一句“Linux 技能脚本入口已修复”（转录外的工具修复），没有用户手写代码。用户启动的会话对应用做的实际修改都按修复纳入。

- **生成结束 2026-09-25T20:58:11.566Z**：execute 在全部生成写入完成后的第一道编译门（FV-2）派发时刻，口径与 01 轮一致。execute 内与生成交错的编译门（Stage 1 收口、Base-7、group1/2）里的修改，按声明边界算作生成收敛。
- **观察截止 2026-09-26T07:40:33.959Z**：材料池最后一条记录。

## 问题清单（`repair-tasks.yaml`）

| # | 出处 | 问题 | 最终卡 / 缺口 |
|---|---|---|---|
| 1 | 迁移·FV-2 编译门 | catch 中 `throw error` 抛未定类型，arkts-limited-throw | `cards/issue-7da8b355891030ab0ada/case-1.json` |
| 2 | 迁移·验证前自查 | bundleName/vendor 停留脚手架默认值 | **无卡**（阻塞，见下） |
| 3 | 迁移·验证闭包 | @Builder 按值传启用态，步进按钮不刷新 | `cards/issue-c4b0a71b1ff405c63013/case-1.json` |
| 4 | 迁移·验证闭包 | 页面 @Local 快照，“使用”组合返回后不刷新 | `cards/issue-fa7ad75016781faf0cc5/case-1.json` |
| 5 | 迁移·验证闭包 | 组合名 TextInput 缺 maxLength | `cards/issue-e3cd92963aa40d922fdc/case-1.json` |
| 6 | 迁移·验证闭包 | ForEach 键只取 id，改名后卡片不刷新 | `cards/issue-3045f4019d7d543e18ca/case-1.json` |
| 7 | ECAT | 打开组合库时 dispose 播放 | `cards/issue-f4de4c0baf567b736a95/case-1.json` |
| 8 | ECAT | 未注册全局未捕获异常观察器 | `cards/issue-0c59c27ee4ceac59cb60/case-1.json` |
| 9 | ECAT | AppScope 图标为 1×1 占位 | **无卡**（阻塞，见下） |
| 10 | ECAT | console.error 未改 hilog | `cards/issue-2b82a569104ca26f84ae/case-1.json` |
| 11 | ECAT | initialize() 失败时无限加载 | `cards/issue-346f57800b71b616129f/case-1.json` |

- **新需求**：第 8 项。调查员核实迁移期所有输入都没有提出全局异常观察器，这一项由 ECAT crash_risk 规则提出。卡片按“入口装配契约缺这一项”归因，写码者没有被标为偏离输入。
- **辅助产物**：搁置 3 组 pipeline_tooling、3 组 test_support 和 1 组 artifact，都没有改应用运行逻辑。其中 dt-verifier 为测试在副本里加了 `.id()`、直挂页面、mock 注入和测试模式分支，都属于测试支撑。
- **未实施 / 净零**：
  - ECAT 在“播放中改设置是否停音”上来回改了 5 次，截止时与迁移终态一致，所以没有保留的修复。
  - `main_pages.json` 告警每轮都被判为误报，没有修改。

## 制卡结果

11 个 job 各派一个独立子代理，最多 6 个并行。9 个返回 `status: valid`，2 个阻塞。

**检查器与 Codex 转录的适配问题（环境缺口）**：共享索引的 effects/files 表是空的。Codex 把读写都包在 `exec` 的 JS 里（`tools.exec_command`、`tools.apply_patch`），索引没有把这些调用抽成读写记录。因此：

- 9 张有效卡的每条边都退回 `force_eligible`，调查员逐条用“调用行 + 执行事件 + 回执行”补了 force 证据后才通过。
- 目标认证只能依赖原文里出现过完整路径。迁移工程的 `AppScope/app.json5` 在转录里只以相对路径出现，第 2、9 项因此在 target 这一步就被拒（`target file has no recorded evidence`），写入边的 force 也用不上。按 skill 规定，这两项没有改检查器，也没有虚构连接。稿件和回执留在 `cards/issue-36316f44068d9bdd3a8a/`（draft-3、pack-feedback-3.json）和 `cards/issue-58fe61073817512b487a/`（draft-1、pack-feedback-1.json）。

**跨仓缺口**：副本 E 上的修复文件与迁移工程 M 的同名文件在索引里是不同路径，转录里也没有复制交接。ECAT 类任务都用 M 侧文件画生成链，E 侧文件列为 `unresolved_targets` 并写明原因（第 7、8、10、11 项）。

**对拆分清单的更正**：第 2、9 项的调查员查到，主会话 19:48:41 在生成期写过 `AppScope/app.json5`。当时它按 a2h-execute Stage 0 的 dev-identity 规则刻意保留 bundleName/vendor 占位，也保留了占位图标。拆分清单里“生成期未写过该文件”的说法有误，原因是我只扫了边界之后的 shell 写入。两份阻塞稿的调查结论是：偏差源自技能规则，其中 dev-identity 与 verify CHECK-2 自相矛盾，且 arkts-app-identity 的读取被截断。这些结论只在稿件里，没有进经验库。

## 经验库变化

`e435fd0d…`（01 轮，3 卡 5 条）→ ingest `dd40ec98…`（+9 卡）→ apply `366c1c65…`（`proposals/plan-1.yaml`，新增 11 条）→ apply `ad8baab3…`（`proposals/plan-2.yaml`，只改顶层主题介绍）。发布版 `ad8baab3bb609abedb0c9072ba8e03d749a73d9e49d8ea964dc9f1cd24706b0b`：12 卡，16 条 active。完整序列见 `revisions.json`。

**新增 11 条**（各引卡片的 diagnosis 与相应 recommendation）：

1. arkts/strict-mode：catch 中继续抛出前把异常收窄为 Error。（卡 1）
2. ui/state：随状态变化的参数不作 @Builder 值参，改为内联或 @ComponentV2 @Param。（卡 3）
3. ui/state：页面直接读共享 @ObservedV2 模型的 @Trace 字段，不复制成 @Local 快照。（卡 4）
4. ui/state：条目以新对象替换时，ForEach 键要包含会变且显示的字段；原地改 @Trace 字段时例外。（卡 6）
5. ui/input：受控输入框的长度上限用 TextInput.maxLength，不靠 onChange 拒绝写回。（卡 5）
6. ui/navigation：源端一个 Composable 内多屏共享的清理，拆成多页后归属外层生命周期。（卡 7）
7. app/entry：入口 Ability 注册 errorManager 全局异常观察器。卡片判为新要求，经验里写明了这一点。（卡 8）
8. app/logging：新增错误日志沿用工程的 hilog 约定。（卡 10）
9. arkts/async：同步读取改成异步 initialize 后，失败分支要复位状态并离开加载态。（卡 11）
10. **process/input-loading（跨卡）**：必读 skill 要读全；批量 cat 被截断或只读前 N 行时，规则并没有进入上下文。4 张卡、3 个写码 agent 合证（卡 1、3、10、11）。这是本批最强的跨卡模式：写码者随后写出的代码正好违反没读到的规则，回报里仍把这些 skill 列为 loaded。
11. **process/spec-handoff（跨卡）**：沿用已生成页面或兄弟任务的写法前，先回源码核对。3 张卡合证（卡 3、5、6）。

**与已有经验的关系**：01 轮的 5 条（string|Resource 重载、主题隐式样式、零硬编码色值、ConstraintLayout 居中、规格与源码冲突时按源端）与本批机制都不重合，所以这次没有补证、融合或修订。

- 01 报告留的待查项是“规格与源码冲突按源端”这条跨卡经验换 app 后是否仍有支持。本批没有出现“实现者读到相左的源码却照规格写”的案例，所以它没有得到新支持。
- 第 7 项虽然也是规格先偏，但下游实现者读源码时正好跳过了相关段落，不满足该条的触发条件。
- 与它最接近的新经验（第 11 条）放进了同一主题目录，并把目录介绍扩展为“规格、已生成代码等二手输入与源码之间的交接”。

**只留在卡里、没写进经验的内容**：

- 项目取值：24 字符、DOMAIN 0xFF00、350 ms、`${preset.id}:${preset.name}` 的具体字段名、各文件行号。
- 面向流水线维护者的建议：在 a2h-execute 入口装配契约与 verify CHECK-1 中补“全局异常观察器”“console.* 改 hilog”，以及“巡检建议加载门时写失败出口”的评审侧动作。这些只在卡片与本报告里记录，给迁移模型读的经验不包含它们。

## 交付物

- 阅读入口：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\runs\02-ear-training\memory\index.md`（revision `ad8baab3…`，16 条经验，16 个主题目录）
- 其他文件：`repair-tasks.yaml`、`metadata.json`（附 `server-metadata.json`）、`dispatch/`、`cards/`（含各稿、回执与查询文件）、`proposals/plan-1.yaml`、`proposals/plan-2.yaml`、`dispatch-log.md`、`revisions.json`

## 用时与 token

- 墙钟：2026-09-27 06:44–07:33（-04:00），约 50 分钟。其中拆分与建索引约 20 分钟；11 个调查员 07:04 起派出，最后一个 07:28 完成，约 24 分钟；归并与导出约 5 分钟。
- 子代理 token（取自完成通知）：11 个合计 2,887,350；单个 205,213–348,797，用时 430–879 s。逐项见 `dispatch-log.md`。
- 编排主代理的 token 用量本地拿不到，未计入。

## 未完成与待复查

- **第 2、9 项无正式卡**。原因是索引不解析 Codex `exec` 内的读写，加上 M 的 `AppScope/app.json5` 从未以完整路径出现。需要索引按会话 cwd 与 exec 的 workdir 解析相对路径后，对同一 job 重新 pack（现有稿件可直接复用）。App 身份与图标的经验暂缺。
- **ECAT 副本 E 上的 9 个修复文件列为未决目标**（第 7、8、10、11 项）。原因是复制交接不在材料里。
- **第 7 项的疑点**：调查员指出 ECAT“打开组合库会打断播放”没有设备复现，而且练习页作为 Navigation 首页内容，推入子页时可能根本不触发离开回调。第 6 条经验只写契约归属与“先确认挂载方式”，没有断言一定会打断。
- **第 3 条经验的疑点**：其中 onShown 没生效的触发机制，卡里标为未单独验证。
- **Codex 派工正文与推理都是加密内容**。各卡的写前输入只能从实际读取回执还原；各卡 unknown 已注明派工里是否另有要求无法核对。
