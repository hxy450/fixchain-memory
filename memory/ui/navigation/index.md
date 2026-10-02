# ui/navigation

页面导航：先确定宿主和注册方式，再处理参数与跳转契约，或返回键与栈变更；同窗口 push 替代另起 Activity 时的窗口方向切换与恢复。

[上一级](../index.md)

## 子主题

- [back-stack](back-stack/index.md) — 系统/页面返回、覆盖层关闭顺序、清栈重建与重复导航的净效果，底部 tab 的 popUpTo 返回语义与外部深链的清栈。
- [hosts](hosts/index.md) — Navigation/@Entry宿主与页面注册（含根 Navigation 默认标题栏与工具栏）、嵌入页取栈、路由跳板和跨页面共享生命周期，外部入口（推送、快捷方式）宿主导航执行器的可用性守卫。
- [parameters](parameters/index.md) — 跳转契约：点击接导航、路由名与参数、默认值/有效性、多个来源入口，以及跳转前共享状态的交接。

## 本级经验

- [把“另起 Activity”的跳转翻成同窗口 push 时补方向隔离：横屏可触发的入口先切到目标页方向，返回后恢复原方向再续做](lesson-17b47c23f2d25008c808.lesson.md)
  - 时机：交互实现阶段，把 Android 启动独立 Activity 的跳转（如登录拦截）翻译成同窗口 Navigation push，且该入口在横屏界面也能触发时
  - 情境：源端页面可在运行时切横屏（setRequestedOrientation），并在其中调用 startActivity、userService.login 等另起页面；目标用 Navigation 在同一窗口 push，方向由 window.setPreferredOrientation 在窗口级控制，目标页按竖屏设计。
