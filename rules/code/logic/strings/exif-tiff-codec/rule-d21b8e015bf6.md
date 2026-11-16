# 写 EXIF 前按输出的实际编码选容器，不把 JPEG 的 APP1 拼接套在 PNG/WebP 上

审的是：代码
触发（任一种）：
- 读到：源码对 JPEG / PNG / WebP 输出都调 setExifFromData（注释「ExifInterface now supports WebP and PNG」）；写错的样子：spliceExifTiff 不看实际编码，一律在开头两字节后插 APP1；位图路径产出的 PNG / WebP 也这样调用
适用范围：自写 EXIF 写入器给多种图像容器写元数据时
做法：
- 按输出文件头判断编码：JPEG 写 APP1（0xFFE1，"Exif\0\0" 加 TIFF）；PNG 写带 CRC 的 eXIf 块；WebP 写 RIFF 的 EXIF 块，首块须为 VP8X 并置 EXIF 标志；截断或非法容器直接报错
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- MARKER_APP1 = 0xe1：JPEG 的 EXIF 段标记（出处：android.media.ExifInterface#MARKER_APP1）
- PNG：EXIF 块在 IHDR 之后（已有则原位替换），CRC32 覆盖块类型和数据（跳过 4 字节长度）：PNG 容器的写法（出处：android.media.ExifInterface#savePngAttributes）
- WebP：VP8X 为第一块、VP8X 里 EXIF 标志置 1、EXIF 块按规定顺序排在图像数据之后；原文件首块是 VP8 / VP8L 时要补 VP8X：WebP 容器的写法（出处：android.media.ExifInterface#saveWebpAttributes）
- 按 JPEG / PNG / WebP 分别写原生 EXIF、非法容器报错后，三种输出都带正确 EXIF：修复后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-67ee41a265150362c3e5（opencamera-hmos）：做法第 1 步 ← 建议 3、诊断；取值 4 ← 诊断
