# data/parsing

打包 JSON 等资源的解析：字段必填与空值语义

[上一级](../index.md)

## 本级经验

- [翻译源端 JSON 解析时按源端取值 API 的空值语义定字段规则：org.json 的 getString 对 null 不抛错，只有缺键才抛](lesson-5034b56be6fd828164c9.lesson.md)
  - 时机：实现阶段把源端 JSON 解析函数翻成 ArkTS 手写解析器、决定各字段必填与空值处理时
  - 情境：源端用 Android org.json 的 getString 等读取打包 JSON 资源；对应 Kotlin 数据类字段声明为非空 String；目标解析器任一字段校验失败就让整页进入加载失败。
