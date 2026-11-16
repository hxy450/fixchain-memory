# 替代 ExifInterface 的手写 EXIF/TIFF 编解码

agent 会看到什么：读到源端用 ExifInterface（androidx.exifinterface）按 TAG_* 名 setAttribute / saveAttributes、setGpsInfo 写 EXIF，对 JPEG / PNG / WebP 输出都写；产物里手写的 TIFF/IFD 编解码：tag 号表、DataView 的有无符号读写、serialize 的值区偏移、APP1 / eXIf / VP8X 容器写法

## 通用查法

### 自写 EXIF 编解码替代 ExifInterface 时，tag 号、类型、布局、容器照库源码写

审的是：代码
触发（任一种）：
- 读到：源端经 ExifInterface 按 TAG_* 名 setAttribute / saveAttributes 读写 EXIF，目标端改成手写 TIFF/IFD 编解码；写错的样子：手写 codec 的 tag 号、IFD_FORMAT 类型、值区偏移、APP1 / eXIf / VP8X 容器凭记忆写，没和库源码对照
适用范围：目标端自己实现 ExifInterface 的 tag 表和读写语义时
做法：
- 按 TAG_* 名在 ExifInterface 源码的 EXIF_TAGS 里找 new ExifTag(TAG_名, 号, IFD_FORMAT_*)，读出 tag 号、所属 IFD 和类型；SSHORT / SLONG / SRATIONAL 按有符号，UNDEFINED 原样保留字节
- 字符串转换看 setAttribute，布局看 writeExifSegment，PNG / WebP 看 savePngAttributes / saveWebpAttributes，照写进目标 codec
- 查不到的登记待验证，不凭记忆补；用 parse(serialize(doc)) 往返单测逐 tag 比对字节
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- new ExifTag(TAG_TRANSFER_FUNCTION, 301, IFD_FORMAT_USHORT)：EXIF_TAGS 表里一条的样子：tag 名、tag 号、数据类型（出处：android.media.ExifInterface#EXIF_TAGS）
- IFD_FORMAT_STRING = 2、IFD_FORMAT_UNDEFINED = 7、IFD_FORMAT_SSHORT = 8、IFD_FORMAT_SLONG = 9、IFD_FORMAT_SRATIONAL = 10：TIFF 数据类型号，后三个是有符号（出处：android.media.ExifInterface（IFD_FORMAT_* 常量））
- position += 2 + 条目数 × 12 + 4 + 该 IFD 超过 4 字节的值之和：writeExifSegment 里各 IFD 的偏移跨 IFD 依次累加，值区不重叠（出处：android.media.ExifInterface#writeExifSegment）
针对本应用要查的：
- 应用依赖版本的 ExifInterface 源码：源工程模块依赖里 androidx.exifinterface:exifinterface 的版本（直接用 android.media.ExifInterface 的按 compileSdk 取平台源码），对应版本里的 ExifInterface 类；按 TAG_* 名在 EXIF_TAGS 里读 tag 号和 IFD_FORMAT_*，再按要做的事读 setAttribute、writeExifSegment、savePngAttributes、saveWebpAttributes 的写法
未核实：tag 表、类型号和布局按 Android 平台 android.media.ExifInterface 核实；应用依赖 androidx.exifinterface 时，本机没有它的源码，版本差异未核
来源：1 张卡，1 个应用
- case-67ee41a265150362c3e5（opencamera-hmos）：做法第 1 步 ← 建议 2、建议 1；做法第 2 步 ← 建议 1、建议 3；做法第 3 步 ← 建议 2、建议 1

## 规矩

- rule-23d3310ef73f｜用代码替代 ExifInterface 时 tag 号和字符串转换从库源码取，删除项不置 -1｜读到：源码只用 ExifInterface.TAG_* 名，removeExifTags 删除 TAG_CFA_PATTERN、TAG_TRANSFER_FUNCTION、TAG_XMP、TAG_INTEROPERABILITY_INDEX；写错：tag 号凭记忆填（如 CFAPattern 写 0x828E、TransferFunction 写 0x0120），XMP、InteroperabilityIndex 置 -1，删除成了空操作
- rule-fc9df4bb9007｜自研 EXIF 读写时有符号类型按有符号读写，ASCII 遇 NUL 截断，UNDEFINED 保留 NUL｜读到：源端经 ExifInterface 读写 SSHORT / SLONG / SRATIONAL 类型的 tag，UserComment 前缀是 "ASCII\0\0\0" 这类真实 NUL；写错：SSHORT / SLONG 用 getUint16 / getUint32 读，写入和有理数解析经 parseUint 把负值钳成 0；读 ASCII / UNDEFINED 时跳过所有 NUL 字节
- rule-01fa37def427｜自研 TIFF/EXIF 序列化时值区偏移跨 IFD 依次推进，不让各 IFD 从同一偏移分配｜读到：源端用 androidx.exifinterface 的 ExifInterface 按 tag 名 setAttribute / saveAttributes，目标端规格要求自研 TIFF/EXIF 段写回；写错：serialize 里 ifd0、exif、gps 都从同一个 dataOffset 调 assignData 再取最大值，三个 IFD 超过 4 字节的值写进同一区域互相覆盖
- rule-d21b8e015bf6｜写 EXIF 前按输出的实际编码选容器，不把 JPEG 的 APP1 拼接套在 PNG/WebP 上｜读到：源码对 JPEG / PNG / WebP 输出都调 setExifFromData（注释「ExifInterface now supports WebP and PNG」）；写错：spliceExifTiff 不看实际编码，一律在开头两字节后插 APP1；位图路径产出的 PNG / WebP 也这样调用
