# 页面导航与标题栏

源端有 startActivity / Intent、跳板 Activity 和透明主题的 Activity、Fragment 事务、Compose Navigation、onBackPressed、Activity 切换转场、Toolbar / ActionBar、DrawerLayout，目标端有 Navigation、NavDestination、NavPathStack、router.pushUrl、pageTransition、自绘标题栏时

## 子主题

- [外部入口与深链](external/index.md)（45 条）：源端有 intent-filter 深链、onNewIntent、PendingIntent、TaskStackBuilder，或交给外部应用的 ACTION_VIEW / ACTION_SEND / Settings Intent，目标端有 EntryAbility 的 onNewWant、want.uri、startAbility 的 Want、WantAgent、systemShare 时
- [页面和组件的入参](params/index.md)（24 条）：源端有 Intent 的 putExtra / get…Extra、Bundle、Fragment 的 setArguments / newInstance / navArgs，目标端有路由参数对象、NavDestination 取参、子组件的 @Param 时
- [标题栏、抽屉与菜单](titlebar/index.md)（61 条）：源端有 Toolbar / ActionBar、onCreateOptionsMenu、setDisplayHomeAsUpEnabled、DrawerLayout、CollapsingToolbarLayout、Compose TopAppBar，目标端有自绘标题栏、NavDestination 的 title / menu、hideTitleBar 时

## 触发族

- [点击入口跳到哪一页](entry-destinations/index.md)（14 条）：读到源端点击监听里 startActivity(Intent) 到别的 Activity、工厂按类型分给不同 Fragment、工具栏各按钮各自的 setOnClickListener、SDK 弹窗配置里的各个回调；产物里入口的 onClick 有没有 pushPathByName / router.pushUrl 到对的页、注册了路由，还是只有 Toast 或 FWD-REF 占位
- [跳转前后的附带动作](navigation-side-effects/index.md)（4 条）：读到源端 startActivity 之前写共享状态（播放队列、Store）、点击浮层只跳转不动队列、激励广告回调之后才导航；产物里 push 前后少了或多了动作：没写队列、清空了队列、只写 Store 不 push、能力不可用时直接 return
- [异步结果回来后的跳转和提示](result-branches/index.md)（6 条）：读到源 Activity / ViewModel 的成功、失败回调（LiveData observe、Handler.post 回 UI）里的 startActivity、finish、Toast，以及启动 ViewModel 的下一路由决策；产物里替换 FWD-REF 或占位按钮后的结果消费（await、@Monitor）、catch 里的提示、aboutToDisappear 之后的 destroyed 短路、push 到首屏自身
- [开头即跳走的跳板 Activity](trampoline-activity/index.md)（2 条）：读到 Activity 的 onCreate / initView 开头不经操作就 startActivity 到别的页并 finish()，或调用方 Intent 指向这种 Activity；产物里把它渲染成可停留的页、跳转放进按钮 onClick，或 pushPathByName 到它对应的页
- [源 Activity 的切换转场](activity-transition/index.md)（3 条）：读到源端 startActivity / finish 切换的 Activity 带 overridePendingTransition 或主题 windowAnimationStyle 的切换动画，交回的代码在 @Entry 页的 pageTransition() 或 NavPathStack 的 push / replace 调用里定转场
- [Navigation 入口和首屏的挂载](navigation-entry/index.md)（7 条）：入口页的 Navigation(...) { } 内容槽里放了什么、有没有 hideNavBar、navDestination 怎么注册，首屏 NavDestination 怎么压栈和处理返回键
- [NavPathStack 的路由名、出栈和返回刷新](navpathstack-routes/index.md)（11 条）：读到 Compose Navigation 的带参路由、popUpTo 回根或子页 pop 回原页；产物里 pushPathByName 的首参和 param、navDestination 按名字分发、pop / clear，以及返回原页后的刷新回调
- [根页的返回键（启动 Activity 没覆写 onBackPressed）](root-back-press/index.md)（2 条）：读过的源码里启动 Activity 或根 Activity 没覆写 onBackPressed、没有 OnBackPressedDispatcher，返回即 finish，onDestroy 里有释放；交回的根 NavDestination 没有 .onBackPressed、按返回露出空白首页，或只 moveAbilityToBackground 而没做释放，或调了 terminateSelf
- [Fragment 事务压栈打开的子页](fragment-backstack-subpage/index.md)（6 条）：读到 FragmentTransaction 的 replace 或 hide + add 加 addToBackStack 在宿主内容区打开子页（含 page_type=sub_component、CardView 卡片式宿主）；产物里子页写成 NavDestination、pushPathByName 推出壳外或清栈切页
- [Activity 的返回键处理（onBackPressed、OnBackPressedDispatcher）](activity-back-press/index.md)（4 条）：读到 Activity 覆写 onBackPressed() 按标志分支，或用 onBackPressedDispatcher.addCallback 登记回调；交回的返回按钮无条件 pop，或 NavDestination 的 .onBackPressed 写成封闭的固定分支
- [透明主题的 Activity（windowIsTranslucent）](translucent-activity/index.md)（1 条）：读到源 Activity 的主题里 android:windowIsTranslucent 为 true、android:windowBackground 为 @android:color/transparent，并有 android:backgroundDimEnabled；产物里对应 NavDestination 的 .mode(...)、页背景是否透明，以及页内那层半透明遮罩
- [Fragment 换页的自定义动画](fragment-custom-animations/index.md)（1 条）：读到 FragmentTransaction.setCustomAnimations(…) 配 res/anim 资源，或先用动画辅助方法缩放列表项再 replace fragment；产物里只有 pushPathByName(...)，对应 NavDestination 上没有 .customTransition(...)
- [宽窗的列表-详情分栏](list-detail-split-pane/index.md)（1 条）：读到 Compose NavDisplay 用 ListDetailSceneStrategy 按目的地的 metadata（listPane、detailPane、detailPlaceholder）分栏；产物里驱动 Navigation .mode(NavigationMode.Split / Stack) 的宽窗条件和 navBarWidth
