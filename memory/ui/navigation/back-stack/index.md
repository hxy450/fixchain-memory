# ui/navigation/back-stack

系统/页面返回、覆盖层关闭顺序、清栈重建与重复导航的净效果，底部 tab 的 popUpTo 返回语义与外部深链的清栈。

[上一级](../index.md)

## 本级经验

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
  - 情境：源页的对话框、底部弹层或下拉菜单以 onDismissRequest 关闭；源页可能另有 BackHandler 处理行内编辑器或未保存门禁，也可能完全没有 BackHandler。目标把这些弹层做成 NavDestination 内 Stack 条件渲染的覆盖层或由 activeDialog 一类状态驱动的组件，而不是自带返回关闭的弹窗机制，系统返回统一交给宿主。
  - 例外：弹层改用自带返回关闭的弹窗机制（openCustomDialog、bindSheet、NavDestinationMode.DIALOG 等）时，由弹窗自身处理返回
- [被 @Entry 页直接组合的子组件要拦截返回键时，由 @Entry 页的 onBackPress 转调子组件注册的处理函数](lesson-803ba029eea852122e77.lesson.md)
  - 时机：页面转换与接线阶段，为源端非根 Composable 里的 BackHandler/PredictiveBackHandler 选择 ArkUI 返回键钩子时
  - 情境：源端在抽屉宿主等非 Activity 根的 Composable 中按状态条件拦截返回（例如抽屉打开时先关抽屉）；目标端该组件不是 @Entry，由唯一的 @Entry 页直接组合，没有作为页面驻留在 Navigation 路由栈内。
  - 例外：组件本身就是 @Entry 页时，直接实现 onBackPress；组件作为 NavDestination 驻留在 Navigation 栈内时，返回由 NavDestination.onBackPressed 处理；来源实测只覆盖被直接组合、未入栈的情况
- [返回按钮与系统返回共用同一处理分支，按源端启动来源标志执行 onBackPressed 的逻辑，不默认 pop](lesson-f19632971e470d55c543.lesson.md)
  - 时机：页面转换阶段，把 Activity 的返回按钮点击与 onBackPressed 翻译成 NavDestination 的返回处理时
  - 情境：源 Activity 按启动来源标志（如 isFromSplash）改变返回行为：首启进入时返回会先执行补救动作（如添加默认城市）再进主页，其他来源才 finish；目标页用 NavPathStack 管理，返回按钮默认写成 pop()，系统返回未处理。
