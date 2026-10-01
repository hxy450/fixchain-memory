# ui/navigation/parameters

跳转契约：点击接导航、路由名与参数、默认值/有效性、多个来源入口，以及跳转前共享状态的交接。

[上一级](../index.md)

## 本级经验

- [Compose 带参路由迁到 NavPathStack 时，目的地名用固定名、参数只走 param，pageMap 按固定名精确匹配](lesson-300200dd52892e9dadd2.lesson.md)
  - 时机：界面转换与导航壳实现阶段，写 pushPathByName 与 navDestination 分发时
  - 情境：源端 Compose Navigation 以带占位符的路由模式（如 detail/{id}）注册目的地，并用拼串函数生成实际路由；目标用 Navigation + NavPathStack，由 pageMap 按目的地名分发。
- [同一目标页有多个启动入口时，按全部源端入口的 Intent extras 定义一个共享路由载荷，并实现每个来源分支](lesson-953309e05bc1cd36c0d1.lesson.md)
  - 时机：功能切片、页面转换与编译修复阶段，为有多个入口的目标页（如搜索页）定义路由参数、编写各入口的 push 与接收端解析、实现选中结果的去向时
  - 情境：Android 目标 Activity 被多个入口以不同 Intent extras 启动（如 searchText、locationType、searchFromMap），并按这些 extra 决定结果去向（setResult 回传或跳转下一页）；目标用 NavPathStack 传单一 param，各入口由不同切片、编译修复或巡检修复分别写入。
- [源端跳转前写入的共享状态（如播放队列）是跳转契约的一部分，按原顺序迁移](lesson-dfcdbb19cd93d29159b2.lesson.md)
  - 时机：功能接线阶段，把列表项点击 → 启动目标页的链路迁成目标导航调用时；路由核验阶段比对跳转一致性时
  - 情境：源端点击处理在 startActivity 之前先把当前列表（过滤后）交给共享播放器或仓库（如 setPlaylist(list, position, true)），目标页只显示共享状态；目标跳转参数只带 id 一类字段。
- [源页面从 arguments、Intent extras 或缓存接收的实体键与数据，在目标以显式入参承接并由宿主真实传入](lesson-289cab2abd4268b26ce0.lesson.md)
  - 时机：界面转换与接线阶段，为 Tab 子组件、多实例子页或详情页定义入参，并在宿主或调用方挂载、跳转时；撤回或调整宿主传给子页面的参数时
  - 情境：源 Fragment 经 newInstance/arguments 或宿主 setCurrentCity 获得城市、ID 等实体键，详情 Activity 经 Intent Serializable 或首页缓存拿到首页数据；目标子组件以 @Param 或路由参数接收，宿主可能新增无参 Builder 挂载，或子组件改读全局选中状态。也包括子页面声明带默认值的状态参数（如当前分组类型），源端据此切换新增按钮与条目元信息，宿主在接线中写了该参数又删掉。
- [源页面由点击回调经 ViewModel 副作用导航时，逐个导航出口在目标 onClick 落实际跳转与参数，不留只含注释的回调](lesson-32af50a1dfb0c1c254af.lesson.md)
  - 时机：界面实现与返修阶段，为页面中的卡片、列表项、空状态按钮编写点击处理与跨页跳转时
  - 情境：源 Fragment 的点击回调触发 ViewModel 副作用（如 OpenTripDetail(id)、OpenCreateTrip），再由副作用处理函数调 findNavController().navigate 并带 bundleOf 参数；目标页面自行用 router 或 NavPathStack 跳转。
- [经 router.pushUrl 进入的 @Entry 页在 aboutToAppear 用 router.getParams() 读取必填入参，不声明等待外部赋值的普通字段](lesson-0d7d6e7302f8c8c77c66.lesson.md)
  - 时机：页面实现阶段，编写由 router.pushUrl 打开、需要入参（如详情 id）的 @Entry 页面时；给页面补 @Entry 或登记路由时
  - 情境：源端 Fragment 经 Navigation Component 进入，nav_graph 声明必填 &lt;argument&gt;，Fragment 用 requireArguments()/navArgs 读取；目标页登记在 main_pages.json、以 @Entry 页面经 router.pushUrl({ url, params }) 打开。
  - 例外：目标页作为 NavDestination 经 NavPathStack 进入：从 NavPathStack 的参数取值；该 struct 是被父组件实例化的子组件：入参由父组件构造时传入
- [路由参数以接收端契约为准：接收方不读取或写死的 extra 不透传，也不在目标页新增对它的消费](lesson-4a7c04b864ef635c87b6.lesson.md)
  - 时机：功能接线阶段，为跨页跳转构造目标页参数、决定哪些发起页状态要带过去时；为目标页新增入参消费或入页自动动作时
  - 情境：源发起页用 putExtra 传一个开关（如显隐标签），但接收 Activity 不读取该 extra，或创建 Fragment 时写死该参数；目标页参数类已用默认值与注释标明该字段由接收端固定。也包括多个调用方 putExtra 一个看似有含义的开关（如“显示一键登录弹窗”），接收 Activity 从不读取；目标页准备在 onReady 读取该参数并触发自动动作。
- [页面路由参数的缺失哨兵值与有效性判定保持一致，错误态下隐藏依赖该参数的操作入口](lesson-c433adebb9d20f273b22.lesson.md)
  - 时机：页面转换阶段为目的地参数写默认值、有效性判定和无效路由错误态时
  - 情境：目标页从路由参数取 id，参数类有默认值；规格要求缺失 id 进入无效路由错误态、不渲染假数据；页面上有开始、编辑等依赖该 id 的按钮。
