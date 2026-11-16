# 入口与生命周期

源端 Application、Activity 和业务基类的 onCreate、onResume、onPause、onDestroy、onBackPressed 里有行为，或者目标端要接到 EntryAbility、入口页、共享服务的停止和释放上时

## 触发族

- [源端基类与跨切片的生命周期接线](lifecycle-wiring-slices/index.md)（4 条）：源端多数 Activity 继承的基类在 onResume / onPause / onNewIntent 里的统一行为、前一切片引擎代码留给后续切片调用的 onStop / onResume 接线入口，在切片计划、派工、占位登记里有没有落点
- [源端 Activity 生命周期里的行为](activity-lifecycle/index.md)（8 条）：源端 Application / Activity 的 onCreate、onDestroy、onBackPressed 或业务基类钩子里做的事（设主题、发初始化请求、首次启动自动执行、页面级埋点、返回语义），在功能清单、HANDOFF、占位登记、派工或执行总结里怎么交代
- [EntryAbility 和入口页上的接线与移交](entry-ability-wiring/index.md)（5 条）：入口装配派工、子任务回报或实施记录里，要落到 EntryAbility（onCreate、onConfigurationUpdate、label）或入口页上的调用和缺陷（全局异常观察器、网络 init、主题同步、返回兜底、脚手架 label），由谁接、接在哪
- [共享服务的停止和最终释放](shared-service-release/index.md)（1 条）：规格写「页面销毁：取消播放任务并 stop()」、源端清理挂在外层 Composable 的 DisposableEffect 上，切片计划的对接点写「某页面.onDisappear → 共享服务.stop()」
