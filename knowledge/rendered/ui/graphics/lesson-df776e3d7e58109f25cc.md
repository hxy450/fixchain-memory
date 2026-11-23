# Bitmap.recycle 迁成 PixelMap.release 前先定唯一所有者：成品只释放一次，多方持有时各自 cloneSync

## 何时使用

图像处理与保存实现阶段，把 Android Bitmap 的后处理、缩略图生成与 recycle 迁成 PixelMap 调用，或把同一张图同时交给多个消费方（画廊图标、Canvas 覆盖层）时

## 适用情境

源端后处理函数返回新位图并释放输入，调用处把返回值赋回同一变量，缩略图与末尾 recycle 都针对成品；调用方另外再 recycle（Java 的 recycle 可重复调用，冗余调用无害）。目标 PixelMap.release 后对象不再可用，同一张图还可能经回调分发给多个组件。

## 例外与边界

- PixelMap 的 cloneSync 与 clone 都从 API 18 起提供，对 YUV、ASTC 格式的 PixelMap 会抛错（62980103）；工程最低 API 低于 18，或要分发的图是这些格式时，改用“一方持有并负责释放、其余只借用不释放”的方式，不要硬写 cloneSync

## 原因

逐行照搬 recycle 会让同一 PixelMap 被多处 release；后处理结果只存进局部变量时，缩略图取到未处理或已释放的原图，成品无人释放。两个消费方共用一个 PixelMap 时，一方释放会让另一方的绘制或编码失效。

## 做法

1. 列出每张 PixelMap 的创建点与唯一释放点：后处理替换输入并释放旧图时，用返回值覆盖同一变量，编码、缩略图与末尾 release 都针对这个成品；调用方不再重复 release。
2. 同一张图交给多个独立持有者时，接收方 cloneSync 出自己的副本并各自释放，或明确由一方持有、其余只借用且不释放。

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境〕安卓 Bitmap.recycle 只在未回收时释放像素，重复调用时第二次起不做任何事
- 〔适用情境 / 原因〕PixelMap 调用 release 后，任何访问该对象内部数据的方法调用都会失败
- 〔做法第 2 步〕PixelMap.cloneSync（API 18 起）同步拷贝出一个新的 PixelMap 对象
