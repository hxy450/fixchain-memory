# ui/navigation/hosts

Navigation/@Entry 宿主与页面注册：栈来源、首屏压栈、路由跳板、默认标题栏、外部入口守卫与跨页生命周期。

[上一级](../index.md)

## 本级经验

- [NavDestination 首屏只注册并压栈不作根内容](lesson-8953e390416a80d7dd8c.lesson.md) · 阶段：execute/converge · 信号：Builder function is empty, current stack is not navPathStack, navDestination, NavDestinationContext
- [main_pages 只登记路由页，子组件和弹窗不登记](lesson-c4a6eaaf6a22c0b8823f.lesson.md) · 阶段：execute/repair · 信号：main_pages.json, 10905402, @CustomDialog, router.pushUrl
- [外部入口导航守卫按目标已注册判断不查栈成员](lesson-1b05b8d5cc528d5dc5bc.lesson.md) · 阶段：execute · 信号：isIntentAvailable, pushPathByName, pageMap, EntryAbility
- [多屏共享清理归外层生命周期，切屏不释放](lesson-2ed8c21943925bf0ae9a.lesson.md) · 阶段：spec/plan/execute · 信号：DisposableEffect, onDispose, EntryAbility.onDestroy, aboutToDisappear
- [嵌入子页只用 @Consumer 注入的根栈](lesson-1cebb531c991239d2691.lesson.md) · 阶段：execute · 信号：@Consumer('navPathStack'), context.pathStack, onReady, @Provider
- [根 Navigation 显式隐藏默认标题栏与工具栏](lesson-69e07207a06a8a8a7ba9.lesson.md) · 阶段：execute · 信号：hideTitleBar, hideToolBar, NavBarContent, Scaffold
- [进入即跳转并 finish 的页面按路由跳板处理](lesson-0b72c197ea20fbe6f277.lesson.md) · 阶段：execute · 信号：finish(), startActivity, initView, onCreate
