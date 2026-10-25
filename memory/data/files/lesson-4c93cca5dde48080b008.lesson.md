# OutputStream 覆盖写改成 fileIo：打开加 TRUNC，按 writeSync 返回值写完，字节视图按偏移切出 ArrayBuffer

ID：`lesson-4c93cca5dde48080b008` · 版本：1

[本主题](index.md)

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

## 来源（按需复核）

- [case-b49b06a3f59e5828d836](../../../store/cases/case-b49b06a3f59e5828d836/b0c21a9a161e7ed16138409305b66db0fde6ae1b4f424aef58675d54daf54e71.json) · 结论：diagnosis, recommendation:3
  卡片版本：`b0c21a9a161e7ed16138409305b66db0fde6ae1b4f424aef58675d54daf54e71`
