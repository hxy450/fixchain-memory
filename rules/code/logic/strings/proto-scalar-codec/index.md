# 手写 proto 编解码的标量读写方法

agent 会看到什么：读到字段表（字段号 | wire type | 标量类型）里同时有 wire type 0 的 INT32 和 FIXED32 / SFIXED32 字段；产物里手写 codec 的 int32() / fixed32() / sfixed32() / varint() / le32() 读写方法和各字段的调用

## 规矩

- rule-1c7585dc7b25｜手写 proto3 编解码按 wire type 选读写法，wire 0 的 int32 不用 fixed32 读｜读到：字段表（字段号 | wire type | 标量类型）里有 wire type 0 的 `INT32` 字段（可能为负），同时有 fixed32/sfixed32 定长字段；写错：encode 写 `w.int32(N, …)`，decode 对同一字段写 `r.fixed32()`；或 decode 用无符号 `r.varint()` 读负值字段
- rule-bc526ac574c7｜手写 codec 基座时每个写方法配对称的读方法，方法名与 proto 标量类型一致｜读到：字段表里同时有 `INT32`（wire 0）和 FIXED32/SFIXED32（wire 5）字段；写错：Writer 有 int32()，Reader 只有无符号 varint()、le32() 和返回有符号值的 fixed32()，缺 int32()；或名为 fixed32() 的方法却做 sfixed32 的符号还原
