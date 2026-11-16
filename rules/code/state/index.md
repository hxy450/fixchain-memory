# 状态与数据流

源端有 ViewModel、LiveData / Flow、Compose remember / mutableStateOf、EventBus、data class copy，目标端有 @Local、@Param、@ObservedV2 / @Trace、@Monitor、AppStorageV2、@Builder 传参和页面的加载、空、错误状态时

## 子主题

- [页面加载、空与错误状态](page-states/index.md)（5 条）：源 Screen 用 hiltViewModel()、collectAsState() 由 ViewModel 和网络状态驱动，或 UiState、规格、决策台账分出 loading、failed、空态、不可用，目标页有加载、空、错误分支，或是模板空壳、写死的假数据时
- [跨页面与跨组件的状态传递](passing/index.md)（29 条）：源端有多页共用的 ViewModel、EventBus 的 post / @Subscribe 和 setResult 回传、Activity 在 setContent 里下传的设置、共享页头、子 Composable 和子组件的状态参数，目标端有 AppStorageV2 / PersistenceV2.connect、@Param / @Event、@Builder 值参、事件 emit 和返回后刷新时
- [Compose 状态迁 V2 与 @Trace 观察](v2-reactivity/index.md)（19 条）：源端有 Compose remember / mutableStateOf / derivedStateOf、LaunchedEffect(key) 这类按键值重跑的副作用、data class copy 更新，目标端有 @Local、@Computed、@ObservedV2 / @Trace 模型和数组、@Watch / @Monitor、UIUtils.getTarget 时
- [ViewModel 与数据层](viewmodel/index.md)（20 条）：源端 ViewModel 用 LiveData / Flow 发布页面数据，数据来自 Repository、Room Dao、assets 文本、引擎或回调实现类，目标端有 VM、store、gateway 的字段从哪赋值、何时赋值、状态初值、addListener 订阅、写后刷新和给 UI 的门面接口时
