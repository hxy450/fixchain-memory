# ui/navigation/back-stack

返回键与栈变更：覆盖层逐层关闭、按启动来源的返回分支、子组件拦截返回、清栈重建与重复导航的净效果。

[上一级](../index.md)

## 本级经验

- [tab 与深链的返回栈后果写验收并显式实现](lesson-39f137ee173e50363f79.lesson.md) · 阶段：spec/execute · 信号：popUpTo, saveState, restoreState, launchSingleTop
- [同一成功多条导航响应只保留一个导航出口](lesson-683d8f5070802c518020.lesson.md) · 阶段：spec/execute · 信号：FLAG_ACTIVITY_NEW_TASK, finish(), startActivity, NavPathStack
- [回根重建返回栈用 clear() 不用 pop()](lesson-96c890012b26b5cb32cd.lesson.md) · 阶段：execute · 信号：popUpTo, navPathStack.clear(), pop(), NavPathStack
- [子组件拦截返回由 @Entry onBackPress 转调](lesson-803ba029eea852122e77.lesson.md) · 阶段：execute · 信号：PredictiveBackHandler, BackHandler, onBackPress, @Event
- [宿主 onBackPressed 自顶向下关闭页内覆盖层](lesson-396d54479492828eeea3.lesson.md) · 阶段：execute · 信号：onBackPressed, onDismissRequest, BackHandler, ModalBottomSheet
- [返回按钮与系统返回共用分支按来源标志处理不默认 pop](lesson-f19632971e470d55c543.lesson.md) · 阶段：execute · 信号：isFromSplash, onBackPressed, pop(), NavDestination
