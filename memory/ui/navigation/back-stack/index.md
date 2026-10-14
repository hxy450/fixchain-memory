# ui/navigation/back-stack

系统/页面返回（含 OnBackPressedDispatcher 后登记先问的回调分发到嵌入子页）、覆盖层关闭顺序、清栈重建与重复导航的净效果，底部 tab 的 popUpTo 返回语义与外部深链的清栈，唯一页面压在空 Navigation 首页上时根页的返回（按源端默认退到后台）；handleDeepLink 外部拉起时清栈并合成“起始页 + 目标页”

[上一级](../index.md)

## 本级经验

- [唯一页面被压在空的 Navigation 首页之上时由根页接管返回键：栈底返回用 moveAbilityToBackground 退后台、不出栈露出空白首页；源端未覆写返回时按 Activity finish() 同时执行 onDestroy 的释放并复位页面实例态，参照设备实测为 HOT 恢复时才保留实例](lesson-efff93743d668b55b55a.lesson.md)
  - 时机：规格提取与入口装配阶段，为单 Activity 应用确定根页面的返回语义、搭建 Navigation 入口壳并决定首页放在 Navigation 内容区还是首次 push 时；把注入经验转成派工要求、确定栈底返回的生命周期效果时
  - 情境：安卓启动 Activity 未覆写 onBackPressed，也没有 OnBackPressedDispatcher、BackHandler 或 KEYCODE_BACK 处理（含 Compose NavHost 的起始目的地），返回键走 Activity 默认行为：默认 finish()，onDestroy 执行（如释放音乐、关闭数据源），实例态（输入框文字、所选值、播放位置）丢失，进程与静态单例保留；部分 Android 12+ 设备与启动方式下任务根 Activity 改为移到后台、onPause 存档、onResume 读档，以参照设备实测为准。目标按 Navigation + NavDestination 模板，用内容为空的 Navigation 首页在启动时 pushPathByName 压入唯一页面，或启动页已生成为 NavDestination、入口只能首次 push。
- [底部 tab 的 popUpTo(start){saveState} 与外部入口的 CLEAR_TOP 要拆出返回栈后果写成验收，并在 onBackPress、onNewWant 显式实现](lesson-39f137ee173e50363f79.lesson.md)
  - 时机：规格提取阶段描述底部 tab 切换和外部深链入口，以及实现阶段核对导航壳差异时
  - 情境：源端 tab 切换用 navigate { popUpTo(startDestination){ saveState }; launchSingleTop; restoreState }，桌面卡片、通知等外部入口用带 FLAG_ACTIVITY_CLEAR_TOP/NEW_TASK 的 Intent 拉起主 Activity；目标端用单 Navigation 加下标或条件渲染切 tab，NavPathStack 承载详情页。
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
- [源端用 NavController.handleDeepLink 处理外部拉起的深链时，目标清空 NavPathStack 并合成“起始页 + 目标页”返回栈，不在当前栈上 push](lesson-69229aa8c7b051229f26.lesson.md)
  - 时机：规格提取与入口接线阶段，把源端 handleDeepLink/navDeepLink 迁成 want 解析后的导航动作、决定打开深链后的返回栈时
  - 情境：源 Activity 在 onCreate、onNewIntent 或 LaunchedEffect(intent) 中调用 navController.handleDeepLink(intent)，目的地以 navDeepLink(uriPattern) 注册；外部链接经 VIEW intent 以新任务（FLAG_ACTIVITY_NEW_TASK）拉起宿主。目标由 UIAbility 的 onCreate/onNewWant 解析 want.uri 后操作 Navigation 的 NavPathStack；规格可能写成“在当前栈上 pushPathByName、目标已在栈顶则只更新参数”。
- [被 @Entry 页或壳页直接组合的子组件要拦截返回键时，由宿主的返回处理转调子组件登记的处理函数；多个登记方按后进先出分发](lesson-803ba029eea852122e77.lesson.md)
  - 时机：页面转换与接线阶段，为源端非根 Composable 里的 BackHandler/PredictiveBackHandler，或把 OnBackPressedDispatcher 的多级回调映射到 ArkUI 返回键钩子时
  - 情境：源端在抽屉宿主等非 Activity 根的 Composable 中按状态条件拦截返回（例如抽屉打开时先关抽屉）；目标端该组件不是 @Entry，由唯一的 @Entry 页直接组合，没有作为页面驻留在 Navigation 路由栈内。也包括源端 OnBackPressedDispatcher 按后登记先问分发（Activity 只登记壳层回调，选择模式等另登记回调），目标壳页的返回处理是封闭分支、嵌入的子页没有登记入口。
  - 例外：组件本身就是 @Entry 页时，直接实现 onBackPress；组件作为 NavDestination 驻留在 Navigation 栈内时，返回由 NavDestination.onBackPressed 处理；来源实测只覆盖被直接组合、未入栈的情况
- [返回按钮与系统返回共用同一处理分支，按源端启动来源标志执行 onBackPressed 的逻辑，不默认 pop](lesson-f19632971e470d55c543.lesson.md)
  - 时机：页面转换阶段，把 Activity 的返回按钮点击与 onBackPressed 翻译成 NavDestination 的返回处理时
  - 情境：源 Activity 按启动来源标志（如 isFromSplash）改变返回行为：首启进入时返回会先执行补救动作（如添加默认城市）再进主页，其他来源才 finish；目标页用 NavPathStack 管理，返回按钮默认写成 pop()，系统返回未处理。
