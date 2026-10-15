# ui/navigation/back-stack

系统/页面返回与返回栈：按源端 API 清栈重建返回栈（TaskStackBuilder 父链、handleDeepLink 新任务、外部入口 CLEAR_TOP 在 onNewWant 清栈、popUpTo 根 inclusive），重复导航的净效果，底部 tab 的 popUpTo 返回语义，覆盖层关闭顺序，未进 Navigation 栈的子组件经 @Entry 转发返回（含 OnBackPressedDispatcher 后登记先问的分发），栈底 NavDestination 的返回接管与源端默认返回（finish 或移到后台）的生命周期效果，按启动来源标志的返回分支

[上一级](../index.md)

## 本级经验

- [唯一页面压在空 Navigation 首页之上时，栈底 NavDestination 在自身 onBackPressed 按栈深接管返回，不写在 @Entry](lesson-efff93743d668b55b55a.lesson.md)
  - 时机：入口装配与页面转换阶段，搭建 Navigation 入口壳，为冷启首页、首启引导页、清栈回根后的页等可能成为栈底的 NavDestination 接返回时；规格提取阶段写栈底返回的验收锚点时
  - 情境：源端根页（启动 Activity 或 NavHost 起始目的地）没有覆写 onBackPressed，也没有 OnBackPressedDispatcher、BackHandler 或 KEYCODE_BACK 处理；目标按 Navigation + NavDestination 模板，用内容为空的 Navigation 首页在启动时 pushPathByName 压入唯一页面，或启动页已生成为 NavDestination、入口只能首次 push（首屏放根内容还是压栈见 lesson-8953e390416a80d7dd8c）。
  - 例外：首屏不必是 NavDestination、作为 Navigation 根内容常驻不压栈时，空栈返回按系统默认处理，不套本条；源端根页有自己的返回处理时按源端逻辑实现
- [外部入口以 CLEAR_TOP 拉起已在栈中的主 Activity 时，目标在 onNewWant 先清 NavPathStack 再落 tab](lesson-4bd76f00e81b3ffc95fd.lesson.md)
  - 时机：规格提取阶段描述桌面卡片、通知、快捷方式等外部入口的返回栈后果时；入口实现阶段在 EntryAbility.onNewWant 与入口页处理热启动外部 Want 时
  - 情境：源端外部入口（桌面卡片、通知等）用带 FLAG_ACTIVITY_CLEAR_TOP|NEW_TASK 的显式 Intent 拉起主 Activity 并落到某个 tab；目标为单例 UIAbility + 单 Navigation，热启动时只回调 onNewWant，NavPathStack 里可能压着详情页；规格可能只写“拉起后落到某 tab”。
  - 例外：Intent 不带 CLEAR_TOP 时，按源端 flag 与 launchMode 推出的栈决定是否保留已压的页面
- [底部 tab 以 popUpTo(起始){saveState} 切换、目标按下标切 tab 时，在 onBackPress 让非起始 tab 先回起始 tab](lesson-39f137ee173e50363f79.lesson.md)
  - 时机：规格提取阶段描述底部 tab 切换的返回与状态保留时；入口装配与实现阶段核对导航壳差异、为下标或条件渲染的 tab 壳接系统返回时
  - 情境：源端 tab 切换用 navigate(route) { popUpTo(startDestination){ saveState = true }; launchSingleTop = true; restoreState = true }；目标用单 Navigation 加下标或条件渲染切 tab，NavPathStack 只承载详情页，规格可能只把它写成“切回 tab 时状态保留”。
  - 例外：源端 tab 切换不带 popUpTo(startDestination)（各 tab 依次压栈，或另有 BackHandler 处理返回）时，按源端实际返回栈实现
- [未进入 Navigation 栈、被 @Entry 页直接组合的子组件拦截返回时，由 @Entry.onBackPress 转调其登记的处理函数](lesson-803ba029eea852122e77.lesson.md)
  - 时机：页面转换与接线阶段，为源端非根 Composable 里的 BackHandler/PredictiveBackHandler，或把 OnBackPressedDispatcher 的多级回调映射到 ArkUI 返回键钩子时
  - 情境：源端在抽屉宿主等非 Activity 根的 Composable 中按状态条件拦截返回（例如抽屉打开时先关抽屉）；目标端该组件不是 @Entry，由唯一的 @Entry 页直接组合，没有作为页面驻留在 Navigation 路由栈内。也包括源端 OnBackPressedDispatcher 按后登记先问分发（Activity 只登记壳层回调，选择模式等另登记回调），目标壳页的返回处理是封闭分支、嵌入的子页没有登记入口。
  - 例外：组件本身就是 @Entry 页、且没有承载内有页面的 Navigation 时，直接实现 onBackPress；组件位于 NavDestination 内容中（含被页面组合的 BasePage 等共享基座）时，返回先交该 NavDestination.onBackPressed，返回 false 即出栈，@Entry.onBackPress 不会被调用；由该 NavDestination 的 onBackPressed 转调基座的裁决函数，不在 @Entry 上兑现
- [源 Activity 按启动来源标志改变返回行为时，返回按钮与系统返回共用同一处理函数并按标志执行源端逻辑，不默认 pop](lesson-f19632971e470d55c543.lesson.md)
  - 时机：页面转换阶段，把 Activity 的返回按钮点击与 onBackPressed 翻译成 NavDestination 的返回处理时
  - 情境：源 Activity 按启动来源标志（如 isFromSplash）改变返回行为：首启进入时返回会先执行补救动作（如添加默认城市）再进主页，其他来源才 finish；目标页用 NavPathStack 管理，返回按钮默认写成 pop()，系统返回未处理。
- [源根 Activity 未覆写返回时，按系统版本与 LAUNCHER 声明判定默认返回是 finish 还是移到后台，再复现对应生命周期](lesson-f5c3e8a577aa2106faad.lesson.md)
  - 时机：规格提取与页面实现阶段，为源端没有返回处理的根 Activity 写返回契约、实现目标栈底返回的生命周期效果时；编排派工转述“源端默认返回”时
  - 情境：源端任务根 Activity 没有覆写 onBackPressed、onKeyDown，也没有注册 OnBackPressedCallback，返回走 Activity 默认行为；它的 onDestroy 有释放逻辑（音乐 release、数据源 close），页面持有实例态（输入框文字、所选值、播放位置），另有跨 Activity 保留的静态单例。
  - 例外：源端有返回处理（覆写 onBackPressed、OnBackPressedCallback、BackHandler）时按源端逻辑实现，不套默认规则
- [源端 popUpTo(根){inclusive=true} 加 navigate(根) 映射为 NavPathStack 重建，不用 pop() 代替](lesson-96c890012b26b5cb32cd.lesson.md)
  - 时机：接线阶段实现删除、克隆等操作完成后的导航时
  - 情境：源端在操作完成后 navigate 到列表并 popUpTo 列表 inclusive，重建返回栈；目标用 Navigation + NavPathStack，列表是 Navigation 根内容。
- [源端对同一次成功有多条导航响应时，目标只保留一个导航出口，并按净效果定义返回栈](lesson-683d8f5070802c518020.lesson.md)
  - 时机：规格提取与接线阶段，把源页面对同一业务结果的多条响应（事件订阅里 finish、成功回调里 startActivity）翻译成目标 NavPathStack 操作时
  - 情境：源 Activity 对同一次成功既在全局事件订阅里关闭本页，又在回调里启动主页（可能带 FLAG_ACTIVITY_NEW_TASK）；全局管理器在回调前发布成功事件；目标由单一 NavPathStack 管理页面，Navigation 根内容可能是启动页。
- [源端对话框、底部弹层或下拉菜单改成页内覆盖层后，在宿主 onBackPressed 里自顶向下逐层关闭，全部关闭后才进未保存门禁或出栈](lesson-396d54479492828eeea3.lesson.md)
  - 时机：页面转换阶段，把源端 Dialog/AlertDialog/ModalBottomSheet/ExposedDropdownMenu（以及可能存在的 BackHandler）改写成 NavDestination 页内覆盖层、确定系统返回如何处理时
  - 情境：源页的对话框、底部弹层或下拉菜单以 onDismissRequest 关闭；源页可能另有 BackHandler 处理行内编辑器或未保存门禁，也可能完全没有 BackHandler。目标把这些弹层做成 NavDestination 内 Stack 条件渲染的覆盖层或由 activeDialog 一类状态驱动的组件，而不是自带返回关闭的弹窗机制，系统返回统一交给宿主。也包括源端 ContextMenu 窗口、ActionMode 多选态被改写成页面 @Local 浮层或选择态，页面是嵌入宿主的组件。也包括 View 体系 AlertDialog（默认可取消、带 setOnCancelListener）被写成自带蒙层的共享页内浮层组件，只接蒙层点击，页面的返回拦截不感知弹窗。
  - 例外：弹层改用自带返回关闭的弹窗机制（openCustomDialog、bindSheet、NavDestinationMode.DIALOG 等）时，由弹窗自身处理返回
- [源端用 handleDeepLink 处理外部拉起的深链时，目标清空 NavPathStack 并按导航图合成返回栈，不在当前栈上 push](lesson-69229aa8c7b051229f26.lesson.md)
  - 时机：规格提取与入口接线阶段，把源端 handleDeepLink/navDeepLink 迁成 want 解析后的导航动作、决定打开深链后的返回栈时
  - 情境：源 Activity 在 onCreate、onNewIntent 或 LaunchedEffect(intent) 中调用 navController.handleDeepLink(intent)，目的地以 navDeepLink(uriPattern) 注册；外部链接经 VIEW intent 以新任务（FLAG_ACTIVITY_NEW_TASK）拉起宿主。目标由 UIAbility 的 onCreate/onNewWant 解析 want.uri 后操作 Navigation 的 NavPathStack；规格可能写成“在当前栈上 pushPathByName、目标已在栈顶则只更新参数”。
  - 例外：intent 不带 FLAG_ACTIVITY_NEW_TASK 时 handleDeepLink 不合成起始页：以 popUpTo(图根, inclusive) 只留下目标一页，返回即离开该 Activity、回到发起方（navigation-runtime 2.9.8 NavController.handleDeepLink）；目标按这一栈形另定，不套用本条的合成；Navigation 根内容是启动页等不在源端栈中的页面时，clear() 会露出它：clear 后先 push 源端起始页再 push 目标
- [源端经 TaskStackBuilder 父栈跳转时，按 Manifest 父链清栈重建返回栈，返回落到父页而非来源页](lesson-2986423250986124d039.lesson.md)
  - 时机：规格提取与基座实现阶段，把基类的父栈跳转方法（抽屉导航等）翻译成 NavPathStack 操作与返回验收时
  - 情境：源基类被多个页面继承，抽屉等跳转经 TaskStackBuilder 发起，Manifest 为目标声明 parentActivityName 或 PARENT_ACTIVITY；目标是单个 Navigation + NavPathStack，跳转可从栈底以外的任意宿主页发起；页面规格里可能有“pushPathByName（主页为根天然在栈底）”一类只在来源页是主页时成立的映射。
  - 例外：父链上某一级就是 Navigation 根内容（不在 NavPathStack 中）时，clear 后不再 push 它，只 push 其余父页与目标；根内容是启动页等不在父链中的页时，clear 会露出它，要先 push 父链根页
