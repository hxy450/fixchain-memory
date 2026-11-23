# 兼容层交给冻结业务的对象，按全部消费方保留尺寸等元数据语义，并按下游处理上限先在原生侧缩放大图

## 何时使用

插件兼容层实现或返修阶段，决定把系统选择器结果、缓存副本以什么分辨率、带哪些元数据包装成原 API 对象交给冻结 Dart 业务，或为性能删改其中的计算时

## 适用情境

Flutter 应用 Dart 冻结；本地兼容包把系统选择器结果包装成 AssetEntity 等原 API 对象，经共享入口分发给多个业务页面；下游有页面用对象宽高计算比例，有链路用 package:image 等纯 Dart 库在 UI isolate 同步解码、缩放、编码；用户可能选择千万像素级相机照片。

## 原因

兼容层返回的对象是冻结业务唯一能拿到的数据，只按报告的那条流程改变它的分辨率或字段，其他消费方就会出错。来源两例：把原图原样交给在 UI isolate 同步做像素运算的业务链，3002×4003 的照片使 UI 线程阻塞约 6 秒，OHOS 以 BUSSINESS_THREAD_BLOCK_6S 结束进程（同一 Dart 代码在 Android 未报此问题；来源输入中没有 skill 或规格说明该看门狗）；为省去整图解码把宽高写成 0，下游按宽高比计算得到 0/0，布局约束变成 NaN 并报错。

## 做法

1. 改写兼容层返回对象前，在整个 lib 中检索该对象及其字段的消费方（如 .width/.height、assets.first.width、传给下游页的 imageWidth/imageHeight），并打开会压缩、上传或编辑原图的代表性链路，记下依赖的字段与业务自身的尺寸上限；不只过滤到报告的流程。
2. 下游在 UI isolate 同步处理原图时，在兼容层用原生图片引擎（ImageSource，或 flutter_image_compress 的 compressAndGetFile）按业务上限等比缩放到两边都不超界（用 ImageSource 解码时 desiredSize 不保持宽高比，要先按原图宽高比算出目标宽高再传），失败回退原文件；不在 Dart 侧整图解码。
3. 宽高从文件头读取（ImageSource.getImageInfo 或读取头信息的库），需要时按 EXIF 方向交换；读取失败给非零兜底，不用 0 占位。

## 可选检查

- 改动共享选图入口后，至少打开一个依赖宽高的页面，并用千万像素级相机原图走会压缩或上传的入口，同时过滤 hilog 中的 FlutterWatchdog 与 BUSSINESS_THREAD_BLOCK_3S/6S。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 3 步〕Flutter 下游按选图对象的宽高算比例时，宽高为 0 会得到 0/0 = NaN，布局约束报 BoxConstraints 错误
- 〔做法第 2 步〕ImageSource.createPixelMap 的 DecodingOptions.desiredSize 是期望输出大小，没设时按原图尺寸解码（声明注释写 (0, 0) 表示按原图尺寸）；与原图比例不一致时会拉伸到指定尺寸
