# Retrofit POST 带 @FormUrlEncoded/@FieldMap 时，目标按表单编码发，不发 JSON

审的是：代码
触发（任一种）：
- 读到：Android 调用通用 post(url, Map) 包装，落到 ApiService 里 @FormUrlEncoded @POST 的 @FieldMap / @Field 重载；写错的样子：目标端这个端点按 JSON 发：Content-Type 是 application/json，参数放在 JSON 请求体里
- 读到：目标端已有的端点目录或仓库层把这个 POST 写成 JSON，调用被搬到新的平台适配层或网关；写错的样子：搬迁后的调用照旧用 JSON 请求体，没有对照 Android 的 @FieldMap 重载核对编码
适用范围：把 Retrofit 接口的 POST 调用迁到目标端网络层、或搬迁已迁好的 POST 调用时
做法：
- 按 Android 调用实际选中的 Retrofit 重载定编码：@FieldMap / @Field 用表单（Content-Type: application/x-www-form-urlencoded，请求体是 URL 转码后的 key=value&…），只有 @Body 才用 JSON；目标端网络封装分 JSON 和表单两种 POST 时选表单那种
- 搬迁既有 POST 调用时，沿用的端点和 JSON 请求体只当未核验的现状，找到对应 Android 调用点和 ApiService 重载核对一次再搬
- 发现一处 @FieldMap 被迁成 JSON 后，扫全仓所有 JSON POST 调用和端点目录，逐个对照 Android post(url, Map) 调用点改正，并为每个端点补一条请求编码的契约测试
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- header 默认是 'content-type': 'application/json'：直接用 @ohos.net.http 发请求、不写 header 时就是 JSON（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequestOptions.header）
- 'content-Type' 为 'application/x-www-form-urlencoded' 时，请求体是 key 和 value 各自 URL 转码后按 "key1=value1&key2=value2" 拼成的字符串：表单编码的请求体格式（出处：js-apis-http.md，HttpRequestOptions 的 extraData）
- 端点改成表单 POST、请求体改成表单 { keyword } 后，抓包里请求带上了关键词：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 每个 POST 调用实际选中的 Retrofit 重载：源工程里 Retrofit 接口（ApiService 一类）的方法声明，以及调用点传的是 Map 还是请求体对象；方法带 @FormUrlEncoded 且参数是 @FieldMap / @Field 的是表单；参数是 @Body 的是 JSON（或按转换器序列化）
- 目标端网络封装里表单 POST 的写法：目标工程的网络层类型定义，找按 Content-Type 区分的 POST 端点和请求体构造；表单版本的端点和请求体一起用，不和 JSON 版本混用
来源：1 张卡，1 个应用
- case-5c348565d345d0c6b3bc（记得日历）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 3；取值 3 ← 诊断
