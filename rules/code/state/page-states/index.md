# 页面加载、空与错误状态

源 Screen 用 hiltViewModel()、collectAsState() 由 ViewModel 和网络状态驱动，或 UiState、规格、决策台账分出 loading、failed、空态、不可用，目标页有加载、空、错误分支，或是模板空壳、写死的假数据时

## 触发族

- [由 ViewModel 和网络状态驱动的源页面](viewmodel-driven-page/index.md)（2 条）：读到的源 Screen 用 hiltViewModel()、collectAsState() 取状态、数据来自 Repository；交回的目标页是模板空壳、写死的假数据，或没有加载、空、错误状态
- [加载、失败、空态和不可用等页面状态](page-load-states/index.md)（3 条）：读到规格、UiState 或决策台账分出 loading、failed、空态、定位不可用、Result 联合；交回的 ViewModel 只有 isLoading / items，页面用 items.length === 0 出空态，或数据层失败时 return []
