# 自研 EXIF 读写时有符号类型按有符号读写，ASCII 遇 NUL 截断，UNDEFINED 保留 NUL

审的是：代码
触发（任一种）：
- 读到：源端经 ExifInterface 读写 SSHORT / SLONG / SRATIONAL 类型的 tag，UserComment 前缀是 "ASCII\0\0\0" 这类真实 NUL；写错的样子：SSHORT / SLONG 用 getUint16 / getUint32 读，写入和有理数解析经 parseUint 把负值钳成 0；读 ASCII / UNDEFINED 时跳过所有 NUL 字节
适用范围：自写 TIFF/EXIF 读写器处理各数据类型时
做法：
- SSHORT / SLONG 用 DataView.getInt16 / getInt32 读、setInt16 / setInt32 写；SRATIONAL 的分子分母都按有符号解析；ASCII 遇第一个 NUL 截断；UNDEFINED 按字节原样保留（含 NUL）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- IFD_FORMAT_UNDEFINED = 7、SSHORT = 8、SLONG = 9、SRATIONAL = 10；STRING（ASCII）= 2：TIFF 数据类型号，后三个是有符号（出处：android.media.ExifInterface（IFD_FORMAT_* 常量））
- getInt16(byteOffset: number, littleEndian?: boolean): number；setInt32(byteOffset: number, value: number, littleEndian?: boolean): void：DataView 的有符号读写；getUint16 / getUint32 是无符号的（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，DataView.getInt16、DataView.setInt32）
- 改为 getInt16/32、setInt16/32、有符号有理数、ASCII 遇 NUL 截断后往返正确：修复后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-67ee41a265150362c3e5（opencamera-hmos）：做法第 1 步 ← 诊断、建议 1；取值 3 ← 诊断
