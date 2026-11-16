# 源端用 SDK data class 反序列化响应时，规格按 data class 逐字段写字段表，不概括

审的是：规格
触发（任一种）：
- 读到：源端通过第三方 SDK 的 kotlinx.serialization data class 直接反序列化服务端 JSON（字段名即 wire key），规格作者已读到 data class 定义；写错的样子：共享响应 Bean 的字段表用「*_report + 当前某某 View + 报告人与被报人」这类文字概括嵌套关系；列了 data class 里没有的字段、漏了字段，或名称相近的两个字段只写一个、只标「—」
适用范围：API 清单和规格提取阶段整理共享响应 Bean 字段表时
做法：
- 按 SDK data class 逐字段写：wire key、类型、平铺还是嵌套、可空性、默认值；只列源码里真实存在的字段
- 名称相近、语义不同的字段分别列出并写明语义（如「作者被本社区封禁」和「当前用户被封禁」）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 修复按 SDK 的 javap 字段表改写 DTO：补齐漏掉的字段、举报类视图改为平铺字段、删除源码里不存在的字段：字段表照 data class 写才和线格式一致（出处：卡里修好并验证过）
针对本应用要查的：
- 响应 Bean 的完整字段：SDK 的 sources jar（或 aar / jar 里的 class）中对应的 @Serializable data class；逐个读构造参数：名字（有 @SerialName 时取它）、类型、是否可空、默认值；嵌套类型递归读到底
来源：1 张卡，1 个应用
- case-bb262f5910f2bb20c35d（jerboa）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 1 ← 诊断
