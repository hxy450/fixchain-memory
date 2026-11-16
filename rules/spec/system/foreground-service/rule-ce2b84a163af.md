# 安卓前台服务映射承载类时，规格写 SDK 确有导出的类，并与 module.json5 的 type 成对

审的是：规格
触发（任一种）：
- 读到：安卓源 Service（如 LifecycleService）里调用 startForeground(...) 承载长任务，manifest 写 foregroundServiceType（如 dataSync）；写错的样子：规格或决策台账把前台服务映射为 ServiceExtensionAbility（公共 SDK 的 @kit.AbilityKit 不导出），或只写了类名、没写 module.json5 extensionAbilities 的 type
适用范围：规格和决策台账里给安卓前台服务选鸿蒙承载类的那一项（AppServiceExtensionAbility 出自声明 @since 20）
做法：
- 选承载类前在项目 SDK 的 kits/@kit.AbilityKit.d.ts 导出和 api 目录确认该类存在；公共 SDK 导出的是 AppServiceExtensionAbility，不导出 ServiceExtensionAbility
- 规格把类名和 module.json5 的 type 成对写出：AppServiceExtensionAbility ↔ "type": "appService"
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- import AppServiceExtensionAbility from '@ohos.app.ability.AppServiceExtensionAbility'：@kit.AbilityKit 导出的服务类扩展基类；kit 里没有 ServiceExtensionAbility（出处：鸿蒙 SDK 的 ets/kits/@kit.AbilityKit.d.ts）
- declare class AppServiceExtensionAbility extends ExtensionAbility（@since 20，@stagemodelonly）：应用后台服务扩展的基类（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.AppServiceExtensionAbility.d.ts，AppServiceExtensionAbility）
- type 取 appService（20+）对应 AppServiceExtensionAbility；type 取 service 时三方应用无法安装，需要特权且不对三方开放：类与 type 的对应（出处：module-configuration-file.md，type标签）
- AppServiceExtensionAbility 当前仅支持 2in1 设备，集成它的组件需要申请 ACL 权限 ohos.permission.SUPPORT_APP_SERVICE_EXTENSION：文档写的约束（出处：js-apis-app-ability-appServiceExtensionAbility.md，约束限制）
未核实：卡里环境是 API 22（HarmonyOS 6.0.2），本机声明是 API 23；文档写 AppServiceExtensionAbility 仅支持 2in1 设备、要 ACL 权限，卡里没写设备类型和权限
来源：1 张卡，1 个应用
- case-b92afb07b8ec2465afcf（CleanSweep）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
