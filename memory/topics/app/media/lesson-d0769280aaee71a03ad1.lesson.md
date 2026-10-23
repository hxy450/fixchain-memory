# 源端 Bitmap 被处理函数替换并 recycle、调用方再冗余 recycle 时，每个 PixelMap 定唯一所有者只 release 一次

ID：`lesson-d0769280aaee71a03ad1` · 版本：1 · 阶段：execute · 主题：[app/media](index.md)

概要：PixelMap 定唯一所有者，成品覆盖变量只释放一次

信号：`Bitmap.recycle`, `recycle()`, `PixelMap`, `PixelMap.release`, `release()`, `cloneSync`

## 何时使用

图像处理与保存实现阶段，迁移 Bitmap 的替换、回收与跨组件传递，确定每个 PixelMap 由谁 release 时

## 适用情境

源端写 bitmap = process(bitmap)，处理函数产出新位图时回收输入，缩略图与末尾 recycle 都针对成品，调用方另有冗余 recycle；或同一位图同时交给多个界面接收方。目标改用 PixelMap，release 后实例不可再用。

## 原因

Java 的 Bitmap.recycle 对已回收位图是空操作（android.graphics.Bitmap.java 以 mRecycled 判定），源端冗余回收无害；照搬成多处 PixelMap.release，又把处理结果放进另一个局部变量而继续使用入参，会对已被处理函数释放的输入再次 release，缩略图取自已释放或未处理的位图。同一 PixelMap 交给两个生命周期独立的接收方时，任一方释放都会让另一方失效。

## 做法

1. 按源端赋值关系迁移：处理函数返回新图并释放输入时，用返回值覆盖同一承载变量，编码、缩略图与末尾 release 都针对这个成品。
2. 为每个 PixelMap 写明唯一所有者：被调方接管并释放后，调用方不再 release；源端调用方的冗余 recycle 不逐行照搬。
3. 同一图像要交给多个生命周期独立的接收方（如画廊按钮与预览覆盖层）时，接收方 cloneSync() 后各自持有、各自释放（@ohos.multimedia.image.d.ts，API 24）。

## 可选检查

- 对释放次数有疑问时，用单测断言一次保存流程中每个 PixelMap 的 release 只调用一次

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [最近媒体以自存 URI 为准，未授权不整库查询](../media-library/lesson-43781ac1c21274acd48b.lesson.md)（共享 1 张卡）
- [权限按目标 API 的 @permission 汇总](../capability/sdk-lookup/lesson-652974ce64a9243faebc.lesson.md)（共享 1 张卡）
- [覆盖写加 TRUNC，按 writeSync 返回值写完](../../data/storage/lesson-89496d5566f87f197bba.lesson.md)（共享 1 张卡）
- [降采样改 desiredSize，方向按字符串映射](lesson-c61656e804e536885d20.lesson.md)（共享 1 张卡）
- [Photo 字节先复制或用完再 release，不释放后用](../camera/capture/lesson-c81407857f6e70183c27.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-b49b06a3f59e5828d836](../../../../store/cases/case-b49b06a3f59e5828d836/b0c21a9a161e7ed16138409305b66db0fde6ae1b4f424aef58675d54daf54e71.json) · 结论：diagnosis, rec-7d42096f35
  卡片版本：`b0c21a9a161e7ed16138409305b66db0fde6ae1b4f424aef58675d54daf54e71`
- [case-d5c3514ada560cb5134d](../../../../store/cases/case-d5c3514ada560cb5134d/f08e3534f55b8cc6ebd570ff39c426fb4462edec6d303e3d2574fe5789a9b67f.json) · 结论：diagnosis, rec-0a1ac8aaf0
  卡片版本：`f08e3534f55b8cc6ebd570ff39c426fb4462edec6d303e3d2574fe5789a9b67f`
