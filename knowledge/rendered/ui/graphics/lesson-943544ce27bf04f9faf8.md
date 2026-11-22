# 图标按源端原始资源落实：缺失时从 Android 密度目录、SDK 平台或依赖库 AAR 复制原图，不用字形、近名图标、系统符号或二次着色替代

## 何时使用

页面转换与截图对齐修复阶段，把源布局中的 @drawable 引用（头像、图标、装饰图、带透明边缘的头图、行尾箭头）落成 $r('app.media.X') 并确认资源是否已迁移时；为工具栏、菜单行、操作栏与悬浮入口选定图标资源，或在已有页面上把占位符号换成源端图标时；规格提取阶段为源端图标与界面字符写转换决策时

## 适用情境

资源迁移把 drawable-xhdpi 等位图直接复制到 resources/xldpi/media 一类限定词目录，不在 base/media；构建日志对这些图只报“does not have a base resource”警告；工程里还有外观相近的通用图标（如生活指数图标）。 也包括规格或布局已给出原始 drawable 名，目标 media 却只有其他模块的同类近名图标（如带 1/2 后缀的阅读器图标），现有代码用 SymbolGlyph 或 Unicode 字形占位，或工程 skill 要求图标优先用已验证的系统 symbol；以及源端用粗体文字字符（“-”“+”）充当按钮图形。也包括源端 Text 直接显示 emoji 字符（如 ⭐、☕️），规格或写者按“不把 emoji 塞进 Text 当图标”一类 symbol 规则改成 SymbolGlyph。 也包括图标由平台主题或框架控件提供（ActionBar 的 Up 与溢出按钮、CheckBox 勾选图），应用 res 里没有同名资源，写者以“平台 chrome、应用无源图”为由用 Polyline、Circle 或字形自绘。 也包括 AppCompat Activity 调 setDisplayHomeAsUpEnabled(true)，返回箭头由 appcompat 库主题提供，已迁移的 media 目录里找不到，目标准备改用系统符号。

## 原因

只在 base/media 查找会把已迁移的资源判为缺失，写者随之用 Text('人')、Text('›') 之类字形、品牌色底或外观相近的通用图标代替，头像、箭头、提醒图标和透明波浪头图的收口都与源端不符；截图修复时按视觉相似挑图也会延续偏差。来源中页面转换者读到源布局列出的全部 drawable 名，只核对 base/media 就把四个资源判为不存在，改成字形占位并在透明头图下垫了品牌色；返修又从通用资源里挑近似图标。 缺图时用近名资源、系统符号或 fillColor 着色去模仿原图，同样会改变图形、线宽与颜色；skill 的“只用已验证 symbol 名称”约束的是名称合法，不保证外形与源端一致。另一应用中写者已读到规格列出的原图名并查到目标缺图，仍改用另一模块的近名图标加黄色着色，交付时称其为原图；同一应用的步进器把文字“-”换成带圆圈的 minus_circle，另一页的菜单与批量底栏在缺图时直接写成纯文字。

## 做法

1. 判断资源可用性时检索 resources 下全部限定词目录（base、xldpi、dark 等）或按资源映射表核对；构建日志里的“does not have a base resource”说明文件在限定词目录：只在屏幕密度目录（如 xldpi）里的，任何密度的设备都取得到，不是缺失；只在 dark、横竖屏、设备类型或语言目录里的，设备状态不一致时（如浅色模式下的 dark 目录）回落 base 取不到，仍按缺失处理。
2. 图标与装饰图按源布局的 src、drawableStart、background 中的 drawable 名取用，写完按源布局的 drawable 清单逐项对照组件中的引用；确认缺失时登记资源缺口，不以文字字形、纯色底或外观近似的图标替代。
3. 头图带透明边缘时，其下的底色取页面背景，不填品牌色。
4. 源图在目标 media 缺失时，从 Android 仓库对应密度目录（如 drawable-xxhdpi）复制原图并引用（重名时加模块前缀），或登记资源缺口；应用 res 里没有、由主题或框架控件提供的图标，从本机 SDK platforms/android-<api>/data/res 复制原图：Holo 主题的在 drawable-<密度> 下，是位图（返回箭头的位图名带 _am 后缀，drawable/ 下的同名 XML 只是包装）；Material 主题的返回箭头和溢出按钮（ic_ab_back_material、ic_menu_moreoverflow_material）在 drawable/ 下，是靠 android:tint="?attr/colorControlNormal" 着色的白色矢量，转 SVG 后按图标所在处生效的 colorControlNormal 设 fillColor（窗口动作栏里取 actionBarTheme 覆盖层的值）；其他控件图（如 CheckBox 勾选框）按各自矢量的 tint 取色。不拿其他模块同类、近名或带 1/2 后缀的图标顶替，不用 Polyline、Circle 或字形自绘平台图标，也不因缺图把“图标 + 文字”结构降成纯文字。 AppCompat/Material 库主题提供的图标（如 homeAsUp 的 abc_ic_ab_back_material）不在 SDK 平台目录，从对应版本库 AAR 的 res/drawable 取矢量转 SVG；矢量声明 autoMirrored=true 的加 matchTextDirection(true)（安卓应用 manifest 没声明 android:supportsRtl="true" 时 RTL 语言下也不镜像，这种情况不加）；路径填充为白色、靠 android:tint="?attr/colorControlNormal" 着色的（abc_ic_ab_back_material 即是），转 SVG 后按图标所在处生效的 colorControlNormal 设 fillColor（窗口动作栏里是 actionBarTheme 覆盖层的 textColorPrimary），这不属于第 5 步说的二次着色。系统符号只在库资源确实取不到时使用，并登记为替代。
5. 原图自带颜色时不再 fillColor 二次着色；替代图颜色不对时先确认是否选错资源。现有代码里对应 Android 位图的 SymbolGlyph 或 Unicode 占位要换成原图，只改颜色或字号不算对齐；交付记录写明每个资源来自 Android 原图复制还是工程既有资源，不把近名资源称作原图。
6. 源端用文字字符充当按钮图形或直接显示字符（粗体“-”“+”、Text 中的 emoji）时按原字符用 Text 实现（短横也可用 Divider/Rect 画同形），symbol 库没有同形名称时不选外形不同的近似 symbol（如 minus_circle）；“只用 symbol、不把 emoji 当图标”一类规则约束的是源端矢量图标资源的映射，与源端字面字符冲突时在规格中记录，不替换。

## 可选检查

- 怀疑资源被替换时，用文件大小或哈希比对工程资源与 Android 原图是否一致。

来源支持：9 张卡 · 已知 6 次迁移（部分未记录） · 已知 6 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 平台资源 android-30、android-34、android-36.1、android-37.0；Android SDK 源码 android-36.1；appcompat 1.1.0、1.7.1、1.8.0；material 1.14.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕鸿蒙按资源逐个查找：先在与设备状态匹配的限定词目录里找，没有匹配目录或目录里没有该资源才去 base；屏幕密度目录不要求与设备一致，有多个密度目录时优先向上取最接近的、否则向下取；目录里带颜色模式（dark/light）、横竖屏、设备类型、语言、文字、MCC/MNC 限定词的，取值必须与设备完全一致才参与匹配。〔成立范围：依据是文档说明。所以只放在 xldpi 等密度目录里的图在任何密度的设备上都取得到；只放在 dark 目录里的图在浅色模式下回落 base，base 没有就取不到。rawfile、resfile 不按设备状态匹配。AppScope 与模块里同名的资源只保留 AppScope 的。〕
- 〔做法第 4 步〕鸿蒙与安卓的屏幕密度限定词同名不同义：鸿蒙 sdpi、mdpi、ldpi、xldpi、xxldpi、xxxldpi 分别对应 dpi 区间 (0,120]、(120,160]、(160,240]、(240,320]、(320,480]、(480,640]，安卓 ldpi、mdpi、hdpi、xhdpi、xxhdpi、xxxhdpi 分别是 120、160、240、320、480、640 dpi；安卓 drawable-hdpi 对应鸿蒙 ldpi，安卓 drawable-ldpi 对应鸿蒙 sdpi。〔成立范围：对两端的位图密度目录成立；按目录名照搬（drawable-ldpi → ldpi）会把 120dpi 的图放进 (160,240] 的目录。鸿蒙的密度限定词只有这六个，安卓的 nodpi、anydpi、tvdpi 没有同名对应。〕
- 〔做法第 4 步〕appcompat 的 abc_ic_ab_back_material 是 24dp 矢量，路径 fillColor 为 @android:color/white，靠 android:tint="?attr/colorControlNormal" 着色，并声明 autoMirrored=true。res/values 里 Theme.AppCompat、Theme.AppCompat.Light 的 homeAsUpIndicator 指向它；values-v21 起这两个主题改取 ?android:attr/homeAsUpIndicator，即平台 Theme.Material 的 ic_ab_back_material，两者 pathData、尺寸、着色和 autoMirrored 都相同。主题级的 colorControlNormal 取 ?android:attr/textColorSecondary，但窗口自带的动作栏是用 actionBarTheme 覆盖层的上下文创建的：Theme.AppCompat、Theme.AppCompat.Light 的 ThemeOverlay.AppCompat.ActionBar 和 Theme.AppCompat.Light.DarkActionBar 的 ThemeOverlay.AppCompat.Dark.ActionBar 都把它改成 ?android:attr/textColorPrimary，所以动作栏里的返回箭头是主文字色，不是次文字色。〔成立范围：对 appcompat 1.1.0、1.7.1、1.8.0 和 Theme.AppCompat 系列成立。布局里自己放、用 setSupportActionBar 接管的 Toolbar 取它所在上下文的值：没设 android:theme 时是主题级的 textColorSecondary，套了 ThemeOverlay.AppCompat.Dark.ActionBar 等覆盖层时是覆盖层的值。应用改了 colorControlNormal 或 actionBarTheme、调用 setHomeAsUpIndicator，或给 Toolbar 设了 navigationIcon、navigationIconTint 时以应用的为准；MaterialComponents、Material3 主题可能另有覆写（如 material 1.14.0 的 Widget.Material3.Toolbar.OnSurface 设了 navigationIconTint），颜色要顺着实际主题查。〕
- 〔做法第 4 步〕Android SDK 平台资源里，Theme.Material 系列的 homeAsUpIndicator（ic_ab_back_material）和溢出按钮图标（ic_menu_moreoverflow_material）是 drawable/ 下的矢量 XML，没有 drawable-<密度> 位图，路径填充白色、靠 ?attr/colorControlNormal 着色（返回箭头还声明 autoMirrored）；Holo 主题的 homeAsUpIndicator（ic_ab_back_holo_dark、ic_ab_back_holo_light）才是位图：drawable/ 下这两个 XML 是带 autoMirrored 的 bitmap 包装，实际位图在 drawable-<密度> 下，文件名带 _am 后缀（ic_ab_back_holo_dark_am.png、ic_ab_back_holo_light_am.png）。〔成立范围：android-30、android-34、android-36.1、android-37.0 的平台资源一致；只对 SDK 平台资源里的主题定义成立，个别主题另指图标（如 Theme.Material.Settings 用 ic_ab_back_material_settings）。应用自己设了 homeAsUpIndicator 或 actionOverflowButtonStyle 时以应用的为准。〕
- 〔做法第 5 步〕Image 的 fillColor 只对 SVG 图源生效，设置后替换 SVG 里所有可绘制元素的填充色，多色 SVG 会被刷成同一种颜色；对 PNG 等位图无效，位图改色要用 colorFilter。〔成立范围：应用没有设 fillColor 时不填充，按 SVG 自身颜色显示；参数类型为 AnimatedDrawableDescriptor 时不生效；传异常值时取主题默认色（浅色模式黑、深色模式白）。API 21 起 Image 设了 supportSvg2(true)（默认 false）时，fillColor 依赖 SVG 里各元素的 fill 配置，fill 为 none 的元素不填充。〕
- 〔做法第 4 步〕Image 的 matchTextDirection 在应用没有另设时为 false，图片不随语言方向翻转；设为 true 时在 RTL 语言环境下镜像显示。安卓矢量或 bitmap 的 autoMirrored 是在布局方向为 RTL 时镜像。〔成立范围：依据是文档说明：鸿蒙这一属性跟随系统语言方向；参数类型为 AnimatedDrawableDescriptor 时不生效。安卓侧的布局方向只有应用 manifest 声明 android:supportsRtl="true"（默认 false）时才会解析成 RTL，没声明时 RTL 语言下 autoMirrored 也不镜像；鸿蒙 matchTextDirection(true) 不看这一项。〕
