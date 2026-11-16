# onNewIntent 与外部深链的再次拉起

agent 会看到什么：读过的源码里外部入口用带 FLAG_ACTIVITY_CLEAR_TOP 的 Intent、handleDeepLink 或 onNewIntent 再次拉起页面；交回的 onNewWant 没清 NavPathStack 就切 tab 或 push，或页面改在 onShown 里刷新

## 规矩

- rule-1ba8728a8909｜CLEAR_TOP 深链热启动时，onNewWant 先 NavPathStack.clear() 再切 tab｜读到：桌面卡片等外部入口的显式 Intent 带 FLAG_ACTIVITY_CLEAR_TOP | FLAG_ACTIVITY_NEW_TASK 拉起主 Activity；写错：onNewWant 里热启动深链只改当前 tab 下标，没有 NavPathStack.clear()，压着的详情页还在
- rule-a720aa31924b｜目标端消费外部深链时先 clear(false) 再依次 push 起始页和目标，不在原栈上 pop 再 push｜读到：源端 LaunchedEffect(intent) { navController.handleDeepLink(intent) }，onNewIntent 里 setIntent；写错：消费 want 时栈顶同名先 pop() 再 pushPathByName(目标)，其余栈保留，运行中收到深链时目标叠在原栈上
- rule-ee4ad6192070｜源页面只在 onNewIntent 里刷新时，目标不在 onShown 里刷新，放到新标签投递之后｜读到：源页面只在 onCreate 和 onNewIntent（先 super.onNewIntent 再刷新）里刷新；写错：目标页在 .onShown(...) 或 onPageShow 里刷新，回到页面就重读
- rule-dadb06d9cde8｜onNewWant 写入的 want 快照要带 revision 并由已存在的页面观察，不只在构造时读一次｜读到：源 Activity 为 standard 启动；目标 UIAbility 为 singleton，`onNewWant` 把新 want 写进共享快照；写错：快照只在 `onCreate` / `onNewWant` 写入，VM 只在构造函数里拷贝一次（注释却说新 want 覆盖旧值），页面不观察，也没有 revision
