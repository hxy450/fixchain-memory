# 网络配置的注入和初始化时机

agent 会看到什么：读到 buildConfigField / BuildConfig 里的地址和签名材料、Hilt @Provides 里带上的 Retrofit baseUrl、决策要求私有注入；产物里 HttpClient 的 baseUrl 空串默认、init() 的调用点、BuildProfile 读取和装配根的配置构造

## 规矩

- rule-f05bdb5f24c0｜源端 baseUrl 由注入带上、目标改显式 init 时，在 EntryAbility.onCreate 调它｜读到：源端 Retrofit.Builder().baseUrl(...) 在 Hilt 模块的 @Provides 方法里注入时带上，Application.onCreate 里没有网络初始化调用；写错：目标网络层的 baseUrl 默认空串、只在 init() 里赋值，但 EntryAbility.onCreate 里没有调用这个 init()，或者只在业务服务（如环境切换）里调用
- rule-527f237c3acf｜静态 HttpClient 的 baseUrl 为空时先报「网络层未初始化」，不把相对路径交给 http.request｜写错：静态 HttpClient 的 baseUrl 默认空串，请求时直接拼 baseUrl + path 交给 httpRequest.request()，没有判空
- rule-b68613cfa9fb｜装配根不用空字符串构造网络配置，接入构建期生成的配置，缺失就显式失败｜读到：源端 gradle / BuildConfig 已有服务端地址和签名材料，决策要求私有注入；写错：装配根写 new …Config('', …, '') 这类以空 baseUrl、空签名密钥构造客户端、不传解码器，靠网络层的空配置守卫返回失败
- rule-4b905aa96eb2｜决策要求构建期注入网络配置时，网络层在同一任务交付配置来源和响应解码器｜读到：源端 gradle 里定义 API_HOST、签名材料和 AES_KEY，代码读 BuildConfig.API_HOST；决策台账要求签名/加密材料经构建 profile 或 gitignored 本地私有配置注入、由网络层集中读取；写错：网络层只把 baseUrl、signSecret、解码器做成配置类的构造参数（解码器默认 null），没有任何配置读取，也没有解码器实现，回执写「通过 … 注入」把接线推给装配者
- rule-424fa275dd75｜运行配置只从环境变量读、缺省写死时，改用 BuildProfile 构建期字段作缺省｜读到：源端成功码、渠道、客户端 id、项目 id 来自 assets 下的配置 json、flavor 常量或 buildConfigField；写错：目标代码里这些配置只从 `getEnvironmentVar` 读，读不到时落到源码里写死的缺省（空串密钥、与源端不同的渠道或 id），没有读 `BuildProfile` 字段
