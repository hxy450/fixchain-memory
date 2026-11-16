# Gson 模型里的 Long 字段和 JSON 数值的解析

agent 会看到什么：读到源端 bean 里 Long / long 的 id、hash、userId，Gson 把 JSON 数值读进 String 字段，@SerializedName、TypeAdapter；产物里模型字段写 number、HTTP 层裸 JSON.parse / JSON.stringify、正则加引号配 reviver 转 BigInt、decoder 里 typeof 不符就 throw

## 规矩

- rule-4e112342395c｜源端 Long 的服务器 id、hash、userId 字段，ArkTS 模型写 bigint，不写 number｜读到：源端 bean 或接口里有 val id: Long、Long?、Java 的 long userId、@Query("userId") userId: Long；写错：目标模型写成 id: number = 0、userId: number、number | null，fromJson 里 (json['id'] as number)，服务方法参数 (userId: number)
- rule-5f661bac942b｜响应里有 64 位整数字段时不用裸 JSON.parse，换保精度解析，请求体配 bigint 的 replacer｜读到：响应模型里有 Long 字段（val id: Long、userId: Long）；写错：HTTP 层统一写 JSON.parse(body) as BaseResponse<T>，请求体 JSON.stringify(data)，没有 bigint 处理
- rule-022b8601b3f4｜用正则加引号和 reviver 转 BigInt 时，范围限定到已知的 64 位字段名｜写错：预处理用 `\d{16,}` 一类正则把响应里所有 16 位以上整数加引号，reviver 把所有 16 位以上的纯数字字符串都 BigInt(…) 成 bigint
- rule-f40d675f476f｜源端以 String 承接 JSON 数值 id 时，全局解析在 JSON.parse 之前保留数字原文｜读到：Android 模型用 Gson 把服务端的 JSON 数值读进 String 字段（id、*_id 一类标识），线上响应或探针里这些字段是数值 token；写错：全局响应解析入口直接 JSON.parse(text)，之后再用 `${value}` / String(value) 把数值转成字符串
- rule-20815b8b8e00｜Gson Bean 改写成显式 decoder 时，string/number 读取保留 Gson 的标量宽松转换｜读到：Android Bean 由 Gson 反序列化（@SerializedName、TypeAdapter），字段声明为 String / Int（如 var id = ""、var x = 0）；写错：decoder 的 string 读取写成 `typeof v !== 'string'` 就 throw DecodeError，number 读取写成 `typeof v !== 'number'` 就抛错
