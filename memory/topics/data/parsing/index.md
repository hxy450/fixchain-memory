# data/parsing

JSON 与二进制字节流到类型化模型的编解码规则：类型宽窄收窄、空值语义、取值层级与大整数精度

[上一级](../index.md)

## 本级经验

- [@ohos.xml 开始事件按顺序无关组装并建命名空间栈](lesson-447985a4376146f6d9f2.lesson.md) · 阶段：execute · 信号：@ohos.xml, XmlPullParser, tokenValueCallbackFunction, attributeWithTagCallbackFunction
- [JSON 取值的空值与类型规则按 org.json 定](lesson-5034b56be6fd828164c9.lesson.md) · 阶段：spec/execute · 信号：org.json, getString, optString, getInt
- [byte\[\] 常量逐下标转写核总长，冲突以源为准](lesson-0bba9db6a18f2e732334.lesson.md) · 阶段：spec/execute · 信号：byte\[\], Uint8Array, KeyA, KeyB
- [fromJson 宽类型取值用 typeof 收窄再赋值](lesson-2622bc32995ac62389c3.lesson.md) · 阶段：execute · 信号：fromJson, typeof, instanceof, Record&lt;string, Object&gt;
- [org.json 输出按库语义：null 删键、转义 /](lesson-0caaa4efc70dad90a15f.lesson.md) · 阶段：spec/execute · 信号：JSONObject.put, JSONObject.NULL, JSONArray, toString(indent)
- [proto3 手写编解码按 wire type 成对实现读写](lesson-ae1aa4ff5e2217b67e06.lesson.md) · 阶段：execute · 信号：wire type, varint, int32, sfixed32
- [先定目标 res.data 对应源端哪层类型，再逐层写取值键](lesson-dc5c370e370c2be803c1.lesson.md) · 阶段：execute/verify · 信号：res.data, BaseResponse&lt;T&gt;, getObject, getArray
- [命名常量替换字面区间时按每处用途选端点](lesson-1d0b6dde849cbd70ee8f.lesson.md) · 阶段：execute · 信号：substring(12,20), substring(12,18), GPB
- [大整数 id 用 bigint，解析前给数字加引号保真](lesson-c066489fcf35ab37378c.lesson.md) · 阶段：spec/execute · 信号：JSON.parse, bigint, Long, 2^53
- [显式解码器保留 Gson 数字与字符串互转的宽松规则](lesson-871d3751cadde6dda1dc.lesson.md) · 阶段：execute · 信号：Gson, string(), number(), typeof
