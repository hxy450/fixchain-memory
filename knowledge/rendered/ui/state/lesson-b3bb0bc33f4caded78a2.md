# 源页面在每次可见时、或由事件订阅与结果回调触发的重新加载，要迁成可见性回调或订阅：Navigation 根页、Tab 内容或经 router 返回的 @Entry 页在子页返回时不会再走 aboutToAppear

## 何时使用

ViewModel 与页面接线阶段，决定目标页由哪些入口触发数据重新加载时；流程闭环阶段从该页新增 push 子流程时；把 Activity 的 onStart/onResume 初始化与只在页面可见时接收的监听映射到 NavDestination 生命周期时

## 适用情境

源 Fragment 用 EventBus @Subscribe（登录成功、记录变化等）和 ActivityResult 回调重拉数据；目标页是 Navigation 下常驻的根内容或 Tab 页，登录、详情等子页用 pushPathByName 覆盖后 pop 返回；工程已有会话状态与应用事件总线。 也包括列表页经 router.pushUrl 打开新增/编辑页，对方保存后 router.back 返回，列表数据只在 aboutToAppear 拉取。也包括源 Activity 在 onStart/onResume 每次可见时重读 Intent、重建列表或校验目录，目标挂在一次性的 onReady/aboutToAppear；以及只应在页面可见时接收的监听（如 NFC 标签监听）挂在 aboutToAppear/aboutToDisappear，被覆盖的页面仍在接收。

## 原因

aboutToAppear 只在组件创建时执行；子页 pop 返回时根页组件没有重建，只在 aboutToAppear 或 activate 里拉数据，等于只加载一次。来源中验收条目写明“源：登录/记录事件 → 标：刷新函数”，实现者却只把它落实成丢弃迟到响应的 token；后续扩展入口的实现者又假设“返回首页会重新刷新”，保存、删除记录也不发刷新事件。真机登录后记录页已有数据，首页统计仍为 0。另一应用中，个人中心是常驻 Tab，接线者没打开源 Fragment、只在 aboutToAppear 加载，规格“登录成功后重载任务数据”的条款没有落实；工程里登录成功事件已有发布方，却没有任何消费者，登录后返回仍显示未登录。 另一应用的地址列表沿用占位版只在 aboutToAppear 加载的写法，新增地址保存返回后列表不变，补 onPageShow 重载后才显示。

## 做法

1. 把源页面所有重新加载的入口列成清单（生命周期回调、事件订阅、结果回调），在目标 ViewModel 为每项写对应订阅（如会话状态订阅、应用事件总线订阅），并确认发布方存在：保存、删除等成功处发布刷新事件。
2. 需要“返回后刷新”时用订阅或 NavDestination 的 onShown 等可见性回调，不依赖 aboutToAppear；订阅在销毁时注销，不因页面暂时不可见的标志而丢弃事件；经 router 返回的 @Entry 页用 onPageShow 重载，并区分首次加载与返回刷新的 loading 状态。重写占位页时不沿用占位版的生命周期写法。
3. onStart/onResume 中的初始化按每次可见映射到 onWillShow/onShown，从后台回前台另由 onShown 的 APP_STATE 原因处理，用“进入子页再返回”“切后台再回前台”两条路径自查；只在可见时应接收的监听在 onShown 登记、onHidden 注销。

## 可选检查

- 登录后返回该页、保存或删除记录后返回该页，数据无需重进即更新。

来源支持：5 张卡 · 4 次迁移 · 4 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕aboutToAppear 只在创建自定义组件的新实例后、build() 之前调用；子页 push 覆盖再 pop 返回时，被覆盖的 NavDestination 和 Navigation 首页内容都没有重建，不会再走 aboutToAppear（被覆盖时触发的是 onWillHide、onHidden 等可见性回调，组件销毁才走 aboutToDisappear）。〔成立范围：对所有 @Component 自定义组件；最常见的不成立情形：页面出栈后重新 push、或 if/else、ForEach 让组件重新创建时，会新建实例并再次调用 aboutToAppear。〕
- 〔适用情境〕Navigation 首页（NavBar，即 Navigation 直接挂载的子节点）不在页面栈中、不具备页面生命周期，收不到 onShown / onHidden；Navigation 内的页面跳转也不会触发所在 @Entry 页的 onPageShow / onPageHide，只有 router 跳转和应用前后台切换会触发。〔成立范围：对放在 Navigation 首页内容区的组件（包括首页里的 Tabs）；最常见的不成立情形：应用切后台再回前台时 @Entry 页的 onPageShow 仍会触发，容易误以为子页 pop 回首页也会触发。〕
- 〔做法第 2 步〕onPageShow / onPageHide 只在 router 路由页面（@Entry 装饰的自定义组件）生效，每次显示 / 隐藏各触发一次，包括 router 跳转返回和应用进入前台 / 后台。〔成立范围：对 @Entry 页面（含 router.back 回到的上一页）；Navigation 里的 NavDestination 页面用 onShown / onHidden；最常见的不成立情形：写在被 @Entry 页引用的普通 @Component 里，不会被调用。〕
- 〔做法第 3 步〕NavDestination 的 onWillShow 在布局显示前执行、应用切到前台时不执行；onShown 在显示后执行，push 进入、上层页出栈露出和应用回前台都会触发；onWillHide 在应用切到后台时不执行，onHidden 在被新页覆盖、出栈或应用切后台时都会触发。从 API 21 起 onShown / onHidden 带 VisibilityChangeReason：TRANSITION（页面跳转）、CONTENT_COVER（全模态开关）、APP_STATE（前后台切换）。〔成立范围：对 NavDestination 的可见性回调；API 21 之前回调没有原因参数；被 NavDestinationMode.DIALOG 页覆盖或它出栈时，下层页这四个回调都不触发（只触发 onInactive / onActive）；最常见的不成立情形：把 onResume 式的每次可见初始化只挂在 onWillShow，从后台回前台时不会执行。〕
- 〔适用情境〕Tabs 中已经显示过的 TabContent 之后被切走时不会销毁，切回时不重建、不再走 aboutToAppear；TabContent 的 onWillShow（API 12 起）在首次显示、Tab 切换、页面切换和窗口前后台切换时触发，onWillHide 在 Tab 切换、页面切换和窗口前后台切换时触发。〔成立范围：对 Tabs 的子组件 TabContent，Stage 模型；最常见的不成立情形：按文档懒加载示例自行释放内容时，内容会重建。〕
- 〔做法第 1 步〕NavDestination 的 onResult（API 15 起）在从其他 NavDestination 通过 pop 或侧滑返回到本页时执行，回调参数是 pop 时带回的结果。〔成立范围：对 NavDestination 页面；最常见的不成立情形：要刷新的是 Navigation 首页内容（NavBar 不是 NavDestination）时收不到。〕
