# app/media

媒体文件出入口与图片处理：picker 与安全控件、沙箱导出、播放 URI、解码预取、PixelMap 释放与快照限制

[上一级](../index.md)

## 本级经验

- [PixelMap 定唯一所有者，成品覆盖变量只释放一次](lesson-d0769280aaee71a03ad1.lesson.md) · 阶段：execute · 信号：Bitmap.recycle, recycle(), PixelMap, PixelMap.release
- [SaveButton 底色圆角设在控件自身，不靠外层容器画](lesson-e1211056a34f58403e3a.lesson.md) · 阶段：execute · 信号：SaveButton, Color.Transparent, backgroundColor, borderRadius
- [SaveButton 授权回调只做快速写入，下载放点击前](lesson-089bb378b1ec034a3e84.lesson.md) · 阶段：execute · 信号：SaveButton, SaveButtonOnClickResult, photoAccessHelper, onClick
- [公共目录产物改落沙箱时每条链写出导出步骤](lesson-b59097ee968fe827f70d.lesson.md) · 阶段：spec/execute · 信号：WRITE_EXTERNAL_STORAGE, ACTION_MEDIA_SCANNER_SCAN_FILE, DocumentViewPicker.save, MediaScannerConnection
- [图库选图用 PhotoViewPicker 并复制进应用目录](lesson-ad1db0aa0434c2e766fd.lesson.md) · 阶段：spec/execute · 信号：PhotoViewPicker, READ_IMAGEVIDEO, MediaStore, photo_manager
- [导入导出按源运行时语义：OOM 兜底与 DEFLATED](lesson-8534b92df38e546092fe.lesson.md) · 阶段：spec/execute · 信号：OutOfMemoryError, RangeError, ZipOutputStream, setMethod
- [本地路径接 Video src 前转为 file:// 地址](lesson-2b3d45c1a89dc1ead7e3.lesson.md) · 阶段：execute · 信号：Video, file://, fileUri.getUriFromPath, setUrl
- [源端主动预取后续图片时用图片解码真实预取并限缓存](lesson-cde53c6eab199d1262b2.lesson.md) · 阶段：execute · 信号：image.createImageSource, createPixelMap, PixelMap.release, imageLoader.enqueue
- [长内容存图先查快照尺寸限制，超一屏分段渲染拼接](lesson-e0f3b5b744e6b0518814.lesson.md) · 阶段：execute · 信号：componentSnapshot.createFromBuilder, SnapshotOptions, readPixels, writePixels
- [降采样改 desiredSize，方向按字符串映射](lesson-c61656e804e536885d20.lesson.md) · 阶段：execute · 信号：inSampleSize, BitmapFactory.Options, TAG_ORIENTATION, DecodingOptions
- [音频导入用 AudioViewPicker 并复制进沙箱](lesson-62ac5e65ac4aa51128bd.lesson.md) · 阶段：spec/execute/repair · 信号：AudioViewPicker, photoAccessHelper, MediaStore.Audio, READ_MEDIA_AUDIO
