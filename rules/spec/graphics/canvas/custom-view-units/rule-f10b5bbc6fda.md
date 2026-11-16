# 源端用 getIntrinsicWidth/Height 定格尺寸时，规格写成设备密度 px 契约并给换算式

审的是：规格
触发（任一种）：
- 读到：自定义 View 用 Resources.getDrawable 取放在 drawable-mdpi…xxxhdpi 多个密度目录的位图，以 getIntrinsicWidth() / getIntrinsicHeight() 作格尺寸进 px 公式，再 setBounds 绘制；写错的样子：规格映射行写「贴图资源固有 px」「解码尺寸」或「同 px 域」，没写明安卓固有尺寸已按设备密度缩放，也没给目标资源的来源目录 dpi 和换算式
适用范围：把用位图固有尺寸参与几何计算的安卓自绘 View 迁成 ArkUI Canvas 时，规格里的映射和单位契约
做法：
- 规格把 getIntrinsicWidth/Height 写成设备密度下的 px 契约：注明目标资源取自哪个密度目录（目录 dpi），以及整数取整式 (px×设备dpi + 目录dpi/2) / 目录dpi
- 来源目录还没由资源迁移确定时写成待核项；不写「贴图固有 px」「解码尺寸」这类能读成原始像素的说法
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- BitmapDrawable#getIntrinsicWidth 返回 bitmap.getScaledWidth(mTargetDensity)：固有尺寸是按目标（设备）密度缩放后的 px，不是 PNG 原始像素（出处：android.graphics.drawable.BitmapDrawable#getIntrinsicWidth、#computeBitmapSize）
- scaleFromDensity(size, sdensity, tdensity) = ((size * tdensity) + (sdensity >> 1)) / sdensity；两密度相同时原样返回：契约里换算式的出处，整数运算、四舍五入（出处：android.graphics.Bitmap#scaleFromDensity）
- DENSITY_MEDIUM = 160、DENSITY_HIGH = 240、DENSITY_XHIGH = 320、DENSITY_XXHIGH = 480、DENSITY_XXXHIGH = 640：mdpi、hdpi、xhdpi、xxhdpi、xxxhdpi 目录的 dpi（出处：android.util.DisplayMetrics#DENSITY_XXXHIGH 等常量）
针对本应用要查的：
- 目标资源取自哪个密度目录：资源迁移的回报或取样记录，以及源工程 res 下同名 PNG 所在的 drawable-*dpi 目录；目录名对到 DisplayMetrics 的 dpi（如 xxxhdpi → 640），写进契约
来源：1 张卡，1 个应用
- case-86f59bc73c08b834ff40（Sokoban）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
