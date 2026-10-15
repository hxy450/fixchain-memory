# 源端位图按密度解码、createScaledBitmap 预缩放后原尺寸绘制时，目标在 PixelMap 上按同样采样预缩放，不在 drawImage 时缩放

ID：`lesson-ad2107690c0cdb9fd4fc` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段把源端位图的解码、预缩放与绘制方式写成目标画布契约时；渲染实现阶段装载并绘制这些位图时

## 适用情境

源端自绘视图用 BitmapFactory.decodeResource 解码（资源只放在某个密度目录时按 设备dpi/目录dpi 缩放并带滤波），再用 Bitmap.createScaledBitmap(src, w, h, filter) 缩到由运行时几何决定的尺寸，onDraw 以 drawBitmap 按位图原尺寸绘制；目标准备在 ArkUI Canvas 的 drawImage 里传 dw/dh 做绘制期缩放。

## 原因

createScaledBitmap 的 filter=false 是最近邻采样，true 是双线性；ArkUI CanvasRenderingContext2D 的 imageSmoothingEnabled 默认为 true（本地 SDK canvas.d.ts），绘制期缩放一律平滑插值，边缘从阶梯变柔。省掉按密度解码这一步，缩放的起点尺寸和取整也随之改变。

## 做法

1. 规格把每一步写成契约：解码是否按资源密度目录与设备密度缩放、预缩放的目标尺寸与 filter 标志、绘制是否按原尺寸；不把 filter=false 写成“普通缩放”。
2. 实现时在 PixelMap 上完成：image.DecodingOptions.desiredSize 做密度解码（尺寸按 Android 取整 (int)(px×设备dpi/目录dpi+0.5)），再用 PixelMap.scaleSync(sx, sy, level) 缩到目标尺寸，filter=false 用 image.AntiAliasingLevel.NONE、true 用 LOW；drawImage 不传 dw/dh。取值：设备 dpi = display.getDefaultDisplaySync().densityPixels×160，目录 dpi 看源工程 res/drawable-<桶> 的目录名，像素读源 PNG 的实际尺寸。
3. 预缩放尺寸依赖运行时几何（如由屏宽算出的格径）时，放在几何计算之后，并按源端的调用时机（每次构造视图实例）重做，不用进程级的一次性缓存。

## 可选检查

- 对采样有疑问时，两端各截同一位图，最近邻放大后并排比较边缘：最近邻缩小呈阶梯，平滑插值为柔边。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-e00d2f72aa6dfc37826b](../../../../store/cases/case-e00d2f72aa6dfc37826b/0526d27c110adaac3bc4a052e4357dc6fa30b1deeb0b9f4aa725056916604041.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`0526d27c110adaac3bc4a052e4357dc6fa30b1deeb0b9f4aa725056916604041`
