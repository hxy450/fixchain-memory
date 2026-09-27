# android-train-ticket-vest7（123高铁订票助手 → harmony_train-ticket_vest28）经验构建报告

- 迁移：`3a9f41ad-48a4-4f1a-a085-fb6393b81f8a`，材料 sha256 `0b720d5f…668c`
- 结论：**partial** — 20 个修复问题中 19 个产出通过 pack 的正式卡并已归并；1 个因检查器无法识别 Codex fork 派工边而阻塞。
- 发布：共享库 revision `faedea8b2fdab367b64dfa5099a31da03b7d5905eeacd2652a5d80ce7fab7174`（153 卡 / 162 条 active lesson），阅读入口 `memory/index.md`
- 用时：2026-09-27T20:19:12Z → 21:46Z，约 1 小时 27 分。Token：19 个制卡子代理合计约 4.89M（另 1 个未回报用量）；编排会话约 0.7M。

## 范围与边界

材料是 3 个并行的 Codex 主会话（S1 `main-01a06a30…`、S2 `main-01a06b1c…`、S3 `main-01a06b28…`）加 55 个子代理转录，时间为 2026-09-04T02:13Z–09-05T12:45Z。

- 基线（F001–F004 MVP、decision-ledger D-001…D-011）早于材料，不可追溯。
- 三个会话交替进行增量生成（OPT-001…008，以及用户临时提出的新页面对齐）和交付后修复，没有单一的生成截止时刻，所以 `generation_end` 为 null，`observation_end` 取最后一条记录 `2026-09-05T12:45:25.464Z`。
- 有两处需求变更记为生成背景，不当作偏差派工：
  - D-013：旅游、存钱、教育三类账本统一进入日常账本的详情页。
  - 用户在最后要求移除启动页。
- 设为 set_aside 的有：spec/验证文档、日报、截图分析、临时构建脚本，以及从别的工程临时复制后又删除的 `hvigorw.bat`。
- pending 中是跨会话代修的编译兼容改动，逐条列在 `repair-tasks.yaml` 里。

## 逐任务结果（均位于 `cards/<job>/`）

| job | 问题 | 最终卡 | 卡内未决目标 |
|---|---|---|---|
| issue-4042c8947009b8610581 | 首页横幅/资讯图点击留作 forward-ref | case-1.json | — |
| issue-974fbf4f7e024029e673 | 底部四图固定 dp 宽度溢出 | case-1.json | — |
| issue-25f05bb6ccf6238a63a1 | 背景 Cover 裁切、横幅入滚动 | case-2.json | — |
| issue-5824acb4fd986e7cbbcc | WebView 子资源错误误报整页失败 | case-1.json | — |
| issue-f04d62041916ea4f2191 | 宿主标题栏与 H5 顶栏重复/缺失 | case-2.json | — |
| issue-50230743abdc791d2a68 | emit 未类型化空对象字面量 | case-5.json | — |
| issue-639b36918b1cd5c1bbe8 | 计算器显示区/字号/margin 偏离 | case-2.json | — |
| issue-a224386ed55020afec18 | 计算器开关与下拉只复刻外观 | case-1.json | module.json5（无生成期写入） |
| issue-b0970c46149a1a9dbb98 | 底部导航条避让缺失/着色错误 | case-1.json | EntryAbility、MainPage（基线来源） |
| issue-6597b7f7858db941262c | 顶部状态栏安全区/沉浸式 | case-4.json | EntryAbility、Index、AddLedgerPage |
| issue-bd76c218ac0773e443e3 | 账本详情/新建页视觉结构偏离 | case-2.json | — |
| issue-0d37e50dbb1a2e0a9bee | 预算不能输小数、未按月关联 | case-1.json | — |
| issue-051eb9784dd65a84a1f8 | 记一笔确定无反应 | case-1.json | — |
| issue-504604963e18f4b6e2f3 | 记一笔/日历用路由页或内嵌块 | case-2.json | EventHub |
| issue-195f9a196894e58b5fb5 | 天气首启无城市 | case-2.json | — |
| issue-9d7fa754a567e2ecec7e | 天气折线/图标变体/切换图标 | case-1.json | — |
| issue-7d027e7b2cd42e741308 | 城市管理/选择页简化 | case-2.json | — |
| issue-c5fdc6640404c3d6440e | FlexGate 加密传输移植错误 | case-2.json | NearbyConfigBootstrap |
| issue-9a108f83b6eca279b883 | 启动页进度条样式与可见时长 | case-2.json | — |
| issue-5bd2103dd7cedb372480 | 附近品牌链接来源未迁移 | **无（blocked）** | 见下 |

对 issue-639b，只有 case-2.json 入库；同目录的 case-1.json 是链路相同的旧稿。

**阻塞原因（issue-5bd2）：** 归因链是 S2 规格作者 → `spawn_agent`（fork_turns=all）子代理 → 目标文件。索引里 `dispatches=0`，该派工边返回 “No matching confirmed dispatch”，而且不允许 force。材料里也没有可替代的文件交接，调查员没有虚构连接。最后一稿和反馈保留在 `draft-5.yaml` 与 `pack-5.out`。要解开这个阻塞，需要检查器支持 Codex fork 派工。

**全局机械限制：** 内核没有从 Codex `exec`（JS 包装的 apply_patch/exec_command）中抽出读写效应（effects/files 均为 0）。所有有效卡的边都是 force 边，每条都引用真实的调用、FileChange 和回执行号。派工和中途消息被加密，截图没有导出，这些缺口已按需记入各卡的 `unknown`。

## 归并（base `7757cf38…` → ingest `fefa9fd8…` → apply `faedea8b…`）

提案见 `proposals/memory-plan-1.yaml`，其中 13 条是更新、18 条是新建，另外新增主题 `ui/web`。

**同机制，补来源并扩写条件或动作（保留原 ID）：**
- ArkTS 对象字面量显式类型：新增事件总线载荷。
- 构建结果判定：结论只引用晚于最后一次改动的构建。
- 编译修复不以删功能换取通过。
- `match_parent` 加 margin 的写法。
- 固定头部留在 Scroll 外：扩展到 RelativeLayout 的 `layout_below`。
- 图标按固有 dp。
- 避让区 px2vp。
- 底部避让：新增“加在占据屏幕底边的那一层”。
- 空回调不算实现。
- style/@Builder 逐实例覆写。
- 贴顶显式对齐。
- 对齐既有页面时按源 XML 替换骨架。
- 参考数据取自 assets。

**不同机制，新建 lesson：**
- 增量对齐时点击入口的导航契约。已有一条“目标页未建就登记前向引用”，两者用 unless 区分：没有后续兑现方时适用新条目。
- Web：`onErrorReceive` 只在主框架错误时切换失败态。
- Web：宿主标题栏按 H5 状态双向显隐。
- 并排 `wrap_content` 图片列按比例分配宽度。
- 背景位图用 Fill。
- 控件点击处理器的副作用迁移。
- 小数输入不用 `InputType.Number`。
- 按月份等关联键建模。
- 底部弹窗不因路由约束改成路由页。
- 校验失败用全局提示。
- 路由页内容原点与顶部 inset。
- 自绘图表共用坐标原点。
- 资源变体按字段映射。
- cryptoFramework 加密移植。
- 首启无已选项的状态。
- 加载页可见时长。
- `@drawable` 引用取值。
- 多组列表的数据源绑定。

**只留在卡里、未提炼的：** 单侧 margin、矢量转 SVG、记一笔字号等具体视觉数值、天气卡片尺寸，以及 OPT-008 之后被用户撤销的启动页可达性细节。

## 待复查

- issue-5bd2 在检查器支持 fork 派工后，可原样 re-pack `draft-5.yaml`。
- pending 中的跨会话兼容改动未单独核实效应。
- 计算器振动在真机上始终被系统触感设置拦截，实际效果没有确认。
