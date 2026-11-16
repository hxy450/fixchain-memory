# 源端恢复后重启应用时，目标端导入成功后也重启应用，不只弹 Toast

审的是：代码
触发（任一种）：
- 读到：源端 import(ctx, uri, true) 的库实现在恢复后 startActivity + System.exit 重启应用；写错的样子：目标端导入成功后只调 showToast(...)，没有重启应用
适用范围：迁移源端备份恢复功能、源端恢复后重启进程时
做法：
- 导入成功后重启应用（返修写成 restartApp），不只弹 Toast
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- restartApp(want: Want): void：ApplicationContext 重启应用并拉起指定 UIAbility，重启时不触发 onDestroy；只能在主线程、应用处于活动状态时调用（@since 12）（出处：鸿蒙 SDK 的 ets/api/application/ApplicationContext.d.ts，ApplicationContext.restartApp）
- restartApp(want: Want): Promise<void>：同族接口：UIAbilityContext 重启当前应用进程（@since 22）（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.restartApp）
未核实：卡里返修写的是 restartApp，没写明调用的是 ApplicationContext 还是 UIAbilityContext 的；卡里的行为出自 HarmonyOS 6.1.1(24)，本机按 API 23 声明核实
来源：1 张卡，1 个应用
- case-087050b57a3e1a6ac4ce（jerboa）：做法第 1 步 ← 诊断、建议 2
