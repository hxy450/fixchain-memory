# EntryAbility 和入口页上的接线与移交

agent 会看到什么：入口装配派工、子任务回报或实施记录里，要落到 EntryAbility（onCreate、onConfigurationUpdate、label）或入口页上的调用和缺陷（全局异常观察器、网络 init、主题同步、返回兜底、脚手架 label），由谁接、接在哪

## 规矩

- rule-b9ce8ce76767｜入口装配的派工要列上注册全局未捕获异常观察器一项，不因安卓源没有而省略｜读到：安卓源里没有 UncaughtExceptionHandler 一类的全局异常处理代码；入口装配契约只要求改 loadContent、main_pages.json、Navigation 外壳与 pageMap、剔除模板；写错：入口装配的派工或任务拆分里，EntryAbility 的改写项只有 loadContent 改向入口页、main_pages.json 只留入口页、Navigation 外壳与 pageMap、剔除 Hello World 模板这几项，没有「onCreate 注册 errorManager.on('error') 观察器、onDestroy 注销」
- rule-2c93ef2c338d｜网络层留有需显式调用的 init 时，回报列出待接线项，接进 onCreate 前不记完成｜读到：网络层回报写着某个文件是「网络初始化入口」，或代码注释写「由 EntryAbility 初始化」；写错：回报写了「网络初始化入口」却写 `Forward-Ref Hooks：无`，没有单列待接线项（文件、生命周期方法、调用语句）
- rule-37b882561c93｜子任务回报导出 API 要宿主调用才生效时，当轮写进拥有宿主文件的切片派工并写明调用点｜读到：子任务回报写着「EntryAbility 侧调用接线归属后续段；未接线前取色函数固定返回浅色套」这类：某个导出函数要宿主调用、未接线前默认值错误；写错：拥有 EntryAbility.ets 的切片派工只列了别的事（暂存 want.uri、核对沉浸式），没有要求在 onCreate 与 onConfigurationUpdate 调用主题同步函数；主会话只记「完成」
- rule-631008557fe0｜接收“由入口宿主兜底”的返回移交前先确认回调可达，不可达就改登记｜读到：上游页面实施记录写“本页不加 onBackPress，栈深≤1 退后台的兜底归入口壳/根页”；写错：占位或移交登记把“栈深≤1 退后台”的兜底指到承载 Navigation 的 @Entry 入口页，派工照此要求在入口页 onBackPress 里实现
- rule-69ece8681822｜子任务在 open_questions 里点名的跨所有权缺陷，编排者要指派归口或登记待办｜读到：子任务返回的 open_questions 点名一处不归它写的缺陷（如 EntryAbility_label 仍是脚手架值、待配置归口方修正）；写错：后续派工和待办登记里没有这一项，阶段推进后这条问题被丢掉
