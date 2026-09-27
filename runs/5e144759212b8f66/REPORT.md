# 骑行记录（migration 9264617d-5373-4aca-8c7d-94c70606545c）会话 → 经验库

- 材料：`materials/`（Codex Desktop，根线程 01a08aae 分 epoch-0/epoch-1，104 份子代理转录），archive sha256 `d8b1574c…810f`
- 边界：生成结束 `2026-09-10T19:10:12.041Z`（a2h-verify PASS 后根线程 task_complete）；观察截止 `2026-09-15T09:23:49.093Z`（材料最后一条记录）
- 清单：`repair-tasks.yaml`；元数据 `metadata.json`；派工 `dispatch/`（jobs + 共享索引 `.inquiry/`）
- 经验库：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\store`，基线 `1cc15ae5…` → ingest `c092d8d1…` → 发布 **`259f95fff1235da423921d0dacad8d92c57db243ba513f360ab8d66db0ecc6c6`**（108 cases / 113 active lessons）
- 阅读包：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\runs\5e144759212b8f66\memory\index.md`；归并提案 `merge/plan-1.yaml`

## 逐任务结果（15/15 pack `status: valid`）

| job | 问题 | 最终卡 | 未决目标 |
|---|---|---|---|
| issue-ae269ba9b3d5c8def239 | 5 入口页二级页面只有 Toast/未注册路由（规格作者自拟“仅截图页”范围） | cards/…/case-3.json | BluetoothPage.ets（另一成因：路由验证按 D-008/D-011 改系统设置，派工加密） |
| issue-f663597a71756594de10 | 三说明页缺图文卡与完整文案（批量读取截断后照片段写） | case-2.json | base/en_US string.json（值来自加密消息） |
| issue-6a2ee155bd552b418d50 | 首页统计卡被 Tab 遮挡（视觉轮按跨设备截图放大源值尺寸） | case-2.json | — |
| issue-ae1e7b09c5cfe5214cd2 | 客服弹窗自拟、反馈按钮按名选 color_accent | case-2.json | —（Mine 标题 /3 顶距写者无转录，记入 unknown） |
| issue-ab54d746c8c33d3061ed | 蓝牙两个开关经共享 @Builder 值参串线 | case-1.json | BluetoothViewModel.ets（无独立生成偏差） |
| issue-3eb3514a903386524e37 | 登录态头部与联动天数页未按 Android 显隐分支/布局 | case-3.json | — |
| issue-2bb1f7385338bea7e396 | 常驻通知绑到页面级订阅 | case-3.json | AppAssembly / NotificationService / BluetoothPage（ROUND48 写入缺失或属其他改动） |
| issue-eb1a9afc22a411d84591 | 设备列表两行都显示 MAC | case-2.json | DeviceInfoModel、BluetoothPage（平台返回 MAC 未核实） |
| issue-d24a32433de0efe7a6a0 | 地图区域为白底+marker 假地图态 | case-3.json | RideMapSurface.ets（修复期新建，创建写入缺失） |
| issue-1ea05be22c68b8603ea7 | “昵称为空”被当成未登录 | case-5.json | ProfileViewModel.ets（修复写入缺失） |
| issue-6147579e732da7b69f07 | 首页固定用户栏被放进 Scroll | case-2.json | — |
| issue-c9f54856d3fb74cbd54b | 蓝牙回调参数/页面快照当开关真值、单协议断开误判 | case-1.json | — |
| issue-6077d9f3d384e0cb140f | 首页统计只在 aboutToAppear 拉取，未迁事件订阅 | case-2.json | — |
| issue-613cce143fdc193142d7 | 网络装配空配置、未实现 AES 解码 | case-2.json | — |
| issue-fa0174cd489361d7586d | 应用内蓝牙开关被写成跳转系统设置 | case-3.json | BluetoothPage.ets（修复写入缺失） |

路径均在 `cards/<job>/` 下；各目录保留全部 draft、pack 回执与 `result.json`。issue-ae269 目录中残留的 case-2.json 为调查员早期稿，未入库，以 case-3 为准。

## 归并取舍

- 更新 8 条（保留 ID，补来源并收紧条件）：读取截断（42df1ac4，扩到源布局与 yield 截断，5 张卡补证）、@Builder 值参（8d297954，开关行）、弹窗按布局还原（1f366fe4）、平台能力真实现（efb94f2d，加地图承载与 SDK 核查）、match_parent+margin（75f4743d）、访问器兜底（1fa08bf9，登录判定与显示回退分开）、异步结果分支副作用（ac7a2e17，失败保留旧值）、编排者兑现待接项（5754b7be，巡检 BLOCKER 派修失败）。
- 新增 14 条：process/scope（截图页范围取可达闭包）、ui/layout×2（Scroll 包含范围；视觉修复先折算 vp 对照源值）、ui/state×4（开关事件目标值、setVisibility 分支、事件订阅式重新加载）、ui/theme（按色值选资源键）、ui/list（新增副行后主行回退）、ui/text（说明页逐字逐卡迁移）、app/bluetooth×3（终态回读、分协议聚合、应用内开关接口）、app/platform（常驻通知应用级服务）、data/network（构建期私有配置与同算法解码器）。
- 项目具体值（QQ 号、尺寸 246/77/116、ROUND 编号、agent 名）留在卡片；未核实的平台行为（getRemoteDeviceName 返回 MAC、未授权 getState）写入 why/条件，不作为规则。

## 搁置与缺口

- 新需求（set_aside new_requirement，未制卡）：备案号、版本名 1.0.0、ContactApi 取 QQ、应用名、协议链接替换。测试用例、spec/验证产物、构建临时文件、纯问答按 test_support/artifact/pipeline_tooling 记录。说明：`new_requirement` 不在 triage skill 列举的四类中，因实际用途不符其余类别而如实另列。
- pending：F006 独立审查首轮 5 个缺口的修复、ROUND44/46–48 具体源码修改、five_page_flow_closure 截断后的其余改动——材料无调用。
- 材料缺口：根线程 epoch-1 在 `2026-09-15T01:19:10Z` 截断（后续用户请求由晚期子代理的 compacted 历史恢复）；five_page_flow_closure 在 `2026-09-11T02:37:34Z` 截断但持续工作到 09-15；bluetooth_toggle_options 仅 3 行；所有派工正文为 encrypted_content；dashboard last_activity 09:31:11Z 晚于材料。
- 环境：共享索引未解析该 Codex Desktop 格式中 `exec` 包装的读写（file catalog 为空）。编排者用临时探针 job 验证 force 边可用后删除探针，并在派工中注明该环境事实；15 张卡的读写边均以原始 JSONL 调用/FileChange/输出行 force 补证。未改动检查器或 skill。
- 清理：删除了编排者自己的转录文本摘录（其中含用户提供的地图 key 与测试账号）；卡片与报告未写入这些值。`dispatch/.inquiry/` 约 0.5 GB 索引保留以便中断复用。

## 用时与 token

- 会话 2026-09-27T17:09:15Z 起，发布与报告完成约 18:15Z（约 66 分钟）；15 个调查子代理累计约 214 分钟（最多 6 路并行）。
- 调查子代理 token 合计约 4,684,238（15 个，单个 19.7 万–46.2 万）；编排主会话 token 宿主未提供精确值。
