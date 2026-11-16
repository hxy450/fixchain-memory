# EventBus 事件的订阅、发布和返回刷新

agent 会看到什么：读到源端 EventBus 的 @Subscribe / onEventMainThread 回调、EventBus.getDefault().post(...)、registerForActivityResult 和 setResult 后 finish；产物里只在 aboutToAppear 刷新一次、子页成功后直接 pop 不发事件、同一次成功两处改栈，或 emit 传 {} 字面量

## 规矩

- rule-b4c57ac33bba｜源端用EventBus订阅事件刷新时，目标在aboutToAppear订阅、aboutToDisappear释放｜读到：源 Fragment 里有 @Subscribe 标注的 onEventMainThread(…Event)（EventBus），如登录成功事件到达后重载账号和列表数据；或规格 AC 的源锚点写着这个回调；写错：目标常驻 Tab 的子组件只在 aboutToAppear 里加载一次数据，没有订阅工程事件总线上对应的事件，aboutToDisappear 里也没有释放
- rule-04f820538e7e｜源页面靠 EventBus @Subscribe 重拉数据时，目标 ViewModel 构造时订阅对应事件并在回调里重拉｜读到：源 Fragment 或 Activity 里有 @Subscribe 方法（登录成功、记录刷新这类事件）和 registerForActivityResult 回调，里面调 ViewModel 重拉统计或列表；写错：目标 ViewModel 只在页面激活时（aboutToAppear 链上）调一次刷新方法，没有订阅会话状态或刷新事件；验收里「源:事件回调 → 标:刷新方法」只落成了丢弃迟到响应的 token
- rule-f1d52d81d371｜Navigation 根页或 Tab 内容要「返回后刷新」时，不靠 aboutToAppear，改用订阅或可见性回调｜读到：规格写「返回主页刷新」「删除后返回主页同步」，首页用 pushPathByName 进入登录、编辑、记录等子页再 pop 返回；写错：首页只在 aboutToAppear 里调激活和刷新，pop 回来后没有任何刷新入口；或订阅回调被页面 inactive 标志丢弃
- rule-b603dcad80b0｜从首页 push 的子流程成功后要发布刷新事件，不只 pop 回首页｜读到：源端子流程（登录、保存记录、删除记录）成功后 EventBus.getDefault().post(刷新事件)，或 setResult 后 finish 让首页的 ActivityResult 回调重拉；写错：目标子页保存或删除成功后直接 pop()，没有发布记录刷新事件
- rule-79b6be36061e｜接线成功导航前先查全局成功事件的订阅，同一次成功只保留一个改动 NavPathStack 的出口｜读到：服务层在返回成功前 emit 全局成功事件（`EVT_*_SUCCESS`），规格里同时有「成功回调导航」和「收到事件后 pop」两条；写错：页面 aboutToAppear 订阅成功事件并在回调里 navPathStack.pop()，成功回调里又 clear() + pushPathByName(…) 或 pop()，同一次成功两次改栈
- rule-11dece72c131｜就绪事件带与平台无关的定时兜底时，采集通道悬置也要照原时长移植兜底｜读到：源端缓存为空时等某个就绪事件才继续；事件的生产者里有 Observable.timer(…, SECONDS) 到时调上送方法，上送方法末尾无条件 EventBus.post(…Event())；写错：目标缓存未命中分支只有 `FWD-REF` 注释、没有代码，把定时兜底和事件发布连同采集源一起悬置；注释称「与 Android 等待语义等价」
- rule-cea76c470d4e｜泛型事件总线 emit 不直接传 {}，先声明载荷接口再传类型化变量｜读到：工程里的事件总线声明成 emit<T extends Object>(name, payload: T)，已有事件都配有导出的载荷接口，调用处先 const payload: <接口> = {…} 再 emit；写错：新增或调用处写成 emit('<事件名>', {}) 或 emit('<事件名>', { … }) 内联对象字面量；新事件名只加进事件名联合类型，没有对应的载荷接口
- rule-98a8a8f68d77｜多个页面订阅同一个全局保存成功事件时，订阅回调先判断是否本入口发起再弹引导｜读到：规格或派工写明保存服务成功时 emit(...) 一个全局成功事件，已有别的页面或组件订阅它弹引导；写错：入口的订阅（on(...)）回调收到成功事件就弹引导，没有判断这次保存是不是本入口发起的
- rule-224e99df309e｜greenrobot EventBus 要同步按引用投递时自建进程内总线，不直接换成 emitter｜读到：源码 `EventBus.getDefault().post(event)` 投递类实例事件，订阅方用 `onEvent` / `onEventMainThread`，订阅回调里还会再 post；写错：目标总线以 `emitter.emit` / `emitter.on` 作传输层承载类实例事件，头注称回调「在发布线程执行」；没有嵌套 post 队列和订阅表快照
- rule-c413cf89e61d｜源码 register(this, priority) 时，目标总线订阅接口保留 priority 形参并在订阅点传入｜读到：源码 `EventBus.getDefault().register(this, 1)` 这类带 priority 的注册；写错：目标总线的订阅 API（如包着 `emitter.on` 的 subscribe）没有 priority 形参，头注写 priority「对本工程订阅方无行为差异，不迁移」，订阅点无优先级可传
- rule-6e479ef79835｜源 Fragment 没有订阅的事件，目标设置组件不要额外订阅来即时刷新｜读到：源 Fragment 全文没有 `onEvent` 订阅，只在 `onResume` 里重读首选项；写错：目标设置组件额外 `on` 了一个事件（如密码移除事件）来即时刷新开关状态
