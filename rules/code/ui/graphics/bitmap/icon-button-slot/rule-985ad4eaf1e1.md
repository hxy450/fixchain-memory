# 固定盒加 centerInside 的图标，外层留盒、内层 Image 设固有 dp，不用满盒 Contain

审的是：代码
触发（任一种）：
- 读到：ImageButton / ImageView（含 AppCompatImageButton）写固定 dp 的 layout_width / layout_height 加 android:scaleType="centerInside"，图标只放在 drawable-xhdpi 等密度目录、固有 dp 小于盒子；映射参考写「centerInside → ImageFit.Contain」；写错的样子：Image 自己设成盒子尺寸再写 .objectFit(ImageFit.Contain)，小图标被放大到满盒
适用范围：安卓图标按钮是固定 dp 触摸盒加 scaleType=centerInside、迁成 ArkUI Image 时
做法：
- 查图标资源所在的密度目录，按像素换算固有 dp：px ÷ 密度因子（xhdpi 为 2）
- 外层容器（如 Row）保留源触摸盒的宽高并让内容居中，内层 Image 的 width / height 设成固有 dp
- 图标固有尺寸大于盒子时才等比缩到盒内；小于盒子时按固有尺寸显示，不放大
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- CENTER_INSIDE：图片宽高都不超过 View 时 scale = 1.0f，否则 scale = min(vwidth/dwidth, vheight/dheight)，再居中：centerInside 只缩不放（出处：android.widget.ImageView#configureBounds；android.widget.ImageView.ScaleType#CENTER_INSIDE）
- ImageFit.Contain：保持宽高比缩小或放大，使图片完整显示在边界内：Contain 会把小图放大到盒子，和 centerInside 不同（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，ImageFit.Contain）
- objectFit(value: ImageFit): ImageAttribute，默认 ImageFit.Cover：Image 的缩放方式（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.objectFit）
- DENSITY_MEDIUM = 160、DENSITY_HIGH = 240、DENSITY_XHIGH = 320、DENSITY_XXHIGH = 480、DENSITY_XXXHIGH = 640：mdpi/hdpi/xhdpi/xxhdpi/xxxhdpi 对 160 的倍数 1、1.5、2、3、4 就是 px 换 dp 的除数（出处：android.util.DisplayMetrics 的 DENSITY_MEDIUM、DENSITY_XHIGH 等常量）
- 保留源触摸盒尺寸的 Row，内部 Image 按 drawable-xhdpi 像素 / 2 设固有 dp，真机布局读数与这些值一致：卡里最终保留的写法（出处：卡里修好并验证过）
- objectFit(value: ImageFit): ImageSpanAttribute：同族接口：ImageSpan 的缩放方式（出处：鸿蒙 SDK 的 ets/component/image_span.d.ts，ImageSpanAttribute.objectFit）
- objectFit(value: ImageFit): VideoAttribute：同族接口：Video 的缩放方式（出处：鸿蒙 SDK 的 ets/component/video.d.ts，VideoAttribute.objectFit）
针对本应用要查的：
- 图标的固有 dp：源工程 res 下 drawable-<密度> 目录里这张图（png、webp）的像素宽高；宽、高的 px 分别除以该目录的密度因子（mdpi 1、hdpi 1.5、xhdpi 2、xxhdpi 3、xxxhdpi 4）
未核实：卡里 target_sdk 是 6.1.1(24)，本机声明是 API 23
来源：1 张卡，1 个应用
- case-747484a613e86334516d（免费来电多多）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 2；取值 5 ← 诊断
