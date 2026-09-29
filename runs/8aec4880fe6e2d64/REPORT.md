# app-photo-shop-flutter（P图美修）session → memory 报告

- 迁移：`0e07f2d2-6280-4809-af70-213e306fcbd6`，Codex 主会话 `019fd645…` + 12 份流水线内子代理/分叉转录（材料池 `materials/`，archive sha256 `905f5ad5…`）
- skill：migloop 0.10.0（首轮以 0.8.3 完成 triage 与 dispatch，续跑时以 0.10.0 重建索引，全部正式卡按 0.10.0 重新 pack 为 `migloop-case/4`）
- 共享库：`store/`，入库前 `a919e7b8…`（211 卡/207 经验）→ 发布 **`e092c7052313a5834c950acdcd6b114b6d18f11cd2aec8c1729dedaa1cb41fb7`**（216 卡/211 经验，全部 active）
- 阅读包：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\runs\8aec4880fe6e2d64\memory\index.md`

## 范围与清单

`repair-tasks.yaml`：生成结束 `2026-08-06T15:11:16.002Z`（a2h-run-zh 流水线回合结束，回顾被中断且无写入），观察截止 `2026-08-21T09:54:24.209Z`（材料末尾；最后一次应用写入 18:24:21Z）。用户在生成结束后报告了 4 轮问题，拆成 5 个任务（动漫化“一直生成中”含两个独立阻断，分成两个任务）。

| job | 问题 | 最终卡 | 未决目标 |
|---|---|---|---|
| issue-96b417fb2e059d43f8bf | OHOS 图库导入不可用（选图链依赖受限媒体库权限） | `cards/issue-96b417fb2e059d43f8bf/case-6.json` | 7：兼容包两文件为修复期新建；module.json5/三份 string.json 净变化为零；PhotoAssetHandler 仅有早于输入的整包复制 |
| issue-d166fd60d66832c204bc | 动漫化选 12MP 大图后 BUSSINESS_THREAD_BLOCK_6S 闪退 | `cards/issue-d166fd60d66832c204bc/case-2.json` | 1：FlutterImageCompressOhosPlugin 为能力扩展，无生成偏差 |
| issue-075213be62b42126e39f | aliyun_oss_plugin 被判 F5 阻断，上传 Future 悬挂 | `cards/issue-075213be62b42126e39f/case-3.json` | 9：本地插件文件均为修复期新建，成因同根 pubspec 图 |
| issue-3cc99a6c512ab85ed874 | 结果下载在 OHOS 请求 Permission.storage 被拒 | `cards/issue-3cc99a6c512ab85ed874/case-5.json` | 0 |
| issue-64090e208edc24d57300 | 修复把 AssetEntity 宽高写成 0，文字/涂鸦 NaN | `cards/issue-64090e208edc24d57300/case-3.json` | 1：插件 pubspec 仅为配套依赖 |

五张卡均为 pack `status: valid` 的 `migloop-case/4`，已全部 ingest。job 5 的调查在首轮完成（旧格式 `case-2.json`），续跑时由编排者按原顺序重放其 draft-1/draft-2 得到 `case-3.json`，稿件内容未改；其余四个 job 在首轮因额度中断，续跑时派新的独立调查员复用旧查询与稿件完成。

缺口：材料池外有写者在 2026-08-06T16:36Z–16:38Z 改了 12 个冻结 Dart 文件并写入 `runtime-defect-fixes.patch`（首屏白屏、保存卡死、页面卡顿三项修复），本导出中没有对应转录，只登记为 pending，未拆成任务。另有两项材料限制：spawn_agent 派工正文是加密的；PowerShell 读取回执中的中文乱码。

## 归并取舍（e092c705）

- 新增主题 `app/hybrid/plugins`，新增 3 条经验：
  - `lesson-45739c78f9767dacbc81`：插件没有现成 OHOS 包时，先按底层能力评估本地兼容插件；判阻断要写明缺失能力，Dart 冻结下的失败也要由插件回调。来源：OSS 卡。
  - `lesson-4b7012d4bdceef5e8c36`：标记插件可用前，追到实际执行的原生实现，核对它请求的权限与返回状态。来源：图库卡与下载权限卡，两者机制相同，合为一条。
  - `lesson-e85bdb26fa6acc0cc9f7`：兼容层交给冻结业务的对象，要按全部消费方保留元数据，并按下游上限在原生侧缩放。来源：闪退卡与 NaN 卡，都是兼容层对象契约问题，合为一条，用两个 how 分支。
- `app/media` 新增 `lesson-ad1db0aa0434c2e766fd`：选图导入用 PhotoViewPicker 并复制进缓存。原生应用也能独立用上这条；它和已有的音频 picker 经验条件不同，所以没有合并。
- 更新 `lesson-6a3a7f46c8fec282affa`（PowerShell 5.1 UTF-8 读取，v2）：补上下载权限卡揭示的新动作，即乱码会把代码行“并入注释”，需按 UTF-8 或 analyzer 行号核对。原有条件与来源保留。
- 未新增的内容：
  - 平台能力降级（`lesson-efb94f2d…`）和厂商 SDK 选型（`lesson-e9890889…`）与 OSS 卡的症状相近，但触发条件不同（平台服务/厂商 SDK，而非 Dart 冻结下的 Flutter 插件选层），保留为独立分支。
  - 项目值（1920、12MP、9568289 等）留在卡中；只把 9568289 作为观察环境事实写进 why。
  - 本轮无退役条目，也没有需要复查的条目。

## 用时与 token

- 第 1 次：2026-09-27T23:14:35Z–约 23:35Z，约 21 分钟。完成 triage、dispatch、索引和 job 5，其余调查员因 429 会话额度中断。主会话用量：output 279,603（thinking 139,469）、cache read 46.0M、cache creation 1.51M，列价约 $23.30。job 5 调查员 196,580 tokens；中断的四个调查员用量不可得。
- 第 2、3 次：23:35Z 启动即遇 429 额度限制，无工作。
- 第 4 次（本次续跑）：2026-09-29T16:09:07Z–约 16:31Z，约 22 分钟。完成 job 5 重放、四个续做调查、ingest、apply、export。四个调查员合计 915,115 tokens（135,974 / 213,836 / 242,501 / 322,804）。本次主会话用量需等运行结束由调度器记录。
