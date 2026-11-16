# Java 实体的数值字段和落库绑定

agent 会看到什么：读到 Java 实体的 getter 返回 Double 这类包装数值、另有 setX(String) 重载，数据层 values.put(KEY, …) 以数值绑定 REAL 列；产物里模型字段写成 string | null，ValuesBucket 直接绑字符串字段、空串以 '' 落库

## 规矩

- rule-e3b689c30e56｜源端 Double 字段在模型和落库绑定上保持数值语义，空串或不可解析绑 NULL｜读到：Java 实体的 getter 返回 `Double`，另有 `setX(String)` 重载；写错：ArkTS 模型把字段写成 `string | null`，只有数值读取的访问器，没有 String 入口「解析失败 → null」的语义
