# 高德 POI 搜索和定位接口的调用

agent 会看到什么：读到高德的 PoiSearchV2 / PoiQueryV2、InputtipsQuery 或 AMapLocation 的 district / city；产物里查询对象带的参数、定位后的地名，以及手头没有 SDK 时服务层用什么顶替

## 规矩

- rule-f5b1c46baa9e｜spec 要求的 SDK 能力手头没有 SDK 时，登记 thirdparty-sdk 占位，不用本地替代静默顶替｜读到：feature spec 数据流写「关键词→PoiSearchV2→结果列表」，验收条目要求非空关键词调用 POI 搜索；写错：服务层里非空关键词改成过滤本地历史记录（按名称、地址匹配取前 N 条），没有 PoiSearchV2 对应的 SDK 调用，也没有 `PLACEHOLDER` 标记、`thirdparty-sdk` 占位登记或计划缺口回报
- rule-36fd89207756｜移植时换掉参考实现的查询 API，就按新 API 的声明补齐它要求的参数｜读到：参考实现的关键词搜索走 InputtipsQuery(keyword, city)，周边搜索的 PoiQueryV2 同时设置了 location 和 bound；写错：移植代码换用了别的查询 API（如关键词搜索改成 new PoiQueryV2），新 API 要求的参数（city，或周边搜索的 location、bound）没补
- rule-0b980e45dc1d｜构造 PoiQueryV2 时 city 不传空串，空时回退有效城市码并 setCityLimit(false)｜读到：高德鸿蒙搜索 SDK 的 PoiSearchV2 声明里，PoiQueryV2 的 city 注明「必须定义，不能为空」「@param city … 必设参数」；写错：代码里 new PoiQueryV2(keyword, '', city) 的 city 默认成 ''，或调用方以 city ?? '' 透传空串，并按 city 是否为空切换 setCityLimit
- rule-b44a8015c32d｜源定位 SDK 直接给行政区名而目标只给坐标时，用 getAddressesFromLocation 取名，不写空名｜读到：源端定位回调取 AMapLocation 的 district（为空取 city）作为地名，再用经纬度在本地城市库粗筛；规格要求匹配失败时保留定位名称；写错：目标定位服务只返回 getCurrentLocation 的坐标，粗筛为空时城市对象名称写成 ''；「已定位」只按本地城市 ID > 0 判断
