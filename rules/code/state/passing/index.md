# 跨页面与跨组件的状态传递

源端有多页共用的 ViewModel、EventBus 的 post / @Subscribe 和 setResult 回传、Activity 在 setContent 里下传的设置、共享页头、子 Composable 和子组件的状态参数，目标端有 AppStorageV2 / PersistenceV2.connect、@Param / @Event、@Builder 值参、事件 emit 和返回后刷新时

## 触发族

- [多参数 @Builder 的状态值参](builder-state-arg/index.md)（5 条）：读到 Compose 子 Composable 以状态算出的 enabled、颜色等作参数，或搬来的 @Builder 片段参数随状态变；产物里 @Builder 带 enabled: boolean 这类值参、调用处传 this.count > 1 一类状态表达式
- [EventBus 事件的订阅、发布和返回刷新](event-bus-refresh/index.md)（11 条）：读到源端 EventBus 的 @Subscribe / onEventMainThread 回调、EventBus.getDefault().post(...)、registerForActivityResult 和 setResult 后 finish；产物里只在 aboutToAppear 刷新一次、子页成功后直接 pop 不发事件、同一次成功两处改栈，或 emit 传 {} 字面量
- [AppStorageV2 / PersistenceV2 的 connect 调用](appstoragev2-connect/index.md)（4 条）：产物里 AppStorageV2.connect、PersistenceV2.connect / globalConnect 的 key 写法和放在 static 初始化器里的调用，以及该取共享实例的页面 new 了私有实例
- [共享 ViewModel 拆成页面实例后的状态下传](split-shared-viewmodel/index.md)（4 条）：读到经 AppStorageV2.connect 由各页 getInstance() 共用的 ViewModel；产物里改成各页 new ViewModel()，跨页的筛选状态靠 @Param + @Monitor 或显式传参下传
- [共享页头传递的视觉字段](shared-header-state/index.md)（1 条）：读到安卓共享页头绑定同时设名称、图标、按条目颜色的浅色背景和 setColorFilter 着色；产物里页头回调、页头更新方法和主容器的 @State 只带 id、title、icon，没带 color
- [子组件内部创建的 ViewModel 和页面的注入点](child-created-viewmodel/index.md)（1 条）：读到占位登记或派工要求页面给覆盖层、子组件的 ViewModel 注入数据源，而这个 VM 由子组件在内部 new 出来；产物里页面只写 Overlay({ … }) 一类构造，子组件没有 @Param / @Event 回调把内部 VM 交给页面
- [Activity 壳层经 setContent 下传的设置和派生结果](shell-passed-settings/index.md)（3 条）：读到源 Activity 在 setContent 里从设置存储读出设置、或在顶层算出派生结果（如 设置.toEnum<…>().isActive(…)），作为 Composable 参数下传各路由，同文件 @Preview 另给示例实参；产物里页面另存一块本地设置字段、取 @Preview 的实参当初值、只在 aboutToAppear 取一次快照，或各页自己写 !== 0 / === 1 重算
