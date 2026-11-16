# 源端用 System.exit 一类调用做「重启」时，规格写明系统重建语义，目标等价是 restartApp 加携带状态

审的是：规格
触发（任一种）：
- 读到：源码里方法体是 System.exit(0)（或 Runtime.exit、Process.killProcess），方法注释写「full app restart」，调用点是通知点击、语言切换、数据重置一类；写错的样子：规格把它写成「System.exit(0) 忠实迁移 = 退出应用（terminateSelf），不附加重启」，或实现映射表里只有 context.terminateSelf()
适用范围：规格提取时为源端进程退出、重启类调用确定目标端等价行为与状态保留要求
做法：
- 先 grep 调用方和方法注释，在规格里写明平台语义：Android 前台进程被杀后，系统按任务栈与 savedInstanceState 重建 Activity
- 目标端等价写成：ApplicationContext.restartApp(want) 拉起新进程进入入口 UIAbility，原由系统保存的界面状态（抽屉开合、列表位置、搜索条件等）随 want.parameters 携带
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- restartApp(want: Want): void（@since 12），重启应用并启动指定 UIAbility，重启时不触发 onDestroy；只能在主线程调用，且应用须处于活动状态：源端「杀进程后系统重建」在目标端的等价接口（出处：鸿蒙 SDK 的 ets/api/application/ApplicationContext.d.ts，ApplicationContext.restartApp）
- terminateSelf(): Promise<void>，销毁当前 Ability：只是退出，不会重新拉起（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.terminateSelf）
- onSaveInstanceState 在 Activity 可能被杀之前调用，回来时用保存的 Bundle 在 onCreate / onRestoreInstanceState 里恢复状态：源端重建后界面状态是系统替它保留的，目标端要自己带（出处：android.app.Activity#onSaveInstanceState）
- parameters?: Record<string, Object>：Want 上携带保存态的字段（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.Want.d.ts，Want.parameters）
针对本应用要查的：
- 重启前要保留哪些界面状态：源工程相关 Activity 的 onSaveInstanceState，以及调用重启的那几个调用点；列出 Bundle 里存的键（抽屉、列表位置、搜索条件等），规格里逐项写成随 Want 携带的参数
未核实：卡里环境是 HarmonyOS 6.1.1(24)，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-f85c825bb16d5a79901c（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
