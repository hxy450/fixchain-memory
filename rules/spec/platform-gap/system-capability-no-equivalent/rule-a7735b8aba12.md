# 规格写「目标平台无对等 API」前要有平台侧正向证据，本地参考查不到只记未查证

审的是：规格
触发（任一种）：
- 读到：源端调用系统能力（ShortcutManager.requestPinShortcut 固定桌面快捷方式、android.app.shortcuts 静态快捷方式、PROCESS_TEXT 文本入口等），本地技能参考里 grep 不到对应条目；写错的样子：规格或台账写「无 1:1 等价」「无三方应用公开 API」「无系统注册机制 → 裁剪」，依据栏填的是本地参考文件里没有条目，没有 SDK 声明或官方文档的命中，并据此标 HARD-DIV 或 PD 裁剪
适用范围：规格提取和决策台账阶段，判定源端依赖的系统能力在目标平台有没有对等能力时
做法：
- 写「无对等能力」之前给出平台侧正向证据：SDK 声明文件、官方文档或技能库里实际命中的条目，并写明出处
- 只有本地参考 grep 无命中时记为「未查证」，不升级成 HARD-DIV 裁剪。例：固定桌面快捷方式查 hms 的 productViewManager，静态快捷方式查 module.json5 的 metadata ohos.ability.shortcuts
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- productViewManager.checkPinShortcutPermitted / requestNewPinShortcut（@since 5.0.2(14)）：三方应用申请固定桌面快捷方式的接口，「无三方 pin API」不成立（出处：鸿蒙 SDK 的 hms/ets/api/@hms.core.appgalleryservice.productViewManager.d.ts，productViewManager.requestNewPinShortcut）
- 静态快捷方式由 abilities 的 metadata 指定：name 用 ohos.ability.shortcuts，resource 指向 profile 配置：静态快捷方式在目标端有承载位置（出处：module-configuration-file.md，shortcuts标签）
来源：1 张卡，1 个应用
- case-7f8dcb2d9341693d1225（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
