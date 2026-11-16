# 规格决定自研替代库时，写清库覆盖的全部容器和要复刻的库内隐式语义

审的是：规格
触发（任一种）：
- 读到：源端用 androidx ExifInterface 读写 EXIF，源码注释「ExifInterface now supports WebP and PNG」，调用 setGpsInfo(location)；写错的样子：映射写「JPEG 段级读写；tag 名域 → 字符串值域不变」，没列 PNG / WebP 容器、数字 tag 号、字符串到二进制的转换和 setGpsInfo 写的字段；判据写「异常分支吞错继续」
适用范围：规格提取阶段决定用自研代码替代源端库时
做法：
- 映射里写清库覆盖的全部容器（ExifInterface 支持 JPEG / PNG / WebP），列出要复刻的库内隐式语义及来源：数字 tag 号、字符串值的二进制转换、setGpsInfo 写入的字段
- 判据里的「异常分支吞错继续」限定为源端实际捕获的异常类型
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 平台 ExifInterface 有 savePngAttributes、saveWebpAttributes 两条写入路径：库覆盖 PNG 和 WebP，不只 JPEG（出处：android.media.ExifInterface#savePngAttributes、android.media.ExifInterface#saveWebpAttributes）
针对本应用要查的：
- 库的覆盖范围和隐式语义：应用依赖版本的库源码（如 androidx.exifinterface 的 ExifInterface 类）；列出它支持的容器、tag 表、setAttribute 的字符串转换和便捷方法（setGpsInfo 等）写入的字段，逐项写进映射
来源：1 张卡，1 个应用
- case-67ee41a265150362c3e5（opencamera-hmos）：做法第 1 步 ← 建议 6；做法第 2 步 ← 建议 6
