# ViewModel 多路请求的部分失败和缓存

agent 会看到什么：读到源 ViewModel 先读缓存再请求、几个请求各自 launch、只在 Result.Success 时替换数据（或规格写「失败读有效缓存、不清空整页」），交回的代码把任一失败映射成整页 ERROR、返回 FAILED 加空模型，或全失败时仍写新时间戳的缓存

## 规矩

- rule-53a4107579b6｜源端多个请求各自 launch、各自更新时，目标页按区块分别判成功失败，不用 a 或 b 为空判整页错误｜读到：源 ViewModel 里几个请求各自 `launch`，各自只在 `Result.Success` 时写自己的 `LiveData`，Activity 各自 observe；规格写「任一请求失败保留其他已成功区块，不清空整页」；写错：目标页面用 `=== null ||` 把两支结果连起来，任一为空就整页 `ERROR`
- rule-2d5d8ab039df｜源页面先用缓存填充再请求详情时，组件的详情失败分支保留内容加轻提示，不切整页 ERROR｜读到：源 Fragment 先读缓存填充列表和趋势，再请求单日详情；ViewModel 只在 Result.Success 时替换数据、失败不动已有内容；决策台账写「网络失败优先读有效缓存、禁止白屏」；写错：组件把网关的 FAILED 和异常一律映射成整页 ERROR 态，build 里只渲染错误文字加重试，日期条和各模块只来自网关成功结果
- rule-88c89f8ba23f｜详情网关先取同城首页缓存构造基础数据再用详情覆盖，失败返回带缓存的结果，不返回 FAILED 加空模型｜读到：源端加载流程先从缓存读首页数据（列表、逐小时、实时、趋势），详情接口只补选中日，ViewModel 只在 Result.Success 时替换选中日；决策台账要求网络失败优先读有效缓存；写错：网关只调详情接口，catch 分支返回 FAILED 加 new 出来的空数据模型，不读首页缓存，也不回填日期列表
- rule-369a0003837b｜多路请求聚合写 TTL 缓存时，全失败不写新时间戳，命中同时校验载荷非空｜读到：安卓源码按刷新时间加 TTL 判定缓存，用 viewModelScope.async 并发两路请求、各路可单独失败；规格验收条目写「成功后写入缓存」「不把空模型等同网络成功」；写错：代码在 Promise.allSettled 的结果全是 `rejected`（或各路载荷全为 null）时仍以 Date.now() 写入载荷为空的缓存记录；缓存命中只比较保存时间与 TTL
- rule-963cea6b8dbc｜决策要求失败保持最近成功数据时，catch 不清空列表，页面只在成功时整体替换｜读到：决策台账写「失败保持显式错误与最近成功数据，不伪造空成功」（显式 Result + 最近成功缓存 + 重试）；写错：ViewModel 的列表加载 catch 里把已成功的 items / groups 清空，或页面同步状态时无条件用 ViewModel 的列表整体替换（replaceAll）
