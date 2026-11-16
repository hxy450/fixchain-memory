# androidx ExifInterface 读写 EXIF

agent 会看到什么：读到源端用 androidx ExifInterface 读写图片 EXIF（注释写着支持 WebP 和 PNG、调 setGpsInfo(location)），规格决定自研替代库，映射只写「JPEG 段级读写」「tag 名域不变」

## 规矩

- rule-88b7bb00bf6d｜规格决定自研替代库时，写清库覆盖的全部容器和要复刻的库内隐式语义｜读到：源端用 androidx ExifInterface 读写 EXIF，源码注释「ExifInterface now supports WebP and PNG」，调用 setGpsInfo(location)；写错：映射写「JPEG 段级读写；tag 名域 → 字符串值域不变」，没列 PNG / WebP 容器、数字 tag 号、字符串到二进制的转换和 setGpsInfo 写的字段；判据写「异常分支吞错继续」
