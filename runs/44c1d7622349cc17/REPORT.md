# 免费来电多多 · 迁移会话到经验库

- 迁移：`34f1eb1d-61e3-4b07-b51c-a3ef5890fad8`（app_rings_harmony，Android → HarmonyOS，Claude Code 主流程 + 两个 Codex 会话）
- 材料：`materials/`（run a2f2578c，20 个主会话 + 201 个子代理转录，archive sha256 8e46be8d…）
- 共享库：`../../store`，基线 `5e618bd2…`（49 卡 / 62 经验）→ 本轮发布 **`1cc15ae5aba4ac38633bc7aa9c3c718b044f5fdf93ebf962de5f36768ac6e334`**（93 卡 / 99 经验，全部 active）
- 阅读包入口：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\runs\44c1d7622349cc17\memory\index.md`
- 交付状态：**partial**。47 个 job 中 44 个产出有效卡并已归并。其余 3 个（#31、#32、#44）已调查完毕，确认无生成期偏差，不制卡，列入 `completion.json` 的 `unresolved_jobs`。它们不是阻塞项，但没有可交付卡，所以不按 completed 交付（续跑时依调度反馈更正）。

## 1. 范围与清单

- 生成结束 `2026-09-20T10:51:00Z`：主会话 7bcbff75 L4598 执行 `mark-stage a2h-verify`（export stage-marks 同值）；verify 期 CHECK-1~10 的修复算生成收敛，只作为追溯背景。
- 观察截止 `2026-09-23T02:54:21Z`：第二次 a2h-retrospect mark-stage（65cc0d15 L164）。最后一次应用写入是 87179513 L453（02:42），此后只有日报与文档。
- 修复分布在 8 个会话（ee33673a、01a0c1d8(Codex)、7e6e56d7、c434fed7、5a5b6f69、79350f0b、87179513、674660cb），均由用户在真机联调中逐条报告。
- 清单 `repair-tasks.yaml` 共 **47 个问题**。盘点方式：
  - 扫描截止期内全部 Write/Edit/MultiEdit/apply_patch，以及带写入特征的 shell 调用。
  - 补入 7e6e56d7 中 4 次用 Python 脚本直接改应用文件的调用。
  - 8 次失败的 Edit 均无写入，不列入。
- 搁置项（set_aside）：
  - 规格与报告记录、回顾文档、日报（含一份写到其他工程目录的日报）、Codex 完备度表：已搁置。
  - 宿主自动 memory、hmigbot skill 参考、构建辅助 bat 与清缓存：已搁置。
  - buildMode 环境切换：已搁置。
  - 未实施的项（搜索返回行为、账号数据差异、设置页 QQ、全仓 margin 清扫提议）：记为 unrepaired。
- pending 只有一项：09-22 对 WindowModel.ets 的挖孔改动是否已完全回退。多名调查员逐次重放 Edit 后确认：已完全回退，只保留 09-21 的 bottomRect 修复。

## 2. 制卡结果（47 个 job → 44 张有效卡，3 个不制卡）

- 调度：共享索引准备一次，之后每个 job 由独立子代理处理，最多 6 个并行。
- 所有有效卡都以 `cards/<job>/case-1.json` 为最终卡，pack 返回 `status: valid`。
- 首稿未通过的 job 保留了多份稿件（draft-1、draft-2…）。

| # | 问题（简） | 结果 / 未决目标 |
|---|---|---|
| 1 | 分类接口少解析一层 data | 卡 |
| 2 | 主页多出 MiniBar | 卡（源头为照抄模板示例行） |
| 3 | V2 页面用 CustomDialogController 崩溃 | 卡 |
| 4 | 登录态昵称兜底 | 卡 |
| 5 | 短信登录后停在启动页 | 卡；MainPage.ets 未决（首轮修复加入的刷新事件） |
| 6 | 彩铃播放页视频层与标题锚点 | 卡（返回键边距、按钮高度只写入 summary/unknown） |
| 7 | 导航指示条读 topRect | 卡 |
| 8 | 设置壁纸页透传 showRightView | 卡 |
| 9 | SaveButton 透明底方角 | 卡（取消声音半模态属新要求 U-6） |
| 10 | 预载路径未转 file:// | 卡 |
| 11 | 来电秀保存链授权窗口与遮罩 | 卡（偏差在修复中引入）；string.json、color.json 未决（新要求附带改动） |
| 12 | 乐观更新被放进成功回调 | 卡 |
| 13 | 19 位 id 精度丢失 | 卡；CallPreviewViewModel.ets 未决（只加了诊断日志） |
| 14 | 直设入口未调服务、loading 不收口 | 卡 |
| 15 | mkdirSync 对已存在目录抛 13900015 | 卡 |
| 16 | Swiper 初始定位被丢弃 | 卡 |
| 17 | 跳转前漏交接 setPlaylist | 卡 |
| 18 | 单页 ViewPager2 写成 Swiper | 卡 |
| 19 | centerInside 图标满盒拉伸 | 卡 |
| 20 | playPause 谓词未读定义 | 卡 |
| 21 | 分页缺门闩与刷新互斥 | 卡；SearchPage.ets 未决（输入交付未核） |
| 22 | 搜索历史区居中 | 卡（条目边距属新要求） |
| 23 | tab 点击不切页 | 卡 |
| 24 | 百分比宽 + margin 右溢（7 个文件） | 卡 |
| 25 | Grid 通栏广告位留空格 | 卡；SearchPage.ets 未决（预防性修改）。卡中注明修复者的“layoutOptions 求值”解释与 dump 不符 |
| 26 | 顶层全高内容层吞点击 | 卡；PlayMusicPage.ets 未决（加固性修改） |
| 27 | 下载链漏写导出步骤 | 卡 |
| 28 | 降级后沿用“设置成功” | 卡（去播放图标属新要求） |
| 29 | 本地音频走相册媒体库 + READ_AUDIO | 卡；module.json5 未决（注释掉权限声明的操作在材料中无记录） |
| 30 | 毫秒当秒 | 卡 |
| 31 | 收听数 0 隐藏 | **不制卡**：生成期忠实复刻 Android，这是联调期新要求（U-12）。见 `cards/issue-d75c1357f986e49b45a7/no-card.yaml` |
| 32 | 挖孔装饰遮挡标题 | **不制卡**：设备厂商的装饰环超出系统避让区，生成期无偏差；WindowModel 净改动为零。见 `cards/issue-0e56c1aa68578c8d532a/no-card.yaml` |
| 33 | 入口卡不等宽不等高 | 卡（宽度偏差在生成期；高度偏差在 verify 期修复） |
| 34 | Column 默认居中 | 卡 |
| 35 | 百分比高 + 纵向 margin 顶穿 | 卡 |
| 36 | ConstraintLayout 锚点转 Column 流 | 卡 |
| 37 | sheet 内弹窗层级与底部避让 | 卡；SetTimerSheet.ets 未决（辅助性 onClick） |
| 38 | 弹窗未按源布局实现 | 卡 |
| 39 | 定时文案显示裸秒数 | 卡 |
| 40 | ForEach 键缺 count、信息条宽度 | 卡 |
| 41 | style 圆角 8dp 被写成胶囊 | 卡（其中一处是 09-22 返修时引入） |
| 42 | 歌单卡与图标尺寸 | 卡（117dp 方卡来自实机截图，不归因生成） |
| 43 | 客服 QQ 改为接口获取 | 卡（归因的是专用弹窗被写成通用弹窗）；ContactApi.ets 未决（新要求） |
| 44 | 隐藏付费条目 | **不制卡**：生成期忠实复刻源布局，这是联调期产品要求（U-14）。见 `cards/issue-89ff80526b75c38723d9/outcome.yaml` |
| 45 | 密码弹窗无法输入 | 卡 |
| 46 | 开关确认写成 sheet | 卡 |
| 47 | 隐私弹窗勾选初值 | 卡（500ms 属新要求；“初始选中”是生成偏差：自定义 View 不读取 android:checked） |

## 3. 归并与发布

- 版本链：
  - ingest 44 张卡：`5e618bd2… → 3f9ae5e6…`
  - apply：`proposals/plan-1.yaml` 使版本变为 `3f9ae5e6… → 1cc15ae5…`
  - export：生成 `memory/`
  - 未退役任何经验；没有 candidate/disputed。
- **新增 37 条经验**。新主题有：
  - `ui/dialog`、`ui/interaction`、`ui/pager`、`ui/list`、`ui/safearea`
  - `app/media`、`data/files`

  其余经验并入已有的 layout、state、navigation、feedback、graphics、input、theme、data/parsing、data/model、process 主题。多张卡机制相同的，合为一条经验、并列来源：
  - 百分比宽/高、layoutWeight 与 margin：4 卡（24/35/33/42）
  - 默认对齐：34/22
  - 图标固有尺寸：19/42
  - 谓词与 getter 的定义：20/39
  - 底部避让：7/37
  - 命中测试与遮罩：26/11
  - 按源布局还原弹窗：38/43/46
- **更新 4 条已有经验**，保留原 ID、补充来源：
  - `lesson-c066489…`（大整数 id）：扩展到“源端用 String 承接数值 token”这一分支。源端为 Long 时的 bigint 做法不变。
  - `lesson-2e636699…`（ForEach 键）：扩展到重新拉取后整表 setList 的情形。
  - `lesson-e9c6e8ef…`（沿用已生成写法前核对源码）：补入 4 个来源：V2 弹窗先例、图标范式、SaveButton 范式、“同款页面”接受授权风险。
  - `lesson-7a065e8f…`（规格或派工与源码冲突时按源实现）：补入 2 个来源：按派工建了源端没有的槽位，按规格写了单页 Swiper。
- 只留在卡片、未提炼成经验的内容：
  - 项目专属数值（117dp 方卡、36vp 边距、各图标具体 dp 等）与接口字段名；
  - 新要求部分（U-6/U-7/U-12/U-14/U-15、客服 QQ 接口）；
  - 设备厂商挖孔装饰环的 4vp 余量；
  - 验证期派修措辞等一次性流程建议。
- 回顾报告里写的“max(TYPE_SYSTEM, TYPE_CUTOUT) 可修复挖孔遮挡”，与修复者本人的真机实测矛盾，**未**作为经验采纳。

## 4. 缺口与说明

- 各 observation 中的根因取自修复者自述，triage 未独立复核，归因由各卡给出。
- 截图未查看；部分修复只有编译通过的记录，真机复验结论不在材料中。
- shell 写入按命令特征识别。未命中这些特征的脚本改写可能遗漏。调查员发现两处在材料里找不到写入调用的改动，已在卡中写入 unknown：SearchPage 的 margin 被改成 LengthMetrics 写法（job 22/24），以及 module.json5 中 READ_AUDIO 被注释掉（job 29）。
- 未决目标与“新要求”判断，见上表与各卡 `unresolved_targets`/`unknown`。

## 5. 用时与 token

- 开始 2026-09-27T15:23:53Z（launch），发布与导出完成约 17:06Z，**约 1 小时 45 分**。
  - triage 约 45 分钟；47 个制卡子代理在 6 个并行槽内约 45 分钟完成；归并与发布约 15 分钟。
- 制卡子代理 token 合计 **8,695,876**（47 个，来自任务回执的 subagent_tokens）。
- 首轮 CLI 回执（`result-1.json`）给出整场会话合计（含子代理），数据如下：
  - token：input 4,090；output 1,821,922（其中 thinking 772,339）；cache read 285,330,354；cache creation 8,941,347。
  - 累计 API 时长 24,270,990 ms（并行累加）；按标价计费 140.49 USD。
- 续跑只修正了交付状态（completed → partial）并补充本节，没有重新调查、入库或发布。
