# 05 PolyPal：session → memory

- 会话包：`C:\Users\hongy\projects\_sessions\_server-download-20260927\downloads\bf0e04fda20dd245\export.tar.gz`（a2h-export-polypal-app-ohos，sha256 216db78e…；run e016be61，host Claude Code 2.1.175，模型 deepseek-v4-pro；hmigbot-lite-1.6.0，runtime v1.4.8）
- 材料：`materials\`，原样解包，21 份转录的 sha256 与导出 manifest 全部一致
- 流程：migloop-session-to-memory 0.8.3（triage、build-cards、maintain 同版本），解释器 `py -3.13`
- 共享库：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\store`，沿用 04 轮 HEAD `37d28648…`，snapshot 后续写，没有新建库

## 范围

- **工程形态**：Flutter + Android 原生混编应用迁鸿蒙，走“路线 C 真混合”：鸿蒙宿主经 flutter_boost 承载 Flutter 页面，原生 Screen 转 ArkTS。涉及四个工程：源 polypal-app-android、源 polypal-app-flutter、目标 polypal-app-ohos，以及 Flutter 鸿蒙适配副本 polypal-app-flutter-ohos。
- **会话构成**：5 个主会话，加上 main-76ad9618 派出的 15 个子代理（1 个 android-analyzer，14 个 migration-worker）。
  - main-76ad9618（09-21 08:30–09-22 09:04）：用户逐步推进阶段 4 native，09-22 派子代理走 spec→plan→execute，之后接 SDK 和插件。
  - main-c83bb2f9（09-22 09:07–09-23 02:19）：先做 forward-ref 接线，再按用户要求迁移启动链路，之后进入用户实机调试。
  - main-fd773e2c、main-15fb7702：两次 /a2h-run 启动。
  - main-5e4fa5da（09-23 02:37–09-24 02:03）：续跑阶段 5 verify 和阶段 6 复盘，之后继续用户调试。
- **用户调试**：用户本人在模拟器上测试，贴 hilog 和抓包，逐项指出问题，涉及网络、登录凭证、首页交互、日志、id 精度等。这些修改按修复纳入，不要求 verify 标签。
- **生成结束 2026-09-22T09:58:32.418Z**：取启动链路迁移最后一次应用写入（main-c83bb2f9 L721）之后的第一道编译门派发（L725），与前几轮“全部生成写入后的第一道编译门”口径一致。用户首次实机反馈在 10:04:12（L751）。
- **观察截止 2026-09-24T02:03:48.614Z**：材料中最后一条带时间戳的记录。最后一次应用写入在 09-23 10:52:28（main-5e4fa5da L2076）。

## 问题清单（`repair-tasks.yaml`，16 项）

| # | 问题 | 最终卡 |
|---|---|---|
| 1 | 网络层没有在启动时初始化 | `cards/issue-8555b02fdd531952938b/case-1.json` |
| 2 | baseUrl 与 path 直接拼接缺分隔符 | `cards/issue-fef2528dd5d4c3b040e6/case-1.json` |
| 3 | 服务地址与环境按猜测填写，两套接口共用一个 baseUrl | `cards/issue-b000698af8cbbc664b87/case-1.json` |
| 4 | 游客登录请求体缺 device_id | `cards/issue-2c1f292dab668274366a/case-1.json` |
| 5 | 公共请求头未按源端拦截器补齐 | `cards/issue-69bfbfee5841bf8c60cf/case-1.json` |
| 6 | 游客登录失败时静默留页，缺失败提示 | `cards/issue-dac1fda1c66cbfa8bc78/case-1.json` |
| 7 | 应用身份元数据停在模板值 | **阻塞**，只有 `draft-3.yaml` |
| 8 | token/refreshToken 应取自响应头 | `cards/issue-31852e28af4327a408a3/case-1.json` |
| 9 | token 失效判定码错误，缺启动刷新 | `cards/issue-7478183bbcfea10865d1/case-1.json` |
| 10 | refreshToken 请求沿用全套公共头 | **无卡（新要求）**，只有 `draft-1.yaml` |
| 11 | pp_home 首页 native↔Flutter 事件通信未迁移 | `cards/issue-b98aad1336d85a238cd7/case-1.json` |
| 12 | Flutter release 日志没经通道转给原生 | `cards/issue-1a0896800abf7e6439f2/case-1.json` |
| 13 | 退出重进后 token 丢失 | `cards/issue-f93cb4842b050b7fb269/case-2.json`（case-1 为同内容前一版） |
| 14 | 欢迎页“跳过”游客登录成功后不进主页 | `cards/issue-9618601c4a21f2f18560/case-1.json` |
| 15 | 启动时已登录但 token 为空仍进主页 | `cards/issue-4e49d2c90fedc95d8f71/case-1.json`（新要求卡） |
| 16 | 64 位整数 id 用 number 承载丢精度 | `cards/issue-c179cd94000a4fea75a5/case-2.json`（case-1 为同内容前一版） |

搁置项：
- **产物**：迁移报告、验证/复盘文档、进度存档与宿主记忆，以及排查用的诊断日志代码。
- **测试支撑**：三个 bigint 精度探针，在同一条命令里写入并删除。
- **流水线工具**：Dart 改动同步到宿主 har 的开发期自动化（sync_flutter.sh、hvigor 插件、hvigorfile 接入），以及误改源 Flutter 工程 pubspec 后在转录外被恢复。
- **未实施**：
  - 用户要求复刻 ToNativeEventKeys，两次都因 API 499 失败。
  - verify 报告的 7 个通道空壳方法、12 个原生 UI 待迁。
  - pp_home 中目标页未迁的事件只留了 TODO。
  - config.json 的 flutter 字段待用户决定。
  - 其他三处持久化 JSON 的 bigint 处理只做了风险提示。

## 制卡结果

16 个 job 各派一个独立子代理，同时最多 6 个，结果：

- **14 张 `status: valid`**，其中 1 张是新要求卡。
- **1 项确认无卡**：属于新要求。
- **1 项阻塞**：检查器接不了遗漏型偏差。

Claude Code 原生 Write/Edit 的写边由检查器自动绑定。需要 force 的只有 Bash cat/sed/python 读取，每张卡 0–3 条。逐卡的偏差定位与备注见 `dispatch-log.md`。

- **没有卡的两项**：
  - **refreshToken 精简头**：源 Android 与 Flutter 的刷新请求都走同一套公共头，用户给的头集合（含 iOS 取值 `Platform-Type '0'`）是修复期新要求。生成期没有偏差起点，调查员只留调查稿，没有硬标问题节点。
  - **应用身份**：归因已核清，编排主会话读到 Stage 0 要派应用身份任务，仍把整个 Stage 0 延后、再降为可选。但生成期没有任何会话写过 AppScope，“偏差者 → 目标”的写边找不到真实调用，pack 三次都退回；调查员没有强连，也没有借修复者搭桥。
- **新要求卡**：问题 15 的启动兜底源端没有，检查器要求每张图有问题节点，调查员把节点标在源端启动判定上，并在 reason 写明它只表示“这条要求不在任何写前输入里”。归并时只引用它对源端行为的诊断和“后续流程要接通”这条建议，没有当作生成者的错。
- **检查器限制**：共两次遇到子代理用 task-notification 回报父会话的交接边不被接受（问题 1、问题 9）。有关环节写进了卡的 summary，没入图。

## 经验库变化

`37d28648…`（04 轮，35 卡 47 条）→ ingest `03e9abf9…`（+14 卡）→ apply `5e618bd2…`（`proposals/plan-1.yaml`）。发布版 `5e618bd27dfea12b3c00b532b67fc7c4f6b671d1a469715a715b80d34897848e`：49 卡，62 条 active，31 个主题目录。完整序列见 `revisions.json`。

**新增 15 条**，新开主题 data/network、app/hybrid、app/startup：

- **跨卡归并的 4 条**：
  1. **process/input-loading**（5 卡：device_id、凭证来源、失效码、服务地址、首页 Model）：派工要求按源码确认的字段类型、请求体、凭证来源、码值、地址，即使规格看似完整、或指定数据源查不到，也要回源码核对；没读到就标未核实。另含“按类名 grep 源 .kt，不只读同名 kapt stub”。
  2. **process/spec-handoff**（4 卡：公共头、凭证来源、失效码、服务地址）：规格需要的值在上游清单或数据源里取不到时，回源码补全或标“待核”，不用端点计数、枚举举例或自拟值收口。四处都出自同一个规格作者：它确认 api-inventory.json 未生成后，仍把网络层标为“已就绪”。
  3. **app/entry**（2 卡：网络初始化、偏好存储初始化）：源端靠 DI 或全局静态工具就绪的基础设施，改成需显式 init 的封装后，在入口 onCreate 最早处调用，并确认启动期读写都晚于初始化；未初始化时报错，不静默返回默认值。
  4. **ui/feedback**（2 卡：失败提示、跳过后跳主页）：迁移源端异步结果回调时，按成功、失败分支列出全部副作用，计划与代码逐项对上。
- **app/startup**（2 卡：启动刷新、启动兜底）：迁移启动链路时打开闪屏各去向页的初始化入口，列出冷启动请求与登录态组合的处理位置。
- **其余 10 条各由一张卡支撑**：
  - data/network 6 条：URL 分隔符、服务地址与环境、拦截器公共头、凭证取自响应头、失效码按拦截器分支迁移、不透明请求体追到构造处。
  - app/hybrid 3 条：MethodChannel 方法集合双向对照、宿主页打开实际挂载的容器子类迁移事件通道、pushNativeRoute 按 pageName 建映射。
  - data/model 1 条：Long 映射 bigint，解析、序列化与持久化保精度。

**修订 4 条（补证并扩展）**：

- `lesson-5754b7be…` 编排者推进前兑现承接项（v1→v2）：新增“子任务回报 completed 时核对约定产物已落盘、回报完整；回报提到需要调用的入口时 grep 调用点”，以及“派发接线时附页面规格的导航关系”。现由两个应用支撑。
- `lesson-4f81eeea…` 移交登记（v2→v3）：新增“UI 转换留业务占位时 TODO 写全源端成功与失败动作”“新建的 init 需要入口调用而不能改入口时，列出文件、生命周期方法与调用语句，不写无前向引用”。现由三个应用支撑。
- `lesson-eb4de4fd…` 前向占位按触发文本兑现（v1→v2）：接线者只接上登录调用就删了 TODO，与 04 轮“只接一半、删标记”同一机制；新增“只接调用、没处理结果分支时保留标记”。
- `lesson-e9c6e8ef…` 沿用已有写法前核对源码（v2→v3）：范围扩到“为新接口方法复用已有解析函数”。写者读到源端新登录方法从响应头取凭证，仍复用按响应体解析的函数。现由三个应用支撑。

**只留在卡里、没写进经验的**：

- PolyPal 的具体域名、错误码数值（2012/2013/2082/5006 只在经验里作为来源例子出现）、页面与事件名、P-S*/F00x 编号、历史 agent 与行号。
- 新要求卡里“产品要求启动拦截时如何加分支”的具体写法。
- 偏好存储改用 UIAbilityContext 的修复理由：材料中没有平台依据，卡里明确不认定为 token 丢失的已证原因，经验只取初始化时机这一层。

## 交付物

- 阅读入口：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\runs\05-polypal\memory\index.md`（revision `5e618bd2…`，62 条，31 个主题目录）
- 其他：
  - `repair-tasks.yaml`
  - `metadata.json`（附 `server-metadata.json`）
  - `dispatch/`
  - `cards/`（各稿、回执、调查稿）
  - `proposals/plan-1.src.yaml` 与展开后的 `plan-1.yaml`
  - `dispatch-log.md`
  - `revisions.json`

## 用时与 token

- 墙钟：2026-09-27 09:58–11:00（-04:00），约 62 分钟。
  - 解包、拆分、建索引：约 16 分钟。
  - 16 个调查员：10:14 首批派出，最后一个 10:49 完成。
  - 归并、导出、写报告：约 11 分钟。
- 子代理 token（完成通知）：16 个合计 4,193,576，单个 184,458–339,252；累计用时 11,345 s，单个 353–1272 s。
- 编排主代理的 token 用量本地拿不到，未计入。

## 未完成与待复查

- **没进库的两项**：应用身份（阻塞）和 refreshToken 精简头（新要求）。
  - 应用身份这张卡若能通过，会给 04 轮的 app/identity 两条经验（`55f44e2e…` 编排者漏掉身份落地、`fb996956…` vendor 保留规则与验证门冲突）各补一个应用的证据。
  - 这需要检查器支持“遗漏型偏差”（偏差者读到要求、从未写目标）的归因形式，由维护者决定。
- **检查器缺口**：子代理 → 父会话的 task-notification 回报边不被接受，本轮两张卡（网络初始化、失效码）的上游环节只能写在 summary 里。
- **单应用支撑**：15 条新经验都只来自 PolyPal，同一个切片实现者（a51cc）、Base 层实现者（a4e09788）和规格作者（main-76ad9618）各自贡献了多张卡，同批卡不算独立验证。
  - 平台事实均取自卡里核过的源码或 SDK 用法：bigint 字面量与 JSON.parse 精度来自会话里的临时编译实测，其余没另做设备实测。
- **未决目标**（均在卡内写明原因）：
  - logger.dart 的注释来源：Flutter 适配副本在材料之外创建。
  - LoginViewModel 返回值调整：生成期实现不算偏差。
  - bigint 链路上 10 个同机制目标没单独入图。
- **材料缺口**：
  - 09-21 08:30 之前的阶段 0–3 与 Flutter 适配会话不在包内。
  - 用户在转录外直接改过 Flutter 副本的 Dart 代码。
  - 多数修复在截止前没有看到用户复测结论，尤其是 token 持久化与 bigint 链路。
- **修复本身待确认**：
  - refreshToken 精简头落地的 `Platform-Type '0'` 是 iOS 取值，与修复期早先定下的鸿蒙 `'1'` 不一致，用户当时说“value你自己替换”。
  - bigint 全局正则会波及所有 16 位以上的整数与纯数字字符串，请求把 bigint 以字符串发出，后端是否接受没有核验。
  - 修复后首页模型的 HomeCardType 枚举仍与源端不一致。
