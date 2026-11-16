# 前台服务 stopSelf 后 onDestroy 复位的语义迁到常驻单例时，stopService 里显式复位状态

审的是：代码
触发（任一种）：
- 读到：源端停止服务是 `stopForeground(true)` + `stopSelf()`，`onDestroy` 里播放器 shutdown 把状态置为停止，下次启动新建实例；写错的样子：目标常驻单例的 `stopService` 只改了部分状态（如只把未定态归为停止），播完后仍停在播放态，同一集再按播放被「同集在播即忽略」吞掉
适用范围：把 Android 前台服务的停止生命周期迁到常驻的播放单例时
做法：
- 在 stopService 里显式完成源端 shutdown 的复位：播放状态置为停止态、清掉「准备好就开播」一类的待办标记、作废在途装载
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- stopSelf：停止已启动的服务，等同对该服务调用 Context#stopService：源端停止后会走到 onDestroy（出处：android.app.Service#stopSelf）
- onDestroy：服务不再使用、将被移除时由系统调用，返回后这个 Service 对象不再被调用：源端每次停止后对象作废，下次启动是新实例；常驻单例要手动复位（出处：android.app.Service#onDestroy）
针对本应用要查的：
- 源端 shutdown 时复位了哪些状态：源工程里服务 onDestroy 调用的播放器 shutdown / release 方法；逐项列出它置的状态和清掉的标记，在目标 stopService 里照做
来源：1 张卡，1 个应用
- case-0b0bf6cdf94608e17cbb（AntennaPod）：做法第 1 步 ← 建议 4、诊断
