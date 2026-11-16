# Kotlin @Serializable 模型迁成的 DTO

agent 会看到什么：读到 Kotlin 的 @Serializable data class（@SerialName、可空字段、enum class 和 Room 存的 .ordinal）、decodeFromString、源端消费点的字段访问路径，或规格对响应结构的文字概括；产物里 DTO 的 interface / class 字段名和嵌套路径、枚举类型、JSON.parse 后的取值和校验，以及按编译提示改掉的字段

## 通用查法

### 手写 DTO 的字段、类型和路径照源端 @Serializable 模型和消费点写，不按规格概括推

审的是：代码
触发（任一种）：
- 读到：源端响应和存储模型是 @Serializable data class（@SerialName、可空 ?、enum class），规格只对结构做文字概括或写 Object；写错的样子：目标 DTO 的字段名、嵌套路径、枚举类型和 JSON.parse 后的校验按规格概括、编译器 Did you mean 提示或 snake_case 习惯写，和源端模型对不上
适用范围：目标端手写 DTO、枚举和 JSON 解析来承接源端序列化模型时
做法：
- 字段名、类型、可空和必填去源端的 @Serializable data class（SDK 里的取 sources jar）读：有 @SerialName 取它，没有 ? 又没默认值的是必填；枚举取成员名作字符串值、声明序作序号表
- 嵌套路径 grep 源端消费点（字段访问、copy(...) 调用），按源端路径声明 DTO；fromJson 按第 1 步逐字段 typeof 检查，可空字段另允许 null
- 源端查不到或和规格冲突的，以源码为准并报回规格，不改用名称相近的字段、不凭推测补名
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ordinal()：枚举常量在声明中的位置，第一个常量为 0：DB 序号表按源端枚举的声明顺序排（出处：java.lang.Enum#ordinal）
针对本应用要查的：
- 每个 DTO 字段的线上名、类型、可空性和是否必填：源工程（或它依赖的 API SDK 的 sources jar）里被解码的 @Serializable data class 和 enum class 声明；逐个读构造参数名（有 @SerialName 时取它）、Kotlin 类型和 ?、默认值；枚举读成员名和声明顺序
- 每个字段的访问路径：源工程里读这个模型的代码，按字段名或 copy( grep；看是平铺访问还是经包装字段访问，DTO 照这个嵌套声明
来源：3 张卡，2 个应用
- case-7eb907f6ed073fe3b558（com.nononsenseapps.feeder）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
- case-95976df1603067128e26（jerboa）：做法第 1 步 ← 建议 3
- case-bb262f5910f2bb20c35d（jerboa）：做法第 2 步 ← 建议 3；做法第 3 步 ← 建议 3

## 规矩

- rule-cda05e39a5af｜规格只文字概括嵌套结构时，写 DTO 前 grep 源端消费点核对访问路径｜读到：规格对响应的嵌套结构只有文字概括；源端消费点是平铺访问（如 view.post.copy(...)、view.community、view.counts）；写错：DTO 照概括写成包装字段（如 post_view / comment_view 嵌套），和源端访问路径不一致
- rule-957aec85288b｜非 SDK REST 的协议响应按协议自身命名，规格只写 Object 时不凭推测补子字段｜读到：规格里协议响应（如 nodeinfo）顶层是 camelCase（openRegistrations），子类型只写 usage: Object；写错：DTO 按「字段名 snake_case 保持」自行拟出 active_half_year / local_posts 这类子字段
- rule-02fa6e9221bc｜基础层用字符串枚举承载线上枚举名，序号只在 DB 读写边界换算｜读到：SDK 数据类字段注释是字符串字面量联合，Room 列存 .ordinal；写错：目标写成数字枚举 enum X { A = 0, B = 1 } 并用于 DTO 字段和请求 query，DTO 枚举字段类型是 number；各 Repository / VM 里有「UI 字符串枚举 ↔ ordinal」的转换桥
- rule-7333d8a4a91d｜直译 decodeFromString 和可空调用时，JSON.parse 结果逐字段校验类型和 null｜读到：kotlinx.serialization 的 runCatching { Json.decodeFromString<T>(text) }.getOrNull() ?: 默认值，@Serializable 类里有非空字段或全为 String / String? 字段；写错：写成 JSON.parse(body) as T 后直接读字段，或读取 helper 只写 value as string；外层 try/catch 只兜住 JSON.parse 的错误，缺字段或类型不符时原样通过、不回落默认值
- rule-723c40a9633d｜页面映射源端字段时 DTO 缺字段，按源端字段名窄化读取，不改用名称相近的字段｜读到：源端读的是某个字段（如 commentView.creator_banned_from_community、copy(creator_banned_from_community = …)），目标 DTO 里没有它，只有名称相近、语义不同的字段；写错：页面写成 creator_banned_from_community: cv.banned_from_community 或 copy.banned_from_community = …，把语义不同的字段当成源端字段；或 DTO 的嵌套路径和源端访问路径不一致时照 DTO 路径读
- rule-38c252ec7f9d｜编译报「属性不存在，是否指 X」时，先核源模型语义，字段属于源模型就补 DTO 声明｜读到：编译错误 `does not exist on type` 并提示 `Did you mean`，被提示的字段名字相近但在源模型里语义不同；写错：按提示把赋值改成名字相近的字段（如作者字段换成当前用户字段），源模型有的字段没补进 DTO 的 class 声明
