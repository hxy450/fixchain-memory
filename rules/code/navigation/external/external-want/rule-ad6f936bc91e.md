# 打开系统设置的 Want 写 com.huawei.settings 时，NEXT 上改为 hmos 包名

审的是：代码
触发（任一种）：
- 读到：源端用 Settings.ACTION_APPLICATION_DETAILS_SETTINGS、Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION 等 Intent 跳系统设置；参考文档给出硬编码的设置包名并标「已验证」；写错的样子：Want 里写 bundleName: 'com.huawei.settings'、abilityName: 'com.huawei.settings.MainAbility'，startAbility 失败只在 catch 里 hilog.warn
适用范围：目标是 HarmonyOS NEXT（SDK 6.x）应用、用显式 Want 打开系统设置或应用权限页时
做法：
- 把系统应用的 bundleName/abilityName 当作随设备和系统版本变的常量，参考里的「已验证」不当作对目标设备的结论；HarmonyOS NEXT 手机上写 bundleName: 'com.huawei.hmos.settings'、abilityName: 'com.huawei.hmos.settings.MainAbility'
- startAbility 的失败不只在 catch 里打日志了事
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- bundleName 'com.huawei.hmos.settings'，abilityName 'com.huawei.hmos.settings.MainAbility'：HarmonyOS NEXT 手机上的系统设置应用，按它改后 aa start 成功（出处：卡里修好并验证过）
- startAbility(want: Want, options?: StartOptions): Promise<void>：拉起显式 Want 指向的 Ability，目标不存在时 Promise 被拒（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.startAbility）
未核实：卡里只在 HarmonyOS NEXT 手机上核对过，其他设备形态未核；原 Want 里的 action 和 page 参数在新包名下落到哪个页面，卡里没写
来源：1 张卡，1 个应用
- case-5aa1e2ae875c4bef3df1（CleanSweep）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 1 ← 诊断、建议 1
