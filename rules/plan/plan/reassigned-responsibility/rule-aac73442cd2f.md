# 三方地图改平台替代时，计划写成具体任务：组件依赖、key 注入、坐标系转换、未配置态验收

审的是：计划与派工
触发（任一种）：
- 读到：源端用第三方地图 SDK 的 MapView；规格或决策只写「地图承载组件」「可验证地图承载」；写错的样子：计划里没有单独的地图接入任务，没写目标组件和依赖、key / client_id 怎么注入、GCJ-02 与 WGS-84 的转换和未配置态的验收
适用范围：规格和计划阶段处理「三方地图改平台替代」这一决策时
做法：
- 单列一个地图接入任务，写明：目标组件与依赖（Map Kit 的 MapComponent 或已决策的三方 SDK）、key / client_id 的注入方式、定位坐标系到地图坐标系的转换（GCJ-02 与 WGS-84）、未配置态的验收条目
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- CoordinateType.WGS84 = 0、CoordinateType.GCJ02 = 1：Map Kit 的两种坐标系（出处：鸿蒙 SDK 的 hms/ets/api/@hms.core.map.mapCommon.d.ts，mapCommon.CoordinateType）
- map.convertCoordinate 目前只支持 WGS84 转 GCJ02：任务里写坐标转换时的方向限制（出处：鸿蒙 SDK 的 hms/ets/api/@hms.core.map.map.d.ts，map.convertCoordinate）
- CoordinateSystemType.WGS84 = 1、CoordinateSystemType.GCJ02 = 2：同族接口：平台定位（地理围栏）一侧的坐标系枚举，取值和 Map Kit 不同（出处：鸿蒙 SDK 的 ets/api/@ohos.geoLocationManager.d.ts，geoLocationManager.CoordinateSystemType）
针对本应用要查的：
- 源端地图 SDK 用的坐标系和 key 配置方式：源工程 AndroidManifest.xml 里地图 SDK 的 meta-data key、模块构建脚本里的地图依赖，以及定位回调里传给地图的坐标；写进任务：目标端对应的依赖、key 放在哪类配置文件里、坐标要不要转换
来源：1 张卡，1 个应用
- case-d24a32433de0efe7a6a0（骑行记录）：做法第 1 步 ← 建议 3
