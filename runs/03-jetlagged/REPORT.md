# 03 JetLagged：session → memory

- 会话包：`C:\Users\hongy\projects\_sessions\_server-download-20260927\downloads\2e827f37484663c4\export.tar.gz`（run c0a9d2cc，host Claude Code 2.1.247，模型 deepseek-flash；hmigbot-plus-1.6.0，runtime v1.5.2）
- 材料：`materials\`，原样解包，97 份转录的 sha256 与导出 manifest 全部一致
- 流程：migloop-session-to-memory 0.8.3（triage、build-cards、maintain 同为 0.8.3），解释器 `py -3.13`
- 共享库：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\store`，沿用 02 轮 HEAD，snapshot 后续写，没有新建库

## 范围

这个 run 只有一个迁移主会话 `main-0527c205`（09-25 06:51–22:33 UTC，中途压缩上下文两次），外加 21 个 hmigbot 审阅会话（只读，负责回 gate）。

- **用户调试**：主会话收到的外部消息只有三类：首条 /a2h-run 指令、四轮 hmigbot 自动注入的“验证闭包仍有阻塞项”、两次经 Stop hook 送达的 gate 答复（“同意，起修复并设备复验”“同意，按选项 1 跑 UT”）。gate 答复都来自审阅会话，没有人工手打的消息，也没有用户手写的代码。gate 答复触发的修复照常纳入。
- **设备**：设备来自主会话自己。它在补验证闭包时发现本机装了 HarmonyOS 模拟器，自行拉起，跑了 85 条设备侧 UI 判定，确认了 3 条缺陷。这 3 条此前的静态门和 FV-2 编译都判了 PASS。
- **生成结束 2026-09-25T18:21:11.253Z**：取 FV-2 终态全量编译的派发时刻，口径与 01、02 两轮一致。execute 内与生成交错的编译门，其中的修改算作生成收敛。
- **观察截止 2026-09-25T22:33:10.284Z**：取主会话最后一条带时间戳的记录。

## 问题清单（`repair-tasks.yaml`）

| # | 出处 | 问题 | 最终卡 / 缺口 |
|---|---|---|---|
| 1 | verify CHECK-2 | 应用显示名停在脚手架默认值 myapplication（AppScope app_name 与 EntryAbility_label） | `cards/issue-7b64dd743c1260eb910f/case-1.json`；AppScope string.json 列为未决目标 |
| 2 | 设备侧 UI 判定 F001-AC04 | 横向 Tab 行 Scroll 写了 height('auto')，指示器用百分比覆盖层，首帧被撑到 597vp，只显示 Day/Week | `cards/issue-2018daf21990f553ec22/case-1.json` |
| 3 | 设备侧 UI 判定 F003-AC34 / F007-AC12 | 抽屉打开时按返回键直接退出应用 | `cards/issue-2b9869554cf9027174a0/case-2.json`（同目录的 case-1 是旧稿，未入库） |

生成结束后，应用代码一共被写了 16 次，都是 Edit，全部归入上面 3 个问题。另有几类只列清单、不制卡：

- **测试支撑**：UT 流水线写入的 ohosTest。
- **流水线工具**：往 `.claude/skills/a2h-verify/scripts` 补装 linter；为了让 UT 脚本能解析，改了 F003 spec 的格式；回顾阶段写的修复知识库条目。
- **报告与判定产物**。
- **未实施**：
  - UT round-0 的 5 条 RED：emoji 少 ZWJ，以及贝塞尔插值精度。两者都作为 D-GAP 待裁决。
  - F005 Lato 字体注册有潜在缺陷。
  - CHECK-2 的 WARN（versionName、默认图标）。
  - Tab 行居中偏差：修复前就存在，没改。

## 制卡结果

3 个 job 各派一个独立子代理，同时派出，**3 张全部 `status: valid`，没有阻塞**。

| job | 偏差定位 | force 边 | 未决目标 | 用时 | token |
|---|---|---|---|---|---|
| 7b64 显示名 | 编排主会话：规范把“资源迁移后由主线程调用 arkts-app-identity”划给它，计划里也列了这一步，推进阶段时漏掉；后来页面转换者点名 label 仍是脚手架值，它也没处理 | 0/4 | AppScope string.json（生成期没有任何写入，找不到可连的边） | 465 s | 243,468 |
| 2018 Tab 行 | Slice 3 实现者：源码与 render 规格都给了正确几何，它把指示器写成百分比覆盖层，又凭一条注释推断 'auto' 可用；项目陷阱表 P-22 从没读过，P-20 只在一次 grep 回执里出现，上下文压缩后丢失 | 1/4 | 无 | 506 s | 275,205 |
| 2b98 返回键 | page_0002 转换者：已从 SDK 注释核到“onBackPress 只对 @Entry 生效”，也起草了移交，落盘时又删掉，只留文件头说明；编排者、接线切片和复核都没接住 | 1/9 | 无 | 644 s | 364,766 |

这次是 CC 转录，读写都进了索引。17 条边里只有 2 条需要 force，都是 Bash 读取没被登记为确定读取。02 轮的 Codex 转录每条边都得 force，这次不用。

## 经验库变化

`ad8baab3…`（02 轮，12 卡 16 条）→ ingest `38991ddc…`（+3 卡）→ apply `c8107293…`（`proposals/plan-1.yaml`）。发布版 `c8107293f1ebae2e905acbb887553bc20b8820328662ff5fc048db15687f2910`：15 卡，22 条 active，18 个主题目录。完整序列见 `revisions.json`。

**新增 6 条**：

1. **app/identity**：落地应用显示名时两处都改：AppScope 的 app_name，以及入口 Ability label 引用的字符串。先从 label 解析出 $string 键，值取 Android 的 android:label。（卡 1 diagnosis、rec2）
2. **process/task-handoff（跨卡）**：编排者推进阶段或派发下游前，要兑现两类事项：规范划给主线程的步骤，以及子任务点名给别人的 open_questions。后者要写进对应切片的派工，或者登记为阻断。（卡 1 diagnosis、rec1、rec4；卡 3 diagnosis、rec3）
3. **process/task-handoff（跨卡）**：功能要靠其他文件或任务补调用点才能生效时，登记成带负责方和验证方式的移交项。断言难写就改用切片级断言，但不能删掉移交。接线者读到上游的转发要求时，要么实现，要么上报。（卡 3 diagnosis、rec2、rec3；卡 1 rec3）
4. **ui/navigation**：@Entry 页直接组合的子组件要拦截返回键时，由 @Entry 页的 onBackPress 转调子组件经 @Event 注册的裁决函数；没有注册时返回 false。（卡 3 diagnosis、rec1）
5. **ui/layout**：横向滚动容器给交叉轴写数值高度，由内容算出，不写 'auto' 也不留空。（卡 2 diagnosis、rec1）
6. **ui/layout**：贴合内容的描边或选中背景画在内容节点自身，两态都保留描边，未选中用透明色；不在内容定尺寸的父级里放 width/height('100%') 覆盖层。（卡 2 diagnosis、rec2）

**修订 1 条（补证并扩展）**：`lesson-42df1ac4d4030421da34`“必读 skill 要读全”从 v1 升到 v2。

- 02 轮的 4 张卡讲的都是批量 cat 被截断、只读前 N 行。这次的卡 2 是同一机制的另一种形态：已加载的 skill 要求先读迁移陷阱表，worker 没读，或者只在 grep 里碰到过，上下文压缩后又丢了。
- 标题、适用情境和原因都相应扩展，新增一条做法：“skill 要求先读的参考同样必读；上下文压缩后，写到相关决策前重读对应小节”。现在由 5 张卡、4 个写码 agent 支撑，跨两个 app、两种宿主（Codex 与 CC）。

**与已有经验的关系**：

- 新的返回键经验和 02 轮的“多屏清理归属外层生命周期”在同一主题下，都要求先确认挂载形态。但一个是资源清理时机，一个是返回键回调，机制不同，分成两条。
- 01 轮留下的待查项是跨卡经验“规格与源码冲突时按源端”换 app 后是否仍有支持。这次仍然没有新支持：卡 2 的输入是对的；卡 3 的 spec 写法不精确，但转换者写前已自行核实 SDK，偏差不属于“照规格写”。
- 02 轮有 2 个 App 身份任务因 Codex 相对路径被阻塞，没有卡。这次第 1 条补上了显示名这一支，bundleName/vendor/图标仍然没有经验。本轮的 bundleName/vendor 由决策记录 D-009 划为部署期范围，CHECK-2 按“不适用”处理。

**只留在卡里、没写进经验的内容**：

- 项目取值：31vp、597vp、JetLagged/myapplication、各行号。
- 派工点名 P-20/P-22 的建议：卡 2 rec4，只对这个工程的陷阱表编号有意义。
- 历史 agent 与切片编号。

## 交付物

- 阅读入口：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\runs\03-jetlagged\memory\index.md`（revision `c8107293…`，22 条经验，18 个主题目录）
- 其他文件：`repair-tasks.yaml`、`metadata.json`（附 `server-metadata.json`）、`dispatch/`、`cards/`（各稿、回执、查询文件）、`proposals/plan-1.yaml`、`dispatch-log.md`、`revisions.json`

## 用时与 token

- 墙钟：2026-09-27 07:40–08:10（-04:00），约 30 分钟。
  - 解包、拆分与建索引：约 12 分钟。
  - 3 个调查员：07:52 派出，最后一个约 08:03 完成，约 11 分钟。
  - 归并与导出：约 5 分钟。
- 子代理 token（取自完成通知）：3 个合计 883,439，单个 243,468–364,766，用时 465–644 s。
- 编排主代理的 token 用量本地拿不到，未计入。

## 未完成与待复查

- **卡 1 的 AppScope string.json 没有画图**：生成期没有任何调用写过它，现值是转录开始前就存在的脚手架原值。成因写在卡片正文里，与 entry 那一侧相同。
- **两条平台行为只有单次设备实测支撑**（HarmonyOS API 12 模拟器，target SDK 5.0.0(12)）：
  - Scroll 上的 `.height('auto')` 不按内容定高；
  - 被直接组合、没有入栈的 NavDestination，其 onBackPressed 不回调。

  经验里都写明了条件。前一条另有工程陷阱表 P-22 佐证，后一条没有官方文档佐证。换 SDK 版本后如有相反证据，应修订第 4、5 条。
- **卡 2 的 unknown**：P-20 那句话在写码时已经不在上下文里。经验按“写前曾收到、写入时不在上下文”表述，没有断言生成者明知违规。
- **未实施的缺陷**（UT 5 条 RED、F005 字体注册、CHECK-2 WARN、Tab 行居中）截至观察截止都没有修改，所以没有卡。之后如果有修复会话，可以再并入。
- **session-role**：本 run 的 session-role 事实只区分 worker 和 reviewer。reviewer 的 gate 答复按自动化处理，没有当作人工输入。
