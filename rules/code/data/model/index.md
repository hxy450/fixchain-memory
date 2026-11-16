# 数据模型与解析

源端有 Kotlin data class / Java bean、Gson 的 @SerializedName、org.json 的 JSONObject、enum、SAX / XmlPullParser，目标端有模型 class、JSON.parse 后的取值、@ohos.xml 解析时

## 触发族

- [Gson 模型里的 Long 字段和 JSON 数值的解析](gson-number-fields/index.md)（5 条）：读到源端 bean 里 Long / long 的 id、hash、userId，Gson 把 JSON 数值读进 String 字段，@SerializedName、TypeAdapter；产物里模型字段写 number、HTTP 层裸 JSON.parse / JSON.stringify、正则加引号配 reviver 转 BigInt、decoder 里 typeof 不符就 throw
- [从 Kotlin data class 迁来的模型类和 JSON 解码](model-class-json-decode/index.md)（5 条）：读到 Kotlin data class 模型（Int / Long / Boolean / String 字段）、kapt stub、assets 下的 JSON 样本；产物里模型 class 的字段、fromJson 的取值写法和它的注释
- [org.json 的读取和序列化语义](org-json/index.md)（4 条）：源码用 org.json 的 JSONObject.getString / getJSONObject / put、JSONArray.toString 读写 JSON；产物里 JSON.parse 后的 as 强转、typeof 守卫和 JSON.stringify 导出
- [逐条解析和导入时单条记录出错的处理](per-record-errors/index.md)（2 条）：源端在循环里逐条 getJSONObject、解析、insert，或列表解析里单条记录的字段取不到；产物里先全量校验再写库、单条失败就 throw 让整页失败
- [移植的模型类和它的构造器](ported-model-class/index.md)（3 条）：读到被移植类的源构造器和相邻类的构造器、或计划写明 models/ 按职责拆文件；交回的目标类构造器初值和源类自身不一样，或同一类型在两个文件里都有 export class
- [@ohos.xml 的 XmlPullParser 解析回调](ohos-xml-pull-parser/index.md)（2 条）：读到源端 SAX 的 ContentHandler.startElement(uri, localName, qName, Attributes) 或 XmlPullParser 在 START_TAG 读属性、按命名空间分发，产物里是 @ohos.xml 的 tokenValueCallbackFunction、attributeWithTagCallbackFunction 循环和 ParseInfo.getNamespace() 的用法
- [共享模型的枚举成员和持久化值](enum-persisted-value/index.md)（1 条）：读到共享模型的 enum 成员名是驼峰、持久化值是 'A_B' 这种带下划线的大写串，页面另有自己的本地 enum；产物里映射函数拿成员名字符串和持久化值比较，或写成 name.toUpperCase() === value
- [Kotlin @Serializable 模型迁成的 DTO](kotlin-serializable-dto/index.md)（7 条）：读到 Kotlin 的 @Serializable data class（@SerialName、可空字段、enum class 和 Room 存的 .ordinal）、decodeFromString、源端消费点的字段访问路径，或规格对响应结构的文字概括；产物里 DTO 的 interface / class 字段名和嵌套路径、枚举类型、JSON.parse 后的取值和校验，以及按编译提示改掉的字段
- [copy() 建的顶层哨兵对象](copy-sentinel/index.md)（1 条）：读到 Kotlin 顶层 val 哨兵 = 原对象.copy()，别处用 === 和它比较判断是不是哨兵；产物里导出的是每次调用都 new 一个实例的函数
- [Moshi 等解析器解析失败时的结果和错误类型](parse-failure-result/index.md)（2 条）：读到源端用 Moshi 严格反序列化（缺字段、类型不符抛 JsonDataException），或用一次 Either.catching(onCatch = …) 包住 XML、JSON 全部格式的解析；产物里 fromJson 给缺字段填默认值、坏响应当空结果，或 catch 里按格式分出不同的错误 kind
- [构造时显式传 null 的引用字段](explicit-null-field/index.md)（1 条）：读到 Java 构造器或委托调用 this(…, null, …) 给 String 等引用字段显式传 null、另有路径传真实值；产物里 ArkTS 模型把这个字段写成非空 string = ''，工厂方法传 ''
- [源端枚举字段在目标模型里的类型](enum-field-type/index.md)（1 条）：读到源端设置或模型字段存成 Int 列、按 toEnum<枚举>() / ordinal 转成多值枚举使用；产物里目标模型字段写成 @Trace …: number，注释写「(0|1)」「Int 0/1」
- [Jsoup 节点遍历改写成的自研解析器](jsoup-traversal-parser/index.md)（2 条）：读到 Jsoup 的 Element / TextNode 遍历（wholeText 计数、pre / table 分支、pushId(element.id())、按元素 ids 建锚点下标）；产物里自研解析器的 appendText / pushElement 计数和上限检查的位置、线性元素有没有 ids 字段
- [模型类的 equals 和脏检查方法](model-equals-dirty-check/index.md)（1 条）：读到源端用 equals(...)、hashCode 或另一个「有没有改过」的比较方法决定是否写库、是否刷新修改时间；产物里只比较标题、正文等可见字段的脏检查函数或 equals
- [Gson 反射序列化写出的 JSON](gson-tojson-output/index.md)（1 条）：读到源端备份或互通 JSON 走 new Gson().toJson(obj) / GsonBuilder 反射序列化，参考里的 JSON 示例标着 [推断]；产物里手写 toJson 的键序、Boolean 写法、null 键是否写出，或 JSON.stringify 加全局 replace 凑 htmlSafe 转义
- [Java 实体的数值字段和落库绑定](java-entity-numeric-field/index.md)（1 条）：读到 Java 实体的 getter 返回 Double 这类包装数值、另有 setX(String) 重载，数据层 values.put(KEY, …) 以数值绑定 REAL 列；产物里模型字段写成 string | null，ValuesBucket 直接绑字符串字段、空串以 '' 落库
