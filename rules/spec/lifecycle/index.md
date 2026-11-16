# 生命周期与配置重建

读到 Activity 的 onCreate、onResume、onPause、onSaveInstanceState、getLastNonConfigurationInstance、configChanges，Compose DisposableEffect、LifecycleEventObserver，或 Application 初始化链，规格里写生命周期映射、存档和刷新时机、配置变化重建时

## 触发族

- [Activity 的 configChanges 和配置变化重建](config-changes-recreate/index.md)（7 条）：读过的 AndroidManifest 里 activity 没写 android:configChanges 或不含 orientation，源码有 onSaveInstanceState、直接 show 的对话框或点击后改过的视图；交回的规格没写配置变化重建后哪些状态保留、哪些回到初值
- [源端挂在生命周期回调上的释放和移交](lifecycle-dispose-handoff/index.md)（5 条）：源端在 DisposableEffect / onDispose、LifecycleEventObserver 的 ON_STOP / ON_RESUME 或引擎的 onStop() / onResume() 里做释放、移交、暂停，规格里写成「页面销毁」「退后台」「停摆」，没写 owner、触发路径和目标端的调用位
- [Activity 的 NonConfigurationInstance 续存分支](non-config-instance/index.md)（2 条）：读到 Activity.onCreate 先取 getLastCustomNonConfigurationInstance() / getLastNonConfigurationInstance()，为 null 才按启动参数分支；规格或验收条目写成「已有实例时忽略启动参数」「单例天然续存」，没分配置重建和各入口
- [Application 初始化链里注册的 BroadcastReceiver](init-chain-receiver/index.md)（1 条）：读到 Application 初始化链里 registerReceiver 注册 BroadcastReceiver（如 CONNECTIVITY_ACTION），或上游契约点名某接收器触发业务；feature 规格的锚点、数据流和 AC 里没有这个触发入口
- [源 Activity 的存档触发回调](save-trigger-callbacks/index.md)（1 条）：读到源 Activity 只在 onPause、onBackPressed、onSaveInstanceState、标题栏 Up 里调 save()，onDestroy 不存档；规格的转换决策写「onHide / aboutToDisappear 等价钩子」，没写哪些回调不存档
- [源 Activity 和业务基类生命周期回调里的刷新和副作用](activity-callback-effects/index.md)（2 条）：读到源页面只在 onCreate、onNewIntent 里刷新（没有 onResume 刷新），或业务基类的 onPostCreate / onResume 里先 findViewById 判空、instanceof 或标志位守卫再做淡入等副作用；规格把它映射成 onActive / 回到前台即刷新，或在基类副作用表里写成无条件表项
- [System.exit 一类的应用「重启」](system-exit-restart/index.md)（3 条）：读到源方法体是 System.exit(0)、Runtime.exit 或 Process.killProcess、注释写「full app restart」，调用点在通知点击、语言切换、数据恢复之后，或同一个源方法被几份规格引用；规格的服务层契约写「忠实迁移 = 退出应用（terminateSelf），不附加重启」，source-notes 没登记它和源码注释的差异
- [相机打开回调里读的一次性入口标志](camera-open-entry-flag/index.md)（1 条）：读到源端在相机打开或预览建立的回调里读桌面小部件、快捷入口置位的一次性拍照标志并读后即清；规格 AC 正文写「相机打开完成后读取」，`标:` 锚点和对接点却写成 aboutToAppear / onPageShow，计划的 cross_slice_edits 挂到页面生命周期
- [onCreate 里同步语句和组合、挂载的先后](oncreate-sync-ordering/index.md)（2 条）：读到 Activity.onCreate 里 setContent { … } 之后还有写同一状态的语句、组合内 LifecycleEventEffect / LaunchedEffect 读它，或 onCreate 里 findViewById 取到 View 后立即调用；规格按源码行序写读写先后，或共享组件的句柄契约没写宿主最早何时可用
