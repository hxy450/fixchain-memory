# 源端生命周期观察者的 ON_STOP 移交，规格先写清 owner 是谁，再逐条写进入 ON_STOP 的用户路径

审的是：规格
触发（任一种）：
- 读到：Compose 里 DisposableEffect(LocalLifecycleOwner.current) 注册 LifecycleEventObserver，ON_STOP 时移交后台、ON_RESUME 时取回，而这个 Composable 是导航路由的目的地；写错的样子：规格把它写成「前后台移交」「退后台移交」，验收只有「退后台再回前台」一个场景，没写 owner 是谁，也没写返回出栈、跳到其他目的地同样触发
适用范围：规格提取阶段翻译源端经 LifecycleEventObserver / DisposableEffect(lifecycleOwner) 挂的 ON_STOP / ON_RESUME 触发契约时
做法：
- 先确认并写明 owner 是谁（Activity、进程、NavBackStackEntry）；导航目的地里的 LocalLifecycleOwner.current 是返回栈条目
- 把让它进入 ON_STOP / ON_RESUME 的用户路径逐条写成触发契约和验收条目：退后台、返回出栈、跳到其他目的地、回到本页，不用「退后台 / 前后台」一笔带过
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- navigation-compose 目的地内的 LocalLifecycleOwner 是返回栈条目，返回出栈或跳到其他目的地时同样进入 ON_STOP：移交触发不只是应用退后台（出处：卡里修好并验证过）
- onHidden 在非栈顶页面 push 进栈、栈顶页面 pop 出栈或应用切到后台时执行：目标端能一并覆盖这几条用户路径的事件，可写进触发映射（出处：arkts-navigation-navdestination.md，页面生命周期）
未核实：导航离开时 ON_STOP 先于观察者注销，依据的是修复期对 navigation-compose 2.9.1 源码的查证，没在设备上复现
来源：1 张卡，1 个应用
- case-1f17a64b74c60410dad7（Cofi）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 1 ← 诊断
