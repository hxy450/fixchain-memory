# 相机 photoAvailable 回调的 JPEG 字节交给异步保存时，先复制 byteBuffer 再释放 Photo

ID：`lesson-376cb07bc6b225bfd396` · 版本：1

[本主题](index.md)

## 何时使用

拍照接线与图像保存实现阶段，从 PhotoOutput 的 photoAvailable 回调取 component.byteBuffer、决定 Photo.release 时机时

## 适用情境

源端 onImageAvailable 先把 JPEG 平面复制成 byte[] 再 image.close()；目标在 photo.main.getComponent(JPEG) 后拿到 byteBuffer，字节要交给排队的后台保存或其他异步消费者。

## 原因

byteBuffer 由 Photo 持有的原生图像提供；先 release 再把同一个 ArrayBuffer 交给异步队列，是释放后使用。SDK 声明没有写明 release 后缓冲的有效期，可依赖的是源端“先复制、再关闭”的顺序。

## 做法

1. await getComponent 后用 byteBuffer.slice(0) 复制出独立的 ArrayBuffer 交给消费者，再在 finally 中 release Photo；不复制时由消费方在使用完成后 release，不在交出前释放。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-b49b06a3f59e5828d836](../../../../store/cases/case-b49b06a3f59e5828d836/b0c21a9a161e7ed16138409305b66db0fde6ae1b4f424aef58675d54daf54e71.json) · 结论：diagnosis, recommendation:1
  卡片版本：`b0c21a9a161e7ed16138409305b66db0fde6ae1b4f424aef58675d54daf54e71`
