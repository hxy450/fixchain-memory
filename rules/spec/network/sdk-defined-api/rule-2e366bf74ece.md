# SDK 源码在工程外时，api-inventory 写下载坐标或字段表，子类型读到定义再写字段

审的是：规格
触发（任一种）：
- 读到：SDK 源码不在工程内，是从工程外临时下载、解包的 sources jar；写错的样子：api-inventory 只保留 model_class，没写 SDK 下载坐标或完整字段表；规格里引用的子类型只写成 Object（如 usage: Object）
适用范围：API 清单和规格提取阶段，把响应结构交给 DTO 实现者时
做法：
- 把 SDK 的下载坐标（group:artifact:version 和 sources jar）或完整字段表写进 api-inventory，交给 DTO 实现者
- 规格引用的子类型先读到定义再写字段，不写成 Object
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 下游在工程和 Gradle 缓存里都找不到 SDK 源码，只能以规格为准写 DTO：api-inventory 不带坐标时下游无从核对（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-bb262f5910f2bb20c35d（jerboa）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、建议 5；取值 1 ← 诊断
