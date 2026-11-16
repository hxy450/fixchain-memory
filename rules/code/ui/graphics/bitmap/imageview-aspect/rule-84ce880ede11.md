# 未设 adjustViewBounds 的 ImageView 一轴被夹紧时，另一轴仍取缩放后的固有尺寸

审的是：代码
触发（任一种）：
- 读到：布局 XML 里 ImageView 的 layout_width / layout_height 为 wrap_content，没有 android:adjustViewBounds="true"，引用的位图只放在低于设备密度的 drawable-ldpi 这类目录，按密度放大后一轴超过父级；写错的样子：目标里图片框的另一轴按被夹紧的轴等比算，如 .height(列宽 * 位图高 / 位图宽) 或写一个 RATIO 常量
适用范围：安卓 ImageView 为 wrap_content、未设 adjustViewBounds，位图经密度放大后某一轴超过父级给的上限，迁成 ArkUI Image 的框尺寸时
做法：
- 框尺寸分轴取：超限的那一轴取父级给的上限；另一轴取密度缩放后的固有像素 = (位图像素 × 设备 dpi + 目录 dpi / 2) / 目录 dpi（整数除），再加上 padding
- 位图只是按 scaleType（如 centerInside）在框内等比缩小绘制，框本身不等比收缩；这个未收缩的轴就是参与 LinearLayout 量子项、分余量的自然尺寸
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ((size * tdensity) + (sdensity >> 1)) / sdensity：位图从目录密度 sdensity 缩放到设备密度 tdensity 的像素尺寸，四舍五入取整（出处：android.graphics.Bitmap#scaleFromDensity）
- DENSITY_LOW = 120、DENSITY_MEDIUM = 160、DENSITY_HIGH = 240、DENSITY_XHIGH = 320、DENSITY_XXHIGH = 480、DENSITY_XXXHIGH = 640：drawable-ldpi / mdpi / hdpi / xhdpi / xxhdpi / xxxhdpi 目录对应的 dpi，即公式里的目录 dpi（出处：android.util.DisplayMetrics#DENSITY_LOW 等常量）
- private boolean mAdjustViewBounds = false;：ImageView 默认不按位图宽高比调整框（出处：android.widget.ImageView#mAdjustViewBounds）
- widthSize = resolveSizeAndState(w, widthMeasureSpec, 0); heightSize = resolveSizeAndState(h, heightMeasureSpec, 0);：未设 adjustViewBounds 时宽高各自按固有尺寸和父级约束解算，只有超限的那一轴被夹到上限（出处：android.widget.ImageView#onMeasure）
- densityDPI: number（display.getDefaultDisplaySync() 返回的 Display 上）：目标端设备的 dpi，即公式里的设备 dpi（出处：鸿蒙 SDK 的 ets/api/@ohos.display.d.ts，Display.densityDPI）
针对本应用要查的：
- 位图所在的密度目录和位图的像素宽高：源工程 res/ 下各 drawable-<密度>/ 目录，按布局里 android:src 引用的资源名找；目录名换成上面的目录 dpi；图片文件的像素宽高就是公式里的位图像素。例：只在 drawable-ldpi 时目录 dpi 取 120
来源：1 张卡，1 个应用
- case-85db2e28957bc67387d9（Bubble Shooter）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断
