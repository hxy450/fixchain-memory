# 源端生命周期回调里的副作用

agent 会看到什么：读过的源码里业务基类、Activity 或 Service 的 onCreate / onResume / onPause / onDestroy / onBackPressed 里有埋点、存档计时、状态复位这类副作用；交回的 aboutToAppear / aboutToDisappear / onHidden / stopService 里这些副作用漏了、多挂了，或没复位

## 规矩

- rule-dc05f09aab4d｜源页面继承业务基类时，打开基类把生命周期副作用逐项落到页面回调，未建好就登记 FWD-REF｜读到：源页面类继承应用自己的业务基类（class … : 基类<…>），基类的 onCreate / onResume / onPause / onDestroy / onBackPressed 里有副作用（如页面展示、退出埋点、停留时长），子类只重写一个页面名 getter；写错：目标页面的 aboutToAppear / aboutToDisappear 里没有基类那些副作用的调用，也没有 FWD-REF 占位；只迁了子类文件里显式出现的埋点
- rule-296dec697d76｜存档、计时这类非幂等方法只挂源端同一时机有的调用位，aboutToDisappear 里源端没有的删掉｜读到：源端 save() 按 now − startingTime 累计时长或写统计，只在 onPause / onBackPressed / onSaveInstanceState / Up 调用，onDestroy 里没有；写错：目标页面的 aboutToDisappear() { this.save…() } 和 .onHidden、onBackPressed 共用同一个存档方法，形成双挂或三挂
- rule-aefa1f576e4b｜前台服务 stopSelf 后 onDestroy 复位的语义迁到常驻单例时，stopService 里显式复位状态｜读到：源端停止服务是 `stopForeground(true)` + `stopSelf()`，`onDestroy` 里播放器 shutdown 把状态置为停止，下次启动新建实例；写错：目标常驻单例的 `stopService` 只改了部分状态（如只把未定态归为停止），播完后仍停在播放态，同一集再按播放被「同集在播即忽略」吞掉
- rule-32c8068b25b4｜Activity 的 onPostCreate、onResume、onStop 各自落点，不塞进 onPageShow｜读到：Activity 里 onPostCreate（启动后只跑一次，如引导页或更新日志分流）、onResume（每次回前台，如校验密码或 init）、onStop（注销 EventBus 等订阅）；写错：onPostCreate 和 onResume 的逻辑一起写进 onPageShow()，每次显示都重跑；onStop 没有落点
- rule-19e55b9fd0bf｜Fragment 生命周期按覆盖类型建状态机，不只挂 onShown/onHidden｜读到：Fragment 里 onActivityCreated → init()（每次视图创建都重建）、onResume、onPause 各有逻辑；页面会被另一个 Fragment 替换、被全屏 Activity 或对话框式 Activity 覆盖；写错：NavDestination 只挂 onShown（注释「onResume 等价」）和 onHidden（注释「onPause 等价」），被替换再返回时视图常驻不重建
- rule-4f793cd492dc｜源端应用终止时释放作用域和持有者，目标写 release() 并在 EntryAbility.onDestroy 调用｜读到：源 Application.onTerminate 里依次取消应用协程作用域、shutdown 各状态持有者（如 TTS、播放器）；spec 的 AC 规定应用终止时释放并标了目标符号；写错：EntryAbility 的 onDestroy() 只打日志，没有 release() 接口和调用；持有者还没创建时也没有登记 FWD-REF 占位，信封也没列为未实现
