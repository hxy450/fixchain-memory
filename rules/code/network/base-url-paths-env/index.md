# 服务地址、接口路径和默认环境

agent 会看到什么：读到 buildConfigField 定义的 BuildConfig.BASE_URL、Retrofit.Builder().baseUrl(...) 和 @GET / @POST 注解、按 BUILD_TYPE 分支的环境工具；产物里的 BASE_URL、接口路径、默认环境常量和 baseUrl 与 path 的拼接

## 通用查法

### 源端服务地址、接口路径或默认环境，从构建脚本、Retrofit 注解和环境工具逐字读出再写常量

审的是：代码
触发（任一种）：
- 读到：源端地址来自 buildConfigField 定义的 BuildConfig.BASE_URL、Retrofit.Builder().baseUrl(...)、Service 上的 @GET / @POST 注解，或按 BuildConfig.BUILD_TYPE 分支的环境工具；写错的样子：目标网络配置里的 BASE_URL、接口路径或默认环境是手写常数：源工程搜不到的域名、脚手架注释里的 'prod'，也没有 TODO 待核标记
适用范围：写目标端网络配置、HTTP 封装和环境常量时
做法：
- 基址去源工程网络模块的 Gradle 构建脚本按 buildConfigField 找（分 buildTypes / productFlavors），没有就读网络装配类里 Retrofit.Builder().baseUrl(...) 的实参或地址常量；默认环境读 getEnv() 指向的环境工具按构建类型的分支
- 接口路径到 Retrofit Service 接口按方法名读 @GET / @POST 注解里的字符串
- 逐字写成一处常量、各处引用它，保留上下文路径和斜杠；查不到就留 TODO 待核标记并在回报里列出，不写推测域名
针对本应用要查的：
- 源端基址：源工程网络模块的 Gradle 构建脚本里 buildConfigField 定义的 BASE_URL（按 buildTypes / productFlavors），或网络装配类里 Retrofit.Builder().baseUrl(...) 的实参、地址常量类和取址方法；按构建变体取实际值，原样写进目标常量，保留末尾的上下文路径和斜杠；新旧两套接口各有取址方法时两个都读，比一比是不是不同 host
- 每个接口的路径：源工程网络模块里的 Retrofit Service 接口，按方法名找 @GET / @POST 注解；注解括号里的字符串原样作路径，记下它带不带前导 /
- 环境枚举和各构建类型下的默认环境：源端桥接里 getEnv() 指向的环境工具类，以及 app 模块 Gradle 构建脚本里的 buildTypes；读出环境工具的全部取值和按构建类型的默认分支（例：某些应用 debug 构建默认测试环境、其余默认正式环境）
未核实：baseUrl 带路径段时，源端带前导 / 的 path 在 Retrofit 下的解析结果，族里规矩没有核实
来源：2 张卡，2 个应用
- case-6be1461999c00a7fe781（青商城）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
- case-b000698af8cbbc664b87（polypal-app-ohos）：做法第 1 步 ← 建议 3；做法第 3 步 ← 建议 2

## 规矩

- rule-c6409b246278｜HTTP 封装的基址和接口路径逐字取自源端 BuildConfig 和 Retrofit 注解，不自拟｜读到：源端网络模块里有 BuildConfig.BASE_URL（或构造 Retrofit 时的 baseUrl(...)），Service 接口方法上有 @POST("…") / @GET("…") 注解；写错：目标封装的 BASE_URL 是源码里搜不到的域名（用应用名拼的占位域名），页面里 post('/…') 的路径和源端注解里的路径不一致
- rule-d169306fb8dd｜规格和清单都没给 host 时，代码回源码查地址常量，查不到留待核标记，不写推测域名｜读到：规格和 API 清单只有 BASE_URL 这类键名、没有 host；派工要求地址从清单或源码提取；写错：网络配置里写出源工程里搜不到的推测域名（https://api.…、dev-api.…、staging-api.…）作为 BASE_URL，没有待核标记，回报里也没列
- rule-81153b1368a8｜规格写新旧接口双轨并存时，先确认是否不同 host，是就让客户端持两个 baseUrl 按规则选｜读到：规格写「双轨制并存（旧接口 + 新接口）」；源端取址分两个方法（旧接口、新接口各一个，按 BuildType 或环境工具选址）；写错：HTTP 客户端只有一个静态 baseUrl 和 init(baseUrl)，注释写「同一套 client 承载，Service 各自声明 path 前缀」
- rule-b2ce4fa5a91d｜Retrofit 改成手工拼 URL 时，拼接函数统一处理 baseUrl 和 path 之间的斜杠｜读到：Retrofit 接口的 @GET / @POST 路径多数不带前导 /（少数带），靠 Retrofit 按 baseUrl 解析相对路径；写错：目标 HttpClient 写成 `${baseUrl}${path}` 直接拼接，而 path 没有前导 /、baseUrl 也没有尾部 /，拼出主机名和路径粘连的 URL
- rule-de2f12ab32b2｜环境默认值照源端环境工具的分支映射到目标构建模式，各处引用同一个常量｜读到：源端 getCurrentEnv 一类桥接返回环境工具的 getEnv()，环境工具按 BuildConfig.BUILD_TYPE 分支给默认值；写错：桥接、偏好封装、网络配置各写一份默认值 `'prod'`，环境词表 dev/staging/prod 取自脚手架 TODO 注释
