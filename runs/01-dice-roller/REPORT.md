# 01 Dice Roller：session → memory

- 会话包：`C:\Users\hongy\projects\_sessions\_server-download-20260927\downloads\3bdf123989a2a39f\export.tar.gz`（run b459afb8，host claude-code，生成/修复模型 glm-5.3；migbot-cc runtime v1.5.2，pack 1.6.3）
- 材料：`materials\`，原样解包，28 份转录 sha256 与导出校验全部一致
- 流程：migloop-session-to-memory 0.8.3（triage、build-cards、maintain 均为 0.8.3 发布包），解释器 `py -3.13`
- 共享库：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\store`，此前不存在，本轮新建；没有导入其他实验的旧经验

## 范围

这是一次无人值守的 E2E 运行，没有用户调试或 vibe coding 的消息。按转录中实际发生的修改判定，不看 verify 标签。

- **生成结束 2026-09-22T15:23:38.860Z**：取 Stage 2 首道编译门派发的时刻。此前的应用写入都属于生成：资源迁移、converter 写页面、入口装配。
- **观察截止 2026-09-22T17:01:41.861Z**：续跑主会话最后一条记录。
- **中断**：生成主会话遇 429 用量上限中断，续跑一次也被 429 打断，第三段主会话完成后续阶段。三段同属一个 run，全部纳入材料池。

## 问题清单（`repair-tasks.yaml`）

| # | 分类 | 问题 | 修改者 | 最终卡 |
|---|---|---|---|---|
| 1 | 修复 | `accessibilityText` 收到 `string \| Resource` 联合类型，编译报 10505001 | 编译门 hmos-builder | `cards/issue-1d6dca36cb9c3cec5d87/case-1.json` |
| 2 | 修复 | Roll 按钮没迁主题色，回落 ArkUI 默认蓝胶囊 | CHECK-3 visual-fixer | `cards/issue-97a40a9d2dce65dc9f9c/case-1.json` |
| 3 | 修复 | 骰面本应自身居中，被写成图加按钮整组居中，骰面偏上 | CHECK-3 visual-fixer | `cards/issue-6448a485599bfc0740c6/case-1.json` |

- **新需求**：无。
- **辅助产物**：4 组 pipeline_tooling 和 2 组 artifact，都没有改应用。
  - pipeline_tooling：验证工具链的 schema 漂移绕行、edge-walk 账本处置、结构门对 TODO 资源的登记、FV-2 强制重编时的 touch。
  - artifact：截图、finding 单、各类报告、回顾报告与 patch。
- **未实施**：3 项有 finding 但到截止都没有改。
  - ActionBar 标题栏缺失：判为决策缺口。
  - ROLL/Roll 大小写：判为平台差异。
  - 无障碍文本在 dump 中不可观测：属 low_confidence。

三张卡都在第一次或第二次 pack 时通过（`status: valid`），`unresolved_targets` 都为空。只有按钮色这张用了 2 条 force 边，调查员回原文确认过读取真实发生。三张卡都判定偏差从规格提取阶段开始；其中两张另判实现阶段的第二处偏差：联合类型那张，实现者凭记忆的签名没去核对；按钮色那张，实现者把"零硬编码色值"误读成不设颜色。

## 经验库变化

`init d34ad607…` → `ingest 3962259…`（3 卡）→ `apply e435fd0d…`（提案 `proposals/plan-1.yaml`）。前后 revision 见 `revisions.json`。

库是新建的，所以没有补证、融合或修订，5 条全部是新增，均为 active。

1. **arkts/api-signatures**：传给 ArkUI 属性方法的值要按该方法的实际重载定型，不传 `string | Resource` 联合值。需要共存时在 getter 里归一成 string；不编译的批次里，凭记忆得出的签名也要对照 .d.ts 核对。（卡 1）
2. **ui/theme**：Android 主题隐式提供的控件外观，要写成目标控件的显式样式，用已迁移的语义色资源。（卡 2）
3. **ui/theme**：「页面零硬编码色值」只禁止字面色值，不禁止用 `$r` 引用语义色。（卡 2）
4. **ui/layout**：ConstraintLayout 里只有一个视图四向锚定 parent、兄弟单向悬挂时，不构成 chain，要用 RelativeContainer 的 alignRules 复刻，不要用 Column 整组居中。（卡 3）
5. **process/spec-handoff**：实现时如果规格写法与写前读到的源码、主题或映射参考冲突，按源端语义实现并在转换报告里标出冲突；有决策记录的例外。三张卡合证。

**只留在卡里的内容**（这些是项目修复值和具体坐标，没有写成通用规则）：`#6200EE`、`borderRadius(4)`、`minHeight 48`、骰面 44.4%/50.0% 等实测比例、具体文件名和变量名。

## 交付物

- 阅读入口：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\runs\01-dice-roller\memory\index.md`（revision `e435fd0dc8d6f271283f510b4f4db9b2d552c5b1356b84fa588921280ffd5e8c`，5 条经验，7 个主题目录）
- 其他文件：`repair-tasks.yaml`、`metadata.json`（附 `server-metadata.json`）、`dispatch/`、`cards/`（含各稿）、`proposals/plan-1.yaml`、`dispatch-log.md`

## 用时与 token

- 墙钟：2026-09-27 05:45–06:04（-04:00），约 20 分钟。其中 3 个调查员并行制卡约 6.5 分钟（05:54–06:01）。
- 子代理 token（取自完成通知）：175,969 + 258,824 + 223,353，合计 658,146；单个调查员用时 305–379 s。
- 编排主代理的 token 用量本地拿不到，未计入。

## 未完成与待复查

- 没有未完成的 job。
- 第 5 条跨卡流程经验的依据是三张卡，但都来自同一个 app、同一轮生成。换到其他 app 后，要看它能否继续得到支持。
