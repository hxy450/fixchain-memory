# ui/list

列表与宫格：多类型 Adapter 页面的 item 布局与绑定分支（默认态、文案模板、附属子卡），分页加载的并发门闩与刷新互斥，下拉刷新 onRefreshing 在程序置 refreshing 时的触发，多列 Grid 中占位与跨列项的排布，列表项主副行与空值回退，多组列表的数据源绑定与级联选择，列表项滑动操作（swipeAction）的挂载位置，长按上下文菜单的契约，宿主改写共享行组件时的覆盖入参，LazyForEach 改 Repeat.virtualScroll 时的项高度与数据切换核对，按列表区分的排序器，侧栏分类与右侧分组列表的联动，条目点击回调与数据源本地变换（shuffled 等）随列表迁移，ExpandableListView 组头的默认交互与展开状态，异步分页列表新增批量修补时的代次保护与行内远端提交的在途锁；可换位列表的位置相关值（首尾、序号、移动可用态）按当前位置求值；LazyForEach 整批换数据或延迟填充时的稳定数据源、reload 通知与跨数据集唯一键；按末项可见状态触发的追加加载（不以 onReachEnd 代替），滚动中计算条目可见比例（onVisibleAreaChange）；LazyColumn stickyHeader 的吸顶分组结构（吸顶内容留在 List 内）

[上一级](../index.md)

## 本级经验

- [ExpandableListView 未设组点击监听时组头仍按默认切换展开；按 isExpanded 切换的资源由可变展开状态驱动](lesson-e01c6f821d631fad5383.lesson.md)
  - 时机：界面实现及对齐修复阶段，把 ExpandableListView + BaseExpandableListAdapter 翻译为 ArkUI 列表，确定组头交互与展开状态时
  - 情境：源 Activity 只调用 expandGroup(n) 设定初始展开，没有 setOnGroupClickListener（或监听返回 false）；getGroupView 按 isExpanded 切换上下箭头等资源；目标用 List/ForEach 渲染分组。
  - 例外：源端注册了 OnGroupClickListener 并返回 true 拦截默认行为，此时按监听体实现
- [LazyForEach 整批替换或延迟填充数据时保持同一数据源实例并发 onDataReloaded 等通知，不重新赋值数据源对象](lesson-92ced15126309dd90a1a.lesson.md)
  - 时机：界面实现、返修或重写阶段，为 LazyForEach 列表实现源端 setAdapter、notifyDataSetChanged 一类整批换数据、排序或延迟填充时
  - 情境：目标列表用 LazyForEach 绑定实现 IDataSource 的数据源对象，并把该对象存在组件状态里；源端在排序、筛选、切换适配器或延迟加载后整批替换数据，写者准备用“this.数据源 = 新数据源”换数据。
  - 例外：列表改用 ForEach 或 Repeat 绑定可观察数组：数组整体重新赋值本身会触发刷新
- [Refresh.onRefreshing 会在程序置 refreshing 时触发，发起刷新前先判断是否已在运行](lesson-fa79c5a6658c68b71a21.lesson.md)
  - 时机：界面转换时把 SwipeRefreshLayout 映射为 Refresh，以及接线时把运行态事件接到 refreshing 绑定状态时
  - 情境：源 setOnRefreshListener 只响应用户下拉，另由运行态事件 setRefreshing 同步指示器；目标 Refresh({ refreshing: $$state }) 的状态会被事件或菜单刷新程序置为 true。
- [SmartRefreshLayout 的加载更多转成 onReachEnd 时，显式建立“加载中不重入、刷新中不派发”的门闩](lesson-0a398b212a8a80bd0c7f.lesson.md)
  - 时机：数据接线阶段，把 SmartRefreshLayout 的 onRefresh/onLoadMore 实现为 Refresh.onRefreshing 与 List/Grid.onReachEnd 分页处理时；规格提取阶段写分页竞态约束时
  - 情境：源页面由 SmartRefreshLayout 驱动分页（setOnLoadMoreListener、观察者里 finishRefresh/finishLoadMore），页面本身没有 isLoading 变量；ViewModel 的页码在响应成功后才自增；目标用 Refresh + onReachEnd 并以 concat 追加。
- [stickyHeader 用 ListItemGroup 头部加 List.sticky(StickyStyle.Header)，吸顶内容不移出 List](lesson-2674172eb470a443213d.lesson.md)
  - 时机：界面实现与规格映射阶段，把 Compose LazyColumn 的 stickyHeader（含按开关在吸顶与普通项之间切换）落成 ArkUI 列表结构，或对吸顶写法没把握、准备改用别的结构时
  - 情境：源端 LazyColumn 内用 stickyHeader 放吸顶内容，其余项随列表滚动，可能由 pinned 一类开关在 stickyHeader 与 item 之间切换；规格映射为 List + ListItemGroup(StickyStyle.Header)，或并列给出“Stack + offset”一类备选；转换批次禁止编译，写者记不清吸顶 API。
- [为新列表数据路径选排序时找到源端该列表自己的排序器，不复用同文件其他列表的比较函数](lesson-eb59181d6dfaeb014aef.lesson.md)
  - 时机：功能实现阶段，为待办、日程等不同列表的数据查询选择排序比较器时
  - 情境：源端按列表区分排序器（如待办用专门的排序器：未完成在前、同状态按创建时间降序），目标多个列表共用同一仓库查询与比较函数，写者正在为新列表加查询方法。
- [为某个宿主改写共享组件时加默认保持原行为的覆盖入参，并检索全部宿主调用点](lesson-67e0a326dea085296fb9.lesson.md)
  - 时机：列表页与弹层接线阶段，源宿主或子类 adapter 改配共享行内的按钮或显隐，或要给多页共享的组件新增宿主须接的事件时
  - 情境：子类用另一动作按钮配置改写次级按钮（图标、文案、点击一起换），宿主按状态把按钮设为 GONE，或为某个宿主给共享面板新增回调事件；目标行组件或面板被多页共享，写者常受写盘边界限制。
- [会换位或增删的列表，位置相关值（首尾标记、序号、上移/下移可用态、首尾圆角）在渲染时按当前位置计算，不取 ForEach/Repeat 生成时的闭包 index](lesson-09a0bceae55d05616ecc.lesson.md)
  - 时机：界面实现阶段，把 Compose itemsIndexed 一类按当前 index 计算行参数的列表迁成 ForEach/Repeat，且列表会换位（上移、下移、拖动）、插入或删除条目时
  - 情境：源端每次重组把当前 index 传给条目（isFirst/isLast、序号、首尾行形状、移动按钮可用态）；目标 ForEach/Repeat 以实例 id 或内容为键（不含位置），在 itemGenerator 中用闭包 index 计算这些值并作为子组件的构造参数。
- [侧栏分类页的右侧做成承载全部一级分组的 List + Scroller：点击 scrollToIndex、onScrollIndex 回写，并迁移程序滚动保护](lesson-7723af3766fb843a2577.lesson.md)
  - 时机：规格提取与界面实现阶段，迁移“左侧一级分类栏 + 右侧分组内容区”的分类页、确定右侧展示范围与左右联动时；按“对比源端”修复联动时
  - 情境：源端左侧一级分类与右侧按一级分类分组的单一滚动列表双向联动：点击左侧滚到对应分组，滚动右侧回写左侧选中项，并用标志位屏蔽点击引发的程序滚动回调（如 LazyListState、animateScrollToItem、visibleItemsInfo）；规格可能只写“右侧展示对应分类分组”“用列表控制器表达选择与滚动联动”。
- [列表长按上下文菜单按源 onCreateContextMenu 契约逐项移植](lesson-9975dd1d15f5c73758e8.lesson.md)
  - 时机：功能切片接线阶段，为列表页与首页区段实现条目长按交互和上下文菜单时
  - 情境：源经 registerForContextMenu 与 onCreateContextMenu 弹出菜单：选择模式中直接返回、设置标题、共享准备函数决定可见项、multi_select 默认隐藏仅子类开放；目标在多个页面、共享组件和区段组件中移植。
- [列表项新增独立副行显示某字段时，主行的空值回退不再回退到同一字段](lesson-b202de11960c156829b5.lesson.md)
  - 时机：界面实现阶段，迁移设备、联系人等列表项的主标题、副标题与空值回退文案时
  - 情境：源端列表项只有一个名称控件，名称为空时回退显示地址或 ID；目标布局另加了一行地址/ID 副标题；名称来自平台接口，无名条目较多。
- [列表项滑动操作挂在 ListItem 上；把行内容抽成 @Builder 时核对容器专属属性实际接在哪个组件](lesson-feaf8a4a916a022b13a1.lesson.md)
  - 时机：界面实现阶段，把 ItemTouchHelper/SwipeActions 的滑动操作转换为 ListItem.swipeAction，并把行布局抽成 @Builder 时
  - 情境：规格与映射参考要求用 ListItem.swipeAction；行内容抽成 @Builder 方法，LazyForEach/ForEach 里的 ListItem 只调用该 builder。
- [多 viewType 列表按每类 holder 的根布局与运行时挂入的子视图定卡片外观：某一类专属的背景、圆角、描边不写进各类共用的 Builder](lesson-9de4c7648d23db5d7f86.lesson.md)
  - 时机：界面实现阶段，为含普通项、推广项等多种 ViewHolder 的列表或网格确定卡片背景、描边与圆角，或参照兄弟页面的卡片实现时；规格准备阶段为列表页登记 item 布局时
  - 情境：Android 列表同时有多类 holder：普通项的外观来自 holder 运行时 addView/inflate 的组件根视图（如 CardView 的 cardCornerRadius），推广项另有带圆角描边的背景 drawable；目标准备用一个共用 Builder 渲染各类卡片，或照搬兄弟页面已有的“白底 + 描边 + 圆角”卡片。
- [多类型 Adapter 承载的页面按全部 item 布局和 handleXxx 分支建区块：默认态、文案模板与附属子卡都来自绑定代码](lesson-e17b45a28a8d92ecbd01.lesson.md)
  - 时机：界面实现与返修重建阶段，把主体内容由 RecyclerView 多类型 Adapter 承载的 Android 页面转成 ArkUI 页面、确定各区块结构与背景层级时
  - 情境：源页面布局只有头图与 SwipeRefreshLayout/RecyclerView 外壳，首屏卡片、趋势图、网格等区块分散在 addItemType 登记的 item 布局与 handleXxx/convert 绑定里：默认选中态、setText 拼接的文案模板（如“平均温度X”“N天降温/M天升温”）、按条件 visibility 显示的附属子卡；UI 快照可能是合成的，item 布局清单可能为空。
- [异步分页列表新增批量异步修补时按列表代次丢弃过期结果、按 ID 修补当前列表；行内远端提交按条目维护在途集合](lesson-4cfd4cbcecfb3de96037.lesson.md)
  - 时机：列表页实现阶段，为触底分页、下拉刷新的列表新增返回后状态同步，或接入逐行远端提交按钮（加入书架、收藏）时
  - 情境：列表由分页回调异步追加、下拉刷新整体替换；返回页面时要逐条 await 本地查询来刷新行内标记；每行还有调用远端接口的提交按钮；页面已有请求序号或 busy 锁保护了部分入口。
- [恒空的广告或占位不在多列 Grid 里生成通栏项](lesson-2bd2620e5d1ef4bb17b4.lesson.md)
  - 时机：界面实现阶段，把含广告跨列的 RecyclerView 多类型网格转成 ArkUI Grid，决定 no-op 占位是否生成 GridItem 与跨列配置时；规格把广告定为 no-op 时
  - 情境：源端 GridLayoutManager 多列，spanSizeLookup 让广告项跨满一行，广告按固定间隔插入（可能紧跟奇数个内容项）；目标端广告是恒空的桩（零高容器）。
- [批量把 LazyForEach 改为 Repeat.virtualScroll 时逐个列表核对项高度与数据切换；内容定高、含 Stretch/layoutWeight 装饰的项先真机核首项尺寸，短列表按豁免用 ForEach](lesson-150e48577e599f64ee23.lesson.md)
  - 时机：架构重构或缺陷修复阶段，按规范批量改写列表渲染（LazyForEach → Repeat(...).virtualScroll()）并确定验收方式时
  - 情境：List 的每个 ListItem 高度由内容决定（按日期分组、条数不等、可折叠），项内有依赖父约束定尺寸的装饰（alignSelf(Stretch) 贯穿轴线、layoutWeight 竖线或内容列）；或列表按日期、分页整体替换数组。重构规则要求统一改用 Repeat 并加空参 virtualScroll()，允许短列表豁免。
  - 例外：项高度固定或由显式尺寸决定，且已在设备上核过首项 bounds
- [按源端适配器绑定核对每个列表的数据源：不同分组不复用同一数组，级联选择实现逐级推进与回退](lesson-b6146f290e871c82e61d.lesson.md)
  - 时机：界面与数据实现阶段，把源端多个 RecyclerView/Adapter（热门、全量、当前层级）迁移为 ArkUI 列表或网格时
  - 情境：源端页面有多组列表分别绑定不同数据（热门城市、省份、当前层级子列表），点击推进到下一层级并支持返回上一级。
- [源端按末项可见状态触发追加加载时，用 onScrollIndex 上升沿复刻，不用 onReachEnd](lesson-4cae87de686327ba6283.lesson.md)
  - 时机：规格提取与列表实现阶段，为分页列表确定触底自动追加加载的触发机制时
  - 情境：源列表用状态派生条件触发追加加载（如 derivedStateOf{最后可见项下标 == 总项数−1} 且不在重试态时 LaunchedEffect 执行一次），条件在首屏未铺满、数据变化或重试态变化后也会重新成立；目标平台另有 List.onReachEnd 这类滚动到底事件。
- [滚动中计算条目可见比例或离顶最近的可见项时，用 onVisibleAreaChange 加即时位置查询，不用 onAreaChange](lesson-0c2a39eb29e0ea76fb22.lesson.md)
  - 时机：列表界面实现阶段，把 onGloballyPositioned/boundsInWindow 一类随滚动变化的可见性计算（自动播放、曝光）迁到 ArkUI 时
  - 情境：源端在 LazyColumn 条目上用 onGloballyPositioned + boundsInWindow 在滚动中计算可见比例并选最近项自动播放；目标准备在条目上挂 onAreaChange。
- [迁移列表时连同条目点击回调与数据源的本地变换（shuffled、filter、sort）一起实现，不只迁渲染](lesson-46307bc26d725b4634ca.lesson.md)
  - 时机：页面 UI 转换阶段，迁移 RecyclerView/Adapter 列表的条目点击与数据源初始化时
  - 情境：源 Fragment 经 adapter 的点击回调或 addOnItemTouchListener 把条目内容回填到输入框等；列表数据来自 ViewModel 对本地静态种子做 shuffled() 等纯本地变换；目标的对应 ViewModel 尚未建立。
- [配置驱动的编辑项列表按源工厂表逐项分派：每个 type 接专属页面、按配置顺序在同一列表内渲染，未匹配类型空渲染；不压成通用控件、不移到列表外，也不用过滤条件静默去掉某类](lesson-71f8a80418dbc2c442ce.lesson.md)
  - 时机：界面实现与对齐阶段，为按配置（如 editorConfig）生成的编辑区确定每项的承载组件、顺序与间距，或增删列表的过滤条件时
  - 情境：源端编辑 Fragment 遍历配置，经工厂把每一项（含外观类 bg/textColor/border 与 photo、text 等）各自创建为对应 Fragment，按顺序加入同一个无间距容器，未匹配类型落到空 Fragment；目标工程已有大量逐类型专页，另有页内文本编辑器、通用控件骨架或子模块选择等替代入口。
