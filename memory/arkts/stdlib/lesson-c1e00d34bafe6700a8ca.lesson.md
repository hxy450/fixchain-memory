# Kotlin 严格解析（toIntOrNull、ZonedDateTime.parse、类型化解码）不改写成 parseInt、Date.parse 或 as

ID：`lesson-c1e00d34bafe6700a8ca` · 版本：2

[本主题](index.md)

## 何时使用

数据层与服务层实现阶段，把外部字符串或 JSON 转成数值、时间或类型化对象的 Kotlin 解析调用改写为 ArkTS 时

## 适用情境

源码用 toIntOrNull/toLongOrNull、ZonedDateTime.parse、Json.decodeFromString 等严格解析，失败时回落默认值、null 或保留旧值；目标侧可选 parseInt、Number、Date.parse 与 as 类型断言，它们接受的输入更宽或不做运行时检查。

## 原因

只照抄了失败时的回落分支，接受范围却被放宽：parseInt 只解析前缀（'15abc' 得 15），Date.parse 接受 '2024-01-02' 这类纯日期，as 不在运行期检查类型；源函数会拒绝的输入在目标被当成有效值，命中错误分支或覆盖旧值。自加源码没有的合法性规则（如把 0 当非法）同样改变结果。

## 做法

1. 改写前写出源函数接受与拒绝的输入：toIntOrNull/toLongOrNull 要求整串为十进制整数（可带正负号）且在 Int/Long 范围内；ZonedDateTime.parse 要求含 T 时间部分与 Z、±HH:MM 或 [Zone]；kotlinx 解码在字段类型不符时抛错。
2. 整数串先用 ^[+-]?\d+$ 整串校验再 Number() 并检查范围；时间串先按 ISO_ZONED_DATE_TIME 格式校验再转 epoch 毫秒；手写 fromJson 对每个字段 typeof 检查，不符即抛给外层回退。只保留源码已有的回落分支。

## 可选检查

- 对每个解析点用一个源函数会拒绝的反例（如 '15abc'、'2024-01-02'、数字类型的字符串字段）和一个边界合法值（如 '0'）核对结果与源函数一致

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-7eb907f6ed073fe3b558](../../../store/cases/case-7eb907f6ed073fe3b558/6cf1c95e0322499dbba90a974bba505f9f4fc45aabf6eacc8c9c824a359dc2d2.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`6cf1c95e0322499dbba90a974bba505f9f4fc45aabf6eacc8c9c824a359dc2d2`
