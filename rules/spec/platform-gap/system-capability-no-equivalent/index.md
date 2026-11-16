# 决策台账里对系统能力写的「平台无对等」和降级条目

agent 会看到什么：读到源端依赖系统级能力（如 dynamicLightColorScheme 壁纸取色），常带 Build.VERSION.SDK_INT 门槛和回退分支；决策台账写「HarmonyOS 无 X API 对等」或降级成固定配色，没有 d.ts 检索结果和能力探测

## 规矩

- rule-792013e7b2db｜决策台账写「平台无对等」前先检索 SDK 声明，把命中接口和弃用、权限标注写进平台约束｜读到：源端功能依赖系统级能力（如 dynamicLightColorScheme / dynamicDarkColorScheme 壁纸取色），模板要求 HARD-DIV 的依据是 SDK d.ts 注释并禁止凭记忆；写错：决策台账的 HARD-DIV / 降级条目写「平台约束：HarmonyOS 无 X API 对等（无 d.ts 能力条款）」，没有检索词、没有命中的 d.ts，自批 approved
- rule-c1a6ad0220e7｜源码带版本门槛和回退分支的系统能力，规格映射成「能力探测 + 原回退」，不直接降级｜读到：源码 if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S && 开关) 用动态配色，否则回退固定 light / dark scheme；设置行 enabled = SDK_INT >= S；写错：规格或台账写成「固定双配色」二值解析，验收条目要求「产物不含取色 API 调用与版本门槛分支」，设置行恒可用但无效果
- rule-4e9396993090｜规格判定平台没有对等能力前先查 SDK 声明；elapsedRealtime 对应 getUptime(STARTUP)｜读到：源端用 `SystemClock.elapsedRealtime()` 计算后台偏移；写错：规格把它映射为墙钟（Date.now()），并写「平台未开放跨休眠单调时钟」一类边界，没有引 SDK 声明作依据；或写成运行期验证项「若平台提供」
- rule-8a4c6e384853｜写「目标平台无对等 / 不迁移」前先在 SDK 声明里按能力名检索，结果写进决策证据｜读到：源端用 PictureInPictureParams、setAutoEnterEnabled、onUserLeaveHint、onPictureInPictureModeChanged 这类系统窗口能力；写错：页面规格、feature-base 或决策台账写「HarmonyOS 无等价 API / 不迁移（恒 false）」，没有检索证据，也没标 [待验证]
- rule-5324c43bcd6b｜规格写「无对等」「已查证」时要附查证记录，查不到就登记待定交决策关口｜读到：上游的功能基线把这项能力列为待决策关口收口的不确定项；写错：平台差异决策的依据栏写「…查证」「无对等」，却没写查了哪个 SDK 声明、哪份知识参考、工程里哪处现有 startAbility / ohos.want.action.viewData 用法及结果；或决策关口收口后同类外跳的裁决不一致（一处保留浏览器外跳、一处删掉）
- rule-a7735b8aba12｜规格写「目标平台无对等 API」前要有平台侧正向证据，本地参考查不到只记未查证｜读到：源端调用系统能力（ShortcutManager.requestPinShortcut 固定桌面快捷方式、android.app.shortcuts 静态快捷方式、PROCESS_TEXT 文本入口等），本地技能参考里 grep 不到对应条目；写错：规格或台账写「无 1:1 等价」「无三方应用公开 API」「无系统注册机制 → 裁剪」，依据栏填的是本地参考文件里没有条目，没有 SDK 声明或官方文档的命中，并据此标 HARD-DIV 或 PD 裁剪
- rule-f262d1c3f179｜源码笔记写「SDK 无某枚举成员」前按成员名搜或读完整枚举体，和规格 AC 冲突时复查｜读到：规格 AC 要求映射到某个 SDK 成员（如音源 CAMCORDER、编码 HEVC）；写错：source-notes 写「AudioSourceType 无 CAMCORDER/UNPROCESSED」「无 HEVC 录制枚举」这类缺失结论，和 AC 冲突却没有按成员名复查的记录
