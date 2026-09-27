# data/parsing

JSON 解析：打包资源的字段必填与空值语义，接口响应容器 Bean 的取值层级

[上一级](../index.md)

## 本级经验

- [源端访问解包后对象的字段时，先确定目标 res.data 对应哪一层类型，再逐层写取值键](lesson-dc5c370e370c2be803c1.lesson.md)
  - 时机：数据层服务实现阶段，把源端 Retrofit/Gson 响应 Bean 的字段访问路径翻译成目标端对原始 JSON 的逐键取值时
  - 情境：源端 success 回调已把 BaseResponse&lt;T&gt; 解包成 T，业务代码写 result.data?.xxx；T 本身是含 data 字段的容器 Bean（如 {total, data:{…}}）；目标网络层把响应 data 原样返回，服务层用 getObject/getArray 按键手动取值。
- [翻译源端 JSON 解析时按源端取值 API 的空值语义定字段规则：org.json 的 getString 对 null 不抛错，只有缺键才抛](lesson-5034b56be6fd828164c9.lesson.md)
  - 时机：实现阶段把源端 JSON 解析函数翻成 ArkTS 手写解析器、决定各字段必填与空值处理时
  - 情境：源端用 Android org.json 的 getString 等读取打包 JSON 资源；对应 Kotlin 数据类字段声明为非空 String；目标解析器任一字段校验失败就让整页进入加载失败。
