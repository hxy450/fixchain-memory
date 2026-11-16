# 自研 TIFF/EXIF 序列化时值区偏移跨 IFD 依次推进，不让各 IFD 从同一偏移分配

审的是：代码
触发（任一种）：
- 读到：源端用 androidx.exifinterface 的 ExifInterface 按 tag 名 setAttribute / saveAttributes，目标端规格要求自研 TIFF/EXIF 段写回；写错的样子：serialize 里 ifd0、exif、gps 都从同一个 dataOffset 调 assignData 再取最大值，三个 IFD 超过 4 字节的值写进同一区域互相覆盖
适用范围：自写 TIFF/EXIF 二进制序列化器替代 ExifInterface 时
做法：
- 按「各 IFD 目录块 → 值区」布局，目录大小统一按 2 + 12 × 条目数 + 4 算，值区偏移跨 IFD 链式推进，不每个 IFD 都从同一 dataOffset 重新分配
- 写 parse(serialize(doc)) 往返单测：ifd0 / exif / gps 各放超过 4 字节的值，再放负的 SSHORT / SLONG / SRATIONAL 和含 NUL 的 UNDEFINED / UserComment，逐 tag 比对字节；规格标为 判:unit 的编解码项不只做语法自检
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 改为值区链式推进、ifdSize 统一为 2+12n+4 后，各 IFD 的长值不再互相覆盖：修复后的写法（出处：卡里修好并验证过）
- 平台 ExifInterface 从 TIFF 头后 8 字节起，每个非空 IFD 占 2 + 条目数 × 12 + 4 + 该 IFD 超过 4 字节的值之和，位置依次累加：源端库的布局：偏移跨 IFD 推进，值区不重叠（出处：android.media.ExifInterface#writeExifSegment）
未核实：布局按 Android 平台 android.media.ExifInterface 核实；应用依赖的是 androidx.exifinterface，本机没有它的源码
来源：1 张卡，1 个应用
- case-67ee41a265150362c3e5（opencamera-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 1 ← 诊断
