# ui/list

列表与宫格：多类型 Adapter 页面的 item 布局与绑定分支（默认态、文案模板、附属子卡），分页加载的并发门闩与刷新互斥，下拉刷新 onRefreshing 在程序置 refreshing 时的触发，多列 Grid 中占位与跨列项的排布，列表项主副行与空值回退，多组列表的数据源绑定与级联选择，列表项滑动操作（swipeAction）的挂载位置，长按上下文菜单的契约，宿主改写共享行组件时的覆盖入参，LazyForEach 改 Repeat.virtualScroll 时的项高度与数据切换核对，按列表区分的排序器，侧栏分类与右侧分组列表的联动，条目点击回调与数据源本地变换（shuffled 等）随列表迁移，ExpandableListView 组头的默认交互与展开状态，异步分页列表新增批量修补时的代次保护与行内远端提交的在途锁；可换位列表的位置相关值（首尾、序号、移动可用态）按当前位置求值

[上一级](../index.md)

## 本级经验

- [ExpandableListView 未设组点击监听时组头仍按默认切换展开；按 isExpanded 切换的资源由可变展开状态驱动](lesson-e01c6f821d631fad5383.lesson.md)
  - 时机：界面实现及对齐修复阶段，把 ExpandableListView + BaseExpandableListAdapter 翻译为 ArkUI 列表，确定组头交互与展开状态时
  - 情境：源 Activity 只调用 expandGroup(n) 设定初始展开，没有 setOnGroupClickListener（或监听返回 false）；getGroupView 按 isExpanded 切换上下箭头等资源；目标用 List/ForEach 渲染分组。
  - 例外：源端注册了 OnGroupClickListener 并返回 true 拦截默认行为，此时按监听体实现
- [LazyForEach 改为 Repeat.virtualScroll 时逐个列表核对：含 Stretch/layoutWeight 装饰的内容定高项先核首项](lesson-150e48577e599f64ee23.lesson.md)
  - 时机：架构重构或缺陷修复阶段，把 LazyForEach 列表改写为 Repeat(...).virtualScroll() 并确定验收方式时
  - 情境：List 的每个 ListItem 高度由内容决定（按日期分组、条数不等、可折叠），项内有依赖父约束定尺寸的装饰（alignSelf(ItemAlign.Stretch) 贯穿轴线、layoutWeight 竖线或内容列）；或列表按日期、分页整体替换数组。
  - 例外：项高度固定或由显式尺寸决定，且已在设备上核过首项 bounds
- [RecyclerView Adapter 承载的列表或页面，按每类 viewType 实际 inflate 的 item 布局与绑定建区块和外观](lesson-e17b45a28a8d92ecbd01.lesson.md)
  - 时机：界面实现与返修重建阶段，把主体由 RecyclerView（尤其多类型 Adapter）承载的 Android 页面或列表转成 ArkUI，确定各区块结构、卡片背景圆角与背景层级时；参照兄弟页面卡片实现时；规格准备阶段为列表页登记 item 布局时
  - 情境：源页面布局只有头图与 SwipeRefreshLayout/RecyclerView 外壳，或 RecyclerView 用 tools:listitem 引用 item 布局；区块与行分散在 addItemType/onCreateViewHolder inflate 的各类 item 布局与 convert/bind 绑定里：默认选中态、setText 拼接的文案模板、按条件 visibility 显示的附属子卡。某类 holder 在绑定时 addView/inflate 子视图（如根视图为 CardView、带 cardCornerRadius），另一类有自己的背景 drawable。UI 快照可能是合成的，item 布局清单可能为空或只登记了一类。
- [Refresh.onRefreshing 会在程序置 refreshing 时触发，发起刷新前先判断是否已在运行](lesson-fa79c5a6658c68b71a21.lesson.md)
  - 时机：界面转换时把 SwipeRefreshLayout 映射为 Refresh，以及接线时把运行态事件接到 refreshing 绑定状态时
  - 情境：源 setOnRefreshListener 只响应用户下拉，另由运行态事件 setRefreshing 同步指示器；目标 Refresh({ refreshing: $$state }) 的状态会被事件或菜单刷新程序置为 true。
- [SmartRefreshLayout 刷新与加载更多转成 Refresh + onReachEnd 时建立互斥门闩：加载不重入、刷新中不派发加载](lesson-0a398b212a8a80bd0c7f.lesson.md)
  - 时机：数据接线阶段，把 SmartRefreshLayout 的 onRefresh/onLoadMore 实现为 Refresh.onRefreshing 与 List/Grid.onReachEnd 分页处理时；规格提取阶段写分页竞态约束时
  - 情境：源页面由 SmartRefreshLayout 驱动分页（setOnLoadMoreListener、观察者里 finishRefresh/finishLoadMore），页面本身没有 isLoading 变量；ViewModel 的页码在响应成功后才自增；目标用 Refresh + onReachEnd 并以 concat 追加。
  - 例外：Refresh 的 refreshing 被程序置真引起的重复刷新，按刷新入口单飞的规则处理；多个页面入口共用单例 ViewModel 的请求去重按共享加载的规则处理
- [为某个宿主改写共享组件时加默认保持原行为的覆盖入参，并检索全部宿主调用点](lesson-67e0a326dea085296fb9.lesson.md)
  - 时机：列表页与弹层接线阶段，源宿主或子类 adapter 改配共享行内的按钮或显隐，或要给多页共享的组件新增宿主须接的事件时
  - 情境：子类用另一动作按钮配置改写次级按钮（图标、文案、点击一起换），宿主按状态把按钮设为 GONE，或为某个宿主给共享面板新增回调事件；目标行组件或面板被多页共享，写者常受写盘边界限制。
- [会换位或增删的列表，位置相关值按当前位置计算：ForEach 不取闭包 index，Repeat 在构建表达式里直接读 ri.index](lesson-09a0bceae55d05616ecc.lesson.md)
  - 时机：界面实现阶段，把 Compose itemsIndexed 一类按当前 index 计算行参数的列表迁成 ForEach/Repeat，且列表会换位（上移、下移、拖动）、插入或删除条目时
  - 情境：源端每次重组把当前 index 传给条目（isFirst/isLast、序号、首尾行形状、移动按钮可用态）；目标 ForEach/Repeat 以实例 id 或内容为键（不含位置），在 itemGenerator 中用闭包 index 计算这些值并作为子组件的构造参数，或改用 Repeat 后以 RepeatItem.index 传值。
  - 例外：键本身随位置变化（如以位置拼键），换位即重建、生成函数随之重跑时，不需要另算位置；条目显示的内容（不是位置）在对象替换后不刷新：按列表键与对象替换的规则处理
- [侧栏分类页的右侧做成承载全部一级分组的 List + Scroller：点击 scrollToIndex、onScrollIndex 回写，并迁移程序滚动保护](lesson-7723af3766fb843a2577.lesson.md)
  - 时机：规格提取与界面实现阶段，迁移“左侧一级分类栏 + 右侧分组内容区”的分类页、确定右侧展示范围与左右联动时；按“对比源端”修复联动时
  - 情境：源端左侧一级分类与右侧按一级分类分组的单一滚动列表双向联动：点击左侧滚到对应分组，滚动右侧回写左侧选中项，并用标志位屏蔽点击引发的程序滚动回调（如 LazyListState、animateScrollToItem、visibleItemsInfo）；规格可能只写“右侧展示对应分类分组”“用列表控制器表达选择与滚动联动”。
- [列表长按上下文菜单按源 onCreateContextMenu 契约逐项移植：长按弹菜单、选择态早返回、标题、可见项与 XML 顺序](lesson-9975dd1d15f5c73758e8.lesson.md)
  - 时机：功能接线阶段，为列表页、共享组件与区段组件实现条目长按交互和上下文菜单时
  - 情境：源列表经 registerForContextMenu 与 onCreateContextMenu 弹出菜单：选择模式中直接返回、setHeaderTitle 设标题、共享准备函数决定可见项；部分菜单项在 XML 中 android:visible=false、只在特定页面或子类中 setVisible(true)（例如进入多选的动作项）；onContextItemSelected 处理点击；目标要在多个页面、共享组件和区段组件中移植。
- [列表项滑动操作挂在 ListItem 上；把行内容抽成 @Builder 时核对容器专属属性实际接在哪个组件](lesson-feaf8a4a916a022b13a1.lesson.md)
  - 时机：界面实现阶段，把 ItemTouchHelper/SwipeActions 的滑动操作转换为 ListItem.swipeAction，并把行布局抽成 @Builder 时
  - 情境：规格与映射参考要求用 ListItem.swipeAction；行内容抽成 @Builder 方法，LazyForEach/ForEach 里的 ListItem 只调用该 builder。
- [异步分页列表新增批量异步修补（如返回时逐条查询行内标记）时，按列表代次丢弃过期结果、按 ID 修补当前列表，不整表回写](lesson-4cfd4cbcecfb3de96037.lesson.md)
  - 时机：列表页实现阶段，为触底分页、下拉刷新的列表新增返回后状态同步等批量异步查询时
  - 情境：列表由分页回调异步追加、下拉刷新整体替换；返回页面时要逐条 await 本地查询来刷新行内标记；页面可能已有请求序号或 busy 锁保护了部分入口。
- [恒空的广告或占位不在多列 Grid 里生成通栏项](lesson-2bd2620e5d1ef4bb17b4.lesson.md)
  - 时机：界面实现阶段，把含广告跨列的 RecyclerView 多类型网格转成 ArkUI Grid，决定 no-op 占位是否生成 GridItem 与跨列配置时；规格把广告定为 no-op 时
  - 情境：源端 GridLayoutManager 多列，spanSizeLookup 让广告项跨满一行，广告按固定间隔插入（可能紧跟奇数个内容项）；目标端广告是恒空的桩（零高容器）。
- [每个列表的数据按源端该列表自己的路径迁移：各 Adapter 绑定各自的数据源与层级状态，本地变换和排序器取自该列表，不复用别的列表](lesson-b6146f290e871c82e61d.lesson.md)
  - 时机：界面与数据实现阶段，把源端多个 RecyclerView/Adapter（热门、全量、当前层级）迁移为 ArkUI 列表或网格时；为某个列表准备数据（本地 shuffled/filter/sort）或新增列表查询、选择排序比较器时
  - 情境：源页面有多组列表分别绑定不同数据（热门、全量分组、当前层级子列表），点击推进到下一层级并支持返回；或列表数据来自对本地集合做 shuffled()/filter/sortedWith 等纯本地变换；或源端按列表区分排序器与排序键（如某列表专用的 Comparator 与另一列表的排序键不同），目标多个列表共用同一仓库查询与比较函数。
  - 例外：数据依赖网络、跨页状态等当前确实不可得的工件时，按前向依赖登记；本条只覆盖可在本地完成的数据准备
- [迁移 RecyclerView/Adapter 列表时连同条目点击与触摸监听一起实现：逐项在条目上接事件，不只迁渲染](lesson-46307bc26d725b4634ca.lesson.md)
  - 时机：页面 UI 转换阶段，迁移 RecyclerView/Adapter 列表的条目交互时
  - 情境：源 Fragment 经 adapter 的点击回调（setOnItemClickListener、ViewHolder 中的 setOnClickListener）或 RecyclerView.addOnItemTouchListener 把条目内容回填到输入框、跳转或切换状态；目标列表只迁了样式链。
- [配置驱动的编辑项列表按源工厂表逐项分派：每个 type 接对应页面、按配置顺序在同一列表内渲染，未匹配类型空渲染](lesson-71f8a80418dbc2c442ce.lesson.md)
  - 时机：界面实现与对齐阶段，为按配置列表生成的编辑区确定每项的承载组件、顺序与间距，或增删列表的过滤条件时
  - 情境：源端遍历配置列表，经 type→Fragment 工厂创建子 Fragment 并按顺序加入同一个无间距容器，未匹配类型落到空 Fragment；目标工程已有逐类型专页，另有页内编辑器、通用控件骨架等替代入口。
