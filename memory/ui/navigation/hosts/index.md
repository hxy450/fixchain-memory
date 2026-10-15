# ui/navigation/hosts

Navigation/@Entry宿主与页面注册（含根 Navigation 默认标题栏与工具栏）、嵌入页取栈、单 Activity 壳内 loadChildFragment 子页的壳内回退栈与嵌入承载、半透明卡片式 Activity 的透明 DIALOG 路由、路由跳板和跨页面共享生命周期，外部入口（推送、快捷方式）宿主导航执行器的可用性守卫；NavHost 四向自定义转场到 customNavContentTransition 与页面绑定，导航目的地内 LocalLifecycleOwner 的 ON_STOP/ON_RESUME 接到 onHidden/onShown

[上一级](../index.md)

## 本级经验

- [NavHost 的 enter/exit/popEnter/popExit 自定义转场迁到 Navigation：用 customNavContentTransition 驱动，各 NavDestination 把位移、透明度与缩放绑定到共享转场状态](lesson-9de3322165e533d6b790.lesson.md)
  - 时机：规格提取、计划派工与界面实现阶段，把 Compose NavHost（或目的地）上的 enterTransition/exitTransition/popEnterTransition/popExitTransition 落到 ArkUI Navigation 时
  - 情境：源端 NavHost 定义四向自定义转场（scaleIn/scaleOut、slideIn/slideOut、tween 时长与延迟等）；目标为 Navigation + NavDestination，在已观察的 API 中 customNavContentTransition 回调拿到的 NavContentInfo 不提供页面的 opacity、translate 属性；规格或派工可能写“customNavContentTransition 或默认转场”二选一，验收只核转场常量是否与源相等。
  - 例外：决策记录以编号批准采用系统默认转场，并写明差异
- [main_pages.json 只登记经 router 进入的 @Entry 页：被 Tabs/父页导入的子组件与 @CustomDialog 不登记，10905402 与 @Entry+export 警告先判定角色](lesson-c4a6eaaf6a22c0b8823f.lesson.md)
  - 时机：入口装配阶段写 main_pages.json 路由登记时；编译修复遇到“登记页面须有且仅有一个 @Entry”（10905402）或“export struct with @Entry”警告时
  - 情境：源端单 Activity 以底部导航承载多个 Fragment，另有 DialogFragment 与经导航跳转的二级页；目标主页面用 Tabs/TabContent import 并实例化页面 struct，弹窗写成 @CustomDialog，这些文件都放在 pages/ 目录；工程用 main_pages.json 登记路由页。
- [一进入就无条件跳转并 finish 的 Activity 是路由跳板：目标按同样条件直达实际页面，不把它的布局做成可见页](lesson-0b72c197ea20fbe6f277.lesson.md)
  - 时机：页面转换阶段迁移入口类 Activity、以及调用方为 Intent(X) 确定目标路由时
  - 情境：Android Activity 在 onCreate/initView 开头按条件 startActivity 到另一页并立即 finish()（如登录入口按配置转到短信登录或一键登录），它的布局文件仍含可渲染的按钮；多个调用方以 Intent 指向这个跳板 Activity。
- [入口页 Navigation 宿主：NavDestination 首屏只在 navDestination 映射中注册并在空栈时压入同一栈，不作根内容；隐藏 navBar 时初始栈必须非空；.navDestination 直接传 @Builder](lesson-8953e390416a80d7dd8c.lesson.md)
  - 时机：入口页实现或收尾接线阶段，创建 Navigation 宿主、决定首屏放在根内容还是压栈、编写 navDestination 分发时；为根 Navigation 决定是否设 hideNavBar 时
  - 情境：目标入口页用 Navigation + @Provider NavPathStack 承载路由；首屏（启动页等）写成返回 NavDestination 的组件，在 onReady 取栈并按启动决策 pushPathByName 下一页；目的地由 @Builder 映射分发。也包括启动页以 NavDestination 为根、已在 pageMap 注册，入口却把它放进 Navigation 内容槽并加 hideNavBar(true)，初始栈为空；或首屏页依赖 onShown、onResult、onBackPressed（如接收文件选择结果），却作为 Navigation 首页内容承载。
  - 例外：首屏是普通组件（不返回 NavDestination）、作为 Navigation 根内容常驻，且不依赖 NavDestinationContext 取栈
- [半透明卡片式 Activity 迁移为透明 DIALOG 路由，遮罩只作页内一层](lesson-22c2a8f0e6b782b95448.lesson.md)
  - 时机：界面实现与规格提取阶段，迁移 windowIsTranslucent 主题的卡片式 Activity 及其内嵌子页时
  - 情境：源主题 windowIsTranslucent=true、windowBackground 透明、backgroundDimEnabled=true，以卡片内的容器承载 Fragment；目标为 Navigation/NavDestination。
- [单 Activity 壳内的 loadChildFragment 子页映射为壳内回退栈，不改成独立路由或清栈切页](lesson-7bcb44f0e376ec67e5a8.lesson.md)
  - 时机：壳层导航实现与页面形态决策阶段，为源端在内容区压栈加载的子 Fragment 确定承载方式、返回与底部导航选中语义时
  - 情境：源主 Activity 用 loadChildFragment（hide 加 add 加 addToBackStack）打开详情、搜索等子页，子页期间底栏与迷你播放条仍在，工具栏随栈深显示上箭头，带 navigationTag 时同步底栏选中；启动器构造时写入默认 extras。目标同时有 Navigation 路由与壳内容槽。
- [外部入口的宿主导航守卫按“目标已注册或路由命中”判断，不用导航栈成员检查](lesson-1b05b8d5cc528d5dc5bc.lesson.md)
  - 时机：入口接线阶段，为推送、桌面快捷方式、通知点击等外部 Want 编写宿主导航执行器（路由器回调里的 pushPathByName）的可用性守卫时
  - 情境：源端跳转前用 isIntentAvailable 一类判断目标是否可用；目标由单一 EntryAbility 加 Navigation pageMap 承载，外部 Want 冷启时暂存、热启时直跳，由宿主页 pushPathByName 入栈；守卫可能先写在跨切片草稿里，再被复制到闪屏页、主页等多个宿主。
- [嵌在 Swiper/Tabs 里的页面组件只用 @Consumer 注入的根 NavPathStack，不在 onReady 用 context.pathStack 覆盖](lesson-1cebb531c991239d2691.lesson.md)
  - 时机：页面转换与主壳接线阶段，为由主页 Tab/Swiper 承载的 Fragment 页确定导航栈来源、编写 onReady 时；把已有页面接入主页 Swiper/Tabs 时
  - 情境：Android 主 Activity 用 ViewPager/底部 Tab 承载多个 Fragment；目标由入口页 Navigation 以 @Provider 提供根 NavPathStack，主页 Swiper 嵌入各 Tab 页组件，子页用 @Consumer('navPathStack') 取栈，外层仍保留 NavDestination 与 onReady；工程里经 pushPathByName 压栈的页面普遍在 onReady 写 this.navPathStack = context.pathStack。
  - 例外：页面本身经 pushPathByName 压入根栈、不在 Swiper/Tabs 子树内时，onReady 的 context.pathStack 就是根栈，该赋值无害
- [根 Navigation 只作路由容器时显式隐藏默认标题栏和工具栏](lesson-69e07207a06a8a8a7ba9.lesson.md)
  - 时机：界面实现阶段，为入口页根 Navigation 编写属性链时
  - 情境：源端外壳没有系统标题栏或工具栏（如 Compose Scaffold 只传自绘 bottomBar 与 snackbarHost），目标以 @Entry 页的 Navigation 作根路由容器，承载 tab 内容和自绘底栏，详情页走 NavDestination。
- [源 Activity 或其基类 onCreate 调 overridePendingTransition(0,0) 时，“进入无转场”是目的地页的属性：进入该页的每条路由（按钮跳转、引导完成、启动分流、抽屉）都关闭转场](lesson-9886f489045488c8b454.lesson.md)
  - 时机：规格提取阶段写页面规格与路由契约时；实现阶段写 pushPathByName/replacePathByName 时
  - 情境：源 Activity 或所继承的基类在 onCreate 调 overridePendingTransition(0,0)；目标用 Navigation 的 push/replace 进入该页，进入路径不止一条，规格可能只把转场禁用挂在抽屉基座等某一条路径上。
- [源端一个 Composable 内多屏共享的清理，拆成多页面后归属外层生命周期，切屏不释放](lesson-2ed8c21943925bf0ae9a.lesson.md)
  - 时机：规格提取与计划阶段，把源端 DisposableEffect/onDispose 等清理映射成目标多页面的生命周期契约时；实现阶段把共享服务的 stop/dispose 挂到页面回调时
  - 情境：源端单 Activity 在同一个 Composable 里用状态变量切换多个屏幕，播放器等资源和 DisposableEffect 清理挂在这个外层 Composable；目标端拆成 Navigation 下的多个页面，共享服务需要重新确定由哪一层、在什么时机停止和释放。
  - 例外：源端清理本就挂在单个屏幕自己的 Composable 上，切屏即离开组合，此时按该屏对应页面的退出处理
- [源端在导航目的地内用 LocalLifecycleOwner 观察 ON_STOP/ON_RESUME 时，owner 是返回栈条目：导航离开与退后台都要触发，目标按 onHidden/onShown 接线；销毁前只补调幂等停止入口，源端 onDestroy 不存档就不在 aboutToDisappear 存档或计时](lesson-19dd006e049c3f9d7563.lesson.md)
  - 时机：规格提取阶段翻译 LifecycleEventObserver 的 ON_STOP/ON_RESUME 触发契约时；页面实现阶段把引擎或服务暴露的 onStop/onResume 一类入口、或源 Activity 的存档时机接到 NavDestination 生命周期时
  - 情境：源 Composable 用 DisposableEffect(LocalLifecycleOwner.current) 注册 LifecycleEventObserver，ON_STOP 时移交后台服务、暂停或保存，ON_RESUME 时取回；该 Composable 位于 navigation-compose 的目的地内。目标页面是 NavDestination，引擎是普通类，需由页面在 onShown/onHidden/aboutToDisappear 中显式调用入口；规格可能把触发写成“退后台/前后台切换”。也包括源 Activity 只在 onPause、onBackPressed、onSaveInstanceState、Up 存档，onDestroy 不存档，存档按 now − startingTime 累计时长或写统计；目标页可能在隐藏很久后才被清栈销毁（桌面图标重进、popToIndex、replace）。
  - 例外：观察者挂在 Activity 或 ProcessLifecycleOwner 上：只对应应用前后台，按 Ability 或应用前后台回调接线
