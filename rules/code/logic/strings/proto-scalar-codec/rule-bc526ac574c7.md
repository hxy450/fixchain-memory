# 手写 codec 基座时每个写方法配对称的读方法，方法名与 proto 标量类型一致

审的是：代码
触发（任一种）：
- 读到：字段表里同时有 `INT32`（wire 0）和 FIXED32/SFIXED32（wire 5）字段；写错的样子：Writer 有 int32()，Reader 只有无符号 varint()、le32() 和返回有符号值的 fixed32()，缺 int32()；或名为 fixed32() 的方法却做 sfixed32 的符号还原
适用范围：编写手写 protobuf 编解码的公共基座（Reader/Writer）时
做法：
- 读写成对提供：writer.int32↔reader.int32，uint32↔uint32，fixed32↔fixed32，sfixed32↔sfixed32；方法名与 proto 标量类型一致，fixed32 返回无符号、sfixed32 返回有符号
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- readFixed32() 与 readSFixed32() 在 Java 里都返回 int（同为 readRawLittleEndian32）：Java 没有无符号 int，两者只差语义；ArkTS 的 number 能表示无符号值，fixed32 应读成 0–2^32-1（出处：com.google.protobuf.CodedInputStream#readFixed32、readSFixed32）
未核实：fixed32 在 ArkTS 里读成无符号是按 proto 标量语义推的，卡里只说了方法名要与语义一致
来源：1 张卡，1 个应用
- case-6b781bb8b1a4eb80b808（Meshtastic）：做法第 1 步 ← 建议 2
