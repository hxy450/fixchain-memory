# 三方 SDK 里定义的接口、字段和参数

agent 会看到什么：读到源端只调三方 HTTP SDK 的方法，请求和响应是 SDK 里的 kotlinx.serialization data class（@Serializable、@SerialName），SDK 源码在工程外的 sources jar 或字节码里；规格的端点表、字段表、参数表和枚举上送形态凭方法名、概括或记忆写出，api-inventory 只留 model_class

## 规矩

- rule-2e366bf74ece｜SDK 源码在工程外时，api-inventory 写下载坐标或字段表，子类型读到定义再写字段｜读到：SDK 源码不在工程内，是从工程外临时下载、解包的 sources jar；写错：api-inventory 只保留 model_class，没写 SDK 下载坐标或完整字段表；规格里引用的子类型只写成 Object（如 usage: Object）
- rule-9b379787a3c5｜网络行为在三方 SDK 里时，规格的端点表从 SDK 路由注解机械导出，不凭方法名推断｜读到：安卓应用源码只调用三方 HTTP SDK 的方法、看不到路由；SDK 的 sources jar 或字节码里路由以 @GET / @POST 注解或常量给出；写错：规格的端点表里有凭方法名或记忆推出的路径（和 SDK 路由注解不一致），或上下文压缩、分批续写之后端点表漏了条目
- rule-442cb69a4e0a｜源端用 SDK data class 反序列化响应时，规格按 data class 逐字段写字段表，不概括｜读到：源端通过第三方 SDK 的 kotlinx.serialization data class 直接反序列化服务端 JSON（字段名即 wire key），规格作者已读到 data class 定义；写错：共享响应 Bean 的字段表用「*_report + 当前某某 View + 报告人与被报人」这类文字概括嵌套关系；列了 data class 里没有的字段、漏了字段，或名称相近的两个字段只写一个、只标「—」
- rule-2b409ef91946｜API 规格里每个枚举字段分写线上形态和本地持久化形态，线上按 SDK 序列化取枚举名｜读到：源端经第三方 SDK 的 kotlinx.serialization 数据类调 REST 接口，字段注释列出字符串字面量联合（如 "All" | "Local" | …）；同一枚举另以 .ordinal 存进 Room 列；写错：请求通用约定写「枚举一律以 ordinal/int 上送」，接口页把 query 参数或请求字段标成「枚举 ordinal」/ Int
- rule-ebdf9ad4e370｜SDK 表单校验让两个参数互斥时，规格的参数表写明二选一和各版本发哪个｜读到：SDK 请求数据类型里有表单校验或转换函数（如 toValidatedForm()）：新的游标参数显式给出时丢弃旧的页码参数，旧版本服务端只发页码；注释写某参数只为旧版本保留；写错：规格的请求参数表把两个互斥参数都列为可选，只写「双轨」，没写二选一和按服务端版本发哪个
