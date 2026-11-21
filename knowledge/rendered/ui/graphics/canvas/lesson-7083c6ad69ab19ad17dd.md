# 按 Android px 公式移植自绘 View 时先定画布上下文单位：用 LengthMetricsUnit.PX 构造，让字号、测宽、几何与触点同域，dp 常量与 vp 输入在边界换算

## 何时使用

规格提取与渲染实现阶段，创建 CanvasRenderingContext2D，并为字体串、measureText、几何公式、触点坐标、窗口避让值和 dp 常量确定单位域时

## 适用情境

源端是 Android 自定义 View：onSizeChanged 给出 int px 尺寸，Paint.setTextSize/measureText 在 px 域推导字号与派生间距，drawable 圆角等常量以 dp 声明，位图资源的固有尺寸（getIntrinsicWidth/Height）也作为 px 量进入格宽、边界等公式；目标用 ArkUI Canvas 逐式移植，规格或已有代码对画布单位的表述不一致（字体串写 px、映射写 vp、触点写 px 域）。

## 原因

CanvasRenderingContext2D 默认按 vp 解释坐标与尺寸参数（字号按字体串里写明的 px 或 vp 后缀解释，未设 font 时默认 14px），要在 px 域运算须在构造时传入 LengthMetricsUnit.PX。单位没定下来时，各写者按各自理解混用：px 字号被当成 vp 放大、measureText 结果偏小、已 vp2px 的触点与 vp 几何比较而点不中。多数写法一致不能代替对构造签名的核对。 源字号若是 sp，还含系统字体缩放，只乘密度或写固定 px 都会偏；三参数 drawImage 按图片像素数以物理像素绘制，与按 vp 写的矩阵混用时图像按密度缩小。

## 做法

1. 按源端运算域选择构造：源公式在 int px 上推导时用 new CanvasRenderingContext2D(settings, LengthMetricsUnit.PX)，再逐式移植布局函数；保留默认 vp 时，整套公式都按 vp 推导，不混用。
2. 选定域后逐项换算跨域输入：字体串后缀与上下文单位一致；TouchObject.x/y 等 vp 量、窗口避让值（getWindowAvoidArea 等窗口接口给的是 px，经 px2vp 写入窗口模型后才是 vp）按域决定是否换算；来自 drawable 或 dimens 的 dp 常量（圆角、描边）在 px 域用 uiContext.vp2px 换算。位图固有尺寸（Drawable.getIntrinsicWidth/Height）是从资源所在密度目录缩放到设备密度后的 px，不是解码像素：目标只保留某一密度目录的位图时，按 Android Bitmap.scaleFromDensity 的整数式 (px×设备dpi + 目录dpi/2) / 目录dpi 换算后再进公式（设备 dpi = vp2px(160)；目录 dpi：mdpi 160、hdpi 240、xhdpi 320、xxhdpi 480、xxxhdpi 640）。
3. 字号与位图绘制尺寸同样按域换算：字体串的 px 后缀按物理像素解释（默认 vp 上下文中也是如此，固定写 'Npx' 会随密度变小）；源字号是 sp（N×scaledDensity）时还含系统字体缩放，用 fp2px(N) 得到物理像素再以 px 后缀写入，不只乘密度（fp2px 只有在应用 configuration 的 fontSizeScale 配为 followSystem 时才随系统字体设置变，缺省的 nonFollowSystem 不跟随），并保留源 Typeface 的粗细。三参数 drawImage(pm, x, y) 按 PixelMap 像素数以物理像素绘制；与按 vp 计算的变换矩阵或目标矩形同用时，改用五参数 drawImage(pm, x, y, w, h)，w、h 取与矩阵源矩形同一组数值（如都取 getImageInfoSync().size）。
4. 规格提取时只写一份画布单位契约：上下文构造参数，以及字体串（含 sp 字号的换算）、measureText、ctx.width、触点、避让值、dp 常量、位图固有尺寸（连同其来源密度目录）和 drawImage 绘制尺寸各自的单位，各 feature 映射引用同一表述。

## 可选检查

- 单位仍有疑问时，在目标设备打印一次 ctx.width 与组件尺寸、同字号的 measureText 结果，对照源端 px 值确认所在域。

来源支持：3 张卡 · 已知 2 次迁移（部分未记录） · 已知 2 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1；Android SDK 平台 android-33、android-34 的 android.jar（对照 TypedValue.deriveDimension 的有无）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕CanvasRenderingContext2D 的单位模式只能在构造时用第二个参数 LengthMetricsUnit 指定、之后不能改；不传或传 undefined、NaN、Infinity 时为 DEFAULT，文档标注「默认单位：vp」的数值参数（坐标、宽高、路径、变换平移、lineWidth、lineDashOffset、shadowOffsetX/Y、只读的 width/height 等）按 vp 解释，传 LengthMetricsUnit.PX 后这些都按 px 解释。〔成立范围：对象：CanvasRenderingContext2D（OffscreenCanvasRenderingContext2D、DrawingRenderingContext 的构造也带 unit 参数，按各自文档）。条件：API 12 起的带 unit 构造。不成立：shadowBlur、miterLimit 文档写的是固定「单位：px」，不随单位模式变；font 的字号按字体串自带的后缀解释，也不随单位模式变（依据是文档说明：字号必须写单位）；Path2D、ImageBitmap、ImageData、OffscreenCanvas 的构造各带自己的 unit 参数（默认 DEFAULT），文档写的是各自配置单位模式，没有写跟随所绘的上下文。〕
- 〔做法第 3 步〕CanvasRenderingContext2D.font 字体串里的字号必须写单位，只支持 px 和 vp 两种后缀（没有 fp）；应用没有设置 font 时默认值是 'normal normal 14px sans-serif'，即 14 个屏幕物理像素。〔成立范围：对象：CanvasRenderingContext2D.font。条件：依据是文档说明（font 小节要求写单位，像素单位文档把 px 定义为屏幕物理像素）。不成立：应用给 font 赋过值后默认值不再适用；源端 sp 字号要跟随系统字体缩放时没有 fp 后缀可写，只能先换成 px 再写入。〕
- 〔做法第 3 步（sp 字号换算）〕Android 把 sp 换成 px（TypedValue.applyDimension；sp 尺寸资源的 getDimension、TextView.setTextSize 都经由它）时，DisplayMetrics.fontScaleConverter 非空就走非线性曲线：系统字体缩放不小于 1.04 时按查表插值，字号越大放大越少（缩放 1.05～1.5 各档里 30sp 及以上不放大）；鸿蒙 UIContext.fp2px 按 fp × 像素密度 × 字体缩放比例线性换算。〔成立范围：对象：源端经 TypedValue 换算的 sp 字号与目标端 fp2px。条件：Android 14（API 34）起的框架实现（API 34 起才有 TypedValue.deriveDimension，DisplayMetrics.scaledDensity 随之标为过时）；鸿蒙应用 configuration 的 fontSizeScale 缺省为 nonFollowSystem，此时应用字体大小不跟随系统设置，fp2px 里的字体缩放比例不随系统字体设置变，配为 followSystem 才跟随，且受 fontSizeMaxScale 上限约束（依据是文档说明）。不成立：源码直接写 N × scaledDensity 的仍是线性，与 fp2px 一致；系统字体缩放低于 1.04 时 Android 也按线性换算。〕
- 〔做法第 3 步（drawImage 绘制尺寸）〕九参数 drawImage(image, sx, sy, sw, sh, dx, dy, dw, dh) 的源矩形 sx/sy/sw/sh：image 是 PixelMap 时，API version 18 之前默认单位是 px，API version 18 起默认单位是 vp；image 是 ImageBitmap 时一直是 vp；dx/dy/dw/dh 默认单位都是 vp。〔成立范围：对象：CanvasRenderingContext2D.drawImage 的九参数形式。条件：「默认单位」随上下文单位模式变，PX 模式下按 px；版本界线按文档写的 API version 18。不成立：三参数、五参数形式没有源矩形参数，不涉及这条差异。〕
- 〔做法第 2 步（位图固有尺寸）〕从 drawable-<密度> 目录加载的位图，BitmapDrawable.getIntrinsicWidth/Height 是按目录密度换算到设备 densityDpi 后四舍五入的 px：目录密度低于设备时（应用 targetSdk 不低于 28）解码保留原像素，由 Bitmap.scaleFromDensity 的整数式 (w × 设备dpi + 目录dpi/2) / 目录dpi 得出；目录密度高于设备时解码阶段就按 (int)(w × 设备dpi / 目录dpi + 0.5f) 缩小。〔成立范围：对象：经 Resources 加载的位图 drawable（Android 9 起的设备由 ImageDecoder 解码；更早的设备由 BitmapFactory 按 inDensity、inTargetDensity 在解码时缩放，inScaled 默认开）。条件：不带密度限定词的 drawable/ 目录按 160 处理；targetSdk 低于 28 时放大也在解码阶段用浮点式完成，结果与整数式只在舍入边界上可能差 1。不成立：drawable-nodpi（密度为 DENSITY_NONE）不做任何缩放，固有尺寸等于位图像素数。〕
- 〔做法第 2 步（触点坐标）〕触摸事件 TouchObject 的 x/y 是以绑定该事件的组件为基准的组件坐标系里的值，windowX/windowY 是相对应用窗口的值，单位都是 vp。〔成立范围：对象：onTouch 回调里的 TouchObject（ClickEvent 的 x/y 同样是 vp、以被点击元素为基准）。条件：依据是文档说明。不成立：onTouch 挂在 Canvas 的父组件上时，x/y 以父组件左上角为原点，不是画布原点。〕
