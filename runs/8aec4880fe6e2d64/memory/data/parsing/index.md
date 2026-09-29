# data/parsing

JSON 解析：打包资源的字段必填与空值语义，源解析器（如 Gson）的标量宽松转换与源数据实际类型，接口响应容器 Bean 的取值层级

[上一级](../index.md)

## 本级经验

- [显式 JSON 解码器按源解析器的接受范围和源数据的实际类型定规则：Gson 的数字与字符串互转要保留](lesson-871d3751cadde6dda1dc.lesson.md)
  - 时机：数据层与网络层实现阶段，把 Retrofit+Gson 的 Bean、响应壳或预置 JSON 资产的读取翻译成 ArkTS 显式解码器时
  - 情境：源端由 Gson 把 JSON 填进 Int/String 字段，或预置资产用字符串存放数值（"id": "43831"）；目标仓库提供只接受单一 typeof 的严格解码函数（string()/number() 类型不符即抛错），真实响应样例尚未采集，规格只写了“Gson → 显式 decoder、显式校验字段”。
  - 例外：源端对该字段确实以类型不符为错误（例如源码显式校验并走失败分支），此时保留严格校验
- [源端访问解包后对象的字段时，先确定目标 res.data 对应哪一层类型，再逐层写取值键](lesson-dc5c370e370c2be803c1.lesson.md)
  - 时机：数据层服务实现阶段，把源端 Retrofit/Gson 响应 Bean 的字段访问路径翻译成目标端对原始 JSON 的逐键取值时
  - 情境：源端 success 回调已把 BaseResponse&lt;T&gt; 解包成 T，业务代码写 result.data?.xxx；T 本身是含 data 字段的容器 Bean（如 {total, data:{…}}）；目标网络层把响应 data 原样返回，服务层用 getObject/getArray 按键手动取值。
- [翻译源端 JSON 解析时按源端取值 API 的空值语义定字段规则：org.json 的 getString 对 null 不抛错，只有缺键才抛](lesson-5034b56be6fd828164c9.lesson.md)
  - 时机：实现阶段把源端 JSON 解析函数翻成 ArkTS 手写解析器、决定各字段必填与空值处理时
  - 情境：源端用 Android org.json 的 getString 等读取打包 JSON 资源；对应 Kotlin 数据类字段声明为非空 String；目标解析器任一字段校验失败就让整页进入加载失败。
