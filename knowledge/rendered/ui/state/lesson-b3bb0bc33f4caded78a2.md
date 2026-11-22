# 源页面在每次可见时、或由事件订阅与结果回调触发的重新加载，要迁成可见性回调或订阅：Navigation 根页、Tab 内容或经 router 返回的 @Entry 页在子页返回时不会再走 aboutToAppear

## 何时使用

ViewModel 与页面接线阶段，决定目标页由哪些入口触发数据重新加载时；流程闭环阶段从该页新增 push 子流程时；把 Activity 的 onStart/onResume 初始化与只在页面可见时接收的监听映射到 NavDestination 生命周期时

## 适用情境

源 Fragment 用 EventBus @Subscribe（登录成功、记录变化等）和 ActivityResult 回调重拉数据；目标页是 Navigation 下常驻的根内容或 Tab 页，登录、详情等子页用 pushPathByName 覆盖后 pop 返回；工程已有会话状态与应用事件总线。 也包括列表页经 router.pushUrl 打开新增/编辑页，对方保存后 router.back 返回，列表数据只在 aboutToAppear 拉取。也包括源 Activity 在 onStart/onResume 每次可见时重读 Intent、重建列表或校验目录，目标挂在一次性的 onReady/aboutToAppear；以及只应在页面可见时接收的监听（如 NFC 标签监听）挂在 aboutToAppear/aboutToDisappear，被覆盖的页面仍在接收。

## 例外与边界

- 每次进入都重新 push 创建的页面（不是返回到栈里已有的实例），aboutToAppear 每次都会执行，首次加载放在里面即可，不在这条的改动范围内。
- 按 Ability 注册的能力（如 NFC 前台派发 registerForegroundDispatch）不随单个页面开关：注册放在 Ability 的前后台回调里，页面只在 onShown/onHidden 登记、注销自己的接收；不要让某个页面的 onHidden 注销整个应用的派发。

## 原因

aboutToAppear 只在组件创建时执行；子页 pop 返回时根页组件没有重建，只在 aboutToAppear 或 activate 里拉数据，等于只加载一次。来源中验收条目写明“源：登录/记录事件 → 标：刷新函数”，实现者却只把它落实成丢弃迟到响应的 token；后续扩展入口的实现者又假设“返回首页会重新刷新”，保存、删除记录也不发刷新事件。真机登录后记录页已有数据，首页统计仍为 0。另一应用中，个人中心是常驻 Tab，接线者没打开源 Fragment、只在 aboutToAppear 加载，规格“登录成功后重载任务数据”的条款没有落实；工程里登录成功事件已有发布方，却没有任何消费者，登录后返回仍显示未登录。 另一应用的地址列表沿用占位版只在 aboutToAppear 加载的写法，新增地址保存返回后列表不变，补 onPageShow 重载后才显示。

## 做法

1. 把源页面所有重新加载的入口列成清单（生命周期回调、事件订阅、结果回调），在目标 ViewModel 为每项写对应订阅（如会话状态订阅、应用事件总线订阅），并确认发布方存在：保存、删除等成功处发布刷新事件。
2. 需要“返回后刷新”时用订阅或 NavDestination 的 onShown 等可见性回调，不依赖 aboutToAppear；页面是 Navigation 首页内容（不是 NavDestination）时没有 onShown，用订阅；订阅在销毁时注销，不因页面暂时不可见的标志而丢弃事件；经 router 返回的 @Entry 页用 onPageShow 重载，并区分首次加载与返回刷新的 loading 状态。重写占位页时不沿用占位版的生命周期写法。
3. onStart/onResume 中的初始化按每次可见映射到 onWillShow/onShown，从后台回前台另由 onShown 的 APP_STATE 原因处理，用“进入子页再返回”“切后台再回前台”两条路径自查；只在可见时应接收的监听在 onShown 登记、onHidden 注销。

## 可选检查

- 登录后返回该页、保存或删除记录后返回该页，数据无需重进即更新。

来源支持：5 张卡 · 4 次迁移 · 4 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕aboutToAppear 在自定义组件新实例创建后、执行其 build() 之前调用；实例没有重建就不会再次调用
- 〔做法第 2 步〕onPageShow 只对 @Entry 装饰的自定义组件（router 页面）生效，页面每次显示时触发一次，包括路由跳转、应用进入前台等场景
- 〔做法第 2 步〕aboutToDisappear 在自定义组件析构销毁之前执行，不允许在其中改变状态变量；在其中用 async await 等异步操作会让组件留在闭包里，阻止垃圾回收
- 〔做法第 3 步〕NavDestination 的 onWillShow 在组件布局显示之前执行，应用切换到前台时不执行（API 12 起）
- 〔做法第 2、3 步〕NavDestination 的 onShown 在组件布局显示之后执行；回调带 VisibilityChangeReason 参数的这一版声明自 API 21 起
- 〔做法第 3 步〕NavDestination 的 onHidden 在组件隐藏后执行：所在页被新 push 进栈的页面覆盖、栈顶页面 pop 出栈或应用切换到后台时都会触发
- 〔做法第 3 步〕VisibilityChangeReason（API 21 起）：TRANSITION 表示页面跳转引起的可见性变化，CONTENT_COVER 表示全模态开启、关闭引起的，APP_STATE 表示前后台切换引起的
- 〔做法第 3 步〕NavDestination 的 onReady 在 NavDestination 即将构建子组件时调用，不随页面每次可见重新调用
- 〔适用情境 / 做法第 3 步〕安卓 Activity.onStart 在 onCreate 之后、或停止后经 onRestart 重新显示给用户时调用，不是一次性回调
- 〔适用情境 / 做法第 3 步〕安卓 NfcAdapter.enableForegroundDispatch 只能在主线程、Activity 处于前台（resumed）时调用，Activity 要在 onPause 中调用 disableForegroundDispatch
- 〔做法第 3 步〕tag.registerForegroundDispatch 的 elementName 必须包含 bundleName 和 abilityName，前台派发按 Ability 注册，不按页面
- 〔原因〕Navigation 下常驻的 Tab 根内容被 pushPathByName 推入的登录等子页覆盖、再 pop 返回时，根内容组件的 aboutToAppear 没有再次触发（真机）
- 〔原因〕经 router.pushUrl 打开新增页、保存后 router.back 返回的 @Entry 列表页，aboutToAppear 没有再次执行，只在 aboutToAppear 里拉取的列表不更新
- 〔适用情境 / 做法第 3 步〕标签订阅放在 aboutToAppear 登记、aboutToDisappear 注销时，页面被 push 进来的新页面覆盖后仍在接收标签事件
