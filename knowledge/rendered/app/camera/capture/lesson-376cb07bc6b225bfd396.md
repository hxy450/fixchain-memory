# 相机 photoAvailable 回调的 JPEG 字节交给异步保存时，先复制 byteBuffer 再释放 Photo

## 何时使用

拍照接线与图像保存实现阶段，从 PhotoOutput 的 photoAvailable 回调取 component.byteBuffer、决定 Photo.release 时机时

## 适用情境

源端 onImageAvailable 先把 JPEG 平面复制成 byte[] 再 image.close()；目标在 photo.main.getComponent(JPEG) 后拿到 byteBuffer，字节要交给排队的后台保存或其他异步消费者。

## 原因

byteBuffer 由 Photo 持有的原生图像提供；先 release 再把同一个 ArrayBuffer 交给异步队列，是释放后使用。SDK 声明没有写明 release 后缓冲的有效期，可依赖的是源端“先复制、再关闭”的顺序。

## 做法

1. await getComponent 后用 byteBuffer.slice(0) 复制出独立的 ArrayBuffer 交给消费者，再在 finally 中 release Photo；不复制时由消费方在使用完成后 release，不在交出前释放。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 原因〕安卓 Image.close() 之后，再读写先前由 Plane.getBuffer 得到的 ByteBuffer 属于未定义行为
- 〔原因〕camera.Photo.release 的说明只写「释放输出资源」，image.Component.byteBuffer 的说明只写「组件缓冲区」；声明和文档都没写 release 之后先前取得的 byteBuffer 是否仍有效
