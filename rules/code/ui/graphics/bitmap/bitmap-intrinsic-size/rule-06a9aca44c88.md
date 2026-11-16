# Canvas 自绘中由位图固有尺寸参与的 px 量，先按目录 dpi 换算到设备 dpi

审的是：代码
触发（任一种）：
- 读到：源端 getIntrinsicWidth() / getIntrinsicHeight() 进格宽、边界余量、触点换算除数等 px 公式；写错的样子：目标直接取迁移位图的解码像素 getImageInfoSync().size.width 作格尺寸，注释写「解码=原样像素、无密度重采样」
适用范围：目标 Canvas 按 px 计算、资源迁移只保留某一个密度目录的位图时
做法：
- 固有尺寸写成 Math.trunc((px * this.getUIContext().vp2px(160) + 目录dpi / 2) / 目录dpi)，px 是迁移位图的解码像素，设备 dpi 取 vp2px(160)，再进格宽、边界、触点除数等公式
- 自己已判断源 API 带密度缩放、而规格或派工写成原始像素时，登记 Spec Gap 或 decision_gaps 并查资源迁移的取样记录，不以规格措辞消解冲突
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- vp2px(value: number): number：UIContext 上 vp 转 px；vp2px(160) 即设备 dpi（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.vp2px）
- 格尺寸 = trunc((px×vp2px(160) + 目录dpi/2) / 目录dpi)，绘制尺寸仍按 (int)(格尺寸×scale)：返修后的换算，房间居中（出处：卡里修好并验证过）
- scaleFromDensity(size, sdensity, tdensity) = ((size * tdensity) + (sdensity >> 1)) / sdensity：源端固有尺寸就是这样从目录密度换算到设备密度的（出处：android.graphics.Bitmap#scaleFromDensity）
- DENSITY_MEDIUM = 160、DENSITY_HIGH = 240、DENSITY_XHIGH = 320、DENSITY_XXHIGH = 480、DENSITY_XXXHIGH = 640：目录 dpi 的取值（出处：android.util.DisplayMetrics#DENSITY_XXXHIGH 等常量）
针对本应用要查的：
- 迁移位图的来源密度目录：资源迁移的回报或取样记录；源工程 res 下同名 PNG 所在的 drawable-*dpi 目录；目录名对到 dpi（mdpi 160 … xxxhdpi 640）作为公式里的目录 dpi
来源：1 张卡，1 个应用
- case-86f59bc73c08b834ff40（Sokoban）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 2 ← 诊断
