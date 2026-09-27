# data/model

模型类型之间的映射：持久化枚举字符串与页面本地类型，大整数 id（源端 Long 或 String 承接）的保精度解析，跨模型数值字段的单位

[上一级](../index.md)

## 本级经验

- [把以字符串持久化的模型枚举映射到页面本地类型时，按模型枚举成员逐一 switch，不用成员名字符串变换去匹配](lesson-b92a8a56aee6db5e9c52.lesson.md)
  - 时机：实现阶段把共享模型枚举（持久化为字符串）映射成页面本地枚举或资源时
  - 情境：模型枚举的持久化值是带下划线的大写串（如 FRENCH_PRESS），页面本地枚举用驼峰成员名。
- [服务器下发的大整数 id 在 JSON.parse 之前保住原文：源端 Long 用 bigint，源端 String 承接的数值 id 保真为字符串](lesson-c066489fcf35ab37378c.lesson.md)
  - 时机：数据模型与网络层实现阶段，映射 Kotlin Long 字段或以 String 承接的数值标识、编写全局响应解析入口与序列化时；规格提取阶段写服务层签名与接口字段类型时
  - 情境：服务器生成的 id、hash、userId 以 JSON 数字下发，取值可达 19 位；源端用 Kotlin Long（Flutter 侧 Dart int）承载，或用 String 字段承接（Gson 把数值 token 直接读成字符串）；目标端 ArkTS 的 number 是双精度，JSON.parse 遇到超过 2^53 的整数直接舍入。
- [逐字段搬运 Builder 或构造调用时，同时核对两端模型字段的单位](lesson-c73deaf6f27d3426c4e9.lesson.md)
  - 时机：功能实现阶段，把源端模型 Builder 或构造调用逐字段翻译成目标端模型构造参数时
  - 情境：目标端两个模型对同名数值字段声明了不同单位（如本地音频时长为毫秒、播放队列时长为秒），源端在同一处直接传值；目标消费方按各自单位显示或换算。
