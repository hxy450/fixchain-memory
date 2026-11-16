# 源接口有 Response<> 包裹的端点时，HTTP 封装把响应头随结果返回，不只返回 body

审的是：代码
触发（任一种）：
- 读到：Retrofit 接口返回 Response<BaseResponse<T>>，调用方读 headers()；写错的样子：HTTP 封装只 JSON.parse(response.result) 返回 body，response.header 被丢弃；统一响应类里没有承载响应头的字段
适用范围：用 @ohos.net.http 实现统一 HTTP 封装、源端有端点需要读响应头时
做法：
- 统一响应类加一个响应头字段（如 header: Object），封装层把 HttpResponse.header 随解析后的 body 一起返回给调用方
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- HttpResponse.header: Object：服务器返回的全部响应头（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，http.HttpResponse.header）
- HttpResponse.result: string | Object | ArrayBuffer：响应体；JSON.parse 的是它，不含响应头（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，http.HttpResponse.result）
- 常见字段按 header['content-type']、header['date'] 这样取：取响应头字段的写法（出处：js-apis-http.md，HttpResponse）
未核实：文档说 header 当前返回的是 JSON 格式字符串，声明里类型是 Object，实际形态未核；响应头键名在目标端是否保留原大小写未核（文档示例都是小写键名）；卡里环境是 API 22，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-31852e28af4327a408a3（polypal-app-ohos）：做法第 1 步 ← 建议 2、诊断
