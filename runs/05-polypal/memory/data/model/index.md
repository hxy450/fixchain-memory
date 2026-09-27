# data/model

模型类型之间的映射：持久化枚举字符串与页面本地类型，源端 Long 等 64 位整数到 ArkTS 类型及其保精度解析

[上一级](../index.md)

## 本级经验

- [把以字符串持久化的模型枚举映射到页面本地类型时，按模型枚举成员逐一 switch，不用成员名字符串变换去匹配](lesson-b92a8a56aee6db5e9c52.lesson.md)
  - 时机：实现阶段把共享模型枚举（持久化为字符串）映射成页面本地枚举或资源时
  - 情境：模型枚举的持久化值是带下划线的大写串（如 FRENCH_PRESS），页面本地枚举用驼峰成员名。
- [源端 Long 承载的服务器 id 在 ArkTS 里用 bigint，响应解析、请求序列化与持久化往返都保住 64 位精度](lesson-c066489fcf35ab37378c.lesson.md)
  - 时机：数据模型与网络层实现阶段，把 Kotlin Long 字段和接口参数映射成 ArkTS 类型、决定 JSON 解析与序列化方式时；规格提取阶段写服务层 ArkTS 目标签名时
  - 情境：源端 bean 或接口用 Kotlin Long（Flutter 侧 Dart int）承载服务器生成的用户 id、hash、userId，后端按 JSON 数字返回，取值可达 19 位；目标端 ArkTS 的 number 是双精度，JSON.parse 遇到超过 2^53 的整数直接舍入。
