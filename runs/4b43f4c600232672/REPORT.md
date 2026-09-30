# 记得日历：session → memory 交付报告

## 结论

- 任务类型：`session`，入口 skill `migloop-session-to-memory`（0.10.0），新增正式卡为 `migloop-case/4`。
- 问题清单：`repair-tasks.yaml`，共 47 个修复问题。生成结束为 2026-08-11T06:08:24.647Z，观察截止为 2026-08-19T07:18:47.009Z。set_aside 包括测试支撑、文档产物和流水线工具，另有 4 项截止前未修改应用代码（unrepaired）；`pending: []`。
- 制卡结果：41 个 job 交付了 pack 返回 `status: valid` 的最终卡。6 个 job 因材料缺口无卡（blocked），偏差代码都来自材料起点（2026-08-03）之前的首轮迁移，材料内找不到偏差写入者。
- 状态：`partial`。本轮已收尾，没有仍在调查或待派发的 job，41 张有效卡都已入库并绑定到 lesson。
- 最终经验库 revision：`55dc232a76750a11173a39edf69c5a835a2d57e5a5ce113738fb42362b6ff8eb`（257 cases / 243 active lessons / 51 topics）。
- 阅读包入口：`C:/Users/hongy/projects/_migloop-multiapp-memory-20260927/runs/4b43f4c600232672/memory/index.md`

## 过程

1. triage：按 triage skill 生成 `metadata.json`、`dispatch/`（47 个 job）和 `repair-tasks.yaml`，共享 inquiry 索引只准备一次，放在 `work/inquiry-cache/…/index.sqlite`。
2. 制卡：每个 job 派一个独立的 general-purpose 子代理（Opus 5.5），同时最多 6 个，完成一个补派一个。首稿到末稿都留在 `cards/<job>/`，最终卡与 `handoff.json` 也在其中。
3. 归并分两次，原因如下：
   - 第一次（batch-1）：规则调整前做过一次中间归并，导入 14 张卡。snapshot `e092c705…` → ingest `1dc009bd…` → apply `2bade92d…`，新增 12 条 lesson，更新 3 条。导出到 `memory-batch1/`，这个包只是历史快照，不作交付。
   - 规则改为“全部收尾后统一归并”后，没有再边制卡边发布。
   - 最终一次（全部 47 个 job 收尾后）：snapshot 确认库仍在 `2bade92d…`，ingest 其余 27 张卡得到 `e2519799…`，按 `work/plan-2.yaml` apply 得到 `55dc232a…`，export 到全新的 `memory/`。
   - batch-1 已入库的卡和 lesson 没有重复导入或新建。其中两条 batch-1 lesson（`lesson-368c4592e4c7075c1871`、`lesson-4ad956bab5fca6d7f418`）按同机制补了新来源。

## 最终归并取舍（plan-2）

**条件与机制相同，沿用原 ID 补来源（13 条）。** 只在新卡带来新条件或新动作时扩写正文：

- 真弹窗形态：`368c`，补底部弹窗 → 半模态。
- 占位只登记真缺值：`a2f6`，补“契约未确认”兜底。
- Stack 全尺寸层参与命中：`4a4f`，补一次性动效层。
- ForEach/Repeat 键：`2e63`，补稳定键须配可观察实例。
- @Builder 值参快照：`8d29`，补 Repeat 按值传 `ri.item`。
- 视觉修复以源为准：`8119`，补容器尺寸与 Canvas 绘制尺寸同源。
- Stack 子项 `.align`：`92ae`，补 FrameLayout 角标。
- 沿用既有写法前核源：`e9c6`，只补来源。
- 入参由宿主真实传入：`289c`，补撤回传参。
- 设置项消费方：`4d0f`，补设置保存副作用与切换即持久化。
- 接收端参数契约：`4a7c`，补不新增消费。
- 异步结果分支：`ac7a`，补按失败类型分派。
- 完成态派生与写入：`4ad9`，补按审查意见修写入键。

**机制或适用条件不同，新建 20 条：**

- `lesson-150e48577e599f64ee23` ui/list：批量改 Repeat.virtualScroll 时核对项高度与数据切换
- `lesson-eb59181d6dfaeb014aef` ui/list：按源端该列表自己的排序器排序
- `lesson-22f5100f6718eaecc66f` data/model：展示型 UI 模型字段按源端 formatter 或目录转换 code/ID
- `lesson-6d3ac9a5c0382377b91e` ui/dialog：源端委托共享组件时复用目标共享组件
- `lesson-29f62d177a17d08b4e4f` ui/dialog：依附式弹窗宿主按锚点所在页确定
- `lesson-f35f4912277e0c9a1b14` ui/dialog：自绘底部弹窗改 bindSheet 时迁移手势门禁
- `lesson-fc724027e2c995632733` ui/state：拆单例或多实例 VM 时显式传递跨页面状态
- `lesson-6677d286e690407d4af4` ui/interaction：侧滑行命中修复限定在按钮热区
- `lesson-963bf871aa4e910a8fc8` ui/layout：锚点坐标在触发时取值
- `lesson-d4e63d27885d9e348723` ui/pager：自绘日历翻页用 Swiper 承载
- `lesson-85b33ff729ab0514a20a` ui/pager：相邻页数据落定后合并提交，查询范围按格子首尾
- `lesson-f395cbdf6742a7f4c761` ui/graphics：自适应公式的参照基数写成独立常量
- `lesson-7e04234bdf5aef97b651` data/network：拦截器读取的公参要有生产者
- `lesson-686bbe76f7c2c783f2bd` data/sync：同步保存后的当前选中项处理
- `lesson-99b35920e77ae01076ea` app/modules：按页面归属划分业务模块
- `lesson-e23468a0e439f8cf53e9` app/logging：按源端日志调用边界规划日志点
- `lesson-d434bb5c16bc721d9a00` app/logging：诊断日志上传的打包清单与协议
- `lesson-af15c43279110b3b7692` process/gates：已批准计划的替换清单逐行收口
- `lesson-afae8d13e00941efe808` process/gates：交互修复与受阻功能点标为未验证
- `lesson-b843621a5b9c279b1b2b` process/task-handoff：重新规划时承接已批准规格

**其他取舍：**

- 没有退役任何 lesson，也没有 candidate、disputed 或 needs_review 条目。
- 卡中只属于本项目的修法仍留在卡里，例如具体行高、控件名、ledger 编号。
- 每张新卡至少绑定 1 条 lesson；27 张卡共被 33 条 lesson 引用。

## 逐 job 最终卡或缺口

- `issue-0389a44b7fd28f48c094` 日历上滑折叠为周历的交互偏离 Android（直接切日视图、无跟手、周数变化不联动、折叠后点击穿透、状态不同步） → `cards/issue-0389a44b7fd28f48c094/case-2.json`（final merge；lesson 1 条；未决目标 4）
- `issue-182739cdd6b02b7eed15` 待办/四象限列表项 UI 与空间按钮未还原 Android（DayTodoAdapter、HomeAdapter、统一空间按钮） → `cards/issue-182739cdd6b02b7eed15/case-4.json`（final merge；lesson 1 条；未决目标 5）
- `issue-1c1dc6394c428c959798` 同步调度吞掉尾随请求、失败队列不重试、本地完成态被云端旧数据覆盖 → `cards/issue-1c1dc6394c428c959798/case-4.json`（batch-1；lesson 1 条；未决目标 1）
- `issue-24bba18989317118cb97` 网络公共参数 nsjdid、oaid 未赋值（及 androidid 改取 ADID） → `cards/issue-24bba18989317118cb97/case-2.json`（final merge；lesson 2 条；未决目标 3）
- `issue-2598c3155e3a9c1beaa3` 页面与组件堆在单文件、按 Android/类型分包，未按业务包拆分 → `cards/issue-2598c3155e3a9c1beaa3/case-6.json`（final merge；lesson 1 条；未决目标 15）
- `issue-265e1cc8347c261db79d` 事线详情页 NewActDetailActivityPage 布局与功能未闭环（复制详情副本、契约未确认占位、编辑态、关联、分享） → `cards/issue-265e1cc8347c261db79d/case-7.json`（final merge；lesson 2 条；未决目标 5）
- `issue-282d676ed02777809cac` 模块化后跨模块依赖违规：HAR 引用宿主 BuildProfile、跨模块相对路径导入 → `cards/issue-282d676ed02777809cac/case-7.json`（batch-1；lesson 1 条；未决目标 1）
- `issue-2f0ae037cbd33aafdcfd` 月历弹窗改 bindSheet 后覆盖导航页：EMBEDDED 未传 targetId 回退 OVERLAY → `cards/issue-2f0ae037cbd33aafdcfd/case-3.json`（batch-1；lesson 1 条；未决目标 0）
- `issue-32cd7964a05af40fea9a` 完成点击路由与即时状态：check 点击被 item 详情吞没、状态需切日期/点两次才更新、状态变化回闪与抖动 → `cards/issue-32cd7964a05af40fea9a/case-2.json`（final merge；lesson 1 条；未决目标 12）
- `issue-35171ce59437beebb0ea` 事线列表宿主参数与数据映射缺失（currentSpaceType 未传、空间图标未按 namespaceId 解析、置顶字段解析、btnAdd） → `cards/issue-35171ce59437beebb0ea/case-1.json`（final merge；lesson 2 条；未决目标 3）
- `issue-4a7f1aef1c804d227365` 时间线页本地数据一直显示加载中、item 布局混乱（layoutWeight 撑高、折叠图标错误） → `cards/issue-4a7f1aef1c804d227365/case-2.json`（final merge；lesson 2 条；未决目标 2）
- `issue-51d51ad98738e338df19` 完成彩纸动画缺失，及修复中出现的只见一粒、全屏 Canvas 常驻遮挡、锚点错位 → `cards/issue-51d51ad98738e338df19/case-1.json`（final merge；lesson 2 条；未决目标 3）
- `issue-58884768863f720f109c` 底部弹窗以组件嵌入页面而非真实底部 Sheet（待办设定时间、月历日程、提醒详情、详情更多菜单） → `cards/issue-58884768863f720f109c/case-6.json`（final merge；lesson 1 条；未决目标 6）
- `issue-5c348565d345d0c6b3bc` 搜索接口 /search/event 以 JSON 发送，Android 与本项目 spec 均为 form-urlencoded keyword → `cards/issue-5c348565d345d0c6b3bc/case-2.json`（batch-1；lesson 1 条；未决目标 1）
- `issue-60960b31a847ea9bb8c7` 吐司未按生成期要求统一封装，200余处直接调用 promptAction/DialogHelper/自绘 Toast → `cards/issue-60960b31a847ea9bb8c7/case-4.json`（final merge；lesson 1 条；未决目标 2）
- `issue-61576f6bb7eacb427f94` 同步状态提示触发条件偏离 Android（SyncProgressHint 非首次同步也显示、SyncErrorHint 在中间轮次闪现） → `cards/issue-61576f6bb7eacb427f94/case-3.json`（batch-1；lesson 1 条；未决目标 5）
- `issue-62417152eaa4c6a19ec1` 日历/月历横向翻页未用 Swiper 跟手分页，相邻页首次加载抖动与数据闪烁 → `cards/issue-62417152eaa4c6a19ec1/case-2.json`（final merge；lesson 2 条；未决目标 2）
- `issue-64d73b23ce87a7bad738` 未登录启动直接跳登录页且返回出现白屏，应先进入主页再按需登录 → `cards/issue-64d73b23ce87a7bad738/case-3.json`（batch-1；lesson 2 条；未决目标 0）
- `issue-677059269bdbd772e57e` 事线列表标题栏重叠、侧滑误触详情/无法右滑关闭、item 越界、缺下拉刷新 → `cards/issue-677059269bdbd772e57e/case-5.json`（final merge；lesson 1 条；未决目标 3）
- `issue-69d294e4afbc31f4ab87` 列表渲染复用导致数据不刷新或高度异常（Repeat.virtualScroll 复用旧节点、ForEach 稳定 key+非观察模型） → `cards/issue-69d294e4afbc31f4ab87/case-4.json`（final merge；lesson 3 条；未决目标 3）
- `issue-6a3dbeed71d0e9f4375f` accessibilityText 传入 ResourceStr 联合类型导致 ArkTS 编译失败（生成交付时构建未通过） → `cards/issue-6a3dbeed71d0e9f4375f/case-2.json`（batch-1；lesson 1 条；未决目标 0）
- `issue-6a6e6b7124655d1844a6` 诊断日志上传：项目 URL 校验强制 HTTPS 拒绝 http 预签名地址，归档只含当天日志且缺数据库各表 TXT → `cards/issue-6a6e6b7124655d1844a6/case-7.json`（final merge；lesson 1 条；未决目标 3）
- `issue-6c62d7c44b9a82b2388c` 退出登录：上传本地数据失败会阻断退出，退出后未清理 RDB 业务表导致首页仍显示旧用户数据 → `cards/issue-6c62d7c44b9a82b2388c/case-3.json`（batch-1；lesson 1 条；未决目标 1）
- `issue-72b2ae4850e7ef2a6ce2` 登录页进入即自动弹出协议弹窗（仅部分入口）、手机号输入框空内容光标被裁切 → `cards/issue-72b2ae4850e7ef2a6ce2/case-final.json`（final merge；lesson 1 条；未决目标 0）
- `issue-7f25b9e411fd7ea08eb8` 首页视图选择未持久化、顶部年月点击选择器缺失 → `cards/issue-7f25b9e411fd7ea08eb8/case-8.json`（final merge；lesson 3 条；未决目标 5）
- `issue-8081ee8b9265d77fd5a8` 公共下拉刷新以 this.RefreshContent 作为 @BuilderParam 传入导致事线页崩溃 → `cards/issue-8081ee8b9265d77fd5a8/case-1.json`（batch-1；lesson 1 条；未决目标 0）
- `issue-845435c8343c4c012e1f` 语音胶囊录音：权限拒绝无引导弹窗、胶囊点击区与录音浮层表现偏离 Android → `cards/issue-845435c8343c4c012e1f/case-1.json`（final merge；lesson 1 条；未决目标 4）
- `issue-84e889d80b54dca3e119` 月历 Canvas 绘制与数据偏离 RMonthView（行高自适应、跨周续行、班/休、颜色模式、查询范围）且点击日期未复用 MonthCalendarPopup → `cards/issue-84e889d80b54dca3e119/case-3.json`（final merge；lesson 1 条；未决目标 4）
- `issue-8c39ab17c6d5d6951b85` 弹窗容器设置 HitTestMode.Block 拦截子控件点击（升级弹窗立即升级、月历弹窗 checkbox/整行） → `cards/issue-8c39ab17c6d5d6951b85/case-2.json`（batch-1；lesson 1 条；未决目标 1）
- `issue-8f714106a538afa3c22a` 空间筛选状态传递与“所有空间”查询语义错误（所有空间无数据、月历切空间不刷新、切换后偶现空态） → `cards/issue-8f714106a538afa3c22a/case-5.json`（final merge；lesson 1 条；未决目标 0）
- `issue-9831097c34ea91e10955` 日程完成态判定未按 Android BoxEvent 规则（ANY_MEMBER、occurrence 日期、同步写入用户状态主键为空） → `cards/issue-9831097c34ea91e10955/case-3.json`（batch-1；lesson 1 条；未决目标 3）
- `issue-9d757be741e1835af4b4` 月历日程弹窗 MonthCalendarPopup 还原与交互偏差（logo间距、到顶下拉关闭、完成提交时机与交换动画、成员显示配置缓存） → `cards/issue-9d757be741e1835af4b4/case-2.json`（final merge；lesson 2 条；未决目标 2）
- `issue-c2923d8f21d1ab03bb58` 提醒详情 NewEventDetailDialog 展示与交互偏离 Android（提醒 code 原样显示、重复文案/结束缺失、空间图标与头像、布局、关联、eventLevel 勾选图标） → `cards/issue-c2923d8f21d1ab03bb58/case-1.json`（final merge；lesson 1 条；未决目标 6）
- `issue-c777abf40cffa3ab181d` 首页标题栏年月未居中、今按钮恒不显示、今提示放错位置且UI未对齐Android → `cards/issue-c777abf40cffa3ab181d/case-5.json`（final merge；lesson 1 条；未决目标 7）
- `issue-c9cc6663456a2ef02f89` 日程列表项 UI 未还原 Android DayEventAdapter（勾选对齐、空间标签、成员状态、子任务、订阅分组、成员按钮拉伸） → `cards/issue-c9cc6663456a2ef02f89/case-2.json`（final merge；lesson 2 条；未决目标 4）
- `issue-e0f695fdf6f76c501e28` 日志埋点未按 Android RXLog.wLog 调用位置迁移，只剩无诊断价值的日志 → `cards/issue-e0f695fdf6f76c501e28/case-9.json`（final merge；lesson 1 条；未决目标 7）
- `issue-e218dc5f282b590164d7` HAR 页面引用了其他模块的资源（Unknown resource name） → `cards/issue-e218dc5f282b590164d7/case-1.json`（batch-1；lesson 1 条；未决目标 2）
- `issue-e2c0fe92e09e74d58cb7` XPopup 锚点/居中类弹窗被实现为页面内叠层组件，点击空白无法关闭 → `cards/issue-e2c0fe92e09e74d58cb7/case-11.json`（batch-1；lesson 1 条；未决目标 7）
- `issue-e3b4733dbfbc7b73d7d4` 首页启动弹窗调度偏离 Android：升级检测仅首装触发、匿名冷启动网络未就绪、立即升级走下载而非应用市场、每日一言未按接口判定 → `cards/issue-e3b4733dbfbc7b73d7d4/case-2.json`（batch-1；lesson 1 条；未决目标 12）
- `issue-e5d42507c82fd492f62b` 四象限天/周/月切换无效、本地查询显示加载遮罩并抖动 → `cards/issue-e5d42507c82fd492f62b/case-1.json`（final merge；lesson 1 条；未决目标 2）
- `issue-ea1fc6a0711a8176b79c` 日程/待办排序未按 Android 规则（EventSortActPage 配置、订阅前后、DayTodoListSorter） → `cards/issue-ea1fc6a0711a8176b79c/case-final.json`（final merge；lesson 2 条；未决目标 3）
- `issue-09abb7cfd292c971d726` 搜索页交互偏离 Android（输入停顿即自动搜索、清空历史加确认框、部分结果误跳订阅详情） → **无卡（blocked）**：这四项偏差都是首轮迁移遗留（HMOS 仓库 07-24 初始化，材料从 08-03 开始）。生成期只有两次无关写入和一次 mv，修复期重构保持了原行为；材料内没有“正确输入→偏差输出”的可核起点，所以未 pack、未交付卡，调查事实保存在 investigation-blocked.yaml。
- `issue-92cfd3a0e0dbb9befc06` 网络层偏离用户既有选型：HTTPDNS SDK 用错包、业务请求未走 Axios、依赖版本未统一 → **无卡（blocked）**：修复确有发生，但没有生成窗口内的偏差：RCP 传输和 @aliyun/httpdns 都早于 2026-08-03（首轮迁移或用户自己的 07-24 提交），生成阶段按用户批准保留了它们；改用 Axios 2.2.13 和 @alidns/httpdns 2.0.4 是 08-14 的新要求，版本冲突来自三方元数据。未交付卡片，详见 triage.yaml。
- `issue-9d2dc06ea8043acbdc87` 我的页常用功能中小组件、每日一言图标被圆角背景裁切且尺寸与其他图标不一致 → **无卡（blocked）**：偏差代码来自材料开始前的首轮迁移，材料内找不到偏差写入者或写前输入，因此未 pack、无正式卡；已核实的分析保存在 blocked-draft.yaml。
- `issue-d245a4c5ba8b8da9ae19` 空间成员数据缺失：NameSpace 未做 topUsers↔userJson 转换，成员头像只剩当前用户 → **无卡（blocked）**：决定性缺陷（members()按严格字符串解析数字uid；NameSpace.fromJson缺topUsers转换）在材料窗口之前的首轮迁移中已存在，材料内只有搬移和一致于Android的复写，找不到有问题的生成写入，因此没有可通过的归因链；调查稿保存在draft-1.yaml，pack反馈保存在pack-1.out。
- `issue-d674e88c0d903489400f` 空间编辑创建态使用用户头像作默认空间图标（应取首个空间图标与颜色） → **无卡（blocked）**：缺陷为材料开始前首轮迁移的遗留；08-10 写者（019feb5b/019feb5c/019febae/019febed）为 UI 测试代理，既未读到 Android 创建态 BoxSpaceIcon/BoxSpaceColor.first()，也未编写头像回退，材料内无可核的“正确输入→偏差→目标”链，故不制卡。
- `issue-f053d28f70f4f49e2ba6` 节日详情页只接收 id 未发起请求导致永久加载，顶部间距与节日故事对齐偏离 → **无卡（blocked）**：Both repaired fragments (no request by id and default-centred content) already existed when the materials begin and came from the first-round migration. No in-material writer introduced or changed them. The UI test design (agent-019fdc2f L207, 2026-08-07) flagged the permanent loading as IMPL_MISSING, and the pipeline then kept it as a declared RED; the dispatch text is encrypted, so no deviating agent can be named. The investigation is kept in draft-1.yaml, and pack returned invalid_draft (no graph).

## 用时与 token

**用时。** 实际工作从 2026-09-29T16:31:23Z 开始（launch-4；09-27 的 launch-1～3 都因 api_error 在启动时失败），到 2026-09-30T06:25Z 左右交付，墙钟约 13.9 小时。其中包括两段停顿：

- 一次额度暂停（HTTP 429）。
- 一次控制器维护停机，期间把索引切换为 WAL。

**token（可取得的部分）。** 只有 result-4/5 有记录，合计：

- 输出 1,601,587
- thinking 648,447
- cache read 286,742,687
- cache creation 6,945,801
- 约 USD 127.79

launch-6 被维护中断，launch-7 是本次续跑，两者没有 result 文件，本报告无法给出其用量。本段续跑中，子代理完成回执里报告的单 job 用量约 18 万～44 万 token。

## 事件与偏离

`work/incidents.md` 记录了四件事：

1. 一位调查员曾临时移动 `/tmp/inv` 下其他运行的文件，随后按原时间戳还原。此后的派工要求临时文件只放在各自的卡目录。
2. 额度暂停中断了 5 个调查。恢复后重新派工，复用了已有草稿。
3. 维护把共享索引切换为 WAL，我删除了自己做的两份备用拷贝。batch-1 的中间归并发生在“统一归并”规则之前（见上文）。
4. 一位调查员短暂派出了 2 个辅助子代理，并发短时超过 6 个上限。此后的派工禁止再派子代理。

其他情况：

- 没有修改 skill、检查器、原工程或远端，也没有执行 git add/commit/push。
- 旧的 `dispatch/.inquiry/…/build.lock` 按要求保留，未删除。
