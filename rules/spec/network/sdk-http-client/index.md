# 三方 SDK 自建的 HTTP 客户端（超时、重试、异常映射）

agent 会看到什么：读到三方 SDK 自己创建 HttpClient、装了 HttpTimeout、HttpRequestRetry、设了 expectSuccess，或在 exception 包和响应校验里按状态码、响应体转成 SDK 自定义异常，应用包装层只给 OkHttp 配了超时；规格的客户端契约只写应用包装层的超时，异常契约只写「4xx/5xx + body {error}」

## 规矩

- rule-1e9a39e22913｜SDK 装了 HttpTimeout 等插件时，规格写 SDK 的超时重试，不用应用 OkHttp 配置｜读到：应用的 Http 包装层只给 OkHttp 配了超时，再通过 SDK 的默认客户端配置把引擎交给 SDK；SDK 自己创建 HttpClient 时装了 HttpTimeout、HttpRequestRetry，设了 expectSuccess；写错：规格的客户端契约只写应用包装层的超时（如「预配 OkHttp：30s 超时」），没有 SDK 自身的请求 / socket / 连接三类超时、重试次数和触发条件、expectSuccess
- rule-b29151e3cdbd｜SDK 有自定义异常映射时，规格写明哪类响应转哪种异常、message 取什么值｜读到：SDK 的 exception 包和响应校验里按状态码和响应体把响应转成 SDK 自定义异常；应用按异常类型或 message 处理错误；写错：规格的异常契约只写「4xx/5xx + body {error}」「某异常（4xx，带 body 文本）」，没写转换的条件、其余响应转什么、message 取什么值
