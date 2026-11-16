# 源端用 System.exit(0) 做整应用重启时，目标用 restartApp，失败再 terminateSelf

审的是：代码
触发（任一种）：
- 读到：方法注释「Performs a full app restart」、方法体 System.exit(0)，调用点是语言切换、恢复或重置数据、通知点击一类；写错的样子：目标重启方法体只有 context.terminateSelf()，注释写「忠实迁移 = 退出应用，不附加重启」一类
适用范围：源端靠 System.exit(0) 结束进程让系统重建任务栈、达到冷启效果的重启方法（按注释和调用点核实为重启语义）
做法：
- 写成 context.getApplicationContext().restartApp({ bundleName: <自身包名>, abilityName: '<入口 UIAbility 名>' })，catch 里 terminateSelf() 兜底
- 需保留的界面状态写进 want.parameters，入口 UIAbility 冷启时取回；冷启分支先过验密门等入口约束
- 推迟的重启放到 windowStage.on('windowStageEvent') 收到 WindowStageEventType.ACTIVE（窗口获焦）后再调
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- restartApp(want: Want): void：重启应用并拉起指定 UIAbility，重启时不触发 onDestroy；只能主线程调用，应用须在前台（出处：鸿蒙 SDK 的 ets/api/application/ApplicationContext.d.ts，ApplicationContext.restartApp）
- 16000053 不在界面顶层；16000063 目标不属于当前应用或不是 UIAbility；16000064 重启太频繁，至少隔 3s：会失败的几种情形，失败时走 terminateSelf 兜底（出处：鸿蒙 SDK 的 ets/api/application/ApplicationContext.d.ts，ApplicationContext.restartApp）
- getApplicationContext(): ApplicationContext：从 Context 取应用级上下文（出处：鸿蒙 SDK 的 ets/api/application/Context.d.ts，Context.getApplicationContext）
- WindowStageEventType.ACTIVE = 2，窗口获焦：推迟的重启在这个事件后执行（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，window.WindowStageEventType.ACTIVE）
- 改为 ApplicationContext.restartApp、失败 terminateSelf 兜底后与源端一致：修好后的写法（出处：卡里修好并验证过）
- restartApp(want) 拉起入口 UIAbility、失败 terminateSelf 兜底，保存态经 Want 参数携带，推迟重启改到窗口获焦时执行后生效：带状态、推迟重启时修好的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 包名和入口 UIAbility 名：目标工程 AppScope 的 app.json5（bundleName）和 entry 模块 module.json5 的 mainElement、abilities；bundleName 取 app.json5 的 app.bundleName；abilityName 取 mainElement 指向的那个 UIAbility 的 name
- 重启前后要带的界面状态和入口约束：源工程 Activity 的 onSaveInstanceState、onCreate 里读 savedInstanceState 的地方，以及入口处的验密、引导一类判断；逐项列出保存的键和入口判断，目标端写进 want.parameters 并在入口 UIAbility 冷启时按同样顺序处理
未核实：case-f85c825bb16d5a79901c 的环境是 HarmonyOS 6.1.1(24)，声明按本机 API 23 核实
来源：2 张卡，1 个应用
- case-29db923e9cadbe8ce53c（omni-notes-hmos）：做法第 1 步 ← 诊断、建议 3；取值 5 ← 诊断
- case-f85c825bb16d5a79901c（omni-notes-hmos）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；做法第 3 步 ← 建议 3、诊断；取值 6 ← 诊断
