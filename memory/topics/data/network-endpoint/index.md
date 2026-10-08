# data/network-endpoint

服务地址、环境与构建期运行配置的来源与注入，baseUrl 与 path 的拼接，以及网络权限声明

[上一级](../index.md)

## 本级经验

- [拼接函数统一处理 baseUrl 与 path 之间的斜杠](lesson-d767b84213eb5ef93034.lesson.md) · 阶段：execute · 信号：${baseUrl}${path}, baseUrl, @GET, @POST
- [服务地址沿键名追到源端常量，host 与环境不自拟](lesson-246252824c631aa6eff5.lesson.md) · 阶段：spec/execute · 信号：BuildConfig.BASE_URL, SpKey.BASE_URL, NetworkModule, baseUrl
- [构建期注入的地址与密钥从私有配置接入，空配置拒发包](lesson-30ccd1d65d2c39029256.lesson.md) · 阶段：execute · 信号：buildProfileFields, process.getEnvironmentVar, BuildConfig, parameterFile
- [网络权限声明进 module.json5，任务要有写者](lesson-faec7be031b7f64752c4.lesson.md) · 阶段：plan/execute/converge · 信号：module.json5, requestPermissions, ohos.permission.INTERNET, ohos.permission.GET_NETWORK_INFO
