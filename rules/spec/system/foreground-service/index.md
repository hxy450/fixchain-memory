# 前台服务的承载类

agent 会看到什么：源端 Service（如 LifecycleService）调 startForeground、manifest 写 foregroundServiceType；规格或决策台账里映射的承载类和 module.json5 extensionAbilities 的 type

## 规矩

- rule-ce2b84a163af｜安卓前台服务映射承载类时，规格写 SDK 确有导出的类，并与 module.json5 的 type 成对｜读到：安卓源 Service（如 LifecycleService）里调用 startForeground(...) 承载长任务，manifest 写 foregroundServiceType（如 dataSync）；写错：规格或决策台账把前台服务映射为 ServiceExtensionAbility（公共 SDK 的 @kit.AbilityKit 不导出），或只写了类名、没写 module.json5 extensionAbilities 的 type
