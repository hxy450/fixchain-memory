# 页面跳转与返回

读到 startActivity / putExtra、finish、onBackPressed、TaskStackBuilder、overridePendingTransition、Compose NavHost / navigate、导航图 <argument>、Fragment 挂进宿主容器，规格里写页面导航表、入参、返回栈、转场和页面清单时

## 触发族

- [点击监听器里的跳转目标](click-target/index.md)（6 条）：读到源页面的 setOnClickListener、onItemChildClick、onClick* 方法或弹窗配置里的链接回调，函数体里 startActivity / start(url) 到别的页；规格的行为契约、对接点、AC、导航表里写的入口和目标页
- [跳转目标页和页面清单](target-page-list/index.md)（3 条）：读到截图页或入口页的 startActivity / start(url) 打开二级页、WebView 页；规格的页面导航表和 AC 里有要打开的页，页面清单、决策台账或目标路由里却没有、标成 pending 或本轮不生成
- [TaskStackBuilder 父栈和回收后的任务栈](task-stack-builder/index.md)（3 条）：读到 TaskStackBuilder.addNextIntentWithParentStack、android:parentActivityName / PARENT_ACTIVITY 组成的任务栈和 putExtra 的布尔参数；规格的实现映射、返回落点、恢复契约或 PD 写成 pushPathByName 带回栈、恢复至最后路由
- [调用方传了、接收方不读的 Intent 参数](unread-intent-extra/index.md)（1 条）：读到调用方 putExtra 传了某个参数、接收方 Activity 不读它；验收条目或 UI 用例写着带这个参数进入会自动弹框或自动执行动作
- [成功后 startActivity 加 finish 的组合跳转](finish-and-start/index.md)（2 条）：读到源页面对同一次成功既 finish() 又 startActivity(主页) 配 FLAG_ACTIVITY_NEW_TASK（可能分在 EventBus 订阅和 LiveData 回调里）；规格的映射表或验收写成 navPathStack.clear() + pushPathByName、本页 pop 两条独立的导航
- [根 Activity 没覆写的返回键](root-back-press/index.md)（3 条）：读到启动页或任务根 Activity 没有覆写 onBackPressed / onKeyDown，或抽屉关闭时调 super.onBackPressed()；规格的返回契约或 AC 写「退后台，不出栈」「系统返回默认」
- [Activity 跳转的转场动画](activity-transition/index.md)（4 条）：读到源 Activity 用 startActivity / finish 跳转，源码里没有 overridePendingTransition、styles 没覆盖 windowAnimationStyle，或本类和基类 onCreate 里 overridePendingTransition(0, 0)；规格的导航关系、ui-graph、路由契约写「无转场」、transition_anim 填 "none"，或 pushPathByName 没带 animated=false
- [源端 Compose Navigation 的 NavHost 和导航调用](compose-navhost/index.md)（7 条）：源端用 NavHost(startDestination = …)、navigate { popUpTo … }、handleDeepLink、enterTransition 等 Compose Navigation 写法，或宿主 onCreate(savedInstanceState)，规格里只抄导航选项标签、写成 push，缺返回栈、栈底返回、重建或转场承载的说法
- [挂在宿主 Activity 里的 Fragment 子组件](hosted-fragment-subcomponent/index.md)（4 条）：源码经 FragmentTransaction 的 add / replace / addToBackStack 把 Fragment 放进宿主 Activity 的容器，页面元数据标 page_type=sub_component，规格把它推成 NavDestination 全屏页、写不出承载它的容器，或宿主没登记各 Tab 的沉浸和避让
- [导航目的地的 argument 声明](nav-destination-args/index.md)（1 条）：导航图 XML 目的地下的 <argument>（app:argType、app:nullable、android:defaultValue）和 Fragment 的 requireArguments() 取参；分页规格里的页面入参一项
- [Compose 的共享元素转场（sharedElement、sharedBounds）](shared-element-transition/index.md)（1 条）：读到源端 Modifier.sharedBounds("<id>-bounds") 包住 Modifier.sharedElement(id)、两层 key 不同；规格把 id 值域写成两对、只写「geometryTransition(id) 双端绑定」或原样列出源端两层 key，没写每端用哪个键、挂在哪个节点、内层不再挂
- [页面之间回传结果的通道（savedStateHandle 回传）](page-result-return/index.md)（1 条）：读到安卓源用 savedStateHandle 回传：子页写结果后 navigateUp()，来源页回来后读取；规格的实现映射只写「NavPathStack param + onResult 回调 / emitter 事件」或「addReturn 后 pop」，没写载荷类型、生产端用哪个出栈调用、消费端在哪个时机读取
