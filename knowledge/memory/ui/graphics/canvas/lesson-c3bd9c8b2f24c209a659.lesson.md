# 源端位图按密度解码、createScaledBitmap 预缩放后原尺寸绘制时，目标在 PixelMap 上按同一采样预缩放

ID：`lesson-c3bd9c8b2f24c209a659` · 版本：1

> 带知识的试验版（未并入 store）：正文按 `knowledge/lessons/lesson-c3bd9c8b2f24c209a659.json` 改了 1 句，后面接了 16 条已核实的平台事实。原文、来源和证据卡见 [memory/ui/graphics/canvas/lesson-c3bd9c8b2f24c209a659.lesson.md](../../../../../memory/ui/graphics/canvas/lesson-c3bd9c8b2f24c209a659.lesson.md)。

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

## 已核实的平台事实

核实时用的是 HarmonyOS 6.1.0（API 23，openharmony ets 6.1.0.105；文档副本含到 API 26 的内容，超出 SDK 的已注明）；安卓 平台资源 android-34；框架源码 android-36.1；androidx Compose 1.10.3（foundation、ui、ui-unit、ui-graphics，按字节码核）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看；每条下面的「写法」是在 SDK 声明里核过的导入语句、归属、签名和枚举成员，写代码时直接照抄。

- 〔原因〕decodeResource → decodeResourceStream：Options 没另设 inDensity/inTargetDensity 时，inDensity 取资源所在目录的密度（无限定目录为 160），inTargetDensity 取 res.getDisplayMetrics().densityDpi；inScaled 默认 true，结果按 设备dpi/目录dpi 缩放（出处：android.graphics.BitmapFactory#decodeResourceStream；android.graphics.BitmapFactory.Options#inScaled）
- 〔原因〕Bitmap.createScaledBitmap(src, w, h, filter)：filter=true 用双线性，false 用最近邻（内部 Matrix + createBitmap(…, filter)）（出处：android.graphics.Bitmap#createScaledBitmap）
- 〔原因〕CanvasRenderer.imageSmoothingEnabled: boolean 默认 true（绘制期缩放走平滑插值），imageSmoothingQuality 默认 'low'（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderer.imageSmoothingEnabled、CanvasRenderer.imageSmoothingQuality）
  写法：全局可用，不用导入（CanvasRenderingContext2D 实例属性）：this.context.imageSmoothingEnabled = false
        this.context.imageSmoothingQuality: ImageSmoothingQuality，取值 'low' | 'medium' | 'high'
- 〔做法第 2 步〕安卓目录 dpi：ldpi 120、mdpi 160、hdpi 240、xhdpi 320、xxhdpi 480、xxxhdpi 640（出处：android.util.DisplayMetrics#DENSITY_LOW 等常量）
- 〔做法第 2 步〕Display.densityPixels（物理像素与逻辑像素的缩放系数，低分屏为 1.0）、Display.densityDPI（每英寸像素，@since 12），由 display.getDefaultDisplaySync() 取得（出处：鸿蒙 SDK 的 ets/api/@ohos.display.d.ts，Display.densityPixels、Display.densityDPI、display.getDefaultDisplaySync）
  写法：import { display } from '@kit.ArkUI'
        const d: display.Display = display.getDefaultDisplaySync()  // d.densityPixels、d.densityDPI；d.width、d.height 为 px
- 〔做法第 2 步〕源 PNG 字节：resourceManager.getMediaContentSync(resId: number, density?: number): Uint8Array（density 0 或缺省按当前系统 dpi 选目录）；image.createImageSource(buf: ArrayBuffer): ImageSource（@since 12）（出处：鸿蒙 SDK 的 ets/api/@ohos.resourceManager.d.ts，ResourceManager.getMediaContentSync；ets/api/@ohos.multimedia.image.d.ts，image.createImageSource）
  写法：import { image } from '@kit.ImageKit'
        const ctx = this.getUIContext().getHostContext()  // Context | undefined，先判空
        const bytes: Uint8Array = ctx!.resourceManager.getMediaContentSync($r('app.media.x').id)
        const src: image.ImageSource = image.createImageSource(bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength))
- 〔做法第 2 步〕DecodingOptions.desiredSize?: Size（{ width, height }，@since 12），(0, 0) 表示按原图尺寸解码；ImageSource.createPixelMapSync(options?) 同步解码，失败返回 undefined（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，DecodingOptions.desiredSize、ImageSource.createPixelMapSync）
  写法：const pm: image.PixelMap = src.createPixelMapSync({ desiredSize: { width: w, height: h } })
        // 参数类型 image.DecodingOptions；image.Size { width: number; height: number }
- 〔做法第 2 步〕PixelMap.scaleSync(x: number, y: number, level: AntiAliasingLevel): void（@since 12），x、y 是宽、高的缩放倍数，原地缩放；createScaledPixelMapSync(x, y, level?) 返回新 PixelMap（@since 18）（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，PixelMap.scaleSync、PixelMap.createScaledPixelMapSync）
  写法：pm.scaleSync(sx, sy, image.AntiAliasingLevel.NONE)  // 原地缩放
        const info: image.ImageInfo = pm.getImageInfoSync()  // info.size.width / info.size.height，API 12
- 〔做法第 2 步〕image.AntiAliasingLevel：NONE = 0 最近邻、LOW = 1 双线性、MEDIUM = 2 双线性加 mipmap、HIGH = 3 三次插值（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，image.AntiAliasingLevel）
  写法：import { image } from '@kit.ImageKit'
        image.AntiAliasingLevel.NONE / LOW / MEDIUM / HIGH
- 〔做法第 2 步〕drawImage(image: ImageBitmap | PixelMap, dx, dy) 不带宽高；带 dw/dh 的重载把图拉伸或压缩到绘制区；dx、dy、dw、dh 默认单位 vp（上下文默认 LengthMetricsUnit.DEFAULT，可构造时传 PX）（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderer.drawImage、CanvasRenderingContext2D.constructor；文档 ts-canvasrenderingcontext2d.md，drawImage）
  写法：全局可用，不用导入：new CanvasRenderingContext2D(settings?: RenderingContextSettings, unit?: LengthMetricsUnit)；new RenderingContextSettings(antialias?: boolean)
        import { LengthMetricsUnit } from '@kit.ArkUI'  // 成员 DEFAULT = 0、PX = 1
        Canvas(this.context).onReady(() => { this.context.drawImage(pm, x, y) })
- 〔做法第 2 步〕设备上 PixelMap.scaleSync(…, AntiAliasingLevel.NONE) 缩小后边缘呈最近邻的阶梯锯齿；imageSmoothingEnabled 为默认 true 时，drawImage 带目标宽高的绘制期缩放是平滑柔边（出处：卡里上机实测）
  写法：pm.scaleSync(sx, sy, image.AntiAliasingLevel.NONE)
        this.context.drawImage(pm, dx, dy, dw, dh)  // 带目标宽高的重载
- 〔适用情境〕decodeResource 的密度缩放有成立条件：资源在无限定的 drawable 目录时目录密度按 160；在 drawable-nodpi（TypedValue.DENSITY_NONE）时 inDensity 不设、不做密度缩放，按资源原像素解码；调用方自己设了 Options.inDensity / inTargetDensity，或 inScaled = false 时以调用方为准；缩放后位图的 density 记为 inTargetDensity（设备 dpi）。Options 没另设时 inPreferredConfig 为 ARGB_8888、inMutable 为 false（出处：android.graphics.BitmapFactory#decodeResourceStream、#setDensityFromOptions；android.graphics.BitmapFactory.Options#inPreferredConfig、#inMutable、#inScaled）
- 〔原因〕Canvas.drawBitmap(bitmap, left, top, paint) 在位图与画布 density 不同时会自动换算缩放；软件绘制路径里 ViewRootImpl 把画布 density 设成设备 dpi，而按密度解码出的位图 density 也是设备 dpi，所以 onDraw 里按位图像素 1:1 绘制。硬件加速画布把画布与位图的 density 交给原生代码处理，本机没有原生源码（出处：android.graphics.Canvas#drawBitmap；android.view.ViewRootImpl#drawSoftware；android.graphics.BaseRecordingCanvas#drawBitmap）
- 〔做法第 2 步〕image.DecodingOptions 的全部字段与缺省值：index 0（第几帧）、sampleSize 1（当前只能取 1）、rotate 0（度）、editable false（不可编辑时 writePixels 等二次编辑会失败）、desiredSize 缺省为原始尺寸（比例不一致时拉伸到指定尺寸）、desiredRegion 缺省整图、desiredPixelFormat 缺省 RGBA_8888（只可设 RGBA_8888、BGRA_8888、RGB_565，带透明通道的图不支持 RGB_565）、fitDensity（API 9，单位 ppi，缺省 0）、desiredColorSpace（API 11）、desiredDynamicRange（API 12，缺省 SDR）、cropAndScaleStrategy（API 18，同时给 desiredRegion 与 desiredSize 时决定先裁还是先缩，推荐 CROP_FIRST）（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，DecodingOptions.index、DecodingOptions.sampleSize、DecodingOptions.rotate、DecodingOptions.editable、DecodingOptions.desiredRegion、DecodingOptions.desiredPixelFormat、DecodingOptions.fitDensity、DecodingOptions.desiredColorSpace、DecodingOptions.desiredDynamicRange、DecodingOptions.cropAndScaleStrategy；文档 arkts-apis-image-i.md，DecodingOptions）
  写法：import { image } from '@kit.ImageKit'
        interface DecodingOptions { index?: number; sampleSize?: number; rotate?: number; editable?: boolean; desiredSize?: Size; desiredRegion?: Region; desiredPixelFormat?: PixelMapFormat; fitDensity?: number; desiredColorSpace?: colorSpaceManager.ColorSpaceManager; desiredDynamicRange?: DecodingDynamicRange; cropAndScaleStrategy?: CropAndScaleStrategy }
        const opts: image.DecodingOptions = { desiredSize: { width: w, height: h }, desiredPixelFormat: image.PixelMapFormat.RGBA_8888, editable: true }
- 〔做法第 2 步〕解码与缩放的异步、同步对应版本：ImageSource.createPixelMap(options?) 返回 Promise<PixelMap>，createPixelMapSync(options?) 同步；PixelMap.scale(x, y, level) 返回 Promise<void>、scaleSync(x, y, level) 同步（都是 API 12，原地缩放）；不带 level 的 scale(x, y) / scaleSync(x, y) 分别是 API 9 / 12；createScaledPixelMap(x, y, level?) 与 createScaledPixelMapSync 是 API 18，返回不可编辑的新 PixelMap；缩放倍数 = 缩放后宽高 / 缩放前宽高，取负数会翻转；用完调 release(): Promise<void>（PixelMap、ImageSource 都有）。文档里的 applyScale / applyScaleSync 是 26.0.0 起的，API 23 SDK 没有（出处：鸿蒙 SDK 的 ets/api/@ohos.multimedia.image.d.ts，ImageSource.createPixelMap、ImageSource.createPixelMapSync、PixelMap.scale、PixelMap.scaleSync、PixelMap.createScaledPixelMap、PixelMap.release；文档 arkts-apis-image-PixelMap.md，scale、createScaledPixelMap、applyScaleSync）
  写法：import { image } from '@kit.ImageKit'
        const pm: image.PixelMap = await src.createPixelMap({ desiredSize: { width: w, height: h } })  // Promise<PixelMap>
        await pm.scale(sx, sy, image.AntiAliasingLevel.NONE)  // scale(x: number, y: number, level: AntiAliasingLevel): Promise<void>
        const out: image.PixelMap = await pm.createScaledPixelMap(sx, sy, image.AntiAliasingLevel.LOW)  // API 18，不可编辑
        await src.release()；await pm.release()
- 〔做法第 2 步〕drawImage 有三个重载：(image, dx, dy) 原尺寸绘制；(image, dx, dy, dw, dh) 缩放到目标区；(image, sx, sy, sw, sh, dx, dy, dw, dh) 先取源矩形再缩放；image 可为 ImageBitmap 或 PixelMap（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderer.drawImage；文档 ts-canvasrenderingcontext2d.md，drawImage）
  写法：全局可用，不用导入（CanvasRenderingContext2D 继承 CanvasRenderer）
        drawImage(image: ImageBitmap | PixelMap, dx: number, dy: number): void
        drawImage(image: ImageBitmap | PixelMap, dx: number, dy: number, dw: number, dh: number): void
        drawImage(image: ImageBitmap | PixelMap, sx: number, sy: number, sw: number, sh: number, dx: number, dy: number, dw: number, dh: number): void
