# Fragment 事务与生命周期迁到 Navigation：按调用点与覆盖类型逐条映射，不压成同步 pop 与 onShown/onHidden

ID：`lesson-dedd435cae5c3c976be2` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与页面实现阶段，把单 Activity 的 FragmentTransaction（replace+addToBackStack、popBackStack(Immediate)、finish）与 onPostCreate、onResume、onPause、onStop、onActivityCreated、onDestroyView 等回调映射到 NavPathStack 与 NavDestination 时

## 适用情境

源 Activity 用一个 fragment_container 承载列表与详情 Fragment：切换时 replace（每次新建 Fragment）并 addToBackStack，详情返回走 popBackStack，外部入口直达时 finish()；Fragment 依赖 onActivityCreated→init 在每次视图创建时重建界面，onResume/onPause 负责注册与挂起。目标用 pushPathByName/pop 与 NavDestination 的 onShown/onHidden/onReady，同名页面可能被栈复用。

## 例外与边界

- 源端以 hide + add 叠加子 Fragment、视图不销毁时，不套用视图重建分支

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

## 来源（按需复核）

- [case-aebac48fa7acdb86e57e](../../../../store/cases/case-aebac48fa7acdb86e57e/aa4810e6d74ae53993bd6b3289dfc890990fa07c4f3c1423c4b210c6b25ef423.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`aa4810e6d74ae53993bd6b3289dfc890990fa07c4f3c1423c4b210c6b25ef423`
