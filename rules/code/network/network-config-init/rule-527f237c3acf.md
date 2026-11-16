# 静态 HttpClient 的 baseUrl 为空时先报「网络层未初始化」，不把相对路径交给 http.request

审的是：代码
触发（任一种）：
- 写错的样子：静态 HttpClient 的 baseUrl 默认空串，请求时直接拼 baseUrl + path 交给 httpRequest.request()，没有判空
适用范围：目标端网络层用静态字段保存 baseUrl、靠初始化入口赋值时
做法：
- 在发请求的入口先判 baseUrl：为空就抛出或记录「网络层未初始化」的明确错误，不再调 httpRequest.request(url, options)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- request(url: string, options?: HttpRequestOptions): Promise<HttpResponse>：HttpRequest 发请求的接口，url 是完整地址（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request）
- 2300001 Unsupported protocol；2300003 Invalid URL format or missing URL：地址缺协议或缺 host 时可能收到的错误码，被统一包装后就看不出是没初始化（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request 的 @throws）
- requestInStream(url: string, options?: HttpRequestOptions): Promise<number>：同族接口：流式请求，同样要完整 url（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.requestInStream）
未核实：相对路径进 http.request 时实际收到的是哪个错误码，卡里只看到统一包装后的 NETWORK
来源：1 张卡，1 个应用
- case-8555b02fdd531952938b（polypal-app-ohos）：做法第 1 步 ← 建议 2
