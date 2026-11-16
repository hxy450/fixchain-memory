# 写 HttpClient 默认头前对照源拦截器的 addHeader，Authorization 格式以源码为准

审的是：代码
触发（任一种）：
- 读到：源端 OkHttp 拦截器里 addHeader("Authorization", token) 等多个公共头；参考模板写的是 `Authorization = Bearer ${token}`；写错的样子：目标 @ohos.net.http 的 HttpClient 默认 header 只有 Content-Type 和平台头，缺源端的其他公共头；Authorization 写成 `Bearer ${token}`，注释却称对应源端拦截器
适用范围：用 @ohos.net.http 自建 HttpClient 替代源端 OkHttp 拦截器链、写默认请求头时
做法：
- 打开源拦截器逐条对照 addHeader，把每个头写进 HttpRequestOptions.header 的默认对象；Authorization 等头的格式照源码（源端直接放 token 就写 header['Authorization'] = token），模板里的 Bearer 只当结构参考
- 取源拦截器 addHeader 键集合与目标默认 header 键集合的差集，非空就补齐，或在规格里写明原因
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- header?: Object，默认 'content-type': 'application/json'：HttpRequestOptions 里的请求头对象（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequestOptions.header）
- request(url: string, options?: HttpRequestOptions): Promise<HttpResponse>：HttpRequest 发请求，公共头经 options.header 传入（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request）
- 补齐源端全部公共头、Authorization 改为直接传 token 后服务端解析正常：修好后的默认头（出处：卡里修好并验证过）
- requestInStream(url: string, options?: HttpRequestOptions): Promise<number>：同族接口：流式请求，同样经 options.header 带公共头（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.requestInStream）
针对本应用要查的：
- 源端公共头的键集合和各自格式：源工程里实现 okhttp3.Interceptor 的类的 intercept 方法，按 addHeader / header 调用找；列出键名和值的拼接方式，与目标默认 header 对象的键逐个比对
来源：1 张卡，1 个应用
- case-69bfbfee5841bf8c60cf（polypal-app-ohos）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 3 ← 诊断
