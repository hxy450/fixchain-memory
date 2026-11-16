# ArkTS Buffer 转独立 Uint8Array 时按 length 分配后 copy，不用 .buffer 视图

审的是：代码
触发（任一种）：
- 读到：构建输出报 Property 'byteLength' does not exist on type 'Buffer'；写错的样子：代码里写 new Uint8Array(buf.buffer, buf.byteOffset, buf.length) 或 new Uint8Array(buffer.from(...).buffer)，或把 byteLength 机械替换成 length 后仍保留这种视图；真机抛 RangeError: The newByteLength is out of range
适用范围：ArkTS 里用 @kit.ArkTS 的 buffer（buffer.from、buffer.alloc 得到的 Buffer）交出独立的 Uint8Array（如填进 cryptoFramework 的 DataBlob）时
做法：
- 写成 const out = new Uint8Array(buf.length); buf.copy(out); 之后把 out 交给 DataBlob 等下游
- 编译报 Buffer 上没有某个 Node 属性时，按 ArkTS buffer 的声明改写法，不把 byteLength 之类字段名换成 length 了事
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- length: number：Buffer 的字节数；Buffer 类上没有 byteLength 属性（出处：鸿蒙 SDK 的 ets/api/@ohos.buffer.d.ts，Buffer.length）
- copy(target: Buffer | Uint8Array, targetStart?: number, sourceStart?: number, sourceEnd?: number): number：把本 Buffer 的数据拷到目标里，sourceEnd 默认是本 Buffer 的 length，返回拷贝的字节数（出处：鸿蒙 SDK 的 ets/api/@ohos.buffer.d.ts，Buffer.copy）
- byteOffset：Buffer 通过内存池创建时（allocUninitializedFromPool，或 buffer.from() 传字符串且长度加内存池偏移小于 4kb）是相对内存池的偏移；直接分配（alloc）时是 0：buf.buffer 可能是整个内存池，按 .buffer/.byteOffset 取视图不可靠（出处：js-apis-buffer.md，Buffer / 属性）
- copy(target: FastBuffer | Uint8Array, targetStart?: number, sourceStart?: number, sourceEnd?: number): number：同族接口：FastBuffer 的 copy（出处：鸿蒙 SDK 的 ets/api/@ohos.fastbuffer.d.ts，FastBuffer.copy）
- 视图写法在真机加密和解密两处抛 RangeError: The newByteLength is out of range；改成按 length 分配后拷贝即恢复：验证过的写法是显式拷贝（出处：卡里修好并验证过）
未核实：RangeError 的精确机制（.buffer 与 byteOffset 所指的内存）卡里没验证；同一写法曾经成功过一次，和运行时缓冲状态有关
来源：1 张卡，1 个应用
- case-c5fdc6640404c3d6440e（android-train-ticket-vest7）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3；取值 5 ← 诊断
