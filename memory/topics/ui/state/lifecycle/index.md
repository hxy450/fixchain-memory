# ui/state/lifecycle

生命周期触发的加载与复位：返回不再走 aboutToAppear、加载入口单飞、监听成对释放、框架会恢复的焦点与状态。

[上一级](../index.md)

## 本级经验

- [TextInput 获焦回调先判是否用户触摸再写业务状态](lesson-4c476a62732697c56c22.lesson.md) · 阶段：execute · 信号：onFocus, enableKeyboardOnFocus, stopEditing, clearFocus
- [共享单例按键丢弃过期响应，加载入口先单飞不取消上一请求](lesson-c883a0ff96c32dfbd9ba.lesson.md) · 阶段：execute · 信号：onRefreshing, Refresh, @Monitor, aboutToAppear
- [回调迁 ViewModel 逐条迁赋值，开关两条路径都落地](lesson-d7c148c4a233c59ff151.lesson.md) · 阶段：execute · 信号：ON_RESUME, onShown, onPageShow, LifecycleEventObserver
- [注册监听存句柄，aboutToDisappear 同引用移除](lesson-14b7f4090b7b83873b22.lesson.md) · 阶段：execute · 信号：addListener, removeListener, aboutToDisappear, aboutToAppear
- [翻译 remember 复位语义时列出框架会恢复的界面态](lesson-1f6e36f8e8bf9df951da.lesson.md) · 阶段：spec · 信号：rememberSaveable, pushPath, NavBar, Tabs
- [重载入口改订阅，子页返回不触发 aboutToAppear](lesson-b3bb0bc33f4caded78a2.lesson.md) · 阶段：execute/converge · 信号：aboutToAppear, onShown, onPageShow, pushPathByName
