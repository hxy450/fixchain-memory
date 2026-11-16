# onCreate 里同步语句和组合、挂载的先后

agent 会看到什么：读到 Activity.onCreate 里 setContent { … } 之后还有写同一状态的语句、组合内 LifecycleEventEffect / LaunchedEffect 读它，或 onCreate 里 findViewById 取到 View 后立即调用；规格按源码行序写读写先后，或共享组件的句柄契约没写宿主最早何时可用

## 规矩

- rule-8c18ab22282e｜onCreate 里 setContent 的组合副作用晚于 onCreate 后续语句，规格按运行顺序写读写先后｜读到：Activity.onCreate 里 setContent { … } 挂 Compose 内容，组合内 LifecycleEventEffect(Lifecycle.Event.ON_CREATE)、LaunchedEffect 或 DisposableEffect 读某个状态，setContent 之后 onCreate 还有写同一状态的语句（如启动计数自增）；写错：规格按源码行号写成「先判后自增」「首启读到 0」，首启边界样例和「时序照搬」验收也按行序推出
- rule-d28f0c415434｜给共享组件加跨页句柄机制时，契约写明宿主最早可用点，差异表列出延后登记｜读到：源端在 onCreate 里 findViewById 同步取得 View 并立即调用它；写错：共享组件的句柄契约没写宿主何时可用、也没有登记回调；源码理解笔记的差异表把「findViewById → 句柄登记」的外显影响写成「无」
