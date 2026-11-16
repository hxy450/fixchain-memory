# 构造时显式传 null 的引用字段

agent 会看到什么：读到 Java 构造器或委托调用 this(…, null, …) 给 String 等引用字段显式传 null、另有路径传真实值；产物里 ArkTS 模型把这个字段写成非空 string = ''，工厂方法传 ''

## 规矩

- rule-c4de2102e2c8｜Java 构造路径显式传 null 的引用字段，目标模型保留 T | null，不用 '' 兼表｜读到：Java 构造器或委托调用 `this(…, null, …)` 对某个 String 字段显式传 `null`，另有路径传真实值；写错：ArkTS 模型把字段写成非空 `string = ''`，工厂方法传 `''`，null 与空串从此混同
