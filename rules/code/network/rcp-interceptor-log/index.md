# rcp 拦截器和 401 刷新链里的取值与日志

agent 会看到什么：读到 rcp.createSession 的 SessionConfiguration 带 baseAddress、请求用 new rcp.Request('相对路径', …) 构造，或源端拦截器里包在 !environment.production 下的 console.info(request.url)；产物里 Interceptor.intercept 和 401→refresh→retry 链里无保护地读 context.request.url、在 hilog 参数里调可能抛错的 getter 或 toString()

## 规矩

- rule-81e61f6a9447｜rcp 用 baseAddress+相对路径建请求时，拦截器里不直接读 context.request.url｜读到：rcp.createSession 的 SessionConfiguration 写了 baseAddress，请求用 new rcp.Request('相对路径', …) 构造；写错：Interceptor.intercept 或其中的刷新/重试分支里无保护地读 context.request.url（如 hilog(…, context.request.url.toString())）
- rule-dee50f24fd01｜源端仅调试用的日志迁进 401 刷新链时，取值放在不会抛错的旁路｜读到：源端拦截器里的日志包在 `!environment.production` 判断下，如 console.info(request.url)；写错：目标端 401→refresh→retry 主链里无保护地计算日志参数（hilog 的参数里调用可能抛错的 getter 或 toString()）
