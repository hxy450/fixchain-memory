# 进程回收后的页面栈恢复（savedInstanceState、NavHost）

agent 会看到什么：读过的源码里宿主用 rememberNavController + NavHost 或 onCreate(savedInstanceState)，规格要求进程回收后恢复页面栈；交回的 EntryAbility 没 setRestoreEnabled、没按 APP_RECOVERY 恢复窗口舞台，Navigation / NavDestination 没设 id 和 recoverable，或接收页用 instanceof 识别路由参数

## 规矩

- rule-efdd37ebe339｜要恢复页面栈时，UIAbility 开启备份恢复并在 APP_RECOVERY 时恢复窗口舞台｜读到：规格要求进程回收后恢复页面栈，或源宿主用 rememberNavController + NavHost / onCreate(savedInstanceState)；写错：EntryAbility 的 onCreate 里没有 this.context.setRestoreEnabled(true)；launchReason 为 APP_RECOVERY 时没有 restoreWindowStage，也没有 onWindowStageRestore，onWindowStageCreate 每次都直接 loadContent
- rule-6baf56db862d｜要恢复页面栈时，Navigation 设 id 和 recoverable，每个 NavDestination 也设｜读到：规格要求进程回收后恢复页面栈，或源宿主用 rememberNavController + NavHost / onCreate(savedInstanceState)；写错：根 Navigation(pathStack) 上没有 .id(...) 和 .recoverable(true)；各页的 NavDestination() 上没有 .recoverable(true)
- rule-8dd4cd90888f｜可恢复页面的路由参数要可序列化，接收端按字段识别，不只靠 instanceof｜读到：源端 NavHost 路由带参数，进程回收后参数由框架随返回栈恢复；写错：接收页用 `instanceof` 某个参数类判断 NavPathStack 传来的参数；开启 recoverable 后恢复出的参数是同形的普通对象，判断不成立
