# 源端 OkHttp 拦截器和统一响应壳

agent 会看到什么：读到源端 OkHttp 的 Interceptor 里 addHeader 加公共头（Authorization 等）、按错误码分支踢登，或统一响应包装类（code、message、data），产物里是 @ohos.net.http 封装的默认 header、响应解包和 token 失效判定

## 通用查法

### 源端有 okhttp3.Interceptor 时，从拦截器读出公共头、成功码和踢登码，目标逐项显式写

审的是：代码
触发（任一种）：
- 读到：源端 OkHttp 的 Interceptor 里 addHeader("Authorization", …) 等公共头，或按 code / 错误码分支处理响应（含统一响应壳）；写错的样子：目标 @ohos.net.http 封装的 header 只有 Content-Type 或照模板写 `Bearer ${token}`，响应直接 JSON.parse(result) as T 返回，或只按 `=== 401` 判失效
适用范围：目标端用 @ohos.net.http 自写 HTTP 封装、替代源端 OkHttp 拦截器链时
做法：
- 打开源工程里实现 okhttp3.Interceptor 的类的 intercept 方法：请求侧按 addHeader / header 列出每个头的键和值的拼法，响应侧读出成功码、响应壳字段名和每个错误码分支的动作
- 目标逐项照写：HttpRequestOptions.header 的默认对象补齐每个头（格式照源码，如直接放 token），先判 responseCode 在 2xx 再按源成功码解包，失效判定逐个命中拦截器里的码
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- header?: Object，默认 'content-type': 'application/json'：HttpRequestOptions 里的请求头对象，公共头写在这里（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequestOptions.header）
- request(url: string, options?: HttpRequestOptions): Promise<HttpResponse>：HttpRequest 发请求，公共头经 options.header 传入（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request）
- responseCode: ResponseCode | number；result: string | Object | ArrayBuffer：HTTP 状态码和响应体，先判状态码再解包（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpResponse.responseCode、HttpResponse.result）
- 例：源拦截器直接放 token 时，补齐源端全部公共头、Authorization 改为直接传 token 后服务端解析正常：带条件的例子（出处：卡里修好并验证过）
针对本应用要查的：
- 公共头的键集合和各自格式：源工程里实现 okhttp3.Interceptor 的类的 intercept 方法，按 addHeader / header 调用找；列出键名和值的拼接方式（是否带前缀），与目标默认 header 对象的键逐个比对
- 成功码、响应壳字段和踢登码：源工程网络模块里的响应包装类、响应拦截器和它引用的错误码枚举；读出成功码的值、code / message / data 的字段名、每个分支的码值和动作，原样用在目标解包和失效判定里
来源：3 张卡，2 个应用
- case-69bfbfee5841bf8c60cf（polypal-app-ohos）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3；取值 4 ← 诊断
- case-6be1461999c00a7fe781（青商城）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
- case-7478183bbcfea10865d1（polypal-app-ohos）：做法第 1 步 ← 建议 3；做法第 2 步 ← 诊断

## 规矩

- rule-ab61ab9515c5｜写 HttpClient 默认头前对照源拦截器的 addHeader，Authorization 格式以源码为准｜读到：源端 OkHttp 拦截器里 addHeader("Authorization", token) 等多个公共头；参考模板写的是 `Authorization = Bearer ${token}`；写错：目标 @ohos.net.http 的 HttpClient 默认 header 只有 Content-Type 和平台头，缺源端的其他公共头；Authorization 写成 `Bearer ${token}`，注释却称对应源端拦截器
- rule-b2304e5c5117｜源端有统一响应壳和鉴权拦截器时，目标封装带 Authorization 头并按成功码解包｜读到：源端有统一响应包装类（code、message、data 字段）按成功码判定，OkHttp Interceptor 给请求加 Authorization 头；写错：目标封装直接 JSON.parse(result) as T 返回，没有按成功码解包，header 里没有 Authorization，也没判 responseCode 是否 2xx
- rule-b7e6e68fd113｜实现 token 失效判定时，码值照源端拦截器分支写全，不照规格举例只判一个码｜读到：规格写的失效码在它指定的数据源里查不到，源端有处理错误码的 okhttp3.Interceptor；写错：目标端自写的 HTTP 客户端只按 HTTP 401（`=== 401`）或单个业务码判失效踢登，源端拦截器里其余踢登码落到普通业务错误分支
- rule-8fd0a673b4b3｜规格写鉴权头「统一注入」时，代码有 token 就给所有请求带 Bearer，不按端点表注入｜读到：规格或端点契约写「SDK 层统一注入」「defaultRequest 拦截，auth != null 时 headers[Authorization]=Bearer」；写错：代码按端点表的 auth 列决定带不带 Authorization: Bearer，查不到端点（未登记路径）或 auth=none 时不带
