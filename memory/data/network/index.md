# data/network

网络层：服务地址与环境、运行配置的构建期注入、URL 拼接、拦截器注入的公共请求头、请求体字段与编码（表单或 JSON）、登录凭证来源与失效踢登，加解密工具的前置返回与异常回退、网关加密传输到 cryptoFramework 的移植，以及多路请求聚合结果的缓存写入与命中，拦截器读取的公共参数（设备标识、当前分组）的生产者，网络权限声明，请求通道内会话密钥前置门（ensureKey）的取舍与握手基址，按承载判定计费网络，链接 getter 追加的渠道等运行期参数

[上一级](../index.md)

## 本级经验

- [RSA-OAEP 包裹密钥加 AES-GCM 的网关移植 cryptoFramework：规格串不加编码后缀，结果判空，Buffer 按长度拷贝](lesson-3684e08592c85de82204.lesson.md)
  - 时机：网络基础设施实现阶段，把 Android 端 RSA-OAEP 包裹会话密钥加 AES-GCM 加密的网关传输改写为 ArkTS cryptoFramework 与 buffer 调用时（含为通过编译改写同步 API 与类型的收敛步骤）
  - 情境：源端用 X509EncodedKeySpec 解析“BEGIN PUBLIC KEY”PEM，以 RSA/ECB/OAEPWithSHA-256AndMGF1Padding 包裹随机密钥，用 AES/GCM/NoPadding 加密可能为空的请求体并解密响应；目标用 createAsyKeyGenerator/convertPemKeySync、Cipher.updateSync/doFinalSync 与 @kit.ArkTS buffer 实现同一协议。
- [Service 只收不透明请求体时，从源端调用链追到 body 的构造处照抄字段与取值来源，不用空对象占位](lesson-0bc494e864b2d8ab1a34.lesson.md)
  - 时机：数据层实现与规格提取阶段，编写 Repository 调用网络 Service、确定 POST 请求体字段时
  - 情境：目标 Service 方法只接收 data: Object（对应源端 @Body RequestBody），规格 API 表没列这个端点或它的请求字段；源端由 ViewModel 调用某个 Repository 方法，在那里组装 body（如 device_id 取自设备 ID 工具）。
  - 例外：源端构造处确实发送空 body（如空 Map 或空 RequestBody）时，照源发送空体
- [process.getEnvironmentVar 读的是设备进程环境：构建期材料不经它读取，保留的读取统一做空值兜底](lesson-ef06973d4b7affc03093.lesson.md)
  - 时机：实现或修复阶段，用 process.getEnvironmentVar 读取运行配置（成功码、密钥、渠道、客户端身份），或改写其“|| 默认值”回退链时
  - 情境：目标代码以 process.getEnvironmentVar(X) || 缺省 读取可选运行配置；安装到设备后进程环境通常没有这些变量；准备把缺省改为构建期字段，或改写回退链。
- [多路请求聚合写 TTL 缓存时全部失败不写新时间戳，命中同时校验时效与载荷非空](lesson-c6379cfcbee86500f91f.lesson.md)
  - 时机：数据层实现阶段，为首页等多路并发请求实现按键（如城市）的 TTL 缓存写入与命中判定时
  - 情境：源端或规格按键缓存多路并发结果，有效期为保存时间加源端 TTL 常量；每一路都可能失败；目标 Service 把各路结果聚合成一条缓存记录，命中条件只看保存时间。源端字面实现可能在全部失败时也以空结果和当前时间写缓存，而规格或决策要求成功后才写、网络失败时读有效缓存。
- [平台计费网络判定按承载显式映射，不直译为单一能力位](lesson-20afdfffa13dc5bca10c.lesson.md)
  - 时机：网络基础层实现阶段，把 isActiveNetworkMetered 等平台判定改写为 @ohos.net.connection 实现时
  - 情境：源以平台判定计费网络并门控刷新、下载、流播或图片，同一工具类对以太网另有放行；目标只能读取 networkCap 与 bearerTypes，SDK 声明没写各承载是否会置 NOT_METERED。
- [把 Retrofit 接口迁成手工拼 URL 时，按相对 URL 解析语义把 endpoint 解析到 baseUrl 上，不统一增删斜杠](lesson-d767b84213eb5ef93034.lesson.md)
  - 时机：网络层实现阶段，把 Retrofit 接口迁成自写 HttpClient，确定 baseUrl 常量与各 Service 的 path 如何连成完整 URL 时
  - 情境：源端用 Retrofit 的 baseUrl 加 @GET/@POST 路径（多数不带前导 /，少数带；baseUrl 可能只到 host，也可能带上下文路径如 /app/），目标改用 @kit.NetworkKit http 手工拼 URL；参考模板示范 `${baseUrl}${path}` 直接拼接；baseUrl 常量与各 Service 的 path 分散在不同文件里。
  - 例外：源端所有 endpoint 都只有一种写法、baseUrl 没有路径段，且没有完整 URL、//authority 或 ../ 形式时，可以用受限拼接（去掉重复斜杠后用一个 / 连接），并在拼接函数旁写明这个前提
- [拦截器按本地键读取的公共参数都要有生产者：按源端初始化序列补齐写入步骤，只迁读取侧不算完成](lesson-7e04234bdf5aef97b651.lesson.md)
  - 时机：迁移或重构隐私同意后的初始化链、网络公共参数与拦截器时，确认每个公参字段由谁写入时
  - 情境：目标拦截器每次请求从偏好键或当前选中项缓存读取设备标识等公参；源端这些值由隐私同意后的 SDK 初始化序列（如获取 OAID）写入，目标只迁了读取侧。
  - 例外：公参来自同步、扫描等多阶段流程的副作用写入（如同步后的默认选中项）时，见 data/sync 的多阶段流程副作用经验，在源序列对应位置落地
- [新增或改写请求通道时按源端重载决定是否内置取 key 门；确需门时按请求实际基址握手，不用运行期可改写的默认基址](lesson-62499aa25e87fa6ab5e1.lesson.md)
  - 时机：网络通道实现或修复阶段，为新增或改写的请求通道决定是否内置会话密钥前置门（ensureKey 一类）及其握手基址时
  - 情境：源端某请求方法只带公共头直接发送、不做前置握手，由调用方先按特定基址握手取会话 key；目标的 key 缓存按基址比对决定命中或重新握手，通道门控若取运行期可被改写的默认基址（例：选择地区或切换服务器后改写），就可能与调用方的握手基址不同。
- [服务地址与环境沿地址键名追到源端常量与取址逻辑：分清各接口族的 host，环境枚举与默认环境按源端规则映射](lesson-246252824c631aa6eff5.lesson.md)
  - 时机：规格提取与网络基础设施实现阶段，确定服务地址、环境枚举与默认环境时
  - 情境：API 清单或规格只给出地址键名（如 SpKey.BASE_URL），或没有产出 API 清单，没有实际 host；源端按接口族分设多套后端地址（如旧接口与新接口），由 DI 模块或环境工具类按构建类型选择环境；BuildConfig.BASE_URL 可能带上下文路径（如 /app/）。
  - 例外：地址与环境已经确定，要决定如何把构建期材料（地址、签名、密钥）注入目标并装配客户端时，见同主题构建期配置注入的经验
- [源端从响应头取 token/refreshToken 时，HTTP 封装把响应头交给调用方，Repository 按源端成功回调取值](lesson-2a4e6af209308c08aaa6.lesson.md)
  - 时机：网络与登录数据层的规格提取和实现阶段，确定登录类接口凭证的取值来源与 HTTP 封装的返回结构时
  - 情境：源端 Retrofit 登录接口返回 Response&lt;BaseResponse&lt;T&gt;&gt;，Repository 在成功回调里用 headers()\["Authorization"\]、headers()\["RefreshToken"\] 写 TokenManager，body 的 data 只含用户信息；目标端 HTTP 封装统一返回解析后的响应体。
- [源端声明 INTERNET 且目标发网络请求时，module.json5 声明 ohos.permission.INTERNET 并指定写入任务](lesson-faec7be031b7f64752c4.lesson.md)
  - 时机：迁移计划拆分、网络层实现与接线收尾阶段，确定由哪个任务、何时在 module.json5 声明网络权限时
  - 情境：源 AndroidManifest 声明 android.permission.INTERNET，可能还有 ACCESS_NETWORK_STATE；目标新建请求封装与页面调用，module.json5 尚无 requestPermissions，或只有其他功能的权限；计划模板按能力段给任务分配输入，网络层任务的写域可能不含 module.json5。
- [源端拦截器统一注入的请求头逐条迁到 HttpClient 默认头，头名与格式以源码为准，不照模板写 Bearer 前缀](lesson-217e93ef9097efc519f1.lesson.md)
  - 时机：网络基础层实现阶段，写 HttpClient 默认请求头与 Authorization 取值格式时
  - 情境：源端用 OkHttp 拦截器（如 TokenInterceptor）给每个请求加鉴权、语言、平台、地区等头，接口声明上看不到这些头；目标端用 @ohos.net.http 自建 HttpClient，skill 参考模板示范 `Authorization: Bearer ${token}`；API 清单可能只给出拦截器路径和 header_write 一类标签。
- [源端经 BuildConfig/gradle 注入服务地址、签名与解密材料时，目标从私有构建配置接入，不以空配置装配网络客户端](lesson-30ccd1d65d2c39029256.lesson.md)
  - 时机：网络基础设施实现与装配阶段，实现网络运行配置来源并在装配根构造 HTTP 客户端时
  - 情境：源端通过 BuildConfig/gradle 注入 API 地址、请求签名材料与 release 响应解密密钥；目标决策要求密钥不进源码、构建期从本地私有配置注入，网络层对空配置拒绝发包；另有决策只记录了“未提供测试环境或测试账号”。
  - 例外：地址与环境本身还没确定时，先按同主题服务地址经验沿键名追到源端取值
- [移植加解密工具与响应解码器时逐分支保留源端的前置返回与异常回退：空串不进 Cipher，解密失败回退为原文](lesson-4232e195ff42fc63ba43.lesson.md)
  - 时机：规格提取与网络层实现阶段，确定响应解密/解码步骤的算法与失败语义，或把 Android 请求参数加密与响应解密工具（AESUtil、aesEncrypt/aesDecrypt 一类）移植为 cryptoFramework 封装时
  - 情境：Android 加密工具开头以 isEmpty 直接返回空串、不调用 Cipher，解密在 catch 中返回原文（明文响应也能通过）；目标用 cryptoFramework 对每个业务值做 AES-CBC，业务参数可能为空（如缺省城市没有经纬度），部分接口返回明文 JSON。也包括源端在响应转换钩子（如 beforeResponse）里按 debug/release 解密响应，是否所有接口都返回密文没有抓包证据，规格或台账准备写“解密失败显式报错、不伪造成功”。
- [迁移 Retrofit POST 时按源方法注解定请求体编码：@FormUrlEncoded 发表单，@Body 看 Converter](lesson-1cc76f37fe0aea9fef25.lesson.md)
  - 时机：接口层实现、模块抽取或把调用搬到平台适配层时，为每个 POST 端点确定请求体编码与 Content-Type；发现同类编码偏差后确定修复范围时
  - 情境：源端经 Retrofit ApiService 发请求，调用点可能先经项目自己的 post(url, Map) 一类包装，最终选中的方法带 @FormUrlEncoded + @FieldMap/@Field、@Multipart + @Part 或 @Body；目标 HTTP 层默认以 application/json 发送，另有表单写法；规格或 API 清单只列参数名、不写 Content-Type，目标里可能已有沿用下来的 JSON 端点。
- [迁移源端链接 getter 时按完整返回表达式构造 URL，带上追加的运行期参数；query 以“key=”结尾是待补值信号](lesson-da377615b178b2fe0c67.lesson.md)
  - 时机：功能切片实现阶段，把源端配置读取与链接 getter（协议、隐私、个人信息清单等）迁移成目标 Service 里的 URL 常量或构造方法时
  - 情境：Android 从 assets JSON 等配置读取基础地址（query 以 aliasCode= 一类空值结尾），由配置类的 getter 在返回时追加启动渠道等运行期参数；目标在 Service 层统一提供受控 WebView 链接，工程已有渠道常量或构建配置。
- [鉴权失效判定按源响应拦截器实际分支的错误码与动作迁移，不把错误码枚举里的举例成员当触发条件](lesson-bad79e090d2af44d167b.lesson.md)
  - 时机：规格提取与网络层实现阶段，写 token 失效判定、踢登与刷新策略时
  - 情境：源端由响应拦截器按响应体业务码分支踢登，错误码枚举里同时有多个登录/token 相关成员（如 LoginExpired、TokenExpired、TokenInvalid）；刷新 token 可能在进入主页的初始化请求里调用，不在拦截器里。
