# 生命周期与启动

源端有 Activity / Fragment 的 onCreate、onStart、onResume、onPause、onDestroy、闪屏和初始化、configChanges、savedInstanceState、Compose DisposableEffect，目标端有 EntryAbility 的回调、aboutToAppear / aboutToDisappear、onShown / onHidden、onReady 时

## 触发族

- [启动链和初始化的顺序](startup-init/index.md)（9 条）：读到闪屏 Activity 按登录态跳转、目标 Activity onCreate 里的初始化请求、View 构造器先开局再 onSizeChanged、WXEntryActivity 的 handleIntent、要靠 EntryAbility.onCreate 调用的 static configure、规格要求照搬的崩溃；产物里启动 ViewModel 的路由方法、aboutToAppear 里不 await 的 async 和 try/catch、EntryAbility 的 onCreate / onNewWant、HANDOFF 标记
- [源端对象、静态字段和监听的存活期](object-lifetime/index.md)（4 条）：读到源 Activity 的实例字段存会话数据、类的 static 字段、getLastNonConfigurationInstance 判空分支、Fragment 只注册不注销的监听；产物里服务的 getInstance() 单例、静态引擎的每局复位函数、hasInstance() 分支、aboutToDisappear 里补的注销
- [源端生命周期回调里的副作用](lifecycle-side-effects/index.md)（6 条）：读过的源码里业务基类、Activity 或 Service 的 onCreate / onResume / onPause / onDestroy / onBackPressed 里有埋点、存档计时、状态复位这类副作用；交回的 aboutToAppear / aboutToDisappear / onHidden / stopService 里这些副作用漏了、多挂了，或没复位
- [入口 Ability 的全局异常监听（errorManager）](error-observer/index.md)（1 条）：读过的源码里有或没有 setDefaultUncaughtExceptionHandler，规格或台账写了未捕获异常照源复刻还是要捕获；交回的 EntryAbility.onCreate 里 errorManager.on('error', …) 的有无和它不一致
- [未声明 android:configChanges 时的配置变化重建](config-change-recreate/index.md)（9 条）：读过的 AndroidManifest.xml 里 Activity 没写 android:configChanges（或不含 orientation），旋转、改配置时安卓会重建页面，构造时的一次性状态和代码设置的视图状态随之复位；交回的 EntryAbility 没有 onConfigurationUpdate、页面没有配置变化的处理入口，或代码设的视图状态写成 @State 旋转后不复位
- [进程回收后的页面栈恢复（savedInstanceState、NavHost）](process-recovery/index.md)（3 条）：读过的源码里宿主用 rememberNavController + NavHost 或 onCreate(savedInstanceState)，规格要求进程回收后恢复页面栈；交回的 EntryAbility 没 setRestoreEnabled、没按 APP_RECOVERY 恢复窗口舞台，Navigation / NavDestination 没设 id 和 recoverable，或接收页用 instanceof 识别路由参数
- [EntryAbility 的入口页和启动顺序](entry-page/index.md)（4 条）：目标工程 EntryAbility 的 onCreate / onWindowStageCreate、loadContent 加载的入口页（DevEco 模板的 Index）、main_pages 登记和 @Entry / export struct，以及首屏前的异步装配
- [Compose 的生命周期观察者和 DisposableEffect](compose-lifecycle-observer/index.md)（4 条）：读到源端 DisposableEffect 里的 LifecycleEventObserver（ON_RESUME、ON_STOP）或 onDispose；交回的代码只在 aboutToDisappear 里 dispose / stop，没有 onShown、onHidden，或刷新方法漏了回调里的赋值
- [onStart / onResume 里每次重做的初始化](onstart-reinit/index.md)（1 条）：读到 Activity 的 onStart() / onResume() 里每次重读 getIntent()、重建列表、校验目录或重设界面文字；产物里 NavDestination 把这段挂在一次性的 .onReady(...) 或 aboutToAppear 里，.onShown 只做别的事
- [派工要求承接的基类横切钩子](base-class-hook/index.md)（1 条）：读到派工写某页承接基类的淡入等钩子，源基类里是 findViewById(R.id.x) 判空后才执行；产物里页面加了 .opacity(...) 加 .onAppear / onShown 的淡入或别的基类横切副作用
- [onCreate 里 findViewById 后对子 View 的接线](findviewbyid-child-wiring/index.md)（3 条）：读到 Activity.onCreate 里 findViewById 取到自定义 View 后立即调它的 setter（设状态、设触摸监听）、只接线一次；产物里宿主在 NavDestination.onReady 或 init 里读子组件 aboutToAppear 登记的句柄、用 ?. 调实例接线，或注释断言 onReady 时句柄必已就绪
- [源端的整应用重启（System.exit、startActivity 后退出进程）](app-restart/index.md)（2 条）：读到源端方法体 System.exit(0)、注释「Performs a full app restart」，或恢复、导入的库实现里 startActivity 后 System.exit 重启应用；产物里对应处只有 terminateSelf()、只弹 showToast，没有 restartApp
- [SavedStateHandle 保存态和数据库值的先后](saved-state-handle/index.md)（1 条）：读到源 ViewModel 用 SavedStateHandle 的 contains / get 守卫表单字段、保存态有值就不取数据库值，或规格 AC 写保存态优先；产物里 aboutToAppear 无条件用数据库值给表单字段赋值，或记成「无等价物，残余」
