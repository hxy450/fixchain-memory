# data/codec

手写二进制编解码（protobuf wire 格式）：字段 wire type 与读写方法的对称，varint 与负数补码的字节拆分

[上一级](../index.md)

## 本级经验

- [手写 proto3 编解码时按字段 wire type 成对实现读写；int32 负值按 64 位补码逐组拆成 10 字节 varint](lesson-ae1aa4ff5e2217b67e06.lesson.md)
  - 时机：数据层实现阶段，在没有 protobuf 运行时的目标端手写 proto3 编解码基座、为每个消息字段选择读写方法时
  - 情境：目标端（如 ArkTS）需按字段表（字段号、wire type、标量类型）手写 proto3 编码与解码；字段表含 wire type 0 的有符号 int32（非 sint32，值可能为负，如 RSSI、海拔），同时存在 fixed32/sfixed32/float 等 4 字节定长字段；可用的位运算只有 32 位。
