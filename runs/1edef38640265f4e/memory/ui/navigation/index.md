# ui/navigation

多屏拆成多页面后的导航：入口 Navigation 宿主与首屏入栈，main_pages 路由页登记与子组件/弹窗的划分，Tab/Swiper 子页的导航栈来源，目的地命名与参数（含多入口共享载荷、router 页面取参），点击出口的跳转接线，返回栈重建、同一结果的单一导航出口、跳转前的状态交接、返回键分发、挂载与生命周期归属

[上一级](../index.md)

## 本级经验

- [Compose 带参路由迁到 NavPathStack 时，目的地名用固定名、参数只走 param，pageMap 按固定名精确匹配](lesson-300200dd52892e9dadd2.lesson.md)
  - 时机：界面转换与导航壳实现阶段，写 pushPathByName 与 navDestination 分发时
  - 情境：源端 Compose Navigation 以带占位符的路由模式（如 detail/{id}）注册目的地，并用拼串函数生成实际路由；目标用 Navigation + NavPathStack，由 pageMap 按目的地名分发。
- [main_pages.json 只登记经 router 进入的 @Entry 页：被 Tabs/父页导入的子组件与 @CustomDialog 不登记，10905402 与 @Entry+export 警告先判定角色](lesson-c4a6eaaf6a22c0b8823f.lesson.md)
  - 时机：入口装配阶段写 main_pages.json 路由登记时；编译修复遇到“登记页面须有且仅有一个 @Entry”（10905402）或“export struct with @Entry”警告时
  - 情境：源端单 Activity 以底部导航承载多个 Fragment，另有 DialogFragment 与经导航跳转的二级页；目标主页面用 Tabs/TabContent import 并实例化页面 struct，弹窗写成 @CustomDialog，这些文件都放在 pages/ 目录；工程用 main_pages.json 登记路由页。
- [入口页 Navigation 宿主：NavDestination 首屏只在 navDestination 映射中注册并压入同一栈，不作根内容；.navDestination 直接传 @Builder](lesson-8953e390416a80d7dd8c.lesson.md)
  - 时机：入口页实现或收尾接线阶段，创建 Navigation 宿主、决定首屏放在根内容还是压栈、编写 navDestination 分发时
  - 情境：目标入口页用 Navigation + @Provider NavPathStack 承载路由；首屏（启动页等）写成返回 NavDestination 的组件，在 onReady 取栈并按启动决策 pushPathByName 下一页；目的地由 @Builder 映射分发。
  - 例外：首屏是普通组件（不返回 NavDestination）、作为 Navigation 根内容常驻，且不依赖 NavDestinationContext 取栈
- [同一目标页有多个启动入口时，按全部源端入口的 Intent extras 定义一个共享路由载荷，并实现每个来源分支](lesson-953309e05bc1cd36c0d1.lesson.md)
  - 时机：功能切片、页面转换与编译修复阶段，为有多个入口的目标页（如搜索页）定义路由参数、编写各入口的 push 与接收端解析、实现选中结果的去向时
  - 情境：Android 目标 Activity 被多个入口以不同 Intent extras 启动（如 searchText、locationType、searchFromMap），并按这些 extra 决定结果去向（setResult 回传或跳转下一页）；目标用 NavPathStack 传单一 param，各入口由不同切片、编译修复或巡检修复分别写入。
- [嵌在 Swiper/Tabs 里的页面组件只用 @Consumer 注入的根 NavPathStack，不在 onReady 用 context.pathStack 覆盖](lesson-1cebb531c991239d2691.lesson.md)
  - 时机：页面转换与主壳接线阶段，为由主页 Tab/Swiper 承载的 Fragment 页确定导航栈来源、编写 onReady 时；把已有页面接入主页 Swiper/Tabs 时
  - 情境：Android 主 Activity 用 ViewPager/底部 Tab 承载多个 Fragment；目标由入口页 Navigation 以 @Provider 提供根 NavPathStack，主页 Swiper 嵌入各 Tab 页组件，子页用 @Consumer('navPathStack') 取栈，外层仍保留 NavDestination 与 onReady；工程里经 pushPathByName 压栈的页面普遍在 onReady 写 this.navPathStack = context.pathStack。
  - 例外：页面本身经 pushPathByName 压入根栈、不在 Swiper/Tabs 子树内时，onReady 的 context.pathStack 就是根栈，该赋值无害
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
- [源页面由点击回调经 ViewModel 副作用导航时，逐个导航出口在目标 onClick 落实际跳转与参数，不留只含注释的回调](lesson-32af50a1dfb0c1c254af.lesson.md)
  - 时机：界面实现与返修阶段，为页面中的卡片、列表项、空状态按钮编写点击处理与跨页跳转时
  - 情境：源 Fragment 的点击回调触发 ViewModel 副作用（如 OpenTripDetail(id)、OpenCreateTrip），再由副作用处理函数调 findNavController().navigate 并带 bundleOf 参数；目标页面自行用 router 或 NavPathStack 跳转。
- [经 router.pushUrl 进入的 @Entry 页在 aboutToAppear 用 router.getParams() 读取必填入参，不声明等待外部赋值的普通字段](lesson-0d7d6e7302f8c8c77c66.lesson.md)
  - 时机：页面实现阶段，编写由 router.pushUrl 打开、需要入参（如详情 id）的 @Entry 页面时；给页面补 @Entry 或登记路由时
  - 情境：源端 Fragment 经 Navigation Component 进入，nav_graph 声明必填 &lt;argument&gt;，Fragment 用 requireArguments()/navArgs 读取；目标页登记在 main_pages.json、以 @Entry 页面经 router.pushUrl({ url, params }) 打开。
  - 例外：目标页作为 NavDestination 经 NavPathStack 进入：从 NavPathStack 的参数取值；该 struct 是被父组件实例化的子组件：入参由父组件构造时传入
- [被 @Entry 页直接组合的子组件要拦截返回键时，由 @Entry 页的 onBackPress 转调子组件注册的处理函数](lesson-803ba029eea852122e77.lesson.md)
  - 时机：页面转换与接线阶段，为源端非根 Composable 里的 BackHandler/PredictiveBackHandler 选择 ArkUI 返回键钩子时
  - 情境：源端在抽屉宿主等非 Activity 根的 Composable 中按状态条件拦截返回（例如抽屉打开时先关抽屉）；目标端该组件不是 @Entry，由唯一的 @Entry 页直接组合，没有作为页面驻留在 Navigation 路由栈内。
  - 例外：组件本身就是 @Entry 页时，直接实现 onBackPress；组件作为 NavDestination 驻留在 Navigation 栈内时，返回由 NavDestination.onBackPressed 处理；来源实测只覆盖被直接组合、未入栈的情况
- [页面路由参数的缺失哨兵值与有效性判定保持一致，错误态下隐藏依赖该参数的操作入口](lesson-c433adebb9d20f273b22.lesson.md)
  - 时机：页面转换阶段为目的地参数写默认值、有效性判定和无效路由错误态时
  - 情境：目标页从路由参数取 id，参数类有默认值；规格要求缺失 id 进入无效路由错误态、不渲染假数据；页面上有开始、编辑等依赖该 id 的按钮。
