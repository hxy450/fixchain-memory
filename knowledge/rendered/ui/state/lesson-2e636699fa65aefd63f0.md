# 列表条目以新对象替换或整表重建时，ForEach/Repeat 键要包含会变且需要显示的字段；要稳定键就改为可观察实例原位更新

## 何时使用

功能实现与页面接线阶段，为可编辑或会重新拉取的列表选定条目更新方式与 ForEach 键时；为消除重建抖动而稳定 ForEach/Repeat 的键时

## 适用情境

列表条目编辑（如改名）后以保留 id 的新对象替换，或操作成功后重新请求列表并整表 setList（id 不变、计数等字段变化）；ArkUI 用 ForEach 渲染，并把条目字段作为子组件的 @Param 传入；源端是 Compose 不设 key 的 forEach 加不可变 copy，或 RecyclerView 整表刷新。也包括分页或 Swiper 的页模型是普通 interface，键原先拼入请求状态与数据导致每次加载都销毁重建（抖动），修复者准备把键缩成只含页标识。也包括 RecyclerView 的 remove+add+notifyItemChanged 被迁成 arr[pos] = 新实例、splice 或整表赋值，行内显示取自条目可变字段（下载态、播放态），注释以“@Trace 字段级刷新”代替键检查。也包括源端 removeAllViews 后逐项 inflate 的结果区改成嵌套 ForEach，键只用显示内容拼接（内容可能完全相同，如多个全零数据块），条目是普通 class，每次计算整体重建。

## 例外与边界

- 更新方式是对 @ObservedV2 条目的 @Trace 字段原地赋值，子组件绑定的仍是同一对象，此时可保留只含 id 的键

## 原因

ForEach 键值不变时复用已有子组件、不再执行条目构建，子组件拿不到替换后的新对象，界面停在旧值；Compose 不设 key 的 forEach 与 RecyclerView 整表刷新每次都拿到新值，所以源端没有这个问题。来源两例：改名后反馈与持久化都已更新，卡片仍显示旧名，只含 id 的键由早期页面写入、重建时被沿用，写码者读到的状态参考只讲“替换实例会触发刷新”；另一应用里弹层列表的键只含下标、id 与类型标志，写者认为“整表重载”即会重渲染，添加成功后计数停在旧值，而它读到的陷阱清单已写明同 id 新值重建时键须含可变字段。另一应用为消除翻页抖动把键缩成只含查询键，页模型仍是普通对象、异步结果以新对象替换，已创建的页节点再也收不到数据，各视图都显示为空；改成 @ObservedV2/@Trace 并原位更新才显示，后来又被改回不可变替换而再次无数据。@Trace 只追踪同一实例上的属性写入，不能代替键变化。只由显示内容拼出的键在内容重复时互相冲突，ForEach 只渲染其中一个；整体重建时内容相同的旧行又会被复用。同键复用时，条目生成函数里的事件闭包（onClick 等）捕获的行对象同样停在旧实例：整表重建为新对象后，闭包里按对象身份 indexOf 当前数组得 -1。键只含下标与分类属性、不含条目身份时，显示子集随宽度或方向变化会复用错位的子节点。

## 做法

1. 先定更新方式：替换对象或整表重建就把会变且显示的字段并入键，如 `${item.id}:${item.name}:${item.count}`；改为给 @Trace 字段原地赋值则可保留 id 键。
2. 写键前列出条目内所有展示字段，并查源端的刷新方式（替换对象、重新请求后 setList），不把“整表重载”当作会重渲染的依据。
3. 对每个修改动作核一遍：动作 → 数组元素是否换成新对象 → ForEach 键是否变化 → 子组件 @Param 与条目事件闭包（onClick 等）捕获的是哪个对象，确认新值能到达条目界面；闭包里要定位当前行时，按行内唯一字段在当前数组里 findIndex，不用对象身份 indexOf，也不用生成时的 index；键至少包含条目身份（id、资源 id 或命令标识），不只用下标加分类属性；页面交付自检对每个 ForEach 都做这一核对。
4. 为消除抖动稳定键时，同步把条目或页模型改为 @ObservedV2 类、需要显示的字段标 @Trace 并原位赋值，@Builder 与子组件 @Param 链传可观察实例或完整 RepeatItem；在测试断言或注释中写明该实例禁止整体替换。
5. 键要随新实例变化时也可追加实例分量（如按 WeakMap 记录的实例序号）：新实例得到新键而重建该行，同实例 @Trace 原地变更时键不变；接线时把数组元素替换写成新实例的同时核对该列表的键。
6. 条目内容可能重复时，键包含本次结果中的位置标识（如分组号加序号），再按需加内容字段；结果每次整体重建且条目是普通 class 时，给每次计算分配代次前缀写入键，确保旧行不被复用。

## 可选检查

- 行内状态（如下载完成后的按钮）在设备上不刷新时，检索写入新对象而键不含实例分量的列表

来源支持：10 张卡 · 9 次迁移 · 9 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕ForEach(arr: Array<any>, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string)（首段 @since 7）：第三个参数自定义键值；LazyForEach(dataSource: IDataSource, itemGenerator, keyGenerator?) 的第三个参数同样是键值生成函数
- 〔原因 / 做法第 1 步〕ForEach 非首次渲染时逐项生成新键值：键值在上次渲染中已存在就不创建新组件、不重跑条目生成函数，直接渲染该键值对应的已有组件；键值不存在才为该项新建组件
- 〔原因 / 做法第 1、3 步〕ForEach 的对象数组项被替换、而新项生成的键值没变时，ForEach 不把数据更新同步给子组件，子组件仍绑定旧数组项，之后新项的属性变化子组件也感知不到；文档的使用建议因此写明数组项为对象类型时不建议用内容相同的数组项替换旧项
- 〔做法第 1 步〕ForEach 不传 keyGenerator 时默认键值为 index + '__' + JSON.stringify(item)；itemGenerator 声明了 index 参数而 keyGenerator 没声明 index 时，框架把 index 拼接在 keyGenerator 返回值之后作为最终键值。文档建议键值里用与 UI 显示相关的数据属性
- 〔原因 / 做法第 3、6 步〕ForEach 键值只用下标时，在数组中间插入一项后旧下标键全被复用、只有末尾新建，界面显示错位（文档例：期望 ['one','new item','two','three']，实际 ['one','two','three','three']）；键值含 index 或用默认键时，插入点之后的项都会重建。文档不建议键值含 index，但说明 index 是保证键值唯一的最终手段，确需使用要接受数据源变更后重建组件的性能损耗
- 〔原因 / 做法第 6 步〕ForEach 对重复键值发运行时警告，不同数组项键值相同时框架行为未定义：首次渲染遇到已出现过的键值不再创建组件（文档例 ['one','two','two','three'] 只建一个 two），UI 更新时出现重复键值框架可能无法正常工作
- 〔例外与边界 / 做法第 1、4 步〕declare const ObservedV2: ClassDecorator、declare const Trace: PropertyDecorator、declare const Param: PropertyDecorator（均 @since 12）：@ObservedV2 类（须用 new 创建）中 @Trace 属性的值变化会触发绑定该属性的 UI 组件刷新，没加 @Trace 的属性变化不触发刷新；观察的是这个对象上的属性写入，数组元素换成另一个对象不在其内。@Trace 修饰的 Array 可观测 push、pop、shift、unshift、splice、copyWithin、fill、reverse、sort
- 〔做法第 4 步〕Repeat 的键值由 RepeatAttribute<T>.key(keyGenerator: (item: T, index: number) => string): RepeatAttribute<T>（@since 12）生成，Repeat 根据键值是否变化判断数据项是否更新；.key() 缺省时生成新的随机键值，发现重复键时在已有键值上递归生成新键直到不重复；文档要求同一数据项每次输出一致、数组变化后仍唯一，允许但不建议用 index
- 〔做法第 4 步〕Repeat 不设 .virtualScroll()（全量加载模式）时页面刷新取决于键值变化：更新前后键值相同，即使数据改变页面也不刷新；设了 .virtualScroll()（懒加载模式，须配合状态管理 V2 与 List、Grid、Swiper、WaterFlow、ListItemGroup 使用）时键值变化或数据变化都会触发刷新，复用缓存池节点时只更新节点的 item 和 index，子孙组件按 V2 规则同步
- 〔做法第 4 步〕Repeat 与 @Builder 或自定义组件混用时，只传 RepeatItem.item 或 RepeatItem.index（按值传递），参数值改变不会引起 @Builder 内的 UI 刷新；整体传 RepeatItem（按引用）才能监听到数据变化；API 20 起也可用 UIUtils.makeBinding() 和 Binding / MutableBinding 传参
- 〔原因 / 做法第 3 步〕安卓 ListActivity 把 ListView 的 AdapterView.OnItemClickListener 转发到 onListItemClick(ListView l, View v, int position, long id)：position 是点击时被点视图在 ListView 里的位置（ListView 加了 header 时 adapter 被包成 HeaderViewListAdapter，position 把 header 计在内），id 是 adapter.getItemId(position)；方法说明建议用 getListView().getItemAtPosition(position) 取数据，即点击时按位置从当前 adapter 取，不经过行对象身份
- 〔原因〕设备上 ForEach 键只含 id（或 id 加下标、静态标志）时，以同 id、字段已变的新对象替换数组项或整表重新赋值后，该行仍显示旧对象的字段：改名后反馈已是新名而卡片仍为旧名；添加成功后计数停在旧值
- 〔原因 / 做法第 4 步〕设备上 Swiper 页用 ForEach、键只含页标识、页模型是普通 interface、异步结果以新对象替换数组项时，已创建的页节点一直收不到新数据，各视图显示为空；用 Repeat 而把 RepeatItem.item 解包传给子组件时同样为空；页模型为 @ObservedV2/@Trace 且新数据在同一实例上原位赋值时能显示，以不可变新对象替换时无数据
- 〔原因 / 做法第 3 步〕设备上整表重建为新对象（如 onPageShow 重新加载）而 ForEach 键不变时，该行不重跑条目生成函数，onClick 闭包捕获的仍是旧对象：在新数组上 indexOf(旧对象) 得 -1，arr[-1] 为 undefined，继续访问其属性抛 TypeError 闪退
- 〔适用情境 / 原因〕设备上 Repeat 键只含 id 与选中位时，以同 id 新实例替换数组元素（arr[pos] = 新对象后整体赋值），行内由新实例字段推导的按钮保持旧状态（下载完成后仍显示下载）；卡里没写这个 Repeat 是否开了 virtualScroll
