# 按 Android px 公式移植自绘 View 时先定画布上下文单位：用 LengthMetricsUnit.PX 构造，让字号、测宽、几何与触点同域，dp 常量与 vp 输入在边界换算

## 何时使用

规格提取与渲染实现阶段，创建 CanvasRenderingContext2D，并为字体串、measureText、几何公式、触点坐标、窗口避让值和 dp 常量确定单位域时

## 适用情境

源端是 Android 自定义 View：onSizeChanged 给出 int px 尺寸，Paint.setTextSize/measureText 在 px 域推导字号与派生间距，drawable 圆角等常量以 dp 声明，位图资源的固有尺寸（getIntrinsicWidth/Height）也作为 px 量进入格宽、边界等公式；目标用 ArkUI Canvas 逐式移植，规格或已有代码对画布单位的表述不一致（字体串写 px、映射写 vp、触点写 px 域）。

## 原因

CanvasRenderingContext2D 默认按 vp 解释坐标与尺寸参数（字号按字体串里写明的 px 或 vp 后缀解释，未设 font 时默认 14px），要在 px 域运算须在构造时传入 LengthMetricsUnit.PX。单位没定下来时，各写者按各自理解混用：px 字号被当成 vp 放大、measureText 结果偏小、已 vp2px 的触点与 vp 几何比较而点不中。多数写法一致不能代替对构造签名的核对。 源字号若是 sp，还含系统字体缩放，只乘密度或写固定 px 都会偏；三参数 drawImage 按图片像素数以物理像素绘制，与按 vp 写的矩阵混用时图像按密度缩小。

## 做法

1. 按源端运算域选择构造：源公式在 int px 上推导时用 new CanvasRenderingContext2D(settings, LengthMetricsUnit.PX)，再逐式移植布局函数；保留默认 vp 时，整套公式都按 vp 推导，不混用。
2. 选定域后逐项换算跨域输入：字体串后缀与上下文单位一致；TouchObject.x/y 等 vp 量、窗口避让值（getWindowAvoidArea 等窗口接口给的是 px，经 px2vp 写入窗口模型后才是 vp）按域决定是否换算；来自 drawable 或 dimens 的 dp 常量（圆角、描边）在 px 域用 uiContext.vp2px 换算。位图固有尺寸（Drawable.getIntrinsicWidth/Height）是从资源所在密度目录缩放到设备密度后的 px，不是解码像素：目标只保留某一密度目录的位图时，按 Android Bitmap.scaleFromDensity 的整数式 (px×设备dpi + 目录dpi/2) / 目录dpi 换算后再进公式（设备 dpi = vp2px(160)；目录 dpi：mdpi 160、hdpi 240、xhdpi 320、xxhdpi 480、xxxhdpi 640）。源端位图放在不带密度限定的 drawable 目录时，目录 dpi 按 160 算；放在 drawable-nodpi 时不缩放，固有尺寸就是解码像素，不套这个换算式。
3. 字号与位图绘制尺寸同样按域换算：字体串的 px 后缀按物理像素解释（默认 vp 上下文中也是如此，固定写 'Npx' 会随密度变小）；源字号是 sp（N×scaledDensity）时还含系统字体缩放，用 fp2px(N) 得到物理像素再以 px 后缀写入，不只乘密度（fp2px 只有在应用 configuration 的 fontSizeScale 配为 followSystem 时才随系统字体设置变，缺省的 nonFollowSystem 不跟随），并保留源 Typeface 的粗细。三参数 drawImage(pm, x, y) 按 PixelMap 像素数以物理像素绘制；与按 vp 计算的变换矩阵或目标矩形同用时，改用五参数 drawImage(pm, x, y, w, h)，w、h 取与矩阵源矩形同一组数值（如都取 getImageInfoSync().size）。
4. 规格提取时只写一份画布单位契约：上下文构造参数，以及字体串（含 sp 字号的换算）、measureText、ctx.width、触点、避让值、dp 常量、位图固有尺寸（连同其来源密度目录）和 drawImage 绘制尺寸各自的单位，各 feature 映射引用同一表述。

## 可选检查

- 单位仍有疑问时，在目标设备打印一次 ctx.width 与组件尺寸、同字号的 measureText 结果，对照源端 px 值确认所在域。

来源支持：3 张卡 · 已知 2 次迁移（部分未记录） · 已知 2 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-37.0 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕CanvasRenderingContext2D 从 API 12 起可在构造时传 unit：LengthMetricsUnit.DEFAULT（vp）或 LengthMetricsUnit.PX；不传或只传 settings 时按 DEFAULT 即 vp，单位模式构造后不能再改
- 〔原因 / 做法第 4 步〕CanvasRenderingContext2D 的 width、height 是只读的组件宽高，默认单位 vp
- 〔原因 / 做法第 3 步〕画布的 font 串语法是 'font-style font-weight font-size font-family'，font-size 单位支持 px、vp，必须写单位；没设 font 时为 'normal normal 14px sans-serif'；font、fillStyle 等是只写属性，读取返回 undefined
- 〔做法第 3 步〕ArkUI 像素单位：px 是屏幕物理像素；vp 与 px 的比例取决于屏幕像素密度，数值不带单位时默认 vp；fp 与 vp 类似，另外随系统字体大小设置变化
- 〔做法第 3 步〕应用 app.json5 的 configuration 里 fontSizeScale 取 followSystem 时应用字号跟随系统，取 nonFollowSystem 时不跟随；不写时为 nonFollowSystem
- 〔适用情境 / 做法第 3 步〕安卓 Paint.setTextSize 的参数按像素解释；DisplayMetrics.scaledDensity 和 density 相同，但会按用户的字体大小偏好调整，所以 N × scaledDensity 是含系统字体缩放的像素值
- 〔原因〕上下文保持默认 vp 时，font 串里写的 px 字号按物理像素绘制，按 px 域公式推出的字号在 3.5 倍密度设备上 measureText 结果偏小约 3.5 倍
- 〔原因 / 做法第 2 步〕TouchObject 的 x、y 是触点在响应组件坐标系中的坐标，单位 vp
- 〔原因〕已经 vp2px 换成 px 的触点和按 vp 算出的几何比较时，图标点不中
- 〔做法第 2 步〕窗口接口返回的 Rect（如避让区域里的矩形）left、top、width、height 单位都是 px
- 〔做法第 2 步〕安卓 shape drawable 的 corners radius 属性格式是 dimension（带单位的尺寸，通常以 dp 写）
- 〔做法第 2 步〕安卓 BitmapDrawable 的固有宽高取 bitmap.getScaledWidth/Height(目标密度)，即按资源所在密度目录缩放到设备密度后的像素数，不是解码出的原始像素
- 〔做法第 2 步〕安卓 Bitmap.scaleFromDensity(size, sdensity, tdensity) 按整数式 ((size × tdensity) + (sdensity >> 1)) / sdensity 换算，两个密度相同或任一为 DENSITY_NONE 时原样返回
- 〔做法第 2 步〕安卓密度目录对应的 dpi：DENSITY_MEDIUM（mdpi）160、DENSITY_HIGH（hdpi）240、DENSITY_XHIGH（xhdpi）320、DENSITY_XXHIGH（xxhdpi）480、DENSITY_XXXHIGH（xxxhdpi）640
- 〔做法第 3 步〕CanvasRenderer.drawImage 的五参数形式按 dw、dh 缩放到目标矩形绘制；三参数形式 drawImage(image, dx, dy) 不给绘制尺寸
- 〔原因 / 做法第 3 步〕三参数 drawImage(pm, x, y) 按 PixelMap 的像素尺寸以物理像素绘制，在默认 vp 上下文里和按 vp 算的变换矩阵同用时图像按密度缩小、位置错开
