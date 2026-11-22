# 源端位图按密度解码、createScaledBitmap 预缩放后原尺寸绘制时，目标在 PixelMap 上按同一采样预缩放

## 何时使用

规格提取阶段把源端位图的解码、预缩放与绘制方式写成画布绘制契约时；渲染实现阶段按契约装载并绘制这些位图时

## 适用情境

源端自绘 View 用 BitmapFactory.decodeResource 解码只放在单一密度目录（如 drawable-ldpi）的位图，再用 Bitmap.createScaledBitmap(raw, w, h, filter) 缩到运行时算出的尺寸，onDraw 里 drawBitmap(bmp, x, y, paint) 按原尺寸绘制；目标在 ArkUI Canvas 上用 drawImage 移植。

## 原因

源端管线有三步，每步都影响像素：decodeResource 按 设备dpi/目录dpi 放大只放在低密度目录里的资源；createScaledBitmap 的 filter=false 为最近邻、true 为双线性（本机 android-36.1 源码 Bitmap.createScaledBitmap 注释）；之后按原尺寸绘制，不再缩放。改成原图解码一次、每帧 drawImage 指定宽高，缩放挪到绘制期，ArkUI CanvasRenderingContext2D 的 imageSmoothingEnabled 默认 true（本机 HarmonyOS 6.1.0 SDK component/canvas.d.ts），边缘从阶梯锯齿变成柔边；位图尺寸依赖运行时几何时，进程级一次性缓存还会让后续实例沿用旧尺寸。

## 做法

1. 规格把每一步写成契约：解码是否按资源所在密度目录与设备密度缩放，预缩放的目标尺寸与 filter 标志，onDraw 是否按原尺寸绘制；不把 filter=false 写成“普通缩放”，也不把预缩放改写成 drawImage 带目标宽高的绘制期缩放。
2. 实现时在 PixelMap 上预缩放：先用 image.DecodingOptions.desiredSize 完成密度解码，尺寸按 Android 取整 (int)(px×设备dpi/目录dpi+0.5)（设备 dpi 取 display.getDefaultDisplaySync().densityPixels×160；目录 dpi 按 res/drawable-<桶> 名，ldpi 120、mdpi 160、hdpi 240、xhdpi 320、xxhdpi 480（无限定的 drawable 按 160；drawable-nodpi 不做密度缩放，按原像素解码；源端自设 Options.inDensity/inTargetDensity 或 inScaled=false 时以源端为准）；资源像素读源 PNG），再用 PixelMap.scaleSync(sx, sy, level) 缩到目标尺寸：filter=false 用 image.AntiAliasingLevel.NONE（最近邻），true 用 LOW（双线性）（本地 SDK ets/api/@ohos.multimedia.image.d.ts，@since 12）；drawImage 不传目标宽高，1:1 绘制。
3. 预缩放尺寸依赖运行时几何（如由屏宽算出的格径）时，放在几何计算之后，按源端调用时机（每次构造视图实例）重做，不用进程级一次性守护缓存已缩放的位图。

## 可选检查

- 对锯齿是否一致有疑问时，两端各截同一颗图元，最近邻放大后并排看边缘：最近邻缩小呈阶梯锯齿，平滑插值是柔边。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，openharmony ets 6.1.0.105；文档副本含到 API 26 的内容，超出 SDK 的已注明）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 平台资源 android-34；框架源码 android-36.1；androidx Compose 1.10.3（foundation、ui、ui-unit、ui-graphics，按字节码核）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕decodeResource → decodeResourceStream：Options 没另设 inDensity/inTargetDensity 时，inDensity 取资源所在目录的密度（无限定目录为 160），inTargetDensity 取 res.getDisplayMetrics().densityDpi；inScaled 默认 true，结果按 设备dpi/目录dpi 缩放
- 〔原因〕Bitmap.createScaledBitmap(src, w, h, filter)：filter=true 用双线性，false 用最近邻（内部 Matrix + createBitmap(…, filter)）
- 〔原因〕CanvasRenderer.imageSmoothingEnabled: boolean 默认 true（绘制期缩放走平滑插值），imageSmoothingQuality 默认 'low'
- 〔做法第 2 步〕安卓目录 dpi：ldpi 120、mdpi 160、hdpi 240、xhdpi 320、xxhdpi 480、xxxhdpi 640
- 〔做法第 2 步〕Display.densityPixels（物理像素与逻辑像素的缩放系数，低分屏为 1.0）、Display.densityDPI（每英寸像素，@since 12），由 display.getDefaultDisplaySync() 取得
- 〔做法第 2 步〕源 PNG 字节：resourceManager.getMediaContentSync(resId: number, density?: number): Uint8Array（density 0 或缺省按当前系统 dpi 选目录）；image.createImageSource(buf: ArrayBuffer): ImageSource（@since 12）
- 〔做法第 2 步〕DecodingOptions.desiredSize?: Size（{ width, height }，@since 12），(0, 0) 表示按原图尺寸解码；ImageSource.createPixelMapSync(options?) 同步解码，失败返回 undefined
- 〔做法第 2 步〕PixelMap.scaleSync(x: number, y: number, level: AntiAliasingLevel): void（@since 12），x、y 是宽、高的缩放倍数，原地缩放；createScaledPixelMapSync(x, y, level?) 返回新 PixelMap（@since 18）
- 〔做法第 2 步〕image.AntiAliasingLevel：NONE = 0 最近邻、LOW = 1 双线性、MEDIUM = 2 双线性加 mipmap、HIGH = 3 三次插值
- 〔做法第 2 步〕drawImage(image: ImageBitmap | PixelMap, dx, dy) 不带宽高；带 dw/dh 的重载把图拉伸或压缩到绘制区；dx、dy、dw、dh 默认单位 vp（上下文默认 LengthMetricsUnit.DEFAULT，可构造时传 PX）
- 〔做法第 2 步〕设备上 PixelMap.scaleSync(…, AntiAliasingLevel.NONE) 缩小后边缘呈最近邻的阶梯锯齿；imageSmoothingEnabled 为默认 true 时，drawImage 带目标宽高的绘制期缩放是平滑柔边
