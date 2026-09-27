# data/network

网络层：服务地址与环境、URL 拼接、拦截器注入的公共请求头、请求体字段、登录凭证来源与失效踢登

[上一级](../index.md)

## 本级经验

- [Service 只收不透明请求体时，从源端调用链追到 body 的构造处照抄字段与取值来源，不用空对象占位](lesson-0bc494e864b2d8ab1a34.lesson.md)
  - 时机：数据层实现与规格提取阶段，编写 Repository 调用网络 Service、确定 POST 请求体字段时
  - 情境：目标 Service 方法只接收 data: Object（对应源端 @Body RequestBody），规格 API 表没列这个端点或它的请求字段；源端由 ViewModel 调用某个 Repository 方法，在那里组装 body（如 device_id 取自设备 ID 工具）。
- [服务地址与环境沿地址键名追到源端常量与取址逻辑：分清各接口族的 host，环境枚举与默认环境按源端规则映射](lesson-246252824c631aa6eff5.lesson.md)
  - 时机：规格提取与网络基础设施实现阶段，确定服务地址、环境枚举与默认环境时
  - 情境：API 清单或规格只给出地址键名（如 SpKey.BASE_URL），没有实际 host；源端按接口族分设多套后端地址（如 Java 旧接口与 Go 新接口），由 DI 模块或环境工具类按构建类型选择环境。
- [源端从响应头取 token/refreshToken 时，HTTP 封装把响应头交给调用方，Repository 按源端成功回调取值](lesson-2a4e6af209308c08aaa6.lesson.md)
  - 时机：网络与登录数据层的规格提取和实现阶段，确定登录类接口凭证的取值来源与 HTTP 封装的返回结构时
  - 情境：源端 Retrofit 登录接口返回 Response&lt;BaseResponse&lt;T&gt;&gt;，Repository 在成功回调里用 headers()\["Authorization"\]、headers()\["RefreshToken"\] 写 TokenManager，body 的 data 只含用户信息；目标端 HTTP 封装统一返回解析后的响应体。
- [源端拦截器统一注入的请求头逐条迁到 HttpClient 默认头，头名与格式以源码为准，不照模板写 Bearer 前缀](lesson-217e93ef9097efc519f1.lesson.md)
  - 时机：网络基础层实现阶段，写 HttpClient 默认请求头与 Authorization 取值格式时
  - 情境：源端用 OkHttp 拦截器（如 TokenInterceptor）给每个请求加鉴权、语言、平台、地区等头，接口声明上看不到这些头；目标端用 @ohos.net.http 自建 HttpClient，skill 参考模板示范 `Authorization: Bearer ${token}`；API 清单可能只给出拦截器路径和 header_write 一类标签。
- [源端构建期注入的服务地址、签名与响应解密材料，按决策从私有构建配置接入并实现同算法解码器；不以空配置装配网络客户端](lesson-30ccd1d65d2c39029256.lesson.md)
  - 时机：网络基础设施实现与装配阶段，实现网络运行配置来源、响应解密，并在装配根构造 HTTP 客户端时
  - 情境：源端通过 BuildConfig/gradle 注入 API 地址、请求签名材料与 release 响应的 AES 等解密密钥，并在解析前解密响应；目标决策要求密钥不进源码、构建期从本地私有配置注入，网络层对空配置拒绝发包；另有决策只记录了“未提供测试环境或测试账号”。
- [用字符串拼接替代 Retrofit 时，在拼接函数里统一处理 baseUrl 与 path 之间的斜杠，不依赖各接口 path 的写法](lesson-d767b84213eb5ef93034.lesson.md)
  - 时机：网络层实现阶段，把 Retrofit 接口迁成自写 HttpClient，确定 baseUrl 常量与各 Service 的 path 如何连成完整 URL 时
  - 情境：源端用 Retrofit 的 baseUrl 加 @GET/@POST 相对路径（多数不带前导 /，少数带），目标端改用 @kit.NetworkKit http 手工拼 URL；参考模板示范 `${baseUrl}${path}` 直接拼接；baseUrl 常量与各 Service 的 path 分散在不同文件里声明。
- [鉴权失效判定按源响应拦截器实际分支的错误码与动作迁移，不把错误码枚举里的举例成员当触发条件](lesson-bad79e090d2af44d167b.lesson.md)
  - 时机：规格提取与网络层实现阶段，写 token 失效判定、踢登与刷新策略时
  - 情境：源端由响应拦截器按响应体 reasonCode 分支踢登，错误码枚举里同时有多个登录/token 相关成员（LoginExpired、TokenEmpty、TokenExpired、TokenInvalid、RemotingLoginExpired 等）；刷新 token 可能在进入主页的初始化请求里调用，不在拦截器里。
