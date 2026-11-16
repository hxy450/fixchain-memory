# OkHttp 拦截器里的请求头和鉴权失效

agent 会看到什么：读到 OkHttp Interceptor.intercept 里 addHeader 注入鉴权、语言、平台头，响应拦截器按错误码分支踢登，刷新 token 的接口在别处调用；规格的网络层写「统一 token 注入」「401/某码 刷新」「自动刷新」，没有逐项的请求头和「码→动作」表

## 规矩

- rule-051acc1596c5｜源端拦截器统一注入请求头时，规格逐项写出每个头的名称、取值来源和格式｜读到：OkHttp 拦截器（Interceptor.intercept 里 Request.Builder.addHeader）给每个请求加鉴权、语言、平台、地区等头，接口声明上看不到；raw_apis 里该拦截器标了 header_write / token_injection；写错：规格网络层只写「统一 token 注入」「统一平台头」，没有逐项列出公共请求头，也没写 Authorization 是直接放 token 还是带 Bearer 前缀
- rule-76c0accae4fe｜规格写鉴权失效判定时，按源端响应拦截器的分支写「码→动作」表，不拿错误码枚举举例｜读到：源端 OkHttp 响应拦截器按响应体错误码分支踢登，错误码枚举里同时有多个登录过期、token 为空、过期、无效、异地登录类成员；写错：规格里写「401/某码 刷新」或「对应错误码枚举（某码 登录过期…）」当作失效条件，没有「码→动作」表、没写出自哪个拦截器
- rule-3767c478193d｜规格写 token 刷新策略前先找源端刷新接口的调用方，不凭推断写「自动刷新」｜读到：源端响应拦截器里没有刷新 token 的调用，刷新接口在别的页面或初始化方法里调用；写错：规格写「401/某码 刷新」或「自动刷新」，没写源端刷新接口的调用方和发起时机
- rule-4eeacf538996｜源端从响应头取登录凭证时，规格的鉴权模型写明凭证来源、头名和写入点｜读到：Retrofit 接口返回 Response<BaseResponse<T>>，调用方在成功回调里用 headers()["Authorization"] 等读响应头写 token、refreshToken；写错：网络层或登录功能规格的鉴权一节只写「统一 token 注入 + 401 刷新」，API 表写「返回 用户 DTO + token」，没写凭证来自响应头、头名和写入点
