# 源端按异常类型分类网络失败时，规格的错误码表写出 BusinessError.code 判据

审的是：规格
触发（任一种）：
- 读到：源端 catch 链按 IllegalArgumentException / SocketTimeoutException / UnknownHostException / IOException（含证书消息）分支，详情用 e.getMessage()；写错的样子：规格的错误码表只以 Java 异常类名和 Java 消息字面量（如 'Trust anchor for certification path not found'）为判据；实现映射表里没有「Java 异常类型 → BusinessError.code」一行
适用范围：规格里写网络失败分类的错误码表和实现映射表，目标端请求走 @ohos.net.http 时
做法：
- 错误码表除源端异常类外写目标判据：@ohos.net.http 失败是 BusinessError，按 code 映射——2300003 URL 格式错误、2300006 无法解析主机、2300028 超时、2300060 / 2300077 证书校验
- 实现映射表加一行「Java 异常类型 → BusinessError.code」，依据写 SDK 声明的 @throws 条款；源端英文消息字面量只列作兜底
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 2300003 - Invalid URL format or missing URL.：URL 格式错误，对源端 IllegalArgumentException（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request 的 @throws）
- 2300006 - Failed to resolve the host name.：无法解析主机，对源端 UnknownHostException（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request 的 @throws）
- 2300028 - Operation timeout.：超时，对源端 SocketTimeoutException（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request 的 @throws）
- 2300060 - Invalid SSL peer certificate or SSH remote key.；2300077 - The SSL CA certificate does not exist or is inaccessible.：证书校验失败，对源端带 Trust anchor… 消息的 IOException（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request 的 @throws）
- 2300003 → MALFORMED_URL，2300006 → UNKNOWN_HOST，2300028 → CONNECTION_ERROR，2300060 / 2300077 → CERTIFICATE；消息匹配降为兜底：修复后分类正确、超时复测得到 'Operation timeout' 的映射（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-bae545fb004bef3f5772（AntennaPod）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 5 ← 诊断
