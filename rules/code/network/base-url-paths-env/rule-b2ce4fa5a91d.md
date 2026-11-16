# Retrofit 改成手工拼 URL 时，拼接函数统一处理 baseUrl 和 path 之间的斜杠

审的是：代码
触发（任一种）：
- 读到：Retrofit 接口的 @GET / @POST 路径多数不带前导 /（少数带），靠 Retrofit 按 baseUrl 解析相对路径；写错的样子：目标 HttpClient 写成 `${baseUrl}${path}` 直接拼接，而 path 没有前导 /、baseUrl 也没有尾部 /，拼出主机名和路径粘连的 URL
- 读到：参考模板的拼接是 `${HttpUtil.baseUrl}${url}`，示例 baseUrl 无尾斜杠、Service 路径带前导 /；写错的样子：照搬了模板的直接拼接，path 却按 Retrofit 注解改写成不带前导 / 的形式
适用范围：网络层把 Retrofit 接口迁成基于 @kit.NetworkKit http 的手工拼接 URL 时
做法：
- 在 HttpClient 的拼接函数里统一处理分隔符：path 以 http:// 或 https:// 开头时直接用；否则去掉 baseUrl 尾部 / 和 path 前导 / 后用单个 / 连接，不依赖各 Service 的 path 写法
- 照搬模板的拼接方式时同时沿用模板示例里 path 的形式；按源 Retrofit 注解改写了 path（去掉或保留前导 /）的，回头检查拼接函数是否仍成立
- 输出前用本次的 baseUrl 常量和一个真实 endpoint 拼出完整 URL 自检，确认主机与路径之间恰有一个 /
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 拼接函数改为：path 以 http 开头直接用，否则缺 / 时补一个、两侧都有时不重复，之后请求正常：修好的写法（出处：卡里修好并验证过）
- request(url: string, options?: HttpRequestOptions): Promise<HttpResponse>：url 是完整 URL，拼错时直接发到错误主机（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request）
- 错误码 2300006 - Failed to resolve the host name.：主机名和路径粘连时请求报这个错（对应 CURLcode 6）（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request）
针对本应用要查的：
- baseUrl 是否带尾部 /，各 path 是否带前导 /：源工程 Retrofit.Builder().baseUrl(...) 的参数和各 Service 接口的 @GET / @POST 注解；目标工程的网络配置常量和各 Service 的 path；两边都列出来，按拼接函数实际拼一遍，看主机与路径之间是不是恰好一个 /
未核实：卡里环境是 HarmonyOS 6.0.2(22)，声明按本机 API 23 核实；baseUrl 带路径段时，源端带前导 / 的 path 在 Retrofit 下的解析结果与「补单个 /」是否一致，卡里没核
来源：1 张卡，1 个应用
- case-fef2528dd5d4c3b040e6（polypal-app-ohos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 3；取值 1 ← 诊断
