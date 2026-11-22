# SDK 序列化的枚举分开写线上形态与本地持久化形态：kotlinx.serialization 默认按枚举名上送，DB 列的 ordinal 只在读写边界换算

## 何时使用

API 规格提取阶段确定枚举参数与字段的线上序列化形态时；基础层建枚举类型、数据层组装请求时

## 适用情境

Android 经第三方 SDK（kotlinx.serialization 数据类）调用 REST 接口，SortType、ListingType 一类枚举既作为 GET query 与 JSON 请求字段，又以 ordinal 整数存入本地 Room 列；目标手写 DTO、枚举与请求组装。

## 原因

Room 列里的 ordinal 只是本地持久化形态，SDK 序列化器按枚举名（或 @SerialName）上送；把 ordinal 当成接口契约，请求就以数字发送枚举，服务端拒绝（如 HTTP 400）而列表空白。数字类型在各层一致，编译与结构检查都不报错，只访问不带枚举参数接口的探针也发现不了。

## 做法

1. 规格对每个枚举字段分列「线上形态」与「本地持久化形态」：线上以 SDK 数据类与序列化器为准（默认按枚举名，@SerialName 覆盖），在请求通用约定里给出示例（如 ?type_=Local&sort=Active）；不从 Room 列的 ordinal 或 toEnum() 推断。
2. 确需 ordinal 的 DB 列另列 SDK 枚举声明序，不用 App 内 when 表的顺序代替。
3. 基础层用字符串枚举承载线上名，序号只在 DB 读写边界换算；规格与已有代码或实测响应冲突时登记决策缺口，并用一次带枚举参数的真实请求核实，不静默照规格。
4. 冒烟或活性探针至少覆盖一个带枚举 query 参数的 GET。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕java.lang.Enum 的 ordinal 是枚举常量在声明中的位置，第一个常量为 0
- 〔做法第 1 步〕java.lang.Enum 的 name 是枚举常量声明时用的标识符
