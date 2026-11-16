# 代码调用带 @permission 的接口时，module.json5 的 requestPermissions 要声明

审的是：资源
触发（任一种）：
- 写错的样子：代码里调 pasteboard.getSystemPasteboard().getData()，module.json5 的 requestPermissions 却没有 ohos.permission.READ_PASTEBOARD（只按别的 d.ts 补了 ohos.permission.NFC_TAG）
适用范围：编写或审 module.json5 的 requestPermissions 时，对照代码里实际用到的系统接口
做法：
- 按代码里用到的每个系统接口在 d.ts 里的 @permission，在 requestPermissions 里逐个声明，如 { "name": "ohos.permission.READ_PASTEBOARD", "reason": "$string:…", "usedScene": { "abilities": […], "when": "inuse" } }；user_grant 权限的 reason 和 usedScene 必填
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getData(): Promise<PasteData> 标注 @permission ohos.permission.READ_PASTEBOARD：读剪贴板要声明的权限（出处：鸿蒙 SDK 的 ets/api/@ohos.pasteboard.d.ts，SystemPasteboard.getData）
- 申请 user_grant / manual_settings 权限时 reason 必填、usedScene 必填，when 只能是 inuse 或 always：requestPermissions 每项的必填字段（出处：declare-permissions.md，在配置文件中声明权限）
针对本应用要查的：
- 代码里用到哪些带权限的接口：目标工程 .ets 文件里对 @ohos.* / @kit.* 模块方法的调用，逐个到鸿蒙 SDK 对应 .d.ts 按方法名找注释里的 @permission；把查到的权限名和对应 UIAbility 写进 requestPermissions
未核实：卡里的环境是 HarmonyOS SDK 6.1.1(24)，@permission 按本机 API 23 的声明核实
来源：1 张卡，1 个应用
- case-cc22f6cc1041c8cc1129（MifareClassicTool）：做法第 1 步 ← 建议 5、诊断
