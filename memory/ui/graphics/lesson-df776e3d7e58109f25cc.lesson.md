# Bitmap.recycle 迁成 PixelMap.release 前先定唯一所有者：成品只释放一次，多方持有时各自 cloneSync

ID：`lesson-df776e3d7e58109f25cc` · 版本：1

[本主题](index.md)

## 何时使用

图像处理与保存实现阶段，把 Android Bitmap 的后处理、缩略图生成与 recycle 迁成 PixelMap 调用，或把同一张图同时交给多个消费方（画廊图标、Canvas 覆盖层）时

## 适用情境

源端后处理函数返回新位图并释放输入，调用处把返回值赋回同一变量，缩略图与末尾 recycle 都针对成品；调用方另外再 recycle（Java 的 recycle 可重复调用，冗余调用无害）。目标 PixelMap.release 后对象不再可用，同一张图还可能经回调分发给多个组件。

## 原因

逐行照搬 recycle 会让同一 PixelMap 被多处 release；后处理结果只存进局部变量时，缩略图取到未处理或已释放的原图，成品无人释放。两个消费方共用一个 PixelMap 时，一方释放会让另一方的绘制或编码失效。

## 做法

1. 列出每张 PixelMap 的创建点与唯一释放点：后处理替换输入并释放旧图时，用返回值覆盖同一变量，编码、缩略图与末尾 release 都针对这个成品；调用方不再重复 release。
2. 同一张图交给多个独立持有者时，接收方 cloneSync 出自己的副本并各自释放，或明确由一方持有、其余只借用且不释放。

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-b49b06a3f59e5828d836](../../../store/cases/case-b49b06a3f59e5828d836/b0c21a9a161e7ed16138409305b66db0fde6ae1b4f424aef58675d54daf54e71.json) · 结论：diagnosis, recommendation:2
  卡片版本：`b0c21a9a161e7ed16138409305b66db0fde6ae1b4f424aef58675d54daf54e71`
- [case-d5c3514ada560cb5134d](../../../store/cases/case-d5c3514ada560cb5134d/f08e3534f55b8cc6ebd570ff39c426fb4462edec6d303e3d2574fe5789a9b67f.json) · 结论：recommendation:4
  卡片版本：`f08e3534f55b8cc6ebd570ff39c426fb4462edec6d303e3d2574fe5789a9b67f`
