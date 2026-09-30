# 按源端 Retrofit 实际选中的重载确定请求体编码：post(url, Map)/@FieldMap 用表单，只有 @Body 用 JSON

ID：`lesson-1cc76f37fe0aea9fef25` · 版本：1

[本主题](index.md)

## 何时使用

接口层实现、模块抽取或把调用搬到平台适配层时，为每个 POST 端点确定请求体编码；发现同类编码偏差后确定修复范围时

## 适用情境

Android 通过 Retrofit 通用 post(url, Map) 包装或 @FormUrlEncoded + @FieldMap/@Field 发送参数；目标端点目录的默认 post 是 application/json，另有 formPost/formBody 一类表单写法；目标里已有端点定义或 jsonBody 调用可以直接沿用；规格或 API 清单只列参数名、不写 Content-Type。

## 例外与边界

- 服务端契约已确认同一端点也接受 JSON（接口文档或抓包证明），且当前决策选择 JSON

## 原因

@FormUrlEncoded 请求以 key=value 表单发出，服务端按表单字段读参数；同一字段以 JSON 发送时服务端读不到（表现为缺少关键词、查询无结果），编译和调用都不报错。规格或清单常只列参数名，沿用既有 JSON 端点会把偏差原样带入。来源中模块抽取者按现状搬迁 JSON 搜索请求，读到 formPost/formBody 与默认 post 并存却没有对照源端调用；更早一次审计已确认源端通用 post(url, Map) 为表单编码并建议全量改用表单，但修复只改了当时审计的一个适配器文件。

## 做法

1. 为每个 POST 端点找到源端调用点与它选中的 ApiService 重载：@FormUrlEncoded/@FieldMap/@Field 用 formPost + formBody；@Body 才用 JSON。在端点目录与 API 清单里为端点记录 Content-Type，不只列参数名。
2. 搬迁或复用既有端点与 jsonBody 调用时，把它们当作未核验的现状，按上一条核对编码，不一致就在交接里列为待修。
3. 发现一处表单被迁成 JSON 后，按模式检索全仓 jsonBody/默认 post 调用及对应源端 post(url, Map) 调用点，覆盖所有适配器和端点目录，不只修当前模块。

## 来源（按需复核）

- [case-5c348565d345d0c6b3bc](../../../store/cases/case-5c348565d345d0c6b3bc/f987b996a3cdc55b5cf4f8197fb8e77bd00d6c812d4f1a1df24a68fa7f451476.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`f987b996a3cdc55b5cf4f8197fb8e77bd00d6c812d4f1a1df24a68fa7f451476`
