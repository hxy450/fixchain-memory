# 由 ViewModel 和网络状态驱动的源页面

agent 会看到什么：读到的源 Screen 用 hiltViewModel()、collectAsState() 取状态、数据来自 Repository；交回的目标页是模板空壳、写死的假数据，或没有加载、空、错误状态

## 规矩

- rule-becbf41a82f3｜首页等数据驱动页面按源 ViewModel 接真实数据并保留加载、空、错误三态，不写死假数据｜读到：源首页由 ViewModel / Repository 驱动：hiltViewModel()、collectAsState() 取网络列表状态，Banner、分类、商品都来自实体数据；写错：目标页把分类写成固定字符串数组、Banner 用本地图标循环、商品卡片写死名称和价格，没有数据加载，也没有加载、空、错误状态
- rule-5b95168cff36｜源 Screen 由 ViewModel 和网络状态驱动时，目标页按源结构逐页转换，不用同一模板空壳｜读到：源 Screen 用 hiltViewModel()、collectAsState() 取状态，带 HorizontalPager、ScrollableTabRow、LazyColumn 等结构；写错：多个业务页由同一模板循环生成：build() 正文只有一个 Text("…内容开发中...")，或只有返回栏和「… 页面」标题文字
