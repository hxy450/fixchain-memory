# 网络接口与同步

读到 Retrofit Service、OkHttp 拦截器、Gson 和 Bean 模型、按异常类型分的网络失败、响应解密钩子，或待推送队列和同步任务，规格里写 API 表、请求头、错误码表、响应契约、测试环境和同步顺序时

## 触发族

- [Service 接口的参数类型和请求体](service-params-body/index.md)（3 条）：读到 Retrofit Service 方法参数是 Long 的 userId / id，或是在调用方组装的 @Body RequestBody，端点在别的模块；规格的 ArkTS 目标签名写 number，API 表漏了跨模块端点或没写请求体字段
- [同步队列的选取条件和失败项](sync-queue/index.md)（2 条）：读到待推送队列的查询只按资源类型 equal(…) 选取、不按同步状态过滤，失败只置 fail 不删除；规格或源码审计写「永久置 FAIL、没有自动恢复」
- [OkHttp 拦截器里的请求头和鉴权失效](okhttp-interceptor-auth/index.md)（4 条）：读到 OkHttp Interceptor.intercept 里 addHeader 注入鉴权、语言、平台头，响应拦截器按错误码分支踢登，刷新 token 的接口在别处调用；规格的网络层写「统一 token 注入」「401/某码 刷新」「自动刷新」，没有逐项的请求头和「码→动作」表
- [接口字段表里 id 的线上类型和数值量级](api-field-token-types/index.md)（1 条）：读到 Android 模型把 id、*_id 声明为 String，golden 响应或探针里同一字段是 JSON 数值；接口字段表只记声明类型，响应契约没写大整数按字符串保真
- [「未提供测试 base_url / 测试账号」的适用范围](missing-test-env-scope/index.md)（1 条）：读到决策台账写「未提供测试 base_url / 测试账号」并限定了作用域、另有「密钥构建期私有注入」；契约文档把它写成「配置缺失时网络返回明确失败」，当成装配空配置的依据
- [按异常类型分类的网络失败](network-error-types/index.md)（1 条）：源端 catch 链按 SocketTimeoutException / UnknownHostException / IOException 等异常类型和 e.getMessage() 分支；规格错误码表里的判据
- [解密失败时回退原文的响应钩子](decrypt-fallback/index.md)（1 条）：源端 beforeResponse 一类响应钩子调用解密函数、catch 里原样返回 content，接口清单里「是否全接口返回密文」仍是 open；规格网络层和决策台账写的解密失败语义
- [源端同步序列的步骤](sync-sequence-steps/index.md)（2 条）：源端同步在保存、排序之后还有写全局状态的步骤（保存当前选中项、更新全局当前 id）；源码笔记或审计总结里列出的同步顺序
- [同步任务的并发调度](sync-concurrency/index.md)（1 条）：源端每次同步触发都 scope.launch 新任务、在 Mutex.withLock 里排队先推后拉；规格里「并发触发复用当前任务」「单飞」这类调度说法
- [Gson 反序列化改写成显式 decoder 的契约](gson-lenient-decoder/index.md)（1 条）：读到源端用 Gson 反序列化 BaseResponse<T> 和各 Bean，真实响应样例还没采集（golden 标 needs_capture）；规格只写「Gson BaseResponse<T> → 显式 JSON decoder」「decoder 必须显式校验字段」，没写数字↔字符串、布尔转字符串这类要保留的宽松转换
- [三方 SDK 里定义的接口、字段和参数](sdk-defined-api/index.md)（5 条）：读到源端只调三方 HTTP SDK 的方法，请求和响应是 SDK 里的 kotlinx.serialization data class（@Serializable、@SerialName），SDK 源码在工程外的 sources jar 或字节码里；规格的端点表、字段表、参数表和枚举上送形态凭方法名、概括或记忆写出，api-inventory 只留 model_class
- [三方 SDK 自建的 HTTP 客户端（超时、重试、异常映射）](sdk-http-client/index.md)（2 条）：读到三方 SDK 自己创建 HttpClient、装了 HttpTimeout、HttpRequestRetry、设了 expectSuccess，或在 exception 包和响应校验里按状态码、响应体转成 SDK 自定义异常，应用包装层只给 OkHttp 配了超时；规格的客户端契约只写应用包装层的超时，异常契约只写「4xx/5xx + body {error}」
- [SDK 按服务端版本分的路由表](server-version-routing/index.md)（1 条）：读到 SDK 的版本路由代码：宽松 semver 解析服务端版本、按 minor 分到各版本路由表、不支持的 minor 抛异常，另有 MIN_SUPPORTED_VERSION 一类常量；规格把整个 minor 写成单个补丁号、写「未知版本落最新分支」、省略解析规则，或把端点下限一律写成最新大版本
