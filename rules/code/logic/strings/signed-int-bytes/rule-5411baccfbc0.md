# 手写 int32 编解码的单测要有负值字节级断言，不只靠自写读写往返

审的是：代码
触发（任一种）：
- 读到：proto 字段类型是 `int32`，目标端手写编解码器；写错的样子：单测只做自写的 encode → decode 往返，没有断言 -1、-268435456、-268435457、INT32_MIN 编出的字节
适用范围：为手写的 protobuf int32 编解码写单元测试时
做法：
- 对 -1、-268435456（-2^28）、-268435457、INT32_MIN 各写字节级断言，期望值对照标准 protobuf 编码结果，不只依赖往返
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- INT32_MIN → 80 80 80 80 F8 FF FF FF FF 01：期望字节（不含 tag）（出处：卡里修好并验证过）
- int32 以无符号 varint 写出，负值长 10 字节：每个负值用例的期望字节都应是 10 个（出处：android.util.proto.ProtoOutputStream#writeInt32）
针对本应用要查的：
- 除 INT32_MIN 外各边界值（-1、-2^28、-2^28-1）的期望字节：源端的 int32 编码函数；源端没有自己的编码函数时，Android SDK 框架源码 android.util.proto.ProtoOutputStream#writeUnsignedVarintFromSignedInt 和 android.util.proto.EncodedBuffer#writeRawVarint64；按其中负值符号扩展到 64 位、每次取低 7 位或上 0x80、再无符号右移 7 位的算法算出字节，再和源端实际编码输出比对一致后写进断言
未核实：别的边界值的期望字节没有核实，要按源端编码函数的算法自己算并和源端实际输出比对
来源：1 张卡，1 个应用
- case-315ff2de8e2d8d4c0c8d（Meshtastic）：做法第 1 步 ← 建议 2；取值 1 ← 诊断、建议 2
