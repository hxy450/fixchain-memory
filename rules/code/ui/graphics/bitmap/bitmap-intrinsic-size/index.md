# 没写固定尺寸的密度目录位图

agent 会看到什么：读到 ImageView / ImageButton 宽高是 wrap_content，或 TextView 的 drawableLeft / drawableStart 挂位图，图在 drawable-xhdpi 这类密度目录里；产物里 Image 没写宽高、写 16、32 之类经验值，照抄相邻控件或别页模板，或固定正方形再叠 padding

## 通用查法

### 源端位图控件没写固定尺寸时，读密度目录里位图的像素换算 Image 宽高

审的是：代码
触发（任一种）：
- 读到：源布局里显示位图的控件没写固定 dp 尺寸：ImageView / ImageButton 的 layout_width、layout_height 是 wrap_content，或 TextView 的 android:drawableLeft / drawableStart 挂 @drawable 位图；写错的样子：对应的 Image 没写 .width() / .height()，或写的数值不是由位图像素按密度换算来的（经验值、相邻控件、别页模板）
适用范围：源端位图（不含矢量图）的显示尺寸由像素和所在密度目录决定、迁成 ArkUI Image 时
做法：
- 按 @drawable 名在源工程 res 下各 drawable-<密度>/ 目录里找同名位图，读文件头里的像素宽高，目录名定 dpi（mdpi 160、hdpi 240、xhdpi 320、xxhdpi 480、xxxhdpi 640）
- 宽、高各自按 vp = px × 160 ÷ dpi 换算，写成 Image(...).width(<宽>).height(<高>)；只写一边时配 .objectFit(ImageFit.Contain)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- DENSITY_MEDIUM = 160（DENSITY_DEFAULT）、DENSITY_HIGH = 240、DENSITY_XHIGH = 320、DENSITY_XXHIGH = 480、DENSITY_XXXHIGH = 640：mdpi / hdpi / xhdpi / xxhdpi / xxxhdpi 各目录的 dpi，1dp 在 160dpi 上等于 1px，dp = px × 160 ÷ dpi（出处：android.util.DisplayMetrics#DENSITY_MEDIUM、DENSITY_XHIGH 等常量与 DisplayMetrics#density 注释）
- mBitmapWidth = bitmap.getScaledWidth(mTargetDensity)：没写尺寸的位图按内禀尺寸显示：像素从所在目录的密度缩放到屏幕密度，等于固定的 dp 数（出处：android.graphics.drawable.BitmapDrawable#computeBitmapSize）
- Length 为 number（数值不带单位）时默认单位 vp：Image 的 .width(n).height(n) 直接写换算出的数值（出处：ts-types.md，Length；ts-pixel-units.md，基本像素单位）
- 例：位图只在 drawable-xxhdpi、72×72px 时显示为 24×24vp：按像素 ÷ 3 改后图标大小与源端一致（出处：卡里修好并验证过）
- 例：图标只在 drawable-xhdpi 时按像素 / 2 设固有 dp：改后真机布局读数与之一致；改前照相邻控件猜的尺寸偏大（出处：卡里修好并验证过）
针对本应用要查的：
- 位图的像素宽高和所在密度目录：源工程（含共享资源模块）res 下各 drawable-<密度限定符>/ 目录里与引用的 @drawable 名同名的 png / jpg / webp 文件；读图片文件头里的像素宽高（png 读 IHDR），目录名里的 mdpi/hdpi/xhdpi/xxhdpi/xxxhdpi 定 dpi；同名文件在几个目录都有时任取一个换算，结果应一致
未核实：drawable-ldpi、drawable-nodpi 等其他密度限定符下的换算基数，族里规矩没有查实；ArkUI 在设备上对 base/media 与密度限定词目录里同名位图的实际选取和缩放没有核对
来源：3 张卡，3 个应用
- case-747484a613e86334516d（免费来电多多）：做法第 1 步 ← 建议 3；取值 5 ← 诊断
- case-ae26f8358584821ce4d4（组件岛Widget Island）：做法第 2 步 ← 建议 1
- case-b911ada02f4ec55d7d14（刺猬猫阅读）：做法第 1 步 ← 建议 2；取值 4 ← 诊断

## 规矩

- rule-32d6afad947b｜源端位图没给尺寸（wrap_content、drawableLeft）时，Image 按像素和密度桶换算写宽高｜读到：ImageView / ImageButton 宽高是 wrap_content（可带 android:scaleType），android:src 是密度目录里的位图；写错：Image 只写 .objectFit(...)、没有 .width() / .height()，或宽高写成 16 这类经验值、相邻控件的盒子尺寸
- rule-6e6aa3f00051｜位图图标显示尺寸按资源像素 ÷ 源密度换算，不凭经验填 32、44｜读到：安卓位图放在 drawable-xxhdpi 等密度目录（如 72×72px 的 png），由 ImageView 显示；写错：Image 写 .width(32).height(32)、44 这类不是由像素换算来的尺寸
- rule-6ad59363c5b0｜wrap_content 图片按资源像素和密度目录定宽高或 Contain，不用固定正方形再叠 padding｜读到：ImageView 的 layout_width / layout_height 是 wrap_content，带 android:padding，src 指向某个密度目录下的位图；写错：Image 写成固定正方形 .width(n).height(n) 再叠 .padding(...)，可视图形被压小或裁切
- rule-741bcca05a1c｜多个页面共用同一种卡片角标时抽成一个公共 @Builder 或组件，在一处定尺寸｜读到：多个列表、搜索页的安卓源码共用同一个卡片 item 布局 XML，里面的角标 ImageView 是 wrap_content；写错：几个鸿蒙页各有一份逐行相同的 @Builder 拷贝，缺的尺寸约束随拷贝传播
- rule-06a9aca44c88｜Canvas 自绘中由位图固有尺寸参与的 px 量，先按目录 dpi 换算到设备 dpi｜读到：源端 getIntrinsicWidth() / getIntrinsicHeight() 进格宽、边界余量、触点换算除数等 px 公式；写错：目标直接取迁移位图的解码像素 getImageInfoSync().size.width 作格尺寸，注释写「解码=原样像素、无密度重采样」
