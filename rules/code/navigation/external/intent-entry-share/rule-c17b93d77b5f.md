# 多个 PendingIntent 按钮迁成 WantAgent 时，每个按钮每次构建用不同 requestCode

审的是：代码
触发（任一种）：
- 读到：源端 `PendingIntent.getBroadcast(context, requestCode, ...)`，requestCode 每次不同（如 `SystemClock.elapsedRealtime().toInt()`）；写错的样子：ArkTS 所有按钮的 WantAgentInfo 都写 `requestCode: 0`，不设 flags
适用范围：通知上多个动作按钮、或同一按钮反复构建并要刷新载荷时
做法：
- 每个按钮、每次构建给递增的唯一 requestCode；要刷新载荷时加 actionFlags: [wantAgent.WantAgentFlags.UPDATE_PRESENT_FLAG]
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- requestCode: number（Request code defined by the user，必填）：WantAgentInfo 的请求码（出处：鸿蒙 SDK 的 ets/api/wantAgent/wantAgentInfo.d.ts，WantAgentInfo.requestCode）
- UPDATE_PRESENT_FLAG：Extra information of the existing WantAgent object is replaced with that of the new object：用新对象的附加信息替换已有 WantAgent 的（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.wantAgent.d.ts，wantAgent.WantAgentFlags.UPDATE_PRESENT_FLAG）
- actionFlags?: Array<abilityWantAgent.WantAgentFlags>（wantAgentFlags 标 @deprecated since 11，@useinstead WantAgentInfo#actionFlags）：WantAgentInfo 里写 flags 的字段（出处：鸿蒙 SDK 的 ets/api/wantAgent/wantAgentInfo.d.ts，WantAgentInfo.actionFlags）
未核实：requestCode 0 复用旧载荷没有设备复现，按声明和源码对照推定；卡里没写修复用的是 wantAgentFlags 还是 actionFlags 字段
来源：1 张卡，1 个应用
- case-f4fef12b5d994df457b2（Cofi）：做法第 1 步 ← 建议 4、诊断
