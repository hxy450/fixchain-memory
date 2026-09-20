# Jetsnack915 经验库 v1 — 归并说明与审核记录（2026-09-19）

- 输入：`C:/Users/hongy/projects/_migloop-jetnack915-cards-20260918/results.json` 指定的 15 张最终封装卡（每 job 最后一稿 case-N.json，revision 以卡内 hash 为准；未改任何来源卡、内核、skill）。
- 流程（按 migloop-memory-maintain SKILL.md）：`init` → `ingest` 15 卡（`f950cd34…`）→ recall search/browse 对比（新库为空，记录在 logs/04）→ 写提案 `proposals/plan-1.yaml`（由 `proposals/build_plan_1.py` 从卡内读 id/claim/revision 绑定证据，正文为维护者撰写）→ `apply`（`7e883fd5…`）→ recall/impact 复查（logs/08、09）。
- 结果：27 条经验，24 active / 3 candidate / 0 disputed；23 个主题节点。目录与全文见 `CATALOG.md`；提案原件保留在 `proposals/`。

## 审核口径

每条经验按 skill 核对四项：when 是否落在卡片指认的偏差阶段；description 是否只用卡片写前输入里可见的特征；why 是否由卡 diagnosis 支持且未超出卡已核范围；how/check 是否直接来自卡 recommendation 并可执行。满足四项且卡未把该机制列为「未核」的标 **active**；机制或方案在卡 unknown 里被明确标为未验证的标 **candidate**（下节）。所有卡的 `semantic_verified=false`、`causal_correctness=not_certified`，active 只表示维护者按卡内证据审核通过，不是对归因的独立认证；这一限制写在 CATALOG 头部。

## 归并理由

### 合并（多卡 → 一条）

| 经验 | 合并的来源 | 理由 |
|---|---|---|
| `lesson-6803500d…` Scaffold 无 topBar 时 innerPadding.top 是状态栏 inset | Profile 卡 + FilterScreen 浮层卡（diagnosis + rec1/2） | 同阶段（规格提取）、同机制（把 `padding(padding).consumeWindowInsets` 误读成只消费底栏）、同动作（按 modifier 传递链逐边写 inset 来源、同区域各层同口径）；两卡互相在 unknown 里指认对方同根。合并保留两个 problem 节点的证据。 |
| `lesson-90838f5b…` 下发 statusBarHeight 不得写「本页不使用」 | Profile rec3 + FilterScreen rec3 | 同为派工/实现阶段的接线动作，机制相同（参数已接线无人消费 / 浮层没拿到偏移）。与上一条分阶段拆开而非并成一条。 |
| `lesson-d036e54e…` 无 dump 合成快照须标 confidence | 返回钮卡 rec2 + 幽灵 Reset 卡 rec2 | 两卡偏差起点都是主会话在 meta.json 自述无真机 dump 的条件下把源码字面写成判据/决策；动作一致（标 confidence、交 verify 用真机量值、不写进决策台账）。 |
| `lesson-5ebfd81b…` 核 d.ts 读 doc 行不只 grep 签名 | 阴影 rec1 + 行高 rec1 + 混合 rec4 + 描边 rec2 | 四卡 diagnosis 都记录了「只核签名」这一共同动作缺口（px 单位行被过滤 / 只核 lineHeight 签名存在 / 只读一句 blendMode 文档 / 只核 BorderOptions 类型）。跨主题的流程经验，单独立 `process/sdk-reading`。 |
| `lesson-841ee37c…` 结构收敛不等于行为核验 | AC67 卡 rec3 + 混合卡 rec5 | 同为收敛/收尾阶段：风险 AC 写进 impl_claims、forward-ref 占位凭「已由 G1 定型」删除，机制同为「无证据清除风险」。 |
| `lesson-1cdbc30d…` 亚阈关页不得放过 | 行距卡 rec4 + 浮层卡 rec4 + 底栏卡 rec4 | 三卡都记录了 ≥0.95 关页规则把「上轮预测不符」「同根已修」「px 总宽铺不满」推迟到 round-3 的事实；同阶段（判读）同动作。 |

### 按阶段分支（同卡 → 多条）

skill 要求「不把所有阶段笼统归成迁移时」，以下卡的 recommendation 跨规格/实现两个阶段，拆成可分别召回的条目：

- 行高卡 → `c67467ba`（规格：同名 API 不等价）+ `89f5064b`（实现：modifier 与容器定高）。
- 返回钮卡 → `7e0d06d6`（规格：修饰符字面 vs 实绘 48）+ `2ae981b8`（实现：按 48 圆心不变并上报）+ 参与 `d036e54e`。
- 省略粒度卡 → `0ebabb99`（规格：不写「等价」）+ `0464ce51`（实现：measureTextSize 方案，candidate）。
- 底栏卡 → `ab7d9425`（规格：标注运算域）+ `86a32ca7`（实现：px/vp 往返）。
- AC67 卡 → `0b0c476c`（规格：列框架恢复的 UI 状态）+ `034ff7e3`（实现：onFocus 判别来源）+ 参与 `841ee37c`。
- 幽灵 Reset 卡 → `017824fd`（规格：Row 度量推演）+ `78a8a4c0`（实现/修复：Visibility.Hidden，candidate）+ 参与 `d036e54e`。
- Qty 字形色卡 → `7c3d6874`（修复：SRC_IN 预混，candidate）+ `7f46ee3c`（判读：像素均值立单）。
- 阴影卡 → `2b6f4b26`（配方单位与一条通路）+ `61a5ff18`（收敛派工对账）+ 参与 `5ebfd81b`。

### 未合并、保留分支的相近条目

- `80154b8a`（规格：blendMode 不能映射成兄弟节点离屏混合）与 `7c3d6874`（修复：SRC_IN 取形须预混）同主题 `ui/render/blend`，但阶段、机制、动作都不同（前者是 OFFSCREEN 混合目标不含兄弟内容，后者是 SRC_IN 丢掉 Plus 加数）；两卡自己也把「生成期缺陷」与「修复中新生偏差」分开。保留两条。
- `c67467ba`/`89f5064b`（lineHeight 撑高单行）与 `0e10b578`（修复期 lineSpacing 合成假设）同源文件，但后者是修复中新生偏差，动作是修复流程纪律；保留在 `process/repair`。
- `7e0d06d6`/`2ae981b8`（M3 IconButton 48）与 `f648d0ae`（M3 TopAppBar 单侧 inset）同在 `ui/layout/material-defaults`：都属「库组件隐含布局」，但机制不同（最小触控尺寸 vs 单侧留白）、来源卡不同，未并成一条。

### 未提炼的内容

- Qty 字形色卡的 `unresolved_targets`（JetsnackElevation.ets 只新增工具函数）与各卡 needs_path 的机械缺口：属证据/检查器状态，不构成可复用动作，留在卡内。
- 各卡 unknown 里「spec 作者是否知道 X」「thinking 已脱敏」类判断：无可执行建议，不提炼。

## candidate 条目与保留的来源未决信息

| 经验 | 保留的未决点（来自卡 unknown） | 转 active 需要 |
|---|---|---|
| `lesson-0464ce51…` 字符级末行截断的 measureTextSize 方案 | 省略卡 unknown：未试验 `ellipsisMode(END)` / `wordBreak(BREAK_ALL)` 是否真达不到字符级末行；「会破坏前四行按词换行」是判定者推断。已写入 unless。 | 一次 BREAK_ALL / ellipsisMode 对照试验；若属性可达则本条降为备选方案。 |
| `lesson-78a8a4c0…` 「近乎不可见」元素用 Visibility.Hidden 保槽位 | Reset 卡 unknown：Android 侧 resetEnabled=true 态是否同样不渲染，基线只覆盖默认态，两态推演来自修复者；修复有意偏离工单的条件显示。已写入 unless。 | 补 Android enabled 态基线截图/dump；确认后决定 how 是否需改为条件显示。 |
| `lesson-7c3d6874…` SRC_IN 取形须按 Plus 预混 | 字形色卡 unknown：round-4 Cart 仍余 G 通道 ≈10–12 级、渐变偏 Shadow3 端 Δt≈0.1，是生成期渐变 Column 尺寸/相位遗留还是预混引入未核；round-4 两 judge 容差不同。写入 why。 | Cart 单 §6 下轮假设（渐变 Column 尺寸/相位与 GradientBorder 对齐）实施并复验后，补充或修正 how。 |

## active 条目中随卡带入的未决信息（已写进 why/unless，不影响动作）

- `21bb8a81`（@BuilderParam）：ArkUI 官方对「箭头函数体内实例化自定义组件」的明文规则未在转录核到，规则以崩溃 + 修复实证为准；W2a 为何唯独此处漏抽无思考记录。
- `80154b8a`（blend 映射）：SDK「blended with the existing content on the canvas … below」能否推出「不含兄弟内容」在写前不可得，属外部材料边界；深色 DARKEN 分支未截图核验。
- `0e10b578`（修复期行距）：「ArkUI 多行行距 = fontSize + lineSpacing」只由 round-3 三页 dump（Karla/Montserrat 16fp）反推，无官方文档；其他字号/字体/API 22 minLineHeight 路径未核。
- `034ff7e3`（onFocus 判别）：「clearFocus 改在 isActiveTab 翻回 true 时执行是否足以压掉焦点恢复」未做对照实验；本条只收录已验证的 touch-down 判别方案。
- `6803500d`/`90838f5b`（安全区）：HomePage 派工「宿主 padding 并传 0」与 F001-AC44「子页自理」冲突无裁决记录；经验按最终保留状态（子页自理）写，未把 HomePage converter 列为偏差。
- `2b6f4b26`（阴影配方）：Feed chip 侧向/顶部扩散约 Android 一半的残差是常量未校完还是 ArkUI 单模糊 vs hwui spot+ambient 固有差异未判；SnackbarHost 改动无回放场景未核。
- `f648d0ae`（M3 单侧 inset）：生成者是否明知末端无 inset 未核；spec 对横向留白沉默被卡记为留白而非错误。
- `7e0d06d6`（IconButton 48）：未逐字核 a2h-spec page-spec 模板是否含 Material 隐式尺寸规则。
- `d3a4b709`（border 计入测量）：映射作者 thinking 脱敏，是否知道 ArkUI 语义不可判；「尺寸落点」差异（Compose size 在 Surface、ArkUI 在内容子项）未追。
- `0ebabb99`（省略「等价」）：android-ui-graph-query 映射参考是否以覆盖渲染语义为目标未追。
- `0b0c476c`（remember 翻译）：偏差边界定在规格输出，卡明确不认定作者在输入充分下失职（平台知识材料缺口）。

## 待审核项（给下一位维护者）

1. 三条 candidate 的转正条件见上表；转正走正常提案（同 id、status: active）。
2. `5ebfd81b`（SDK 阅读）与 `1cdbc30d`（亚阈关页）是跨卡归纳的流程经验，why 引用了四张/三张卡的 diagnosis 事实；若任一来源卡被撤回或修订，`impact` 会把它们置 needs_review（已验证 `impact --id case-75329cae60986f74dc43` 返回 `2b6f4b26`、`5ebfd81b`、`61a5ff18`）。
3. `requires` 全部为空：本批经验之间没有结论级依赖（如 px 往返实现并不依赖 spec 标注运算域这条成立）。若后续认为「实现阶段经验以规格阶段经验为前提」，可在提案里补 requires，但注意 active 条目不能依赖非 active 条目。
4. 主题树按本批内容建立（`ui/{render,text,layout,component,input}` + `process/{spec-confidence,sdk-reading,convergence,verify,repair}`）；`ui/layout/compose-measure` 与 `ui/layout/material-defaults` 边界（源码度量推演 vs 库组件隐含值）在下一批卡进来时复核。
5. 所有卡的 semantic_verified=false；若后续对任一卡做了语义认证或撤回，按 skill 用 `withdraw`/重新 `ingest`，再看 `impact` 恢复受影响条目。

## 目录内文件

- `store/`：经验库（HEAD.json、snapshots/、cases/），只能经 memory.py 读写。
- `proposals/build_plan_1.py`、`proposals/plan-1.yaml`：v1 提案与生成脚本。
- `logs/01-init.json`、`02-ingest.json`、`03-snapshot-after-ingest.json`、`04-recall-before-proposal.txt`、`05-apply-plan-1.json`、`06-browse-all.json`、`07-snapshot-full-after-plan-1.json`、`08-recall-checks.txt`、`09-impact-shadow-case.json`、`lessons-after-plan-1.json`。
- `CATALOG.md`：主题目录、经验表、来源卡映射、全文。
