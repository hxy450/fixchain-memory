# Fragment 事务与生命周期迁到 Navigation：按调用点与覆盖类型逐条映射，不压成同步 pop 与 onShown/onHidden

## 何时使用

规格提取与页面实现阶段，把单 Activity 的 FragmentTransaction（replace+addToBackStack、popBackStack(Immediate)、finish）与 onPostCreate、onResume、onPause、onStop、onActivityCreated、onDestroyView 等回调映射到 NavPathStack 与 NavDestination 时

## 适用情境

源 Activity 用一个 fragment_container 承载列表与详情 Fragment：切换时 replace（每次新建 Fragment）并 addToBackStack，详情返回走 popBackStack，外部入口直达时 finish()；Fragment 依赖 onActivityCreated→init 在每次视图创建时重建界面，onResume/onPause 负责注册与挂起。目标用 pushPathByName/pop 与 NavDestination 的 onShown/onHidden/onReady，同名页面可能被栈复用。

## 例外与边界

- 源端以 hide + add 叠加子 Fragment、视图不销毁时，不套用视图重建分支
- 「replace 恒新实例」以源端每次 replace 都新建 Fragment 为前提；调用点传入的是缓存复用的同一个 Fragment 对象时，返回后实例字段仍在、只重建视图，按这一点映射，不改成 NEW_INSTANCE 新建页面。
- 用 VisibilityChangeReason 区分覆盖类型要求 API 21 及以上；工程最低 API 低于 21 时 onShown、onHidden 不带这个参数，只用 navDestinationSwitch 的目标页与窗口焦点事件区分。

## 原因

FragmentManager 的各事务语义不同：replace 每次新建实例；popBackStack 排到下一轮执行，栈中只剩根时不做任何事；popBackStackImmediate 同步出栈；finish() 结束整个 Activity，不是出栈。Fragment 被 replace 覆盖时视图销毁（onDestroyView），返回时经 onActivityCreated→init 重建；被全屏 Activity 覆盖走 onPause/onStop，被对话框式或外部窗口遮挡只 onPause。NavPathStack 默认推入模式在同帧 pop 后再 push 同名页时会复用栈中实例（已观察新页 onReady 不触发），NavDestination 页面也始终常驻；压成一次同步 pop/push 与 onShown/onHidden 两个挂点，会漏掉新实例、视图重建、注销与结束应用这些可观察结果。

## 做法

1. 按源端每个事务与退出调用点列分支，逐条写目标调用：replace + addToBackStack（恒新实例）用 pushPath(info, { launchMode: LaunchMode.NEW_INSTANCE })；popBackStackImmediate + replace 先同步出栈再按新实例压栈；popBackStack 排到下一轮执行，栈深只剩根页时为空操作；finish() 按结束 Activity 实现（例：在提示时长后 terminateSelf，期间屏蔽输入；源端依赖进程内静态状态在下次进入时保留的，改为 moveAbilityToBackground 并复位页面实例态），不写成 pop。“退化为 pop”“由 NavPathStack 天然保留”一类注释不算实现，做不到就登记占位。
2. 生命周期按覆盖类型建状态机并分别落点：被 Fragment 页替换 → onPause + onDestroyView，返回时重走 onActivityCreated→init 重建视图；被全屏 Activity 页覆盖 → onPause + onStop；被对话框式或外部 Activity 遮挡 → 仅 onPause；回到本页 → onResume。用 uiObserver 的 navDestinationSwitch 目标页、窗口焦点事件与 onShown/onHidden 的 VisibilityChangeReason 区分覆盖类型。
3. onPostCreate 只执行一次、onResume 每次回前台执行、onStop 中注销订阅，各自落点，不合并进一个页面显示回调；同工程其他页已有的 onResume→onShown 写法不作依据，按本页源码的全部回调对照。
4. 规格提取时把事务与生命周期写成独立验收项：返回后的视图重建、onDestroyView 的销毁、finish 与 popBackStack 的区别、同名页面能否复用，不只写“onResume → onPageShow”“切换详情 → pushPathByName”。

## 可选检查

- 同名页面二次进入时确认新实例的 onReady 触发；检索目标页的 pop() 与 pushPathByName() 调用，与源端 finish、popBackStack、replace 调用点一一对照。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕FragmentManager.popBackStack() 是异步的：只把出栈请求排队，等应用回到事件循环时才执行
- 〔原因 / 做法第 1 步〕FragmentManager.popBackStackImmediate() 在调用内立即执行出栈，效果相当于随后调用 executePendingTransactions
- 〔原因 / 做法第 2 步〕Fragment.onDestroyView 在 onCreateView 创建的视图已从 Fragment 分离时调用；下次这个 Fragment 要显示时会创建新视图
- 〔做法第 3 步〕Activity.onPostCreate 在 Activity 启动完成时调用（onStart、onRestoreInstanceState 之后），随创建走一次；onResume 则在每次回到前台时调用
- 〔原因 / 做法第 1 步〕NavigationOptions.launchMode 没有另设时为 LaunchMode.STANDARD；NEW_INSTANCE 与 STANDARD 相比不复用栈中的同名实例，新建页面默认执行 push 动效
- 〔原因〕设备上同一帧内先 pop 再 pushPathByName 同名页面（默认 STANDARD 模式）时，复用了栈中的同名 NavDestination 实例，新页的 onReady 不触发
- 〔做法第 1 步〕NavPathStack.pop() 返回出栈的栈顶 NavPathInfo；栈为空时返回 undefined
- 〔做法第 1 步〕UIAbilityContext.terminateSelf() 销毁当前 UIAbility，不是路由栈的出栈
- 〔做法第 2 步〕NavDestination 的 onShown、onHidden 自 API 21 起带 VisibilityChangeReason：TRANSITION 表示页面跳转、CONTENT_COVER 表示全模态的开启和关闭、APP_STATE 表示前后台切换引起的可见性变化
- 〔做法第 2 步〕Window.on('windowEvent') 回调的 WindowEventType 中 WINDOW_ACTIVE 表示窗口获焦、WINDOW_INACTIVE 表示失焦
