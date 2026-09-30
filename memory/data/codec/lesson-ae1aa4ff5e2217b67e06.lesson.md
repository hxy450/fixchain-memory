# 手写 proto3 编解码时按字段 wire type 成对实现读写；int32 负值按 64 位补码逐组拆成 10 字节 varint

ID：`lesson-ae1aa4ff5e2217b67e06` · 版本：1

[本主题](index.md)

## 何时使用

数据层实现阶段，在没有 protobuf 运行时的目标端手写 proto3 编解码基座、为每个消息字段选择读写方法时

## 适用情境

目标端（如 ArkTS）需按字段表（字段号、wire type、标量类型）手写 proto3 编码与解码；字段表含 wire type 0 的有符号 int32（非 sint32，值可能为负，如 RSSI、海拔），同时存在 fixed32/sfixed32/float 等 4 字节定长字段；可用的位运算只有 32 位。

## 原因

wire type 决定线上字节数：wire 0 的 varint 长度可变，负 int32 在线上是 64 位符号扩展后的 10 字节 varint；用 4 字节定长方法读 varint 字段，会让该字段之后的整条消息错位。用 32 位位运算拼负数字节时，跨 32 位边界的第 5 组（bit28..34）只有 bit32..34 来自高位，凭“剩余高位全为 1”写常量只对 ≥ -2^28 的值成立。来源中生成者已读到字段表写明 rx_rssi 为 wire 0 INT32，编码写 int32，解码却选了读端唯一返回有符号数的 4 字节 fixed32()；同一编码器把负值第 5 字节写死为 0xFF，INT32_MIN 一类取值直到设备单测才暴露。

## 做法

1. 按字段表的 wire type 选读写方法，不按值是否有符号选：wire 0 用 varint 族（int32/uint32/enum/bool），wire 5 用 fixed32/sfixed32/float，wire 1 用 fixed64 族。
2. 基座为每个写方法提供同名、同 wire type 的读方法（writer.int32 ↔ reader.int32，sfixed32 ↔ sfixed32），方法名与 proto 标量类型一致；每个 message 写完，逐字段对照 encode 中的 w.xxx(N, …) 与 decode 中 field === N 分支的 r.xxx()。
3. int32 负值编码时取 lo = value >>> 0、hi = 0xFFFFFFFF：前 4 组取 lo 的 bit0..27，第 5 组取 (lo >>> 28) | ((hi & 0x0f) << 4)，其后依次取 hi >>> 3、10、17、24 的 7 位分组，末字节为 hi >>> 31（即 0x01），除末字节外都置续位 0x80；读端按 32 位窗口累加 7 位组后用 value | 0 还原符号。

## 可选检查

- 对负值字段有疑问时，用字节级用例对照标准编码：INT32_MIN 的值部分为 80 80 80 80 F8 FF FF FF FF 01，并覆盖 -1、-268435456、-268435457；再用“负值 int32 字段后接更高字段号”的往返用例确认后续字段未错位。

## 来源（按需复核）

- [case-315ff2de8e2d8d4c0c8d](../../../store/cases/case-315ff2de8e2d8d4c0c8d/336d3073c4913805e98971d1939b13a9e60ebbd6b84a97fe4ce12c1f09e8d4cb.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`336d3073c4913805e98971d1939b13a9e60ebbd6b84a97fe4ce12c1f09e8d4cb`
- [case-6b781bb8b1a4eb80b808](../../../store/cases/case-6b781bb8b1a4eb80b808/24d878a8aaa32c3bdfd97e6c38e9535508127e0644d3461891a191099f6f7298.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`24d878a8aaa32c3bdfd97e6c38e9535508127e0644d3461891a191099f6f7298`
