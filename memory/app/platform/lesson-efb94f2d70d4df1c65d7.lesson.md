# 决策已批准等价实现的平台能力要真实现，只在运行期按实际结果降级；判定“平台没有”前先查本地 SDK 声明，确需替代就显式登记

ID：`lesson-efb94f2d70d4df1c65d7` · 版本：5

[本主题](index.md)

## 何时使用

实现平台服务（后台任务、进度通知、通知授权、画中画回退、动态取色等）或解决指向平台切片的前向占位，而决策账本对该能力批准的是等价实现、可验证承载或应用内回退时

## 适用情境

源端依赖系统后台 Worker、带动作的进度通知、通知权限、画中画、Material You 动态取色等平台能力；决策账本已为这些能力批准“等价平台抽象”“可验证的平台承载”或“应用内回退”方案，而不是延期；接手者可能认定“没有对应 API”，或把“禁止伪造进度”理解为可以不实现。

## 例外与边界

- 决策账本对该能力明确批准的是延期或仅前台实现

## 原因

把“禁止伪造”读成可以不实现，会写出恒 false、两支相同的桩，报告仍标已接线；把“一时没找到 API”当成结论，会私自降级（如把动态取色降成颜色模式切换，而 @ohos.wallpaper 声明有 getColors 与 on('colorChange')），或用通用通知槽替代具名渠道却不声明。

## 做法

1. 实现前读决策账本该条目选定的方案及所属规格与切片计划；“禁止伪造”只约束失败时如实上报，不等于可以不实现。
2. 服务层写出能力检测、权限请求、长时任务与通知动作，失败时返回可观察的原因（例：backgroundTaskManager 长时任务、WantAgent 进度通知与动作、Preferences 持久化计时状态）。具体能力的写法见各能力经验（动态取色、画中画等）。
3. 判定平台无对等能力前，在本地 SDK 的 d.ts（openharmony/ets/api、hms/ets/kits 等）里按能力关键词查，不跳过标 @deprecated 的接口（例：@ohos.wallpaper.d.ts 的 getColors/on('colorChange') 自 API 9 标 deprecated，本机 HarmonyOS 6.1.0(23) 公开 SDK 里没有替代接口），采用时配不可用时的回落；查证与记录方法见 lesson-9c973e50aaea054facdc。确需替代时把“源端能力 → 目标实现”写成显式映射（如源渠道 id、名称、重要度 → 目标槽类型与级别），登记到迁移报告或决策账本，不在实现里默默降级。
4. 自检：对本次实现的函数 grep 恒定返回和“? X : X”，再与账本里 approved 的实现类决策逐条对照。
5. 依赖厂商 SDK 与 Key 的能力（地图、登录等）按 lesson-e9890889e591196c3d0d 接入：Key 缺失只让运行期返回不可用，不以不可用适配器或静态图片充当实现。

来源支持：6 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-470d704a6ec794b4c3c9](../../../store/cases/case-470d704a6ec794b4c3c9/e7b22c984628feae31f593f0a2b3ecb03c60fc956620aa16dc545800bc3c3def.json) · 结论：recommendation:3
  卡片版本：`e7b22c984628feae31f593f0a2b3ecb03c60fc956620aa16dc545800bc3c3def`
- [case-ac823e7436e1b08612ba](../../../store/cases/case-ac823e7436e1b08612ba/001e12d63eb0e435e0b1844db82cdbae78fc17a4ab6d1e93e6e523d3d5f4f174.json) · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`001e12d63eb0e435e0b1844db82cdbae78fc17a4ab6d1e93e6e523d3d5f4f174`
- [case-d24a32433de0efe7a6a0](../../../store/cases/case-d24a32433de0efe7a6a0/2206bc2201ee16bf2198465b77cc6ce7b3b6fd4008992a7d06c0a056cd70b8f4.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`2206bc2201ee16bf2198465b77cc6ce7b3b6fd4008992a7d06c0a056cd70b8f4`
- [case-e92bb15630afd5b03216](../../../store/cases/case-e92bb15630afd5b03216/3c459a0f7e7078bb6d188d0b884628fc5b13cc3d830f20b2470474135d084b9c.json) · 结论：recommendation:1
  卡片版本：`3c459a0f7e7078bb6d188d0b884628fc5b13cc3d830f20b2470474135d084b9c`
- [case-f93a2f80bafd58105489](../../../store/cases/case-f93a2f80bafd58105489/a31992dda441d418d620d2db720885c2895c03be5e9882cfbc1d05e0a6baee6d.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`a31992dda441d418d620d2db720885c2895c03be5e9882cfbc1d05e0a6baee6d`
- [case-fa0174cd489361d7586d](../../../store/cases/case-fa0174cd489361d7586d/63fcc49dc5b8874f4ec05a58223d719edb8d9772407305f713df4a84ec09fa84.json) · 结论：recommendation:1
  卡片版本：`63fcc49dc5b8874f4ec05a58223d719edb8d9772407305f713df4a84ec09fa84`
