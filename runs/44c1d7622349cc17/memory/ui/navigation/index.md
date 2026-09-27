# ui/navigation

多屏拆成多页面后的导航：目的地命名与参数、返回栈重建、同一结果的单一导航出口、跳转参数与跳转前的状态交接、返回键分发、挂载与生命周期归属

[上一级](../index.md)

## 本级经验

- [Compose 带参路由迁到 NavPathStack 时，目的地名用固定名、参数只走 param，pageMap 按固定名精确匹配](lesson-300200dd52892e9dadd2.lesson.md)
  - 时机：界面转换与导航壳实现阶段，写 pushPathByName 与 navDestination 分发时
  - 情境：源端 Compose Navigation 以带占位符的路由模式（如 detail/{id}）注册目的地，并用拼串函数生成实际路由；目标用 Navigation + NavPathStack，由 pageMap 按目的地名分发。
- [构造目标页路由参数以接收端契约为准：接收 Activity 不读取或写死的 extra 不透传](lesson-4a7c04b864ef635c87b6.lesson.md)
  - 时机：功能接线阶段，为跨页跳转构造目标页参数、决定哪些发起页状态要带过去时
  - 情境：源发起页用 putExtra 传一个开关（如显隐标签），但接收 Activity 不读取该 extra，或创建 Fragment 时写死该参数；目标页参数类已用默认值与注释标明该字段由接收端固定。
- [源端 popUpTo(根){inclusive=true} 加 navigate(根) 映射为 NavPathStack 重建，不用 pop() 代替](lesson-96c890012b26b5cb32cd.lesson.md)
  - 时机：接线阶段实现删除、克隆等操作完成后的导航时
  - 情境：源端在操作完成后 navigate 到列表并 popUpTo 列表 inclusive，重建返回栈；目标用 Navigation + NavPathStack，列表是 Navigation 根内容。
- [源端一个 Composable 内多屏共享的清理，拆成多页面后归属外层生命周期，切屏不释放](lesson-2ed8c21943925bf0ae9a.lesson.md)
  - 时机：规格提取与计划阶段，把源端 DisposableEffect/onDispose 等清理映射成目标多页面的生命周期契约时；实现阶段把共享服务的 stop/dispose 挂到页面回调时
  - 情境：源端单 Activity 在同一个 Composable 里用状态变量切换多个屏幕，播放器等资源和 DisposableEffect 清理挂在这个外层 Composable；目标端拆成 Navigation 下的多个页面，共享服务需要重新确定由哪一层、在什么时机停止和释放。
  - 例外：源端清理本就挂在单个屏幕自己的 Composable 上，切屏即离开组合，此时按该屏对应页面的退出处理
- [源端对同一次成功有多条导航响应时，目标只保留一个导航出口，并按净效果定义返回栈](lesson-683d8f5070802c518020.lesson.md)
  - 时机：规格提取与接线阶段，把源页面对同一业务结果的多条响应（事件订阅里 finish、成功回调里 startActivity）翻译成目标 NavPathStack 操作时
  - 情境：源 Activity 对同一次成功既在全局事件订阅里关闭本页，又在回调里启动主页（可能带 FLAG_ACTIVITY_NEW_TASK）；全局管理器在回调前发布成功事件；目标由单一 NavPathStack 管理页面，Navigation 根内容可能是启动页。
- [源端独立窗口的对话框改成页内覆盖层后，在宿主 onBackPressed 里自顶向下逐层关闭，全部关闭后才进未保存门禁或出栈](lesson-396d54479492828eeea3.lesson.md)
  - 时机：页面转换阶段，把 BackHandler 与 AlertDialog/ModalBottomSheet 改写成 NavDestination.onBackPressed 加页内覆盖层时
  - 情境：源页用 BackHandler 处理行内编辑器或未保存门禁，另有 AlertDialog、Dialog 或 ModalBottomSheet 以 onDismissRequest 关闭；目标把这些弹层做成页内 Stack 覆盖层或由 activeDialog 一类状态驱动的组件，系统返回统一交给宿主。
- [源端跳转前写入的共享状态（如播放队列）是跳转契约的一部分，按原顺序迁移](lesson-dfcdbb19cd93d29159b2.lesson.md)
  - 时机：功能接线阶段，把列表项点击 → 启动目标页的链路迁成目标导航调用时；路由核验阶段比对跳转一致性时
  - 情境：源端点击处理在 startActivity 之前先把当前列表（过滤后）交给共享播放器或仓库（如 setPlaylist(list, position, true)），目标页只显示共享状态；目标跳转参数只带 id 一类字段。
- [被 @Entry 页直接组合的子组件要拦截返回键时，由 @Entry 页的 onBackPress 转调子组件注册的处理函数](lesson-803ba029eea852122e77.lesson.md)
  - 时机：页面转换与接线阶段，为源端非根 Composable 里的 BackHandler/PredictiveBackHandler 选择 ArkUI 返回键钩子时
  - 情境：源端在抽屉宿主等非 Activity 根的 Composable 中按状态条件拦截返回（例如抽屉打开时先关抽屉）；目标端该组件不是 @Entry，由唯一的 @Entry 页直接组合，没有作为页面驻留在 Navigation 路由栈内。
  - 例外：组件本身就是 @Entry 页时，直接实现 onBackPress；组件作为 NavDestination 驻留在 Navigation 栈内时，返回由 NavDestination.onBackPressed 处理；来源实测只覆盖被直接组合、未入栈的情况
- [页面路由参数的缺失哨兵值与有效性判定保持一致，错误态下隐藏依赖该参数的操作入口](lesson-c433adebb9d20f273b22.lesson.md)
  - 时机：页面转换阶段为目的地参数写默认值、有效性判定和无效路由错误态时
  - 情境：目标页从路由参数取 id，参数类有默认值；规格要求缺失 id 进入无效路由错误态、不渲染假数据；页面上有开始、编辑等依赖该 id 的按钮。
