# Slice 计划碰到厂商 SDK 时追加 hmos-sdk-docs，依赖声明和初始化列进 scope

审的是：计划与派工
触发（任一种）：
- 读到：skill 映射表把高德列为 hmos-sdk-docs 的厂商 SDK；feature spec 的范围写「高德地图、定位权限、POI 搜索」，数据流写「关键词→PoiSearchV2→结果列表」；写错的样子：Slice 计划 Step 3c 的 suggested_skills 里没有 hmos-sdk-docs，scope 只列服务层、没有 SDK 依赖声明与初始化，占位表为空；或者把整套地图、定位、POI、路线能力登记为 deferred 占位
适用范围：按 feature spec 写 Slice 计划、为任务绑定 suggested_skills 和登记占位时，源端依赖厂商 SDK 的那些 Slice
做法：
- 按 feature spec 里的厂商 SDK 关键词逐项追加 suggested_skills（高德 → hmos-sdk-docs），scope 里列上 SDK 依赖声明（oh-package.json5 的 dependencies）和初始化
- 提交前逐个核对：某个 SDK 既没有 skill 绑定、又没有 `thirdparty-sdk` 占位，就是计划缺口，补齐后再交
- 决策里已查到厂商鸿蒙包时，不把整套地图、定位、POI、路线能力登记为 deferred 占位，只把 Harmony Key 列为待用户提供项
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- @amap/amap_lbs_common、@amap/amap_lbs_map3d、@amap/amap_lbs_search、@amap/amap_lbs_location、@amap/amap_lbs_navi：要列进 scope 的高德鸿蒙依赖（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-02861b75cc4ec53a32d9（android-panorama-map-vest7）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4；做法第 3 步 ← 建议 3；取值 1 ← 诊断
