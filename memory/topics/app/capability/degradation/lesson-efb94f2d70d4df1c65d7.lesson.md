# 决策已批准等价实现的平台能力要真实现，只在运行期按实际结果降级；判定“平台没有”前先查本地 SDK 声明，确需替代就显式登记

ID：`lesson-efb94f2d70d4df1c65d7` · 版本：4 · 阶段：execute · 主题：[app/capability/degradation](index.md)

概要：决策批准的平台能力要真实现，只在运行期按结果降级

信号：`backgroundTaskManager.startBackgroundRunning`, `ohos.permission.KEEP_BACKGROUND_RUNNING`, `notificationManager.requestEnableNotification`, `WantAgent`, `backgroundModes`, `MapView`, `WorkManager`, `DynamicColors`

## 何时使用

实现平台服务（后台任务、进度通知、通知授权、画中画回退、动态取色、地图承载等）或解决指向平台切片的前向占位时

## 适用情境

源端依赖系统后台 Worker、带动作的进度通知、通知权限、画中画、Material You 动态取色，或用第三方地图 SDK 的 MapView 显示当前位置与轨迹；决策账本已为这些能力批准“等价平台抽象”“可验证的平台承载”或“应用内回退”方案，而不是延期。也包括规格把地图、POI 与导航列为核心功能并要求经能力适配层隔离，台账只批准了认证、广告、微信等少数能力的不可用降级，厂商 SDK 的 Key 尚未提供，计划汇总行却写“地图执行已批准不可用 UX”。

## 例外与边界

- 决策账本对该能力明确批准的是延期或仅前台实现

## 原因

把“禁止伪造进度”读成可以不实现，会写出恒 false、两支相同的桩，报告仍标已接线；把“一时没找到 API”当成结论，会私自降级。来源中接手的编排者把后台计时服务写成恒定“仅前台”、持久化恒 false、授权强制 false，违背已批准的等价实现决策；修复轮一个 worker 认定没有壁纸取色接口，把动态主题降成颜色模式切换，下一轮在本地 SDK 查到 @ohos.wallpaper 的 getColors 与 on('colorChange')；另一个 worker 用通用通知槽替代具名高重要度渠道，没有声明这项替代。另一应用里决策要求地图用“平台能力的可验证承载”，实现者读过源端地图视图、定位 marker 与缩放逻辑，仍把定位成功态写成白底加定位标记图片，并把巡检项标为已解决；规格未点名地图组件、计划没有地图接入任务，占位一直保留到用户发现页面空白。

## 做法

1. 实现前读决策账本该条目选定的方案；“禁止伪造”只约束失败时如实上报，不等于可以不实现。
2. 服务层写出能力检测、权限请求（如 notificationManager.requestEnableNotification）、长时任务（backgroundTaskManager.startBackgroundRunning，并在 module.json5 声明 ohos.permission.KEEP_BACKGROUND_RUNNING 与对应 backgroundModes）、通知动作（WantAgent），失败时返回可观察的原因。
3. 源端地图视图落成真实地图组件（平台 Map Kit 或已决策的三方地图 SDK）并绑定定位坐标；key、client_id 等配置缺失而无法接入时显示“地图服务未配置”一类真实状态并登记缺口，不以静态图片冒充地图态或把巡检项标为已解决。规格或计划阶段把这类替代写成具体任务：目标组件与依赖、配置注入方式、坐标系换算和未配置态验收。
4. 判定平台无对等能力前，在本地 SDK 的 ets/api/*.d.ts 里查（含标记 deprecated 的接口）；确需替代时把“源端能力 → 目标实现”写成显式映射，并登记到迁移报告或决策账本，不在实现里默默降级。
5. 自检：对本次实现的函数 grep 恒定返回和“? X : X”，再与账本里 approved 的实现类决策逐条对照。
6. Key 等配置缺失只让运行期返回不可用：注册真实适配器并在缺 Key 时回退，不把不可用适配器作为默认且唯一的实现；规格与汇总行矛盾时把缺口写入决策缺口或登记三方 SDK 占位，回执写明“未接入”，不报告该功能完成。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [解前向占位按触发文本逐项兑现，写常量不算闭合](../../../process/deferred-fulfillment/lesson-eb4de4fd7452308a0483.lesson.md)（共享 2 张卡）
- [应用内计时替代后台 Worker 时恢复入口共用扣减函数](lesson-35a684862ee500f08912.lesson.md)（共享 1 张卡）
- [设置开关逐项落实运行期消费方，只调 setter 不算完成](../../cross-cutting/lesson-4d0f0176b3d09c33f1eb.lesson.md)（共享 1 张卡）
- [应用内开关蓝牙先查 access 开关接口再定方案](../sdk-lookup/lesson-7a081dc36013a60358ac.lesson.md)（共享 1 张卡）
- [平台差异只收敛做不到的一步，其余出口照源保留](lesson-9c973e50aaea054facdc.lesson.md)（共享 1 张卡）

来源支持：6 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-470d704a6ec794b4c3c9](../../../../../store/cases/case-470d704a6ec794b4c3c9/e7b22c984628feae31f593f0a2b3ecb03c60fc956620aa16dc545800bc3c3def.json) · 结论：rec-92785d8b2d
  卡片版本：`e7b22c984628feae31f593f0a2b3ecb03c60fc956620aa16dc545800bc3c3def`
- [case-ac823e7436e1b08612ba](../../../../../store/cases/case-ac823e7436e1b08612ba/001e12d63eb0e435e0b1844db82cdbae78fc17a4ab6d1e93e6e523d3d5f4f174.json) · 结论：diagnosis, rec-13e3f15228, rec-772fe7ba85, rec-fd3c015fc6
  卡片版本：`001e12d63eb0e435e0b1844db82cdbae78fc17a4ab6d1e93e6e523d3d5f4f174`
- [case-d24a32433de0efe7a6a0](../../../../../store/cases/case-d24a32433de0efe7a6a0/2206bc2201ee16bf2198465b77cc6ce7b3b6fd4008992a7d06c0a056cd70b8f4.json) · 结论：diagnosis, rec-59241eb2e8, rec-76d4969ce8, rec-d37e95302e
  卡片版本：`2206bc2201ee16bf2198465b77cc6ce7b3b6fd4008992a7d06c0a056cd70b8f4`
- [case-e92bb15630afd5b03216](../../../../../store/cases/case-e92bb15630afd5b03216/3c459a0f7e7078bb6d188d0b884628fc5b13cc3d830f20b2470474135d084b9c.json) · 结论：rec-ef6e149dc6
  卡片版本：`3c459a0f7e7078bb6d188d0b884628fc5b13cc3d830f20b2470474135d084b9c`
- [case-f93a2f80bafd58105489](../../../../../store/cases/case-f93a2f80bafd58105489/a31992dda441d418d620d2db720885c2895c03be5e9882cfbc1d05e0a6baee6d.json) · 结论：diagnosis, rec-c9c8266b9b, rec-72f1481ba4, rec-77b36baf01
  卡片版本：`a31992dda441d418d620d2db720885c2895c03be5e9882cfbc1d05e0a6baee6d`
- [case-fa0174cd489361d7586d](../../../../../store/cases/case-fa0174cd489361d7586d/63fcc49dc5b8874f4ec05a58223d719edb8d9772407305f713df4a84ec09fa84.json) · 结论：rec-11c42acd8a
  卡片版本：`63fcc49dc5b8874f4ec05a58223d719edb8d9772407305f713df4a84ec09fa84`
