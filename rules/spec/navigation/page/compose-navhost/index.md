# 源端 Compose Navigation 的 NavHost 和导航调用

agent 会看到什么：源端用 NavHost(startDestination = …)、navigate { popUpTo … }、handleDeepLink、enterTransition 等 Compose Navigation 写法，或宿主 onCreate(savedInstanceState)，规格里只抄导航选项标签、写成 push，缺返回栈、栈底返回、重建或转场承载的说法

## 通用查法

### 源端用 Compose Navigation 时，规格按起始目的地和导航选项推出返回栈，写成按返回回到哪的验收

审的是：规格
触发（任一种）：
- 读到：源端 NavHost(startDestination = …) 配合 navigate(route) { popUpTo(…) }、handleDeepLink(intent) 这类调用，或起始目的地没有 BackHandler；返回栈后果由框架隐含决定，源码里没有显式代码；写错的样子：规格只抄导航选项的标签或写「push 到目标页」，没有「从某页按系统返回回到哪一页、栈底再按返回是退出还是移到后台」的验收条目
适用范围：规格提取阶段为 Compose Navigation 写导航契约和返回栈验收时
做法：
- 从源工程读出导航图的起始目的地，再逐个看进入页面的方式（切 tab、深链拉起、普通 navigate）带的 popUpTo、launchSingleTop 等选项，推出进入之后的返回栈
- 每种进入方式写一条验收：按系统返回回到哪一页；栈底再按返回是退出还是移到后台，不因源码里没有对应代码就省略
- 写明目标端承接的入口：返回键走 @Entry 页的 onBackPress，栈底移到后台对应 moveAbilityToBackground
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Navigation 的 handleDeepLink 对外部 VIEW 意图（经 NEW_TASK 拉起）会清栈并以起始目的地 + 目标合成返回栈：例：深链进入的页面按返回回到起始页（出处：卡里修好并验证过）
- 切 tab 带 popUpTo(startDestination) 时，非起始 tab 按系统返回先回起始 tab，起始 tab 上才退出：例：底部导航切 tab 的返回栈后果（出处：卡里修好并验证过）
- 从 Android 12（S）起，任务根且声明 ACTION_MAIN + CATEGORY_LAUNCHER 的 Activity 按返回时连同任务移到后台；更早版本结束当前 Activity：栈底返回写「退出」还是「移至后台」的依据（出处：android.app.Activity#onBackPressed）
针对本应用要查的：
- 导航图的起始目的地：源工程 NavHost 的 startDestination 参数；它是 popUpTo 回退和深链合成返回栈的第一页
- 每种进入方式带的导航选项：源工程里 navController.navigate(...) 的选项 lambda 和 handleDeepLink 的调用处；读出 popUpTo 的目标、saveState / restoreState、launchSingleTop，推出进入后的返回栈
- 起始 Activity 是否满足移到后台的条件：源工程 AndroidManifest.xml 里承载起始目的地的 Activity 的 intent-filter；声明了 android.intent.action.MAIN 和 android.intent.category.LAUNCHER 的，Android 12 起按返回移到后台
未核实：深链合成返回栈属框架隐含语义，卡里没核到修复后返回键行为的单独运行验证
来源：3 张卡，2 个应用
- case-16af2a52e0c933739747（Cofi）：做法第 2 步 ← 建议 4；做法第 3 步 ← 建议 1
- case-7c2d5eb3b8d385b5c7b7（Cofi）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4；取值 1 ← 诊断
- case-902870a7e6081dd22611（Jetsnack）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1；取值 2 ← 诊断

## 规矩

- rule-456bdf0d9151｜源端起始目的地无 BackHandler 时，导航规格写明“栈底返回=退出/移至后台”验收项｜读到：源端 NavHost 的 startDestination 页面没有 BackHandler，栈底返回依赖 Activity 默认行为；写错：导航规格、全局约定和页面规格都没写栈底返回的语义，返回拦截只写了编辑页等个别页面
- rule-16a479dad3a0｜tab 切换带 popUpTo(startDestination) 时，规格分写返回栈后果和状态保留两条验收｜读到：Compose Navigation 切 tab 用 navigate(route) { popUpTo(startDestination) { saveState = true }; launchSingleTop = true; restoreState = true }，源注释说在其他底部 tab 按返回回到起始目的地；写错：规格只把它抄成「launchSingleTop + restoreState + popUpTo(saveState)」标签，或只解释成切回 tab 时滚动位置保留；没有「非起始 tab 按系统返回回起始 tab」的验收条目
- rule-a6d539755a96｜迁移 handleDeepLink 时，规格写明外部拉起清栈并合成 [起始页, 目标] 返回栈｜读到：源端 LaunchedEffect(intent) { navController.handleDeepLink(intent) }，NavHost 有 startDestination；写错：规格数据流写「→ NavPathStack.pushPathByName」，AC 写「不中断当前导航栈（目标已在栈顶则仅更新参数）」，没写返回栈语义
- rule-227762288754｜源宿主用 NavHost 或接收 savedInstanceState 时，规格单列进程回收后重建分支｜读到：源宿主 Activity 的 onCreate(savedInstanceState) / super.onCreate(savedInstanceState)，或 Compose 的 rememberNavController() + NavHost(startDestination = …)；源码里没有显式的保存代码；写错：规格的宿主生命周期节只写「onCreate 初始化 → 冷启进入起始页」和前后台回切，没有「进程回收后重建 → 恢复页面栈与路由参数」的分支，也没有对应的平台差异决策
- rule-8311ebfd67f4｜源端 NavHost 有自定义转场时，规格写可实现的承载机制和要改的页面，不给默认动画分支｜读到：源 NavHost 写了 enterTransition / exitTransition / popEnterTransition / popExitTransition（如 scaleIn + slideIn、scaleOut + slideOut，带时长、延迟、缩放值）；写错：规格把转场映射写成「NavDestination 系统转场 + 自定义参数近似（customNavContentTransition 或默认动画参数调优）」，验收判据只核转场常量与源逐值相等，没写页面绑定义务
- rule-51b1fedbe5b3｜壳层 lambda 里 NavHost 起点会在会话内重算时，规格写出重算时机和换图清栈｜读到：Compose 源端在 ModalNavigationDrawer 等会重组的壳层内容 lambda 里写 NavHost(startDestination = 读偏好或状态的函数)，没有 remember；写错：规格只写「栈空时 pushPathByName 首屏」「只推一次」「初始路由压栈」，没写起点在哪些重组时重算、起点变化后清栈重进、popUpTo 基准随之改变
