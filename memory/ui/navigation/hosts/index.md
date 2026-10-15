# ui/navigation/hosts

Navigation/@Entry宿主与页面注册（含根 Navigation 默认标题栏与工具栏）、嵌入页取栈、单 Activity 壳内 loadChildFragment 子页的壳内回退栈与嵌入承载、半透明卡片式 Activity 的透明 DIALOG 路由、路由跳板和跨页面共享生命周期，外部入口（推送、快捷方式）宿主导航执行器的可用性守卫；Activity 切换转场按源端迁移（overridePendingTransition(0,0) 关闭，未调用时按主题默认窗口动画），NavHost 四向自定义转场到 customNavContentTransition 与页面绑定，导航目的地内 LocalLifecycleOwner 的 ON_STOP/ON_RESUME 接到 onHidden/onShown；LAUNCHER 路由跳板在进程存活后从桌面重进的再分流，.navDestination 直接传 @Builder，只在 onPause/onSaveInstanceState 存档时接 onHidden

[上一级](../index.md)

## 本级经验

- [Activity 切换转场按源端迁移：overridePendingTransition(0,0) 时各进入路由关闭，未调用时按主题默认窗口动画写转场](lesson-9886f489045488c8b454.lesson.md)
  - 时机：规格提取阶段写页面规格与路由契约、决定页面切换动画时；实现阶段写 pushPathByName/replacePathByName 或 router.pushUrl 页的 pageTransition 时
  - 情境：源 Activity 或所继承的基类在 onCreate 调 overridePendingTransition(0,0)；目标用 Navigation 的 push/replace 进入该页，进入路径不止一条，规格可能只把转场禁用挂在抽屉基座等某一条路径上。也包括多个 Activity 只用 startActivity/finish 切换，源码没有 overridePendingTransition、styles 也没覆盖 windowAnimationStyle，目标 @Entry 页或 NavDestination 没有转场设置。
  - 例外：目的地以复用实例进入（singleTop、CLEAR_TOP 回到已有实例，只走 onNewIntent）时不执行 onCreate，该路径不受此约束
- [LAUNCHER 入口是路由跳板且任务根被改写时，进程存活后从桌面图标重进要在 onNewWant 按同一条件再分流](lesson-16375a31f9d9cfe6cd55.lesson.md)
  - 时机：规格提取阶段把 LAUNCHER 路由跳板 Activity 映射为入口分流时；入口装配阶段接线 EntryAbility.onNewWant 与入口页时
  - 情境：源端 LAUNCHER Activity 是按条件 startActivity 后 finish 的无界面跳板（未声明 launchMode 即 standard），跳往主页时带 FLAG_ACTIVITY_CLEAR_TOP；应用内跳转用 TaskStackBuilder.startActivities 或 NEW_TASK|CLEAR_TASK 重建任务，使任务根变为主页。目标为单例 UIAbility 加单个 Navigation，进程存活时再次从桌面拉起只回调 onNewWant/onForeground，页面栈原样保留。
- [NavHost 的 enter/exit/popEnter/popExit 自定义转场迁到 Navigation：用 customNavContentTransition 驱动，各 NavDestination 把位移、透明度与缩放绑定到共享转场状态](lesson-9de3322165e533d6b790.lesson.md)
  - 时机：规格提取、计划派工与界面实现阶段，把 Compose NavHost（或目的地）上的 enterTransition/exitTransition/popEnterTransition/popExitTransition 落到 ArkUI Navigation 时
  - 情境：源端 NavHost 定义四向自定义转场（scaleIn/scaleOut、slideIn/slideOut、tween 时长与延迟等）；目标为 Navigation + NavDestination，在已观察的 API 中 customNavContentTransition 回调拿到的 NavContentInfo 不提供页面的 opacity、translate 属性；规格或派工可能写“customNavContentTransition 或默认转场”二选一，验收只核转场常量是否与源相等。
  - 例外：决策记录以编号批准采用系统默认转场，并写明差异
- [Navigation 的 .navDestination 直接传 @Builder 方法，不包箭头函数](lesson-cba110ebcf236088156f.lesson.md)
  - 时机：入口页实现与收尾接线阶段，编写 Navigation 的 navDestination 分发时；冷启动日志出现 Builder function is empty 时
  - 情境：入口 Navigation 用 @Builder 方法按名称分发目的地（如 pageMap），写成 .navDestination((name, param) =&gt; { this.pageMap(name, param) }) 一类箭头包装。
  - 例外：向自定义组件的 @BuilderParam 槽传页面内容不适用本条：那里按箭头闭包只调用 @Builder 的规则写（见 lesson-7d643db6ab406ae64c77）
- [Tab 子页嵌在 Swiper/Tabs 时只用注入的根 NavPathStack，onReady 不用 context.pathStack 覆盖](lesson-1cebb531c991239d2691.lesson.md)
  - 时机：页面转换与主壳接线阶段，为由主页 Tab/Swiper 承载的 Fragment 页确定导航栈来源、编写 onReady 时；把已有页面接入主页 Swiper/Tabs 时
  - 情境：Android 主 Activity 用 ViewPager/底部 Tab 承载多个 Fragment；目标由入口页 Navigation 以 @Provider 提供根 NavPathStack，主页 Swiper/Tabs 嵌入各 Tab 页组件，子页用 @Consumer 取栈，外层仍保留 NavDestination 与 onReady；工程里经 pushPathByName 压栈的页面普遍在 onReady 写 this.navPathStack = context.pathStack。
  - 例外：页面本身经 pushPathByName 压入根栈、不在 Swiper/Tabs 子树内时，onReady 的 context.pathStack 就是根栈，该赋值无害；Tab 内有意创建独立 Navigation 承载子导航时，Tab 内的页面用该 Navigation 自己的栈
- [main_pages.json 只登记入口页与经 router 进入的 @Entry 页，被导入的子组件与 @CustomDialog 不登记](lesson-c4a6eaaf6a22c0b8823f.lesson.md)
  - 时机：入口装配阶段写 main_pages.json 路由登记时；编译修复遇到“登记页面须有且仅有一个 @Entry”（10905402）或“export struct with @Entry”警告时
  - 情境：源端单 Activity 以底部导航承载多个 Fragment，另有 DialogFragment 与经导航跳转的二级页；目标主页面用 Tabs/TabContent import 并实例化页面 struct，弹窗写成 @CustomDialog，这些文件都放在 pages/ 目录；工程用 main_pages.json 登记路由页。
- [一进入就无条件跳转并 finish 的 Activity 是路由跳板：目标按同样条件直达实际页面，不把它的布局做成可见页](lesson-0b72c197ea20fbe6f277.lesson.md)
  - 时机：页面转换阶段迁移入口类 Activity、以及调用方为 Intent(X) 确定目标路由时
  - 情境：Android Activity 在 onCreate/initView 开头按条件 startActivity 到另一页并立即 finish()（如登录入口按配置转到短信登录或一键登录），它的布局文件仍含可渲染的按钮；多个调用方以 Intent 指向这个跳板 Activity。
  - 例外：有分支不跳走、执行到 setContentView 显示布局时，不整页当跳板：只把跳走的分支做成直达，留下的分支仍渲染该页；跳板同时是 LAUNCHER 入口时，进程存活后从桌面图标重进的再分流另按“LAUNCHER 入口是路由跳板”的经验在 onNewWant 处理；本条只决定跳板不渲染、调用方直达
- [半透明卡片式 Activity 迁移为透明 DIALOG 路由，遮罩只作页内一层](lesson-22c2a8f0e6b782b95448.lesson.md)
  - 时机：界面实现与规格提取阶段，迁移 windowIsTranslucent 主题的卡片式 Activity 及其内嵌子页时
  - 情境：源主题 windowIsTranslucent=true、windowBackground 透明、backgroundDimEnabled=true，以卡片内的容器承载 Fragment；目标为 Navigation/NavDestination。
- [外部入口的宿主导航守卫按“目标已注册或路由命中”判断，不用导航栈成员检查](lesson-1b05b8d5cc528d5dc5bc.lesson.md)
  - 时机：入口接线阶段，为推送、桌面快捷方式、通知点击等外部 Want 编写宿主导航执行器（路由器回调里的 pushPathByName）的可用性守卫时
  - 情境：源端跳转前用 isIntentAvailable 一类判断目标是否可用；目标由单一 EntryAbility 加 Navigation pageMap 承载，外部 Want 冷启时暂存、热启时直跳，由宿主页 pushPathByName 入栈；守卫可能先写在跨切片草稿里，再被复制到闪屏页、主页等多个宿主。
- [导航目的地内的 ON_STOP/ON_RESUME 观察者按返回栈条目生命周期接 onHidden/onShown，不窄化为退后台](lesson-19dd006e049c3f9d7563.lesson.md)
  - 时机：规格提取阶段翻译 LifecycleEventObserver 的 ON_STOP/ON_RESUME 触发契约时；页面实现阶段把引擎或服务暴露的 onStop/onResume 一类入口接到 NavDestination 生命周期时
  - 情境：源 Composable 用 DisposableEffect(LocalLifecycleOwner.current) 注册 LifecycleEventObserver，ON_STOP 时移交后台服务、暂停或保存，ON_RESUME 时取回；该 Composable 位于 navigation-compose 的目的地内。目标页面是 NavDestination，引擎是普通类，需由页面在 onShown/onHidden/aboutToDisappear 中显式调用入口；规格可能把触发写成“退后台/前后台切换”。
  - 例外：观察者挂在 ProcessLifecycleOwner 上：只对应应用前后台，按 Ability 前后台回调接线；观察者挂在 Activity 上：除应用前后台外，被其他 Activity 覆盖、配置变更重建时也会 ON_STOP（Activity.java 的 onStop 说明），按 Ability 前后台回调加页面覆盖情形接线；源端的存档写在 Activity 的 onPause/onSaveInstanceState 而不是 Compose 观察者里：按存档触发点逐个映射，不在 aboutToDisappear 存档
- [根 Navigation 只作路由容器时显式隐藏默认标题栏和工具栏](lesson-69e07207a06a8a8a7ba9.lesson.md)
  - 时机：界面实现阶段，为入口页根 Navigation 编写属性链时
  - 情境：源端外壳没有系统标题栏或工具栏（如 Compose Scaffold 只传自绘 bottomBar 与 snackbarHost），目标以 @Entry 页的 Navigation 作根路由容器，承载 tab 内容和自绘底栏，详情页走 NavDestination。
- [源壳在内容容器内以 hide+add+addToBackStack 打开子页、底栏仍可见时，子页留在壳内并由壳维护回退栈](lesson-7bcb44f0e376ec67e5a8.lesson.md)
  - 时机：壳层导航实现与页面形态决策阶段，为源端在主 Activity 内容区压栈加载的子 Fragment 确定承载方式、返回与底部导航选中语义时
  - 情境：源主 Activity 在内容容器内用 FragmentTransaction 的 hide(当前) + add(子页) + addToBackStack 打开详情、搜索等子页（项目封装名如 loadChildFragment），子页期间底栏、迷你播放条等壳元素仍在，工具栏随回退栈深度显示上箭头，可能按子页标签同步底栏选中；另有 replace 并清栈的切页入口（如 loadFragment）。目标同时有 Navigation 路由与壳内容槽。
  - 例外：源端子页以新 Activity 或替换整个壳的方式打开（底栏不可见）时，按普通路由页处理
- [源端一个 Composable 内多屏共享的 DisposableEffect 清理，拆成多页后归属外层生命周期，key 不随屏幕变时切屏不释放](lesson-2ed8c21943925bf0ae9a.lesson.md)
  - 时机：规格提取与计划阶段，把源端 DisposableEffect/onDispose 等清理映射成目标多页面的生命周期契约时；实现阶段把共享服务的 stop/dispose 挂到页面回调时
  - 情境：源端单 Activity 在同一个 Composable 里用状态变量切换多个屏幕，播放器等资源和 DisposableEffect 清理挂在这个外层 Composable；目标端拆成 Navigation 下的多个页面，共享服务需要重新确定由哪一层、在什么时机停止和释放。
  - 例外：源端清理本就挂在单个屏幕自己的 Composable 上，切屏即离开组合，此时按该屏对应页面的退出处理；源端观察的是 LocalLifecycleOwner 的 ON_STOP/ON_RESUME（暂停与恢复，不是释放）：按返回栈条目生命周期接 onHidden/onShown
- [源端只在 onPause、onSaveInstanceState 存档时，目标接 onHidden，不在 aboutToDisappear 存档或计时](lesson-33e61b21f6981abc40d2.lesson.md)
  - 时机：规格提取与页面实现阶段，把源 Activity 的存档、计时、统计调用点映射到 NavDestination 回调（onHidden、onBackPressed、aboutToDisappear）时
  - 情境：源 Activity 只在 onPause、onBackPressed、onSaveInstanceState、Up 调用存档，onDestroy 不存档；存档有非幂等副作用（按 now − startingTime 累计时长、写统计）。目标页是 Navigation 下的 NavDestination，可能在隐藏（退后台）很久之后才被清栈销毁（桌面图标重进、popToIndex、replace）。
  - 例外：源端在 onDestroy 或 finish 路径里也做同一存档：此时 aboutToDisappear 才是对应的存档钩子
- [返回 NavDestination 的首屏不作 Navigation 根内容：只在映射中注册并在空栈时压入同一栈，隐藏 navBar 时初始栈必须非空](lesson-8953e390416a80d7dd8c.lesson.md)
  - 时机：入口页实现或收尾接线阶段，创建 Navigation 宿主、决定首屏放在根内容还是压栈时；为根 Navigation 决定是否设 hideNavBar 时
  - 情境：目标入口页用 Navigation + @Provider NavPathStack 承载路由；首屏（启动页等）写成返回 NavDestination 的组件、已在 pageMap 注册，在 onReady 取栈并按启动决策 pushPathByName 下一页，或依赖 onShown、onResult、onBackPressed（如接收文件选择结果）；入口却把它放进 Navigation 内容槽，可能还加 hideNavBar(true)，初始栈为空。
  - 例外：首屏是普通组件（不返回 NavDestination）、作为 Navigation 根内容常驻，且不依赖 NavDestinationContext 取栈或页面生命周期回调
