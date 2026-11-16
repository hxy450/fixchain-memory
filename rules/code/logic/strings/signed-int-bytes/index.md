# 手写字节编解码里的有符号整数

agent 会看到什么：读到 proto 字段类型 int32（wire type 0、可能为负）或 Java 源码里 byte 与 0x80 以上 int 字面量比较；产物里手写的 varint 编码、Uint8Array / number[] 字节比较和编解码单测

## 规矩

- rule-361c9f0f0540｜手写 int32 负值 varint 时拆成 lo/hi 两个 32 位半字逐 7 位写，不写死 0xFF｜读到：proto 字段类型是 `int32`（不是 `sint32`），wire type 0（varint），值可能为负；写错：手写的编码函数在低 4 组 7 位之后直接写死 `0xff` ×5 再加 `0x01`，第 5 组没取低 32 位的 bit28..31
- rule-5411baccfbc0｜手写 int32 编解码的单测要有负值字节级断言，不只靠自写读写往返｜读到：proto 字段类型是 `int32`，目标端手写编解码器；写错：单测只做自写的 encode → decode 往返，没有断言 -1、-268435456、-268435457、INT32_MIN 编出的字节
- rule-f6b0dc27e016｜Java byte 与 0x80 以上的 int 字面量比较时，先换成有符号值再照写｜读到：Java 源码里 `byte` 变量与大于 0x7F 的 int 字面量（如 0x81、0xFE）做 `<`、`>` 比较；写错：ArkTS 直接拿 Uint8Array 或 number[] 里 0–255 的字节和同一字面量比较，注释称与 Java 有符号位模式一致
