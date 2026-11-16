# spec 要求的 SDK 能力手头没有 SDK 时，登记 thirdparty-sdk 占位，不用本地替代静默顶替

审的是：代码
触发（任一种）：
- 读到：feature spec 数据流写「关键词→PoiSearchV2→结果列表」，验收条目要求非空关键词调用 POI 搜索；写错的样子：服务层里非空关键词改成过滤本地历史记录（按名称、地址匹配取前 N 条），没有 PoiSearchV2 对应的 SDK 调用，也没有 `PLACEHOLDER` 标记、`thirdparty-sdk` 占位登记或计划缺口回报
适用范围：实现阶段遇到 spec 要求的厂商 SDK 能力（POI 搜索、地图、路线等），而当前没有 SDK 或 skill 可用时
做法：
- 登记 `thirdparty-sdk` 占位，或回报计划缺口，让上游补 SDK 依赖和 skill
- 不用本地历史过滤等替代实现顶替 SDK 能力并当作满足验收条目；接入 SDK 后可以保留本地结果作失败时的回退
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 接入 @amap/amap_lbs_search 后，POI 搜索改为高德优先、失败回退本地历史：返修后的形态（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-02861b75cc4ec53a32d9（android-panorama-map-vest7）：做法第 1 步 ← 建议 5；做法第 2 步 ← 建议 5、诊断；取值 1 ← 诊断
