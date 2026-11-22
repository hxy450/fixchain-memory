# 图标按源端原始资源落实：缺失时从 Android 密度目录、SDK 平台或依赖库 AAR 复制原图，不用字形、近名图标、系统符号或二次着色替代

## 何时使用

页面转换与截图对齐修复阶段，把源布局中的 @drawable 引用（头像、图标、装饰图、带透明边缘的头图、行尾箭头）落成 $r('app.media.X') 并确认资源是否已迁移时；为工具栏、菜单行、操作栏与悬浮入口选定图标资源，或在已有页面上把占位符号换成源端图标时；规格提取阶段为源端图标与界面字符写转换决策时

## 适用情境

资源迁移把 drawable-xhdpi 等位图直接复制到 resources/xldpi/media 一类限定词目录，不在 base/media；构建日志对这些图只报“does not have a base resource”警告；工程里还有外观相近的通用图标（如生活指数图标）。 也包括规格或布局已给出原始 drawable 名，目标 media 却只有其他模块的同类近名图标（如带 1/2 后缀的阅读器图标），现有代码用 SymbolGlyph 或 Unicode 字形占位，或工程 skill 要求图标优先用已验证的系统 symbol；以及源端用粗体文字字符（“-”“+”）充当按钮图形。也包括源端 Text 直接显示 emoji 字符（如 ⭐、☕️），规格或写者按“不把 emoji 塞进 Text 当图标”一类 symbol 规则改成 SymbolGlyph。 也包括图标由平台主题或框架控件提供（ActionBar 的 Up 与溢出按钮、CheckBox 勾选图），应用 res 里没有同名资源，写者以“平台 chrome、应用无源图”为由用 Polyline、Circle 或字形自绘。 也包括 AppCompat Activity 调 setDisplayHomeAsUpEnabled(true)，返回箭头由 appcompat 库主题提供，已迁移的 media 目录里找不到，目标准备改用系统符号。

## 例外与边界

- 源端在布局或代码里给图标设了着色（ImageView 的 android:tint / app:tint、setColorFilter，Compose Icon 的 tint，或矢量自带的 android:tint 主题属性）时，目标按同一颜色给 SVG 设 fillColor、给位图设 colorFilter，这是还原源端着色，不属于第 5 步的二次着色
- 把占位符号或近似图标换成原图时只换图源：原有的按钮或可点击容器、点击回调、无障碍文字保留，图标显示尺寸、点击区与间距按源布局取，不随换图改动

## 原因

只在 base/media 查找会把已迁移的资源判为缺失，写者随之用 Text('人')、Text('›') 之类字形、品牌色底或外观相近的通用图标代替，头像、箭头、提醒图标和透明波浪头图的收口都与源端不符；截图修复时按视觉相似挑图也会延续偏差。来源中页面转换者读到源布局列出的全部 drawable 名，只核对 base/media 就把四个资源判为不存在，改成字形占位并在透明头图下垫了品牌色；返修又从通用资源里挑近似图标。 缺图时用近名资源、系统符号或 fillColor 着色去模仿原图，同样会改变图形、线宽与颜色；skill 的“只用已验证 symbol 名称”约束的是名称合法，不保证外形与源端一致。另一应用中写者已读到规格列出的原图名并查到目标缺图，仍改用另一模块的近名图标加黄色着色，交付时称其为原图；同一应用的步进器把文字“-”换成带圆圈的 minus_circle，另一页的菜单与批量底栏在缺图时直接写成纯文字。

## 做法

1. 判断资源可用性时检索 resources 下全部限定词目录（base、xldpi、dark 等）或按资源映射表核对；构建日志里的“does not have a base resource”说明文件在限定词目录：只在屏幕密度目录（如 xldpi）里的，任何密度的设备都取得到，不是缺失；只在 dark、横竖屏、设备类型或语言目录里的，设备状态不一致时（如浅色模式下的 dark 目录）回落 base 取不到，仍按缺失处理。
2. 图标与装饰图按源布局的 src、drawableStart、background 中的 drawable 名取用，写完按源布局的 drawable 清单逐项对照组件中的引用；确认缺失时登记资源缺口，不以文字字形、纯色底或外观近似的图标替代。
3. 头图带透明边缘时，其下的底色取页面背景，不填品牌色。
4. 源图在目标 media 缺失时，从 Android 仓库对应密度目录（如 drawable-xxhdpi）复制原图并引用（重名时加模块前缀；按密度放进限定词目录时按 dpi 对应，drawable-hdpi 放 ldpi、drawable-xhdpi 放 xldpi、drawable-xxhdpi 放 xxldpi，不按同名对应），或登记资源缺口；应用 res 里没有、由主题或框架控件提供的图标，从本机 SDK platforms/android-<api>/data/res 复制原图：Holo 主题的在 drawable-<密度> 下，是位图（返回箭头的位图名带 _am 后缀，drawable/ 下的同名 XML 只是包装）；Material 主题的返回箭头和溢出按钮（ic_ab_back_material、ic_menu_moreoverflow_material）在 drawable/ 下，是靠 android:tint="?attr/colorControlNormal" 着色的白色矢量，转 SVG 后按图标所在处生效的 colorControlNormal 设 fillColor（窗口动作栏里取 actionBarTheme 覆盖层的值）；其他控件图（如 CheckBox 勾选框）按各自矢量的 tint 取色。不拿其他模块同类、近名或带 1/2 后缀的图标顶替，不用 Polyline、Circle 或字形自绘平台图标，也不因缺图把“图标 + 文字”结构降成纯文字。 AppCompat/Material 库主题提供的图标（如 homeAsUp 的 abc_ic_ab_back_material）不在 SDK 平台目录，从对应版本库 AAR 的 res/drawable 取矢量转 SVG；矢量声明 autoMirrored=true 的加 matchTextDirection(true)（安卓应用 manifest 没声明 android:supportsRtl="true" 时 RTL 语言下也不镜像，这种情况不加）；路径填充为白色、靠 android:tint="?attr/colorControlNormal" 着色的（abc_ic_ab_back_material 即是），转 SVG 后按图标所在处生效的 colorControlNormal 设 fillColor（窗口动作栏里是 actionBarTheme 覆盖层的 textColorPrimary），这不属于第 5 步说的二次着色。系统符号只在库资源确实取不到时使用，并登记为替代。
5. 原图自带颜色时不再 fillColor 二次着色；替代图颜色不对时先确认是否选错资源。现有代码里对应 Android 位图的 SymbolGlyph 或 Unicode 占位要换成原图，只改颜色或字号不算对齐；交付记录写明每个资源来自 Android 原图复制还是工程既有资源，不把近名资源称作原图。
6. 源端用文字字符充当按钮图形或直接显示字符（粗体“-”“+”、Text 中的 emoji）时按原字符用 Text 实现（短横也可用 Divider/Rect 画同形），symbol 库没有同形名称时不选外形不同的近似 symbol（如 minus_circle）；“只用 symbol、不把 emoji 当图标”一类规则约束的是源端矢量图标资源的映射，与源端字面字符冲突时在规格中记录，不替换。

## 可选检查

- 怀疑资源被替换时，用文件大小或哈希比对工程资源与 Android 原图是否一致。

来源支持：9 张卡 · 已知 6 次迁移（部分未记录） · 已知 6 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的平台资源；android-36.1 的源码；androidx.appcompat:appcompat 1.3.1、1.7.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕应用使用资源时，系统先在与设备状态匹配的限定词目录里找；没有匹配的限定词目录、或其中找不到该资源时，才去 base 目录找
- 〔做法第 1 步〕含移动国家码和网络码、语言、文字、横竖屏、设备类型、颜色模式限定词的目录，取值必须与设备当前状态完全一致才参与匹配；屏幕密度不要求一致：有多个密度目录时先向上取最接近的，没有再向下取最接近的，所以只放在某一个密度目录里的资源在任何密度的设备上都能匹配到
- 〔做法第 4 步〕鸿蒙的密度限定词按 dpi 区间划分：sdpi (0,120]、mdpi (120,160]、ldpi (160,240]、xldpi (240,320]、xxldpi (320,480]、xxxldpi (480,640]；安卓的 ldpi、mdpi、hdpi、xhdpi、xxhdpi、xxxhdpi 分别是 120、160、240、320、480、640 dpi，所以安卓 hdpi 对应鸿蒙 ldpi、安卓 ldpi 对应鸿蒙 sdpi，同名的 ldpi 不是同一档
- 〔适用情境 / 做法第 1 步〕media 资源只在限定词目录（如 xldpi/media）里、base/media 下没有同名文件时，构建日志对它报 “does not have a base resource” 警告，构建本身照常完成
- 〔做法第 4 步〕安卓平台的 Material 返回箭头 ic_ab_back_material 和溢出按钮 ic_menu_moreoverflow_material 都在 drawable/ 下，是 24dp×24dp、viewport 24×24 的矢量，路径 fillColor 为白色，靠 android:tint="?attr/colorControlNormal" 着色；返回箭头声明了 autoMirrored="true"，溢出按钮没有
- 〔做法第 4 步〕安卓平台的 Holo 返回箭头是位图 ic_ab_back_holo_dark_am、ic_ab_back_holo_light_am（drawable-mdpi 到 drawable-xxhdpi 各一份）；drawable/ 下的 ic_ab_back_holo_dark.xml、ic_ab_back_holo_light.xml 只是引用该位图并设 autoMirrored="true" 的 bitmap 包装
- 〔做法第 4 步〕应用主题没有另设 colorControlNormal、actionBarTheme 时：Theme.Material 与 Theme.Material.Light 的 colorControlNormal 为 ?attr/textColorSecondary、homeAsUpIndicator 为 ic_ab_back_material；动作栏用的 ThemeOverlay.Material.ActionBar 和 ThemeOverlay.Material.Dark.ActionBar 把 colorControlNormal 设为 ?attr/textColorPrimary
- 〔做法第 4 步〕appcompat 1.3.1 和 1.7.1 的 abc_ic_ab_back_material 是 24dp×24dp、viewport 24×24 的矢量，pathData 为 M20,11L7.8,11l5.6,-5.6L12,4l-8,8l8,8l1.4,-1.4L7.8,13L20,13L20,11z，路径 fillColor 为 @android:color/white，声明 autoMirrored="true" 和 android:tint="?attr/colorControlNormal"
- 〔做法第 4 步〕应用主题没有另设这几项时，appcompat 1.3.1、1.7.1 的 Base.V7.Theme.AppCompat 与 Base.V7.Theme.AppCompat.Light 把 homeAsUpIndicator 设为 @drawable/abc_ic_ab_back_material、colorControlNormal 设为 ?android:attr/textColorSecondary、actionBarTheme 设为 ThemeOverlay.AppCompat.ActionBar；Base.Theme.AppCompat.Light.DarkActionBar 的 actionBarTheme 是 ThemeOverlay.AppCompat.Dark.ActionBar；这两个动作栏覆盖层的 colorControlNormal 都是 ?android:attr/textColorPrimary
- 〔做法第 4 步〕安卓 Drawable 设了 tint 而没设 tintMode 时按 SRC_IN 混合：矢量路径原来的白色被 tint 颜色整个替换，只保留原有透明度
- 〔做法第 4 步〕安卓应用没有在 manifest 里另设 android:supportsRtl="true" 时（该属性默认 false），View 的布局方向一律解析为 LTR，autoMirrored 的 drawable 在 RTL 语言下也不镜像
- 〔做法第 4 步〕Image 的 matchTextDirection 不设时为 false，图片不随语言方向翻转；设为 true 时在 RTL 语言环境下镜像显示
- 〔做法第 4、5 步〕Image 的 fillColor 只对 SVG 图源生效，设置后替换 SVG 里所有可绘制元素的填充色；对 png 等位图不起作用（位图改色要用 colorFilter）；不设时不做填充
- 〔做法第 6 步〕Divider 的 strokeWidth 不设时为 1px，数值的默认单位是 vp，不支持百分比；水平分割线时它决定线高，但优先级低于通用属性 height；color 不设时为 '#33182431'
