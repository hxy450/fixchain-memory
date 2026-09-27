# 极准天气（app_hnaccurateweather_live_android）迁移：session → memory 报告

- 迁移：`dc1176d6-edc1-4b76-a9d4-31bd94c63ea0`，宿主 Codex（gpt-5.6-sol），材料 68 份转录（archive sha256 `6d6f5ecf…8500`）
- 状态：**completed**。30 个问题全部产出通过 pack 的正式卡，已归并进共享库
- 共享库：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\store`
  - 修订：`faedea8b…` → ingest `88512019…` → apply **`738957e22fbfb31e88dbbe0703f0be4d51ced46428c5f6e181e817028e7b0dd0`**
  - 规模：183 张卡，182 条 active 经验
- 阅读包：`runs/f6f89fad6b0f16f2/memory/index.md`

## 1. 范围与边界（triage）

- **生成结束 `2026-08-13T13:29:02.643Z`**
  - 首个修复线程 main-019ffb4e 的第一条记录。
  - 生成期根编排会话 `019fee60…` **不在材料中**；它的子代理（spec/execute/verify/build 各阶段）齐全，最后一条记录在 11:16:37Z。
- **观察截止 `2026-08-21T09:35:59.738Z`**：材料最后一条记录；最后一次应用写入在 08-20 02:36。
- **修复分两段**
  - 08-13/15：D:\ 工程上 5 条并行主线程（天气首页、15 日、黄历、我的城市、我的）及其子代理。
  - 08-19/20：C:\Users\zm\Desktop 副本上 9 条主线程。
  - 副本关系的旁证：08-19 读到 08-13 修复新建的文件。复制过程本身无材料。
  - 生成期写入只登记在 D:\ 路径，所以 08-19 的问题同时列出 C:\ 实际路径和 D:\ 同名路径。
- **产物**
  - `repair-tasks.yaml`：30 个问题，另有 set_aside / pending / coverage。
  - `dispatch/`：30 个 job。
  - `dispatch-r2/`：只重发了 issue-9ad29d… 一项，原因见下文。
- **pending（未核实项）**
  - AccountModels.ets 两次 apply_patch 回执失败，但读回文件已含改动，材料中找不到成功写入的调用。
  - AuthViewModel 诊断探针是否有残留。
  - 08-15 至 08-19 的复制过程无材料。
- **triage 失误（已更正）**
  - issue-9ad29d…（添加城市搜索）首轮漏列了 D:\AddCityPage.ets。调查员因此无法接链，得到 needs_revision，没有强连。
  - 更正做法：同标题（同 job ID）单独重发到 `dispatch-r2/`，交回原调查员，第二轮通过。
  - `repair-tasks.yaml` 已同步修正并注明。

## 2. 逐任务最终卡

30 张正式卡都是 `status: valid`。“未决”列是卡内 `unresolved_targets` 的数量，大多是 C:\ 副本路径（归因在同名 D:\ 图中），或修复新建、没有生成期历史的文件。

| # | job | 最终卡 | 图 | 未决 | 归因要点 |
|--:|---|---|--:|--:|---|
| 1 | issue-5d12548f9d559985c27d | cards/…/case-1.json | 2 | 2 | 转换者未读 Adapter item 布局，占位区块与不透明列表遮住头图；天气组件缺城市入参 |
| 2 | issue-2cb47bb8a097227ee9cf | case-1.json | 1 | 3 | 只归因修复新生回归（删 `\|\| ''` 后读 .length）；生成期写者在缺失的根会话中，未决 |
| 3 | issue-853ca988d9a2683b1c8d | case-1.json | 4 | 0 | Gson 标量宽松、解密回退原文，均被写成严格 typeof |
| 4 | issue-951ecf2aad87b8f0fe96 | case-1.json | 1 | 1 | AES 空串分支漏迁；WeatherHttpClient 的 STRING 改动与材料矛盾，未归因 |
| 5 | issue-a4833bfb773223515dd1 | case-1.json | 1 | 0 | 按 ID 查库补经纬度这一步在 feature 拆分时丢失 |
| 6 | issue-fa7bbda457517260efc4 | case-1.json | 2 | 0 | 全失败写成有效缓存；单例取消语义错误 + 多入口无单飞；规格读取为乱码 |
| 7 | issue-e7af91622703010ed47f | case-1.json | 6 | 0 | 详情页独立接口被聚合为整页错误；首页数据没有交接到详情页；按位置赋值（修复期引入） |
| 8 | issue-1cfad6c2eaf32070939a | case-2.json | 2 | 0 | 无参 Builder 吞掉城市参数；网关直接输出原始码值 |
| 9 | issue-4dad731ff5682f738fa4 | case-1.json | 1 | 0 | 缓存优先 / 禁白屏已知而未实现 |
| 10 | issue-c9f068102d7b9057938e | case-1.json | 1 | 0 | 资产 id 是字符串，按目标类型用 number 解码 |
| 11 | issue-b59456e0156cf1b82ad6 | case-1.json | 2 | 0 | 用 2021 前 120 天的静态资产替代农历库；附属请求失败连带整个月历 |
| 12 | issue-d64f11b7100c739bb292 | case-2.json | 1 | 1 | 批量读取被截断未补读，视觉样式凭空编写 |
| 13 | issue-2906493a39c662495a11 | case-1.json | 3 | 2 | 丢天气字段与定位城市；invisible 占位与重复安全区 |
| 14 | issue-8c249997059a2524ea7b | case-1.json | 3 | 0 | 只申请 LOCATION、先查开关后授权、拒绝时静默；构建警告被忽略 |
| 15 | issue-8a889aba046e2d2f1f3e | case-1.json | 3 | 1 | 缺逆地理编码；@Builder 按值传入且不可观察 |
| 16 | issue-cf6e5b0120e30d1395dd | case-1.json | 1 | 1 | 多来源首屏挂在同一个奖励钩子上 |
| 17 | issue-46ac36102451125de693 | case-2.json | 1 | 1 | 常驻 Tab 未订阅登录事件 |
| 18 | issue-327636c44f08419021a9 | case-2.json | 1 | 1 | 路由跳板 Activity 被做成可见的方式选择页 |
| 19 | issue-f62209d059dec8e6aca4 | case-3.json | 1 | 1 | 未打开 DialogHelper，隐私弹窗写成通用单按钮 |
| 20 | issue-c89aab9f64f62b2e0de6 | case-1.json | 2 | 0 | 同意勾选动画与 700ms 延时，规格与复刻两段都漏迁 |
| 21 | issue-766f31f27e3feb426eb4 | case-1.json | 1 | 1 | 首启返回、参数私有类、shape 用 Cover 铺背景、未设对齐 |
| 22 | issue-9ad29d4616c38b46a04d | case-3.json（dispatch-r2） | 1 | 3 | 异步结果作为 @Builder 值参；PlaceDao 无证据，未归因 |
| 23 | issue-0dd25455d592a77ed652 | case-1.json | 2 | 6 | 丢 Lottie 动画层、沉浸判定错误；返修按截图改错首屏 |
| 24 | issue-4ecfc0b10264caacad49 | case-1.json | 2 | 2 | 前向钩子没有携带恢复与回写语义；定位置顶在规格中无人认领 |
| 25 | issue-55bbad53c11b2d1b95e6 | case-2.json | 2 | 0 | 均为修复期引入：Adapter 文案模板 / 黄历卡被删；叠放曲线被改成顺序排列 |
| 26 | issue-04bf2dcacf8602ede15e | case-1.json | 2 | 2 | 复活已注释的绑定、尺寸取近似值；宿主对所有 Tab 统一留白 |
| 27 | issue-9ccc879e5d89039f29f4 | case-1.json | 2 | 4 | 历法数据未接入就删了占位标记；宜忌数据绑到弃用资产 |
| 28 | issue-5b1c11815476c648a9dc | case-2.json | 1 | 5 | 按单一渠道截图删除入口（修复期）；日期格未按 item 布局实现 |
| 29 | issue-06c7df8f8d85e13580ac | case-2.json | 2 | 2 | 居中约束放进了 Row；shape 当位图；宿主统一留白 |
| 30 | issue-d827908975df4e90ae2b | case-1.json | 1 | 1 | 只查 base/media 就判资源缺失、改成占位；显隐按列表是否为空推断 |

各 job 目录还保留了首稿、多轮稿件与 pack 回执。常见需要修订的原因是 Codex 经 exec/PowerShell 读取的文件没有进入索引，按回执补 force 证据后通过。

## 3. 归并与发布（maintain）

- **规模**：42 条 upsert（新增 20、更新 22），30 张卡全部被引用，没有 retire。主题介绍更新了 14 个。
- **新增经验（20）**
  - 流程：PowerShell 5.1 读 UTF-8 中文必须带编码；沿 helper/DAO/适配器委托链追到最终实现；按 feature 切分归属时写跨 feature 契约。
  - 数据：Gson 标量宽松解码；加解密工具的前置返回与回退分支；多路聚合写缓存前先确认有成功；算法库实时计算不改绑静态资产。
  - 界面：多类型 Adapter 页按 item 布局与 handleXxx 分支建区块；RelativeLayout 无规则子项叠放；按区块做失败隔离；入参承接与宿主传参；路由跳板 Activity；按来源处理返回；Tab 宿主按 Tab 分别处理沉浸；Lottie 层；被注释的绑定不迁；视觉属性逐项取自源；资源查全部限定词目录；单例取消语义与单飞。
  - 应用：逆地理编码补行政区名。
- **更新经验（22，机制相同，补来源并补具体动作）**
  - 读取被截断、上下文压缩后重读、弹窗按实际布局、点击处理器的状态与时序、移交登记、前向占位兑现、验收以代码落点为准、访问器 / 码值映射、事件驱动重载、@Builder 值参（补异步重赋值与原位更新）、多入口共享载荷、drawable 取值（shape → borderRadius）、默认对齐、异步结果各分支、编译警告（权限）、定位权限成组、截图修复以源码为准（补渠道变体）、同名布局按源集、setVisibility 分支（补 invisible 占位与开关条件）、ConstraintLayout 父居中、运行配置注入（补 getEnvironmentVar 语义）、规格冲突（明确“决策已批准的差异按决策”）。
- **取舍**
  - job 2 的卡只描述修复期回归，因此并入已有的“构建期运行配置注入”经验，没有为它单独立生成期规则。
  - 各卡中过于领域化的建议留在卡内，不提炼为经验。例如：定位城市与收藏列表合并、图表 ±2 边界、授权路径的实机验证方法。
- **校验**：apply 后没有 needs_review，snapshot 中 182 条均为 active；export 的 `store_changed: false`。
- **阅读包**：`memory/`，44 个主题。提案与过程产物在 `merge/`：plan.yaml、new-lessons.yaml、updates.yaml、topics.yaml，以及 ingest / apply / export 的输出。

## 4. 缺口

- 生成期根编排会话 019fee60 缺失，根向子代理派工的正文为加密内容。
  - 多张卡的 `unknown` 记录了无法核实的派工要求。
  - job 2 的生成期主因无法归因。
- Codex 子会话会继承父会话历史，索引中存在同一写入的多份回放；各卡已按记录时间与 session_meta 区分真实写者。
- 08-15 至 08-19 的工程复制无材料；C:\ 副本上的片段来源依据 08-19 补丁删除行与 D:\ 历史逐字一致。
- Android 源码与截图不在材料中，只能依据转录内的读取回执。

## 5. 用时与用量

- 墙钟：2026-09-27 21:47Z 启动，约 23:12Z 交付，约 1 h 25 min。
- 子代理：31 次制卡调查（30 个 job，其中 1 个二轮），合计约 9.01 M tokens、2062 次工具调用，累计约 359 agent-minutes，最多 6 路并行。
- 编排会话自身的 token 用量无法从本会话读取。
