# ui/navigation

页面导航：先确定宿主和注册方式，再处理参数与跳转契约，或返回键与栈变更；同窗口 push 替代另起 Activity 时的窗口方向切换与恢复。

[上一级](../index.md)

## 子主题

- [back-stack](back-stack/index.md) — 系统/页面返回与返回栈：按源端 API 清栈重建返回栈（TaskStackBuilder 父链、handleDeepLink 新任务、外部入口 CLEAR_TOP 在 onNewWant 清栈、popUpTo 根 inclusive），重复导航的净效果，底部 tab 的 popUpTo 返回语义，覆盖层关闭顺序，未进 Navigation 栈的子组件经 @Entry 转发返回（含 OnBackPressedDispatcher 后登记先问的分发），栈底 NavDestination 的返回接管与源端默认返回（finish 或移到后台）的生命周期效果，按启动来源标志的返回分支
- [hosts](hosts/index.md) — Navigation/@Entry宿主与页面注册（含根 Navigation 默认标题栏与工具栏）、嵌入页取栈、单 Activity 壳内 loadChildFragment 子页的壳内回退栈与嵌入承载、半透明卡片式 Activity 的透明 DIALOG 路由、路由跳板和跨页面共享生命周期，外部入口（推送、快捷方式）宿主导航执行器的可用性守卫；Activity 切换转场按源端迁移（overridePendingTransition(0,0) 关闭，未调用时按主题默认窗口动画），NavHost 四向自定义转场到 customNavContentTransition 与页面绑定，导航目的地内 LocalLifecycleOwner 的 ON_STOP/ON_RESUME 接到 onHidden/onShown；LAUNCHER 路由跳板在进程存活后从桌面重进的再分流，.navDestination 直接传 @Builder，只在 onPause/onSaveInstanceState 存档时接 onHidden
- [parameters](parameters/index.md) — 跳转契约：点击接导航、路由名与参数、默认值/有效性、多个来源入口，以及跳转前共享状态的交接。

## 本级经验

- [把“另起 Activity”的跳转翻成同窗口 push 时补方向隔离：横屏可触发的入口先切到目标页方向，返回后恢复原方向再续做](lesson-17b47c23f2d25008c808.lesson.md)
  - 时机：交互实现阶段，把 Android 启动独立 Activity 的跳转（如登录拦截）翻译成同窗口 Navigation push，且该入口在横屏界面也能触发时
  - 情境：源端页面可在运行时切横屏（setRequestedOrientation），并在其中调用 startActivity、登录拦截等另起页面；被启动 Activity 在 AndroidManifest 有自己的 android:screenOrientation 或未声明；目标用 Navigation 在同一窗口 push，方向由 window.setPreferredOrientation 在窗口级控制。
