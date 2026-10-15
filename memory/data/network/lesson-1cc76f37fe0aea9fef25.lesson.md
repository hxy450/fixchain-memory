# 迁移 Retrofit POST 时按源方法注解定请求体编码：@FormUrlEncoded 发表单，@Body 看 Converter

ID：`lesson-1cc76f37fe0aea9fef25` · 版本：3

[本主题](index.md)

## 何时使用

接口层实现、模块抽取或把调用搬到平台适配层时，为每个 POST 端点确定请求体编码与 Content-Type；发现同类编码偏差后确定修复范围时

## 适用情境

源端经 Retrofit ApiService 发请求，调用点可能先经项目自己的 post(url, Map) 一类包装，最终选中的方法带 @FormUrlEncoded + @FieldMap/@Field、@Multipart + @Part 或 @Body；目标 HTTP 层默认以 application/json 发送，另有表单写法；规格或 API 清单只列参数名、不写 Content-Type，目标里可能已有沿用下来的 JSON 端点。

## 原因

@FormUrlEncoded 请求以 application/x-www-form-urlencoded 的 key=value 体发出，服务端按表单字段读参数；同一字段以 JSON 发送时服务端读不到（表现为缺参数、查询无结果），编译和调用都不报错。@Body 参数经 Converter.convert 转成 RequestBody，参数本身是 okhttp3.RequestBody 时原样透传，所以 @Body 的编码由 Retrofit.Builder 注册的 Converter.Factory（Gson、Moshi 为 JSON）或所传 RequestBody 的 MediaType 决定，不能一律当 JSON。规格常只列参数名，沿用既有端点会把偏差原样带入。

## 做法

1. 为每个 POST 端点追到源端调用点实际选中的 ApiService 方法（经过项目包装函数时逐层追到带注解的重载），按注解定编码：@FormUrlEncoded + @Field/@FieldMap 发 key=value 表单体；@Multipart + @Part 发 multipart/form-data；@Body 按 Retrofit.Builder 的 addConverterFactory 或所传 RequestBody 的 MediaType 定 Content-Type。
2. 用目标 HTTP 层对应的表单或 multipart 写法发送（例：目标封装提供 formPost/formBody 时用它，不用默认 JSON post）；在端点目录与 API 清单里为每个端点记录 Content-Type，不只列参数名。
3. 搬迁或复用既有端点与 JSON 调用时，把它们当作未核验的现状，按第 1 步核对编码，不一致就在交接里列为待修。
4. 发现一处表单被迁成 JSON 后，检索全仓默认 JSON post 调用及对应源端调用点，覆盖所有适配器和端点目录，不只修当前模块。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5c348565d345d0c6b3bc](../../../store/cases/case-5c348565d345d0c6b3bc/f987b996a3cdc55b5cf4f8197fb8e77bd00d6c812d4f1a1df24a68fa7f451476.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`f987b996a3cdc55b5cf4f8197fb8e77bd00d6c812d4f1a1df24a68fa7f451476`
