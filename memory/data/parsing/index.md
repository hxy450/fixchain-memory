# data/parsing

JSON 与 XML 解析：打包资源的字段必填与空值语义，源解析器（如 Gson）的标量宽松转换与源数据实际类型，接口响应容器 Bean 的取值层级，自写 fromJson 的运行期类型收窄，以及 @ohos.xml 拉取解析的回调顺序与命名空间作用域，org.json 构造的宽松语法与取值类型校验；org.json 与 Gson 写侧（put(null) 删键、“/”转义；Gson 键序、省略 null 与 HTML 转义）与读侧取值强转

[上一级](../index.md)

## 本级经验

- [备份/导出 JSON 按 org.json 或 Gson 库语义序列化（null 删键或省略、“/”与 HTML 转义），不用 JSON.stringify](lesson-0caaa4efc70dad90a15f.lesson.md)
  - 时机：规格提取与数据层实现阶段，把源端用 JSONObject.put、JSONArray.toString(n) 或 Gson.toJson 生成的备份、导出或请求 JSON 写成目标契约与序列化代码时
  - 情境：源端 serialize() 对可空值直接 put（如 put(key, steps?.serialize())、put(key, time)），再以 JSONObject/JSONArray 的 toString() 或 toString(indent) 写文件；对应 Kotlin 字段声明为可空；目标准备用 DTO 加 JSON.stringify(obj, null, n) 输出，规格可能写“null 字段输出 JSON null（键保留）”。也包括源端以 Gson 反射序列化实体（new Gson().toJson(obj)，未调 serializeNulls/disableHtmlEscaping），目标手写 toJson 或照抄标注为推断的示例 JSON。
- [显式 JSON 解码器按源解析器的接受范围和源数据的实际类型定规则：Gson 的数字与字符串互转要保留](lesson-871d3751cadde6dda1dc.lesson.md)
  - 时机：数据层与网络层实现阶段，把 Retrofit+Gson 的 Bean、响应壳或预置 JSON 资产的读取翻译成 ArkTS 显式解码器时
  - 情境：源端由 Gson 把 JSON 填进 Int/String 字段，或预置资产用字符串存放数值（"id": "43831"）；目标仓库提供只接受单一 typeof 的严格解码函数（string()/number() 类型不符即抛错），真实响应样例尚未采集，规格只写了“Gson → 显式 decoder、显式校验字段”。
  - 例外：源端对该字段确实以类型不符为错误（例如源码显式校验并走失败分支），此时保留严格校验
- [源端访问解包后对象的字段时，先确定目标 res.data 对应哪一层类型，再逐层写取值键](lesson-dc5c370e370c2be803c1.lesson.md)
  - 时机：数据层服务实现阶段，把源端 Retrofit/Gson 响应 Bean 的字段访问路径翻译成目标端对原始 JSON 的逐键取值时；页面回调依赖服务层解析产出的 success、errorCode 等字段，准备给出“逐行一致”的复核结论时
  - 情境：源端 success 回调已把 BaseResponse&lt;T&gt; 解包成 T，业务代码写 result.data?.xxx；T 本身是含 data 字段的容器 Bean（如 {total, data:{…}}）；目标网络层把响应 data 原样返回，服务层用 getObject/getArray 按键手动取值。
- [用 @ohos.xml 重建 SAX 开始事件时采用与回调顺序无关的组装，并自建命名空间作用域](lesson-447985a4376146f6d9f2.lesson.md)
  - 时机：实现阶段，用 XmlPullParser 的 token 与属性分离回调重建 namespace-aware 开始事件（本元素属性与命名空间 URI）时
  - 情境：源 SAX/XmlPullParser 在开始标签读取本元素属性并按 uri 加前缀分发命名空间；目标用 tokenValueCallbackFunction 与 attributeWithTagCallbackFunction 两路回调，SDK 声明未写两路回调先后，也未保证 getNamespace() 给出元素 URI。
- [翻译源端 JSON 解析时按源解析器与取值 API 的语义定规则：org.json 的 getString 对 JSON null 返回 "null"、缺键才抛，JSONObject 构造接受的语法比 JSON.parse 宽](lesson-5034b56be6fd828164c9.lesson.md)
  - 时机：实现阶段把源端 JSON 解析函数翻成 ArkTS 手写解析器、决定各字段必填与空值处理时；把 org.json 读取导入文件的逻辑映射为 JSON.parse 并写失败验收时
  - 情境：源端用 Android org.json 的 getString 等读取打包 JSON 资源；对应 Kotlin 数据类字段声明为非空 String；目标解析器任一字段校验失败就让整页进入加载失败。也包括源端用 new JSONObject(text) 与 getJSONObject、getString 读取导入文件，规格把它写成“JSON.parse 加显式 class、纯语言构造”，失败条目只列非法 JSON、缺键与空集合。也包括源端 toRecipe、fromJson 一类函数用 getString/getInt/getJSONArray 读备份或许可数据，数据中有 "description": null 一类值；目标准备用 as string 直取、把 null 或缺键的数组读成空数组，或写成“非字符串即抛”的取值函数。
- [自写 fromJson 从宽类型输入取值时用 typeof/instanceof 收窄：as 只是编译期断言，?? 只兜底缺失与 null](lesson-2622bc32995ac62389c3.lesson.md)
  - 时机：数据模型实现阶段，为迁移实体编写 fromJson 反序列化方法、确定字段取值与默认值时
  - 情境：ArkTS 模型的 fromJson 接收 Record&lt;string, Object&gt; 等宽类型输入，字段声明为 number/string/boolean 并带默认值；源端是强类型 data class（Int/Long/Boolean 字段），没有可照搬的序列化代码，由目标自行补写。
  - 例外：源端经 Gson 等解析器填充并容忍数字与字符串互转时，按源解析器的接受范围转换（见本主题 Gson 标量宽松转换的经验），不一律回落默认值
