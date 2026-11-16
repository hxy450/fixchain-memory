# 启动链和初始化的顺序

agent 会看到什么：读到闪屏 Activity 按登录态跳转、目标 Activity onCreate 里的初始化请求、View 构造器先开局再 onSizeChanged、WXEntryActivity 的 handleIntent、要靠 EntryAbility.onCreate 调用的 static configure、规格要求照搬的崩溃；产物里启动 ViewModel 的路由方法、aboutToAppear 里不 await 的 async 和 try/catch、EntryAbility 的 onCreate / onNewWant、HANDOFF 标记

## 规矩

- rule-49e6667d5d58｜迁启动链时打开闪屏每个路由目标页的初始化入口，已登录冷启动的请求逐项落到 ViewModel｜读到：闪屏 Activity 按登录态 navigation() / startActivity(Intent) 进入已登录目标 Activity，目标 Activity 的 onCreate 初始化里发刷新 token、拉配置、检查版本等请求；写错：目标端启动 ViewModel 的路由方法在已登录分支直接返回主页目标，没有发起这些请求（例如没有先刷新 token）
- rule-93531a8a7606｜快照依赖引擎首次写入而初始化是异步的，布局加「引擎已启动」门控并下一帧重试｜读到：源端 View 构造器里先调开局初始化，onSizeChanged 才生成背景，所以背景取到的是首次开局后的状态；写错：目标的开局初始化在偏好就绪后的异步冷启链里（Promise / await 之后），布局或取快照的函数没有判断引擎是否已启动，可能在首次开局之前取到初始值
- rule-1bfadff2b2cd｜微信回调由 EntryAbility 的 onCreate、onNewWant 把 want 交给 handleWant｜读到：源端 WXEntryActivity / WXPayEntryActivity 里 handleIntent(getIntent(), this) 接微信回调；写错：EntryAbility 的 onCreate / onNewWant 没把 want 交给 WXApi.handleWant，回调页只留 FWD-REF 空实现，onResp 没人调用
- rule-7ae532851947｜基础模块暴露未调用就抛错的 static configure/init 时，在模块源码就地写 HANDOFF 标记｜读到：流水线规则要求：要靠另一处调用点（如 EntryAbility.onCreate）才算完成的代码必须写 `// HANDOFF: owner=… what=… verify=grep:…`，散文交代会被放行；写错：基础模块里 static configure(...) 未调用时取配置就 throw（如「configuration is missing」），源码没有 `// HANDOFF:` 标记，只在注释、handoff 文档或「Suggested P-ID」里写「由启动 owner 调用」
- rule-f625bf97aa68｜规格要求照搬源端崩溃时，抛出点到生命周期入口之间不加 try/catch，也不放进不等待的 async｜读到：规格、决策台账或派工写明某条源端异常照搬为崩溃（「throw 等价复刻」「勿加防护」），源端调用链上没有 catch（如 Arrays.fill 越界抛 ArrayIndexOutOfBoundsException 直接崩溃）；写错：aboutToAppear 里调用 this.bootAsync() 不 await，整段包在 try { … } catch { hilog.error(…) } 里只记日志；或调用链上有 Promise.catch
- rule-037ecfc06327｜启动入口接线时，带缺失即抛错守卫的 static configure/init 逐一在 onCreate 调用｜读到：基础模块里有 static configure( 或 static init(，取配置时未配置就抛「configuration is missing」一类错误；写错：EntryAbility.onCreate 或 bootstrap 里没有调用这些 configure / init，业务请求在生成 URL 前就抛配置缺失
- rule-fb8fb008f93d｜源端在 onCreate 链上直接调起一键登录 SDK 时，目标不借用先查自有协议勾选的按钮逻辑｜读到：源端登录 Activity 在 onCreate → 初始化 → SDK 初始化回调末尾无条件调用一键登录，直接进入官方 SDK 的授权页流程；写错：目标页在 onReady 或 aboutToAppear 里调用登录按钮的处理方法，该方法在协议未勾选（默认 false）时先弹应用自有的协议确认框
- rule-70fc512dddf0｜源端加载页由 SDK 初始化驱动而目标初始化瞬时完成时，首次冷启动补足最短展示时长｜读到：SplashActivity 继承外部 SDK 的启动 Activity，进度回调更新 ProgressBar，SDK 初始化结束才 startActivity 进 MainActivity；规格要求首次冷启动有可见加载页；写错：目标端初始化 load 返回后立刻把进度置满并跳转，没有 setTimeout 之类的最短展示时长
- rule-3e9112f2bb34｜源端不初始化的崩溃上报，目标的 onCreate 不加同意门控和本地采集初始化｜读到：源端 Application.onCreate 里 ACRA.init 只在构建期上报地址非空时调用，参照构建里为空；写错：EntryAbility.onCreate 里新增「隐私同意 ∧ 开关」的合成门控，并初始化本地崩溃日志采集
