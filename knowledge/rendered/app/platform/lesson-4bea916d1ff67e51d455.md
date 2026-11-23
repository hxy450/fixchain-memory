# 打开系统设置的显式 Want 包名随设备与系统版本变化：写前在目标设备核对，启动失败要可观察，不照抄参考里标“已验证”的值

## 何时使用

系统能力实现阶段，为“打开系统设置/应用权限页”编写 startAbility 显式 Want（bundleName/abilityName）时；维护迁移 skill 参考中的系统应用包名时；只为重开被拒权限时改用 requestPermissionOnSetting

## 适用情境

源端经 Settings.ACTION_* 一类 Intent 跳转系统设置（全部文件访问、应用详情等）；目标为 HarmonyOS NEXT 应用，需要以显式 Want 指定系统设置应用，规格与源码都不给目标包名，可查到的参考文档给出硬编码的厂商设置包名并标注已验证。跳设置只是为了让用户重新打开已被拒绝的运行时权限时，目标可以用 abilityAccessCtrl 的 requestPermissionOnSetting（API 12 起）由系统弹出权限设置框，不需要设置应用的包名；代码已经这样写的照留，不改成显式 Want。

## 原因

系统设置应用的包名是与设备、系统版本相关的常量，参考里的“已验证”只对其当时的设备成立；startAbility 被拒后若只在 catch 里记日志，按钮在用户看来就是点了没反应。来源中实现者照抄参考中的 com.huawei.settings，HarmonyOS NEXT 真机上的设置应用为 com.huawei.hmos.settings，两个权限页的“打开设置”都失效，直到视觉验证才发现。

## 做法

1. 有设备时写前用 hdc shell bm dump -a 查找设置应用包名，再用 bm dump -n <包名> 取 Ability 名（来源 HarmonyOS NEXT 手机为 com.huawei.hmos.settings / com.huawei.hmos.settings.MainAbility）；生成期无法核对时，在交付报告或验证清单登记“打开设置需真机确认”。
2. startAbility 失败要让调用方可观察（返回结果或给用户提示），不只 hilog 后吞掉。
3. 维护参考文档时为系统应用包名注明验证时的系统版本与设备，HarmonyOS NEXT 与旧版 EMUI/HarmonyOS 分开写。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕HarmonyOS NEXT 手机上系统设置应用的包名是 com.huawei.hmos.settings，入口 Ability 是 com.huawei.hmos.settings.MainAbility；显式 Want 写成 com.huawei.settings 时拉不起设置页
- 〔原因 / 做法第 2 步〕UIAbilityContext.startAbility 只能在调用方处于前台时拉起；显式 Want 指向的 Ability 不存在时 Promise 以 BusinessError 16000001（The specified ability does not exist）被拒，目标组件不可见时报 16000004；失败只体现在 Promise 拒绝上
