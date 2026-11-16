# 构造 PoiQueryV2 时 city 不传空串，空时回退有效城市码并 setCityLimit(false)

审的是：代码
触发（任一种）：
- 读到：高德鸿蒙搜索 SDK 的 PoiSearchV2 声明里，PoiQueryV2 的 city 注明「必须定义，不能为空」「@param city … 必设参数」；写错的样子：代码里 new PoiQueryV2(keyword, '', city) 的 city 默认成 ''，或调用方以 city ?? '' 透传空串，并按 city 是否为空切换 setCityLimit
适用范围：鸿蒙工程用高德鸿蒙搜索 SDK 的 PoiQueryV2 做关键词搜索，而调用方可能不给城市时
做法：
- city 为空时先回退成一个有效城市码再构造：new PoiQueryV2(<关键词>, <类型，可为 ''>, <非空城市码>)
- 回退后调 query.setCityLimit(false) 保留全国搜索，并 query.setPageNum(1)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- PoiQueryV2 构造的 city：必须定义，不能为空（必设参数）：空串不是合法的「不限城市」（出处：高德鸿蒙搜索 SDK 的 PoiSearchV2.d.ets，PoiQueryV2 构造的 @param city（卡里读到的声明，search 11.2.0））
- 空城市回退安卓端的默认城市码，setCityLimit(false)、setPageNum(1)：修好后的查询参数（出处：卡里修好并验证过）
针对本应用要查的：
- 城市为空时回退用的城市码：源工程安卓端发起 POI 搜索的代码（PoiSearch.Query 的 city 参数）或它引用的默认城市常量；取安卓端没有城市时传的那个城市码（城市编码或 adcode）作回退值
未核实：修复后真机仍为空结果（后来定位为 Key 平台不匹配的环境问题），回退城市码和 setCityLimit(false) 单独能否让搜索出结果没有上机确认；setPageNum(1) 的必要性卡里没有单独说明
来源：1 张卡，1 个应用
- case-15e27ba62ddc28121b8e（android-panorama-map-vest7）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 1 ← 诊断；取值 2 ← 诊断
