# Intent 发起的外部入口、通知动作和分享

agent 会看到什么：读到 Intent / PendingIntent 发起的动作：快捷方式和通知点进页面的 startActivity、通知按钮 PendingIntent.getBroadcast、isIntentAvailable 判断、ACTION_SEND 分享面板；产物里 EntryAbility 的 want 路由、WantAgent、导航守卫和 systemShare

## 规矩

- rule-718a09651127｜外部入口页的 want 在 EntryAbility 路由里要有分支并 pushPathByName，目标页兼容对象参数｜读到：页面规格把桌面快捷方式、本地通知点击列为本页入口（外部 Intent 携带参数），源端热启直接 startActivity 目标页；写错：EntryAbility 的 onCreate / onNewWant 和 want 路由函数里没有这类 want 的分支，只有目标页注释写「由基座 pushPathByName 进入」；或目标页只按某个参数类的 instanceof 读参数
- rule-dc8c6cd5f507｜源端跳转前判断目标能否启动时，目标守卫查注册名或 pageName 非空，不查导航栈成员｜读到：源端跳转前对构造出的目标 Intent 做 isIntentAvailable 一类判断（能否被解析启动），热启分支直接 startActivity 目标页；写错：宿主导航执行器的守卫写成 navPathStack.getAllPathName().indexOf(pageName) < 0 → return false
- rule-3d7f4b133068｜源端通知按钮是 getBroadcast 时，进程存活用 SEND_COMMON_EVENT 静默派发，挂起态才拉起｜读到：通知按钮 `PendingIntent.getBroadcast(...)` 交给 BroadcastReceiver 处理，应用不被拉起；写错：ArkTS 按钮 WantAgent 只用 `OperationType.START_ABILITY`，EntryAbility 的 onCreate/onNewWant 解析 want 参数后派发，没有公共事件订阅
- rule-3102eb55145d｜源端分享面板含 App 内渠道时逐项接到目标入口，不用系统分享面板整体替代｜读到：源端分享面板的渠道列表里除系统和第三方平台外还有 App 内渠道分支（把截图带进发帖页）；规格的依赖接缝写明该渠道及目标端承接页和路由参数；写错：分享整体写成只用 systemShare.ShareController(...).show(...) 打开系统分享面板（传 `'general.jpeg'` 这类 utd），没有 App 内渠道的分支，也没有跳转承接页
- rule-c17b93d77b5f｜多个 PendingIntent 按钮迁成 WantAgent 时，每个按钮每次构建用不同 requestCode｜读到：源端 `PendingIntent.getBroadcast(context, requestCode, ...)`，requestCode 每次不同（如 `SystemClock.elapsedRealtime().toInt()`）；写错：ArkTS 所有按钮的 WantAgentInfo 都写 `requestCode: 0`，不设 flags
- rule-6b03bc701850｜规格指定的分享能力与源码交互形态不一致时回报缺口，不在错误路线上加封装｜读到：源端分享是带渠道项的应用内面板（shareImage(...) 加渠道列表，按 platformName 分发）；写错：分享按钮直接调用系统分享封装（new systemShare.ShareController(...).show(...)），巡检修复又在这条路线上新增 await ShareController.show() 的异步封装
- rule-c483a1b9f3f1｜无 UI 的 trampoline Activity 接进入口时保留前后台状态和透明模态窗口，不只加一行分发｜读到：源端通知按钮的 PendingIntent 指向一个无 UI、透明、独立任务的 trampoline Activity 来分派动作；写错：EntryAbility.onCreate / onNewWant 只各加一行按 want 分发的调用，和主入口共用；没有前后台状态跟踪，也没有取消、过去时刻时的模态窗口
- rule-bc9d732e6210｜源端 await 分享后才弹成功提示时，目标用 shareCompleted/dismiss 结算｜读到：源代码先 await Share.share({ title, text, url })（Capacitor 等插件的分享调用），之后才弹成功 toast，catch 里弹失败 toast；写错：目标只写 await controller.show(context, options) 就返回，随后弹成功提示；没有注册 on('shareCompleted') 和 on('dismiss')，取消分享时没有失败提示
