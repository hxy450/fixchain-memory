# data/network-auth

鉴权凭证、会话密钥与拦截器公共参数的获取来源、注入格式、失效判定及其写入侧生产者

[上一级](../index.md)

## 本级经验

- [token 失效判定按响应拦截器实际分支的码迁移](lesson-bad79e090d2af44d167b.lesson.md) · 阶段：spec/execute · 信号：reasonCode, HandleErrorInterceptor, TokenInterceptor, LoginExpired
- [响应头携带 token 时 HTTP 封装连头一起返回](lesson-2a4e6af209308c08aaa6.lesson.md) · 阶段：spec/execute · 信号：headers()\["Authorization"\], RefreshToken, Response&lt;BaseResponse, TokenManager
- [拦截器注入的请求头逐条迁到默认头，格式以源码为准](lesson-217e93ef9097efc519f1.lesson.md) · 阶段：execute · 信号：addHeader, TokenInterceptor, Authorization, Bearer
- [拦截器读取的本地公参键都要有写入者，只迁读取不算完](lesson-7e04234bdf5aef97b651.lesson.md) · 阶段：execute · 信号：Interceptor, OAID, preferences, deviceId
- [请求通道按源端重载决定取 key 门，握手基址随请求](lesson-62499aa25e87fa6ab5e1.lesson.md) · 阶段：execute/repair · 信号：ensureKey, OkGo, baseUrl, sessionKey
