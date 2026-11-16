# 源端位图是密度解码、预缩放再 1:1 绘制时，规格逐步写出解码、预缩放采样和绘制方式

审的是：规格
触发（任一种）：
- 读到：自绘 View 里 BitmapFactory.decodeResource 解码只放在单一密度目录（如 res/drawable-ldpi）的位图，再 Bitmap.createScaledBitmap(raw, w, h, false) 预缩放，onDraw 里 drawBitmap(bmp, x, y, null) 原尺寸绘制；写错的样子：规格写成「decodeImage + drawImage 指定 w/h」或「filter=false 等价为普通缩放」，没有密度解码这一步，也没写缩放的采样方式
适用范围：规格提取阶段把源端位图的解码、预缩放和绘制翻译成 ArkUI Canvas 的绘制契约时
做法：
- 契约分三步写：解码是否按资源所在密度目录和设备密度缩放（decodeResource 对单一密度目录的资源按 设备 dpi / 目录 dpi 缩放，带滤波）；预缩放的目标尺寸和 filter 标志（false 最近邻、true 双线性）；onDraw 是否原尺寸绘制
- 不把 filter=false 写成「普通缩放」，不把预缩放改写成 drawImage 带 dw/dh 的绘制期缩放而不写采样方式
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- createScaledBitmap 的 filter 为 true 用双线性，为 false 用最近邻：filter=false 不是普通缩放，是最近邻（出处：android.graphics.Bitmap#createScaledBitmap）
- decodeResourceStream：opts.inDensity 取资源所在目录的密度，opts.inTargetDensity 取 res.getDisplayMetrics().densityDpi：decodeResource 按 设备 dpi / 目录 dpi 缩放解码结果（出处：android.graphics.BitmapFactory#decodeResourceStream）
- imageSmoothingEnabled: boolean，@default true：ArkUI 画布绘制期缩放默认是平滑插值（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderer.imageSmoothingEnabled）
- 按绘制期缩放实现时，鸿蒙端是原图平滑放大，安卓端最近邻缩小带锯齿：把预缩放写成绘制期缩放的后果（出处：卡里修好并验证过）
针对本应用要查的：
- 位图资源在哪个密度目录、原图像素尺寸：源工程 res/drawable-<密度桶>/ 目录：按资源名找它只出现在哪个桶里，再读 PNG 的实际宽高；桶名换成 dpi（DisplayMetrics.DENSITY_LOW 120、MEDIUM 160、HIGH 240、XHIGH 320、XXHIGH 480），写进契约的解码一步
来源：1 张卡，1 个应用
- case-e00d2f72aa6dfc37826b（Bubble Shooter）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 4 ← 诊断
