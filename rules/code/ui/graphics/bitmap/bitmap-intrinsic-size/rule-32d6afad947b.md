# 源端位图没给尺寸（wrap_content、drawableLeft）时，Image 按像素和密度桶换算写宽高

审的是：代码
触发（任一种）：
- 读到：ImageView / ImageButton 宽高是 wrap_content（可带 android:scaleType），android:src 是密度目录里的位图；写错的样子：Image 只写 .objectFit(...)、没有 .width() / .height()，或宽高写成 16 这类经验值、相邻控件的盒子尺寸
- 读到：TextView / EditText 用 android:drawableLeft / drawableStart 挂位图图标，没给图标尺寸；写错的样子：图标 Image 的 .width / .height 是 14、16 之类经验值或从别的页面照抄的
- 读到：复用已转换页面的 @Builder，模板里的 Image 只有 objectFit；写错的样子：照抄模板，Image 同样没有 .width / .height
适用范围：源端位图（不含矢量图）的显示尺寸由像素和所在密度目录决定、迁成 ArkUI Image 时
做法：
- 在源工程 res/drawable-<密度桶>/ 下读出位图像素宽高，按 vp = px × 160 ÷ 桶 dpi 换算（xhdpi ÷2、xxhdpi ÷3），写成 Image(...).width(<宽>).height(<高>)，宽高各算各的
- objectFit 只对应 scaleType，不代替尺寸：可只写换算出的 .height(...) 配 .objectFit(ImageFit.Contain)；多张位图像素不同时逐张换算，或取统一外框配 Contain
- 同一布局其余 wrap_content 位图逐个照做；复用别页 Builder 时按本页安卓布局核对宽高、scaleType 和 margin
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- DENSITY_MEDIUM = 160（DENSITY_DEFAULT）、DENSITY_HIGH = 240、DENSITY_XHIGH = 320、DENSITY_XXHIGH = 480、DENSITY_XXXHIGH = 640：mdpi / hdpi / xhdpi / xxhdpi / xxxhdpi 各桶的 dpi，1dp 在 160dpi 上等于 1px，dp = px × 160 ÷ dpi（出处：android.util.DisplayMetrics#DENSITY_MEDIUM、DENSITY_XHIGH 等常量与 DisplayMetrics#density 注释）
- mBitmapWidth = bitmap.getScaledWidth(mTargetDensity)：没写尺寸的位图按内禀尺寸显示：像素尺寸从所在桶的密度缩放到屏幕密度，等于固定的 dp 数（出处：android.graphics.drawable.BitmapDrawable#computeBitmapSize）
- Length 为 number（数值不带单位）时默认单位 vp：Image 的 .width(n).height(n) 直接写换算出的数值即可（出处：ts-types.md，Length；ts-pixel-units.md，基本像素单位）
- width(value: Length): T；height(value: Length): T；不设宽时用能完整容纳内容的宽度，超过父容器时画到父容器外：不写宽高就按资源固有像素，可能放大并越出（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.width / CommonMethod.height）
- objectFit(value: ImageFit): ImageAttribute：Image 的缩放方式，只管图片在组件框里怎么放，不给组件定尺寸（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.objectFit）
- ImageFit.Contain：保持宽高比缩放，使图片完整显示在显示边界内（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，ImageFit.Contain）
- 改成按位图像素和密度桶换算的宽高后与源端一致，不再放大、越出，真机布局读数与换算值一致（例：drawable-xhdpi 下 36×40px 是 18×20dp，24×24px 是 12×12dp）：照抄值、经验值、相邻控件的尺寸或没写尺寸改成换算值后修好（出处：卡里修好并验证过）
- 只补 .height(<换算后的 vp>)，保留 Contain，宽度按比例自适应：修好后角标不再显示过大（出处：卡里修好并验证过）
针对本应用要查的：
- 位图的像素宽高和所在密度桶：源工程（含共享资源模块）res 下各 drawable-<密度限定符>/ 目录里与 android:src 或 drawableLeft 引用的 @drawable 名同名的 png / jpg / webp 文件；读图片文件头里的像素宽高，目录名里的 mdpi/hdpi/xhdpi/xxhdpi/xxxhdpi 定 dpi，按 px × 160 ÷ dpi 得 vp；同名文件在几个桶都有时任取一个换算，结果应一致；例：只在 drawable-xhdpi 时除以 2
未核实：case-84754321501fb68838ca 的验证在鸿蒙 SDK API 22 上、case-e7f02c687378e98dc213 和 case-747484a613e86334516d 的目标 SDK 是 HarmonyOS 6.1.1(24)，本机声明按 API 23 核实；ArkUI 在设备上对 base/media 与密度限定词目录里同名位图的实际选取和缩放没有核对
来源：5 张卡，4 个应用
- case-747484a613e86334516d（免费来电多多）：做法第 1 步 ← 建议 3、诊断；取值 7 ← 诊断
- case-84754321501fb68838ca（企业安全培训）：做法第 1 步 ← 建议 1、诊断；取值 7 ← 诊断
- case-ae26f8358584821ce4d4（组件岛Widget Island）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 2、建议 3；取值 8 ← 诊断
- case-bf7423609eeb65569b09（实时公交）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 7 ← 诊断
- case-e7f02c687378e98dc213（免费来电多多）：做法第 1 步 ← 建议 1、诊断；取值 7 ← 诊断
