# ui/state/lifecycle

生命周期触发的加载与复位：返回不再走 aboutToAppear、加载入口单飞、监听成对释放、框架会恢复的焦点与状态。

[上一级](../index.md)

## 本级经验

- [ON_STOP 接 onHidden，含导航离开](lesson-19dd006e049c3f9d7563.lesson.md) · 阶段：spec/execute · 信号：LocalLifecycleOwner, LifecycleEventObserver, ON_STOP, ON_RESUME
- [TextInput 获焦回调先判是否用户触摸再写业务状态](lesson-4c476a62732697c56c22.lesson.md) · 阶段：execute · 信号：onFocus, enableKeyboardOnFocus, stopEditing, clearFocus
- [remember 按首次或 key 变才求值](lesson-3b4a96141329db62a6af.lesson.md) · 阶段：execute · 信号：remember {, remember(, derivedStateOf, LaunchedEffect
- [共享单例按键丢弃过期响应，加载入口先单飞不取消上一请求](lesson-c883a0ff96c32dfbd9ba.lesson.md) · 阶段：execute · 信号：onRefreshing, Refresh, @Monitor, aboutToAppear
- [回调迁 ViewModel 逐条迁赋值，开关两条路径都落地](lesson-d7c148c4a233c59ff151.lesson.md) · 阶段：execute · 信号：ON_RESUME, onShown, onPageShow, LifecycleEventObserver
- [每次可见的重载迁 onShown 或订阅](lesson-b3bb0bc33f4caded78a2.lesson.md) · 阶段：execute/converge · 信号：aboutToAppear, onShown, onHidden, onWillShow
- [注册监听存句柄，aboutToDisappear 同引用移除](lesson-14b7f4090b7b83873b22.lesson.md) · 阶段：execute · 信号：addListener, removeListener, aboutToDisappear, aboutToAppear
- [翻译 remember 复位语义时列出框架会恢复的界面态](lesson-1f6e36f8e8bf9df951da.lesson.md) · 阶段：spec · 信号：rememberSaveable, pushPath, NavBar, Tabs
