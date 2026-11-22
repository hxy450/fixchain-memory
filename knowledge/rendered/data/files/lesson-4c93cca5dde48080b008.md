# OutputStream 覆盖写改成 fileIo：打开加 TRUNC，按 writeSync 返回值写完，字节视图按偏移切出 ArrayBuffer

## 何时使用

数据与服务层实现阶段，把 Java FileOutputStream/openOutputStream 加 write(data) 的整文件写入翻译为 fileIo.openSync/writeSync，或把 Uint8Array 字节交给要求 ArrayBuffer 的接口时

## 适用情境

源端以非追加方式打开输出流后一次 write(data) 覆盖整个文件；目标照参考示例写 openSync(WRITE_ONLY | CREATE) 加一次 writeSync，示例针对新建文件与字符串内容；要写的字节可能是 subarray 视图（如元数据写入器返回的切片）。

## 原因

不带 TRUNC 打开已存在的文件只覆盖前段，新内容较短时旧尾部残留；writeSync 返回实际写入的字节数，不检查就无法发现短写。Uint8Array 视图的 .buffer 是整个底层缓冲，直接传会写入视图范围以外的字节。

## 做法

1. 覆盖写用 fileIo.OpenMode.WRITE_ONLY | fileIo.OpenMode.CREATE | fileIo.OpenMode.TRUNC 打开（源端为追加时才用 APPEND）；按 writeSync 返回的字节数循环写入剩余部分，返回 0 时抛错。
2. Uint8Array 交给要 ArrayBuffer 的接口时用 bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength)，不直接传 bytes.buffer。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕fileIo 以 OpenMode.TRUNC 打开时，文件已存在且以只写或读写方式打开就把它的长度裁剪为零；OpenMode.APPEND 让后续写入追加到文件末尾
- 〔原因 / 做法第 1 步〕fileIo.writeSync 返回实际写入的数据长度（字节）；options.length 不写时为缓冲区长度，options.offset 不写时从文件当前位置写起
- 〔适用情境〕java.io.FileOutputStream 不带 append 参数的构造等同 append 为 false，按 O_WRONLY | O_CREAT | O_TRUNC 打开：已存在的文件先被截成 0 长度再写
- 〔原因 / 做法第 2 步〕Uint8Array 的 buffer 是它引用的整个 ArrayBuffer；subarray 返回的视图与原数组共用同一个 ArrayBuffer，视图范围由 byteOffset、byteLength 标出
