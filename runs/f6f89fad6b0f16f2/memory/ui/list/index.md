# ui/list

列表与宫格：多类型 Adapter 页面的 item 布局与绑定分支（默认态、文案模板、附属子卡），分页加载的并发门闩与刷新互斥，多列 Grid 中占位与跨列项的排布，列表项主副行与空值回退，多组列表的数据源绑定与级联选择

[上一级](../index.md)

## 本级经验

- [SmartRefreshLayout 的加载更多转成 onReachEnd 时，显式建立“加载中不重入、刷新中不派发”的门闩](lesson-0a398b212a8a80bd0c7f.lesson.md)
  - 时机：数据接线阶段，把 SmartRefreshLayout 的 onRefresh/onLoadMore 实现为 Refresh.onRefreshing 与 List/Grid.onReachEnd 分页处理时；规格提取阶段写分页竞态约束时
  - 情境：源页面由 SmartRefreshLayout 驱动分页（setOnLoadMoreListener、观察者里 finishRefresh/finishLoadMore），页面本身没有 isLoading 变量；ViewModel 的页码在响应成功后才自增；目标用 Refresh + onReachEnd 并以 concat 追加。
- [列表项新增独立副行显示某字段时，主行的空值回退不再回退到同一字段](lesson-b202de11960c156829b5.lesson.md)
  - 时机：界面实现阶段，迁移设备、联系人等列表项的主标题、副标题与空值回退文案时
  - 情境：源端列表项只有一个名称控件，名称为空时回退显示地址或 ID；目标布局另加了一行地址/ID 副标题；名称来自平台接口，无名条目较多。
- [多类型 Adapter 承载的页面按全部 item 布局和 handleXxx 分支建区块：默认态、文案模板与附属子卡都来自绑定代码](lesson-e17b45a28a8d92ecbd01.lesson.md)
  - 时机：界面实现与返修重建阶段，把主体内容由 RecyclerView 多类型 Adapter 承载的 Android 页面转成 ArkUI 页面、确定各区块结构与背景层级时
  - 情境：源页面布局只有头图与 SwipeRefreshLayout/RecyclerView 外壳，首屏卡片、趋势图、网格等区块分散在 addItemType 登记的 item 布局与 handleXxx/convert 绑定里：默认选中态、setText 拼接的文案模板（如“平均温度X”“N天降温/M天升温”）、按条件 visibility 显示的附属子卡；UI 快照可能是合成的，item 布局清单可能为空。
- [恒空的广告或占位不在多列 Grid 里生成通栏项](lesson-2bd2620e5d1ef4bb17b4.lesson.md)
  - 时机：界面实现阶段，把含广告跨列的 RecyclerView 多类型网格转成 ArkUI Grid，决定 no-op 占位是否生成 GridItem 与跨列配置时；规格把广告定为 no-op 时
  - 情境：源端 GridLayoutManager 多列，spanSizeLookup 让广告项跨满一行，广告按固定间隔插入（可能紧跟奇数个内容项）；目标端广告是恒空的桩（零高容器）。
- [按源端适配器绑定核对每个列表的数据源：不同分组不复用同一数组，级联选择实现逐级推进与回退](lesson-b6146f290e871c82e61d.lesson.md)
  - 时机：界面与数据实现阶段，把源端多个 RecyclerView/Adapter（热门、全量、当前层级）迁移为 ArkUI 列表或网格时
  - 情境：源端页面有多组列表分别绑定不同数据（热门城市、省份、当前层级子列表），点击推进到下一层级并支持返回上一级。
