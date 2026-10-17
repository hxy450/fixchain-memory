# 源端位图按密度解码、createScaledBitmap 预缩放后原尺寸绘制时，目标在 PixelMap 上按同一采样预缩放

ID：`lesson-c3bd9c8b2f24c209a659` · 版本：2 · 阶段：spec/execute · 主题：[ui/graphics/drawing](index.md)

概要：预缩放位图在 PixelMap 上按同一采样缩放

信号：`BitmapFactory.decodeResource`, `createScaledBitmap`, `drawBitmap`, `drawImage`, `imageSmoothingEnabled`, `PixelMap`, `scaleSync`, `AntiAliasingLevel.NONE`, `desiredSize`, `drawable-ldpi`, `densityPixels`

## 何时使用

规格提取阶段把源端位图的解码、预缩放与绘制方式写成画布绘制契约时；渲染实现阶段按契约装载并绘制这些位图时

## 适用情境

源端自绘 View 用 BitmapFactory.decodeResource 解码只放在单一密度目录（如 drawable-ldpi）的位图，再用 Bitmap.createScaledBitmap(raw, w, h, filter) 缩到运行时算出的尺寸，onDraw 里 drawBitmap(bmp, x, y, paint) 按原尺寸绘制；目标在 ArkUI Canvas 上用 drawImage 移植。

## 原因

源端管线有三步，每步都影响像素：decodeResource 按 设备dpi/目录dpi 放大只放在低密度目录里的资源；createScaledBitmap 的 filter=false 为最近邻、true 为双线性（本机 android-36.1 源码 Bitmap.createScaledBitmap 注释）；之后按原尺寸绘制，不再缩放。改成原图解码一次、每帧 drawImage 指定宽高，缩放挪到绘制期，ArkUI CanvasRenderingContext2D 的 imageSmoothingEnabled 默认 true（本机 HarmonyOS 6.1.0 SDK component/canvas.d.ts），边缘从阶梯锯齿变成柔边；位图尺寸依赖运行时几何时，进程级一次性缓存还会让后续实例沿用旧尺寸。

## 做法

1. 规格把每一步写成契约：解码是否按资源所在密度目录与设备密度缩放，预缩放的目标尺寸与 filter 标志，onDraw 是否按原尺寸绘制；不把 filter=false 写成“普通缩放”，也不把预缩放改写成 drawImage 带目标宽高的绘制期缩放。
2. 实现时在 PixelMap 上预缩放：先用 image.DecodingOptions.desiredSize 完成密度解码，尺寸按 Android 取整 (int)(px×设备dpi/目录dpi+0.5)（设备 dpi 取 display.getDefaultDisplaySync().densityPixels×160；目录 dpi 按 res/drawable-<桶> 名，ldpi 120、mdpi 160、hdpi 240、xhdpi 320、xxhdpi 480；资源像素读源 PNG），再用 PixelMap.scaleSync(sx, sy, level) 缩到目标尺寸：filter=false 用 image.AntiAliasingLevel.NONE（最近邻），true 用 LOW（双线性）（本地 SDK ets/api/@ohos.multimedia.image.d.ts，@since 12）；drawImage 不传目标宽高，1:1 绘制。
3. 预缩放尺寸依赖运行时几何（如由屏宽算出的格径）时，放在几何计算之后，按源端调用时机（每次构造视图实例）重做，不用进程级一次性守护缓存已缩放的位图。

## 可选检查

- 对锯齿是否一致有疑问时，两端各截同一颗图元，最近邻放大后并排看边缘：最近邻缩小呈阶梯锯齿，平滑插值是柔边。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-e00d2f72aa6dfc37826b](../../../../../store/cases/case-e00d2f72aa6dfc37826b/0526d27c110adaac3bc4a052e4357dc6fa30b1deeb0b9f4aa725056916604041.json) · 结论：diagnosis, rec-da06731845, rec-60fe8acb94, rec-c3033be492, rec-404ad822b5
  卡片版本：`0526d27c110adaac3bc4a052e4357dc6fa30b1deeb0b9f4aa725056916604041`
