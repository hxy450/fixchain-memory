# 兼容层交给冻结业务的对象，按全部消费方保留尺寸等元数据语义，并按下游处理上限先在原生侧缩放大图

ID：`lesson-e85bdb26fa6acc0cc9f7` · 版本：1

[本主题](index.md)

## 何时使用

插件兼容层实现或返修阶段，决定把系统选择器结果、缓存副本以什么分辨率、带哪些元数据包装成原 API 对象交给冻结 Dart 业务，或为性能删改其中的计算时

## 适用情境

Flutter 应用 Dart 冻结；本地兼容包把系统选择器结果包装成 AssetEntity 等原 API 对象，经共享入口分发给多个业务页面；下游有页面用对象宽高计算比例，有链路用 package:image 等纯 Dart 库在 UI isolate 同步解码、缩放、编码；用户可能选择千万像素级相机照片。

## 原因

兼容层返回的对象是冻结业务唯一能拿到的数据，只按报告的那条流程改变它的分辨率或字段，其他消费方就会出错。来源两例：把原图原样交给在 UI isolate 同步做像素运算的业务链，3002×4003 的照片使 UI 线程阻塞约 6 秒，OHOS 以 BUSSINESS_THREAD_BLOCK_6S 结束进程（同一 Dart 代码在 Android 未报此问题；来源输入中没有 skill 或规格说明该看门狗）；为省去整图解码把宽高写成 0，下游按宽高比计算得到 0/0，布局约束变成 NaN 并报错。

## 做法

1. 改写兼容层返回对象前，在整个 lib 中检索该对象及其字段的消费方（如 .width/.height、assets.first.width、传给下游页的 imageWidth/imageHeight），并打开会压缩、上传或编辑原图的代表性链路，记下依赖的字段与业务自身的尺寸上限；不只过滤到报告的流程。
2. 下游在 UI isolate 同步处理原图时，在兼容层用原生图片引擎（ImageSource，或 flutter_image_compress 的 compressAndGetFile）按业务上限等比缩放到两边都不超界，失败回退原文件；不在 Dart 侧整图解码。
3. 宽高从文件头读取（ImageSource.getImageInfo 或读取头信息的库），需要时按 EXIF 方向交换；读取失败给非零兜底，不用 0 占位。

## 可选检查

- 改动共享选图入口后，至少打开一个依赖宽高的页面，并用千万像素级相机原图走会压缩或上传的入口，同时过滤 hilog 中的 FlutterWatchdog 与 BUSSINESS_THREAD_BLOCK_3S/6S。

## 来源（按需复核）

- case-64090e208edc24d57300 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`fa1e30c795208b78dfb1b0f313b85160336c40c2ce56d072b7fe0e0641abed04`
- case-d166fd60d66832c204bc · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`8a13c1a88691478b3e62951c85de57be40c3a2f7adf63b040ee34ccf671ca632`
