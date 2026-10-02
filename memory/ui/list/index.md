# ui/list

列表与宫格：多类型 Adapter 页面的 item 布局与绑定分支（默认态、文案模板、附属子卡），分页加载的并发门闩与刷新互斥，多列 Grid 中占位与跨列项的排布，列表项主副行与空值回退，多组列表的数据源绑定与级联选择，列表项滑动操作（swipeAction）的挂载位置，LazyForEach 改 Repeat.virtualScroll 时的项高度与数据切换核对，按列表区分的排序器，侧栏分类与右侧分组列表的联动，条目点击回调与数据源本地变换（shuffled 等）随列表迁移，ExpandableListView 组头的默认交互与展开状态

[上一级](../index.md)

## 本级经验

- [ExpandableListView 未设组点击监听时组头仍按默认切换展开；按 isExpanded 切换的资源由可变展开状态驱动](lesson-e01c6f821d631fad5383.lesson.md)
  - 时机：界面实现及对齐修复阶段，把 ExpandableListView + BaseExpandableListAdapter 翻译为 ArkUI 列表，确定组头交互与展开状态时
  - 情境：源 Activity 只调用 expandGroup(n) 设定初始展开，没有 setOnGroupClickListener（或监听返回 false）；getGroupView 按 isExpanded 切换上下箭头等资源；目标用 List/ForEach 渲染分组。
  - 例外：源端注册了 OnGroupClickListener 并返回 true 拦截默认行为，此时按监听体实现
- [SmartRefreshLayout 的加载更多转成 onReachEnd 时，显式建立“加载中不重入、刷新中不派发”的门闩](lesson-0a398b212a8a80bd0c7f.lesson.md)
  - 时机：数据接线阶段，把 SmartRefreshLayout 的 onRefresh/onLoadMore 实现为 Refresh.onRefreshing 与 List/Grid.onReachEnd 分页处理时；规格提取阶段写分页竞态约束时
  - 情境：源页面由 SmartRefreshLayout 驱动分页（setOnLoadMoreListener、观察者里 finishRefresh/finishLoadMore），页面本身没有 isLoading 变量；ViewModel 的页码在响应成功后才自增；目标用 Refresh + onReachEnd 并以 concat 追加。
- [为新列表数据路径选排序时找到源端该列表自己的排序器，不复用同文件其他列表的比较函数](lesson-eb59181d6dfaeb014aef.lesson.md)
  - 时机：功能实现阶段，为待办、日程等不同列表的数据查询选择排序比较器时
  - 情境：源端按列表区分排序器（如待办用专门的排序器：未完成在前、同状态按创建时间降序），目标多个列表共用同一仓库查询与比较函数，写者正在为新列表加查询方法。
- [侧栏分类页的右侧做成承载全部一级分组的 List + Scroller：点击 scrollToIndex、onScrollIndex 回写，并迁移程序滚动保护](lesson-7723af3766fb843a2577.lesson.md)
  - 时机：规格提取与界面实现阶段，迁移“左侧一级分类栏 + 右侧分组内容区”的分类页、确定右侧展示范围与左右联动时；按“对比源端”修复联动时
  - 情境：源端左侧一级分类与右侧按一级分类分组的单一滚动列表双向联动：点击左侧滚到对应分组，滚动右侧回写左侧选中项，并用标志位屏蔽点击引发的程序滚动回调（如 LazyListState、animateScrollToItem、visibleItemsInfo）；规格可能只写“右侧展示对应分类分组”“用列表控制器表达选择与滚动联动”。
- [列表项新增独立副行显示某字段时，主行的空值回退不再回退到同一字段](lesson-b202de11960c156829b5.lesson.md)
  - 时机：界面实现阶段，迁移设备、联系人等列表项的主标题、副标题与空值回退文案时
  - 情境：源端列表项只有一个名称控件，名称为空时回退显示地址或 ID；目标布局另加了一行地址/ID 副标题；名称来自平台接口，无名条目较多。
- [列表项滑动操作挂在 ListItem 上；把行内容抽成 @Builder 时核对容器专属属性实际接在哪个组件](lesson-feaf8a4a916a022b13a1.lesson.md)
  - 时机：界面实现阶段，把 ItemTouchHelper/SwipeActions 的滑动操作转换为 ListItem.swipeAction，并把行布局抽成 @Builder 时
  - 情境：规格与映射参考要求用 ListItem.swipeAction；行内容抽成 @Builder 方法，LazyForEach/ForEach 里的 ListItem 只调用该 builder。
- [多类型 Adapter 承载的页面按全部 item 布局和 handleXxx 分支建区块：默认态、文案模板与附属子卡都来自绑定代码](lesson-e17b45a28a8d92ecbd01.lesson.md)
  - 时机：界面实现与返修重建阶段，把主体内容由 RecyclerView 多类型 Adapter 承载的 Android 页面转成 ArkUI 页面、确定各区块结构与背景层级时
  - 情境：源页面布局只有头图与 SwipeRefreshLayout/RecyclerView 外壳，首屏卡片、趋势图、网格等区块分散在 addItemType 登记的 item 布局与 handleXxx/convert 绑定里：默认选中态、setText 拼接的文案模板（如“平均温度X”“N天降温/M天升温”）、按条件 visibility 显示的附属子卡；UI 快照可能是合成的，item 布局清单可能为空。
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
- [迁移列表时连同条目点击回调与数据源的本地变换（shuffled、filter、sort）一起实现，不只迁渲染](lesson-46307bc26d725b4634ca.lesson.md)
  - 时机：页面 UI 转换阶段，迁移 RecyclerView/Adapter 列表的条目点击与数据源初始化时
  - 情境：源 Fragment 经 adapter 的点击回调或 addOnItemTouchListener 把条目内容回填到输入框等；列表数据来自 ViewModel 对本地静态种子做 shuffled() 等纯本地变换；目标的对应 ViewModel 尚未建立。
