# 源端位图按密度解码、createScaledBitmap 预缩放后原尺寸绘制时，目标在 PixelMap 上按同一采样预缩放

## 何时使用

规格提取阶段把源端位图的解码、预缩放与绘制方式写成画布绘制契约时；渲染实现阶段按契约装载并绘制这些位图时

## 适用情境

源端自绘 View 用 BitmapFactory.decodeResource 解码只放在单一密度目录（如 drawable-ldpi）的位图，再用 Bitmap.createScaledBitmap(raw, w, h, filter) 缩到运行时算出的尺寸，onDraw 里 drawBitmap(bmp, x, y, paint) 按原尺寸绘制；目标在 ArkUI Canvas 上用 drawImage 移植。

## 原因

源端管线有三步，每步都影响像素：decodeResource 按 设备dpi/目录dpi 放大只放在低密度目录里的资源；createScaledBitmap 的 filter=false 为最近邻、true 为双线性（本机 android-36.1 源码 Bitmap.createScaledBitmap 注释）；之后按原尺寸绘制，不再缩放。改成原图解码一次、每帧 drawImage 指定宽高，缩放挪到绘制期，ArkUI CanvasRenderingContext2D 的 imageSmoothingEnabled 默认 true（本机 HarmonyOS 6.1.0 SDK component/canvas.d.ts），边缘从阶梯锯齿变成柔边；位图尺寸依赖运行时几何时，进程级一次性缓存还会让后续实例沿用旧尺寸。

## 做法

1. 规格把每一步写成契约：解码是否按资源所在密度目录与设备密度缩放，预缩放的目标尺寸与 filter 标志，onDraw 是否按原尺寸绘制；不把 filter=false 写成“普通缩放”，也不把预缩放改写成 drawImage 带目标宽高的绘制期缩放。
2. 实现时在 PixelMap 上预缩放：先用 image.DecodingOptions.desiredSize 完成密度解码，尺寸按 Android 取整 (int)(px×设备dpi/目录dpi+0.5)（设备 dpi 取 display.getDefaultDisplaySync().densityPixels×160；目录 dpi 按 res/drawable-<桶> 名，ldpi 120、mdpi 160、hdpi 240、xhdpi 320、xxhdpi 480、xxxhdpi 640、tvdpi 213（无限定的 drawable 按 160；drawable-nodpi 不做密度缩放，按原像素解码；源端自设 Options.inDensity/inTargetDensity 或 inScaled=false 时以源端为准）；资源像素读源 PNG），再用 PixelMap.scaleSync(sx, sy, level) 缩到目标尺寸：filter=false 用 image.AntiAliasingLevel.NONE（最近邻），true 用 LOW（双线性）（本地 SDK ets/api/@ohos.multimedia.image.d.ts，@since 12）；drawImage 不传目标宽高，1:1 绘制。
3. 预缩放尺寸依赖运行时几何（如由屏宽算出的格径）时，放在几何计算之后，按源端调用时机（每次构造视图实例）重做，不用进程级一次性守护缓存已缩放的位图。

## 可选检查

- 对锯齿是否一致有疑问时，两端各截同一颗图元，最近邻放大后并排看边缘：最近邻缩小呈阶梯锯齿，平滑插值是柔边。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码；AOSP android-16.0.0_r1 的 BitmapFactory.cpp、android_graphics_Canvas.cpp。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1、2 步〕BitmapFactory.decodeResource 在应用没有另设 Options.inDensity、inTargetDensity 时：inDensity 取资源所在目录的密度（无限定目录按 DENSITY_DEFAULT 160；drawable-nodpi 的资源密度为 DENSITY_NONE，不设 inDensity、不做密度缩放），inTargetDensity 取设备的 densityDpi
- 〔原因 / 做法第 2 步〕应用没有另设 Options.inScaled 时它为 true；inScaled 为 true、inDensity 与 inTargetDensity 都不为 0 且 inDensity 不等于 inScreenDensity 时，解码结果按 inTargetDensity/inDensity 缩放，宽高取 (int)(原宽高÷inSampleSize×比例+0.5)（没设 inSampleSize 时按 1），缩放用双线性采样，解出的位图密度记为 inTargetDensity
- 〔做法第 2 步〕DisplayMetrics 里与资源密度目录同名的密度常量：DENSITY_LOW 120（ldpi）、DENSITY_MEDIUM 160（mdpi，也是 DENSITY_DEFAULT）、DENSITY_TV 213（tvdpi）、DENSITY_HIGH 240（hdpi）、DENSITY_XHIGH 320（xhdpi）、DENSITY_XXHIGH 480（xxhdpi）、DENSITY_XXXHIGH 640（xxxhdpi）；另有 DENSITY_140、180、200、220、260、280、300、340、360、390、400、420、440、450、520、560、600 等设备密度值，资源目录名里没有对应的桶
- 〔原因 / 做法第 1、2 步〕Bitmap.createScaledBitmap(src, dstWidth, dstHeight, filter)：filter 为 true 用双线性，为 false 用最近邻；javadoc 写目标宽高与源位图相同时直接返回源位图，源码里只在源位图不可变时才返回源对象，可变位图仍复制一份；新位图沿用源位图的密度
- 〔原因 / 做法第 1 步〕Canvas.drawBitmap(bitmap, left, top, paint) 不带目标矩形，按位图本身尺寸绘制；位图与画布密度都不为 0 且不同时按 画布密度/位图密度 缩放（双线性）；任一为 0 时不缩放：硬件加速的 View 画布（RecordingCanvas）密度为 0，软件绘制时 ViewRootImpl 把画布密度设为屏幕 densityDpi，decodeResource 解出的位图密度也已是设备 densityDpi，所以 onDraw 里画这类位图按像素 1:1
- 〔做法第 2 步〕image.DecodingOptions.desiredSize 是期望输出尺寸，须为正整数，与原图比例不同时拉伸或缩放到该尺寸；不设时按原始尺寸，(0, 0) 也表示按原图尺寸解码
- 〔做法第 2 步〕PixelMap.scaleSync 有 scaleSync(x, y) 与 scaleSync(x, y, level) 两种重载，都自 API 12 起；x、y 是宽高缩放倍数（缩放后宽高 / 缩放前宽高），不能为 0；带 level 的重载按给定的 AntiAliasingLevel 插值，level 对 ASTC 格式的 PixelMap 不生效；文档另写 API 26 起建议改用 applyScaleSync（超出本机 SDK 的 API 23，本机声明里没有）
- 〔做法第 2 步〕image.AntiAliasingLevel（API 12 起）：NONE = 0 最近邻插值，LOW = 1 双线性插值，MEDIUM = 2 双线性插值并开启 Mipmap，HIGH = 3 三次卷积插值
- 〔做法第 2 步〕PixelMap.createScaledPixelMapSync(x, y, level?)（API 18 起）按倍数缩放并返回一个新的、不可编辑的 PixelMap；不传 level 时按 AntiAliasingLevel.NONE
- 〔做法第 2 步〕Display.densityDPI 是屏幕每英寸物理像素数（浮点，如 160.0、480.0）；Display.densityPixels 是物理像素与逻辑像素的缩放系数，取值范围 [0.5, 4.0]，低分辨率屏为 1.0
- 〔原因 / 做法第 1 步〕画布绘制上下文的 imageSmoothingEnabled 在应用没有另设时为 true（绘制图片时做平滑处理），imageSmoothingQuality 默认 low；drawImage 带 dw、dh 时把图像拉伸或压缩到目标宽高绘制
- 〔原因〕按原图解码、每帧用 drawImage 指定目标宽高绘制（imageSmoothingEnabled 未另设）时，设备上图元边缘是平滑插值的柔边；源端 createScaledBitmap(filter=false) 预缩放后 1:1 绘制，边缘是阶梯锯齿
