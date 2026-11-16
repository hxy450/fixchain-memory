# 网络

源端有 Retrofit 接口注解、OkHttp / OkGo 请求和拦截器、BaseResponse 响应壳、BuildConfig 里的服务地址，目标端有 @ohos.net.http 的封装、请求 url 和 header、响应解包时

## 触发族

- [Retrofit 接口注解声明的路径、方法和请求编码](retrofit-endpoints/index.md)（3 条）：读到源端 Retrofit 接口上的 @GET / @POST 路径、@FormUrlEncoded 加 @Field / @FieldMap、@Body；产物里请求调用的 url 路径、方法、Content-Type 和请求体格式
- [响应壳 BaseResponse 和 Bean 的字段](response-bean/index.md)（3 条）：读到源端 Retrofit 回调里的 BaseResponse<T>、解包后的容器 Bean 和 data class 字段声明，交回的代码手写了 res.data 的取值键链或 BaseResponse 等响应类型
- [Retrofit Response<> 带的响应头](response-header/index.md)（2 条）：读到源端 Retrofit 接口返回 Response<BaseResponse<T>>、Repository 从 headers()["Authorization"] 取 token，交回的 HTTP 封装或解析函数只返回、只读 body
- [OkGo 请求通道和会话密钥握手门](okgo-handshake-gate/index.md)（2 条）：读过的源码里 OkGo.post(url).headers(headers).execute() 一类的请求重载有的没有取会话密钥的前置步骤、由调用方按特定基址先握手；交回的目标通道照别的通道自加了握手门，或门取的是会被切服改写的默认 baseUrl
- [服务地址、接口路径和默认环境](base-url-paths-env/index.md)（6 条）：读到 buildConfigField 定义的 BuildConfig.BASE_URL、Retrofit.Builder().baseUrl(...) 和 @GET / @POST 注解、按 BUILD_TYPE 分支的环境工具；产物里的 BASE_URL、接口路径、默认环境常量和 baseUrl 与 path 的拼接
- [网络配置的注入和初始化时机](network-config-init/index.md)（5 条）：读到 buildConfigField / BuildConfig 里的地址和签名材料、Hilt @Provides 里带上的 Retrofit baseUrl、决策要求私有注入；产物里 HttpClient 的 baseUrl 空串默认、init() 的调用点、BuildProfile 读取和装配根的配置构造
- [网络回调里信封成功和 data 层错误码的判别](envelope-errorcode/index.md)（2 条）：读到源端网络回调先按信封 isSuccess 分流、再在 data 层用 optInt("errorCode") / optBoolean / has("…") 判别；产物里回调用服务层解析出的 report.success / report.errorCode 分支
- [源端 OkHttp 拦截器和统一响应壳](okhttp-interceptor/index.md)（5 条）：读到源端 OkHttp 的 Interceptor 里 addHeader 加公共头（Authorization 等）、按错误码分支踢登，或统一响应包装类（code、message、data），产物里是 @ohos.net.http 封装的默认 header、响应解包和 token 失效判定
- [预签名上传的诊断日志包](presign-log-upload/index.md)（2 条）：读过的源码里上传函数先取 presign 地址再 PUT，打包日志目录、设备信息和 ObjectBox 分表 TXT，清单有 android:usesCleartextTraffic；交回的代码里网络层对上传地址的 https 校验和归档里装了什么
- [配置地址拼接运行期参数的链接](config-url-concat/index.md)（1 条）：读到配置读取类的 getter 返回 url + 渠道 getter() 一类拼接、assets JSON 配置里的地址 query 以 = 结尾；产物里 Service 把配置地址写成 const / static readonly URL 常量，取链接的方法直接返回它
- [OkHttp 缓存迁成 rcp ResponseCache](okhttp-response-cache/index.md)（3 条）：读到 OkHttp 的 Cache(dir, 容量)、CacheControl.Builder 的 maxAge / maxStale 或缓存拦截器；产物里 rcp.ResponseCache 的 CacheConfiguration.maxSize、Cache-Control 头里的指令，以及 cache.set 外面的 catch
- [request.agent 的下载任务](request-agent-download/index.md)（1 条）：读到源端用 OkHttp 或 getInputStream 把文件下到缓存目录，或参考模板按 request.agent.create → on('completed') → start() 落码；产物里有没有调 task.start()，完成和失败回调怎么接
- [源端 catch 里的 HTTP 失败和目标的失败信封](http-failure-envelope/index.md)（2 条）：读到源端请求包在 try/catch 或错误回调里，catch 中 error instanceof HttpErrorResponse 时设错误并 return false、成功路径才改 hasMore / 游标；产物里目标客户端永不 reject、返回失败信封，调用方有没有 res.status !== 200 分支，单测有没有注入失败信封
- [HTTP 非 2xx 响应的状态码和原因短语](http-status-reason/index.md)（3 条）：读到源端按 isSuccessful、response.code / getResponseCode 判 2xx，非 2xx 分支用 OkHttp 的 response.message（原因短语）构造 HttpError(code, message)；产物里 requestInStream 返回的响应码有没有判 2xx、错误文案用没用 rcp Response.reasonPhrase、错误类的 message 和 description 怎么取
- [rcp 拦截器和 401 刷新链里的取值与日志](rcp-interceptor-log/index.md)（2 条）：读到 rcp.createSession 的 SessionConfiguration 带 baseAddress、请求用 new rcp.Request('相对路径', …) 构造，或源端拦截器里包在 !environment.production 下的 console.info(request.url)；产物里 Interceptor.intercept 和 401→refresh→retry 链里无保护地读 context.request.url、在 hilog 参数里调可能抛错的 getter 或 toString()
