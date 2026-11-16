# OkHttp Cache 的 MiB 容量迁到 rcp CacheConfiguration.maxSize 时按字节传

审的是：代码
触发（任一种）：
- 读到：OkHttp 的 Cache(dir, N MiB) 提供自动 HTTP 缓存，容量常量按 MiB 写；写错的样子：rcp.ResponseCache 的 CacheConfiguration.maxSize 直接传 MiB 数（如 maxSize: 200），ResponseCache.set 报 item is too long for cache limits，缓存计数一直为 0
适用范围：目标端用 @kit.RemoteCommunicationKit 的 rcp.ResponseCache 做 HTTP 响应缓存、运行在 API 26 时（卡里实测的版本）
做法：
- new rcp.ResponseCache({ persistent: { kind: 'file-system', pathToFolder: <缓存目录> }, maxSize: <MiB 数> * 1024 * 1024 })，maxSize 按字节传；单测里自建缓存的 maxSize 同样按字节写
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- maxSize 传 MiB 数时 200 被当成 200 字节，约 216 字节的记录被拒；改成 maxSizeMb * 1024 * 1024 后缓存写入成功、相关用例全部通过：API 26 运行时 maxSize 的单位是字节（出处：卡里修好并验证过）
- constructor(configuration: CacheConfiguration)：ResponseCache 的构造；maxSize、maxItems 为负时抛 1007900401（出处：鸿蒙 SDK 的 hms/ets/api/@hms.collaboration.rcp.d.ts，rcp.ResponseCache.constructor）
- cache?: ResponseCache：把缓存挂到 rcp 的 Configuration 上（出处：鸿蒙 SDK 的 hms/ets/api/@hms.collaboration.rcp.d.ts，rcp.Configuration.cache）
- getState(): Promise<CacheState>，CacheState.count 是缓存里的响应条数：用来确认缓存确实写进去了（出处：鸿蒙 SDK 的 hms/ets/api/@hms.collaboration.rcp.d.ts，rcp.ResponseCache.getState）
未核实：按字节解释是卡里在 API 26 运行时实测的；本机 API 23 的声明写 50 MBytes by default、@default 50，API 23 运行时按哪种单位没核实
来源：1 张卡，1 个应用
- case-4315af870be24f182303（com.nononsenseapps.feeder）：做法第 1 步 ← 建议 1、诊断；取值 1 ← 诊断
