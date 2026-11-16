# Retrofit 接口注解声明的路径、方法和请求编码

agent 会看到什么：读到源端 Retrofit 接口上的 @GET / @POST 路径、@FormUrlEncoded 加 @Field / @FieldMap、@Body；产物里请求调用的 url 路径、方法、Content-Type 和请求体格式

## 通用查法

### 写目标端网络请求时，从源端 Retrofit 接口注解读出路径、方法和编码再照写

审的是：代码
触发（任一种）：
- 读到：源工程 Retrofit 接口（ApiService 一类 interface）的方法带 @GET / @POST 路径注解、@FormUrlEncoded、@Field / @FieldMap 或 @Body；写错的样子：目标请求的 url 路径、方法或 Content-Type 和源端 Retrofit 注解对不上：路径按语义拼出、表单接口用了默认的 application/json
适用范围：把 Retrofit 接口调用迁到目标端网络层，定每个请求的路径、方法和请求体编码时
做法：
- 按调用点找到源端 Retrofit 接口里实际选中的方法（同名重载按传 Map 还是对象区分），读出：注解名是方法，注解字符串是路径，@FormUrlEncoded 加 @Field / @FieldMap 是表单，@Body 是 JSON
- 目标端每个源端接口一个方法，路径和方法照抄；表单接口写 Content-Type: application/x-www-form-urlencoded、请求体按 key=value&… 拼，不用默认的 JSON 头
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- header 默认是 'content-type': 'application/json'：直接用 @ohos.net.http 发请求、不写 header 时就是 JSON（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequestOptions.header）
- 'content-Type' 为 'application/x-www-form-urlencoded' 时，请求体是 key 和 value 各自 URL 转码后按 "key1=value1&key2=value2" 拼成的字符串：表单编码的请求体格式（出处：js-apis-http.md，HttpRequestOptions 的 extraData）
针对本应用要查的：
- 每个请求在源端的路径、方法和编码：源工程里 Retrofit 接口文件（带 @GET、@POST、@FormUrlEncoded、@Body 注解的 interface），按调用点用的方法名和参数找到对应的那个声明；注解里的字符串是路径、注解名是方法；方法带 @FormUrlEncoded 且参数是 @FieldMap / @Field 的是表单，参数是 @Body 的是 JSON
- 目标端网络封装里 JSON 和表单两种 POST 的写法：目标工程的网络层类型定义，找按 Content-Type 区分的 POST 方法和请求体构造；表单接口用表单版本的方法和请求体，不和 JSON 版本混用
来源：2 张卡，2 个应用
- case-5c348565d345d0c6b3bc（记得日历）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
- case-7825d414bc05105dc41b（青商城）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

## 规矩

- rule-03111b324a2d｜目标调用的接口路径只取自安卓 Service 注解或已有服务，不按语义拼统一的 save｜读到：安卓 Service 用 Retrofit 注解分接口声明，如 @POST(".../add")、@POST(".../update")、@POST(".../delete")、@GET(".../page")，实体字段含省市区、默认开关等；写错：目标请求调用里的路径字符串（如按语义拼的 ".../save"）在安卓 Service 的 @POST / @GET 注解里找不到，请求体字段比安卓实体少
- rule-fe3477b6dc30｜Retrofit POST 带 @FormUrlEncoded/@FieldMap 时，目标按表单编码发，不发 JSON｜读到：Android 调用通用 post(url, Map) 包装，落到 ApiService 里 @FormUrlEncoded @POST 的 @FieldMap / @Field 重载；写错：目标端这个端点按 JSON 发：Content-Type 是 application/json，参数放在 JSON 请求体里
