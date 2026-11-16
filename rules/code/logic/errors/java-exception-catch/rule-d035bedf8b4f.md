# 网络错误分类先比 BusinessError.code，不复用 Java 异常的英文消息做关键词

审的是：代码
触发（任一种）：
- 读到：源端按 SocketTimeoutException / UnknownHostException / IllegalArgumentException / IOException 分类，证书失败靠消息 'Trust anchor for certification path not found' 判断；写错的样子：目标端按消息匹配 'timeout'、'Unknown host'、'Failed to parse url'、'malformed'、'Trust anchor…' 等 Java/英文关键词分类，没有先比 code
适用范围：目标端用 @ohos.net.http 发请求、要把失败分成源端那几类错误时
做法：
- 先比 (e as BusinessError).code：2300003 → URL 格式错误类，2300006 → 未知主机类，2300028 → 连接/超时类，2300060、2300077 → 证书类
- 确需按消息匹配时只作兜底，关键词用目标平台的实际消息（如 'Operation timeout'），不用 Java 异常消息
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 2300003 - Invalid URL format or missing URL.；2300006 - Failed to resolve the host name.：URL 格式错误、无法解析主机（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request 的 @throws）
- 2300028 - Operation timeout.：超时；消息原文也就是兜底匹配时该用的关键词（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request 的 @throws）
- 2300060 - Invalid SSL peer certificate or SSH remote key.；2300077 - The SSL CA certificate does not exist or is inaccessible.：证书校验失败（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request 的 @throws）
- request(url: string, options?: HttpRequestOptions): Promise<HttpResponse>：带这组 @throws 的请求接口（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request）
- requestInStream(url: string, options?: HttpRequestOptions): Promise<number>：同族接口：流式请求，带同一组错误码（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.requestInStream）
- 分类函数先按 2300003 / 2300006 / 2300028 / 2300060 / 2300077 映射，消息匹配降为兜底；超时复测得到消息 'Operation timeout'、归到连接错误类：修复后的分类写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-bae545fb004bef3f5772（AntennaPod）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 6 ← 诊断
