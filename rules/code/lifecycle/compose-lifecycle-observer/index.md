# Compose 的生命周期观察者和 DisposableEffect

agent 会看到什么：读到源端 DisposableEffect 里的 LifecycleEventObserver（ON_RESUME、ON_STOP）或 onDispose；交回的代码只在 aboutToDisappear 里 dispose / stop，没有 onShown、onHidden，或刷新方法漏了回调里的赋值

## 规矩

- rule-8fa3803a0a87｜把 ON_RESUME 观察者迁进 ViewModel 刷新方法时，回调里的每个赋值都迁，含授权后隐藏插页｜读到：Compose 界面的 Lifecycle.Event.ON_RESUME 观察者重查权限，权限新获得时把 remember 的插页显隐状态置 false（注释如 Permission was granted, dismiss permission screen）；写错：ViewModel 的刷新方法只更新授权标志，由 NavDestination 的 onShown 或 onPageShow 调用，没有授权后把插页状态置 false；拒绝分支置 true 却已迁
- rule-d567d8e41596｜页面离开要销毁引擎时先调移交入口 onStop 再 dispose，onShown 时调 onResume｜读到：引擎类公开 onStop()/onResume() 生命周期入口；源端 DisposableEffect(LocalLifecycleOwner.current) 里的 LifecycleEventObserver 在 ON_STOP 移交后台、ON_RESUME 取回；写错：NavDestination 页的 aboutToDisappear 只调 engine.dispose()，没有 .onShown / .onHidden，engine.onStop() 在工程里没有调用方
- rule-aaa793a4d538｜共享播放服务不在页面 aboutToDisappear 里 stop，页面离开只解除监听，Ability 销毁时停止｜读到：源端 DisposableEffect 的 onDispose 挂在承载多屏的外层 Composable 上，切屏只改状态变量；写错：页面的 aboutToDisappear() / onDisappear() 里调用 dispose() 或共享播放服务的 stop()
- rule-e619f8cd6211｜Lifecycle ON_PAUSE/ON_RESUME 暂停恢复，目标同时接应用前后台和页面显隐两类回调｜读到：源端观察 Lifecycle.Event.ON_PAUSE / ON_RESUME 暂停、恢复播放；写错：只接了 NavDestination 的 onHidden / onShown（或 onPageHide / onPageShow），应用切后台时不暂停
