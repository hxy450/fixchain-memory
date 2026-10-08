# data/network-request

POST 请求体的字段来源与表单/JSON 编码选择，以及请求参数与响应加解密的移植与空值、失败回退

[上一级](../index.md)

## 本级经验

- [@FieldMap 用表单编码，@Body 才用 JSON](lesson-1cc76f37fe0aea9fef25.lesson.md) · 阶段：execute/repair · 信号：@FieldMap, @FormUrlEncoded, @Field, @Body
- [Service 收不透明 body 时追到源端构造处照抄字段](lesson-0bc494e864b2d8ab1a34.lesson.md) · 阶段：spec/execute · 信号：@Body, RequestBody, data: Object, device_id
- [cryptoFramework 规格串只写算法位数，结果判空](lesson-3684e08592c85de82204.lesson.md) · 阶段：execute/converge · 信号：cryptoFramework, createAsyKeyGenerator, convertPemKeySync, doFinalSync
- [移植加解密工具保留空串直返与解密失败回退原文](lesson-4232e195ff42fc63ba43.lesson.md) · 阶段：execute · 信号：AESUtil, aesEncrypt, aesDecrypt, isEmpty
