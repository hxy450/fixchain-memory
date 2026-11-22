# app/resources

资源批量转换：Android values 转 element JSON（颜色值形态与 #AARRGGBB 字节序、数组项结构、引用写法）与 drawable 转 media（VectorDrawable 转 SVG 的 viewBox 与显示尺寸、反编译 APK 的内联片段、资源文件名合法性），以及宣布资源阶段完成前的产物校验，以及快捷方式等图标的画布尺寸与图形显示区（低分辨率源图的处理），以及自适应图标转分层图标的图层尺寸与可见区裁切，以及 strings.xml 转 string.json 的 aapt2 编译语义（转义、引号、空白）与内联样式标记的保留；Compose Material 库图标（Rounded 等变体）的矢量来源；语言限定目录只放源端有的文字资源类型（键集审计不复制非文字资源）

[上一级](../index.md)

## 本级经验

- [8 位颜色保持 #AARRGGBB 字节序，转换后与源逐项往返核对](lesson-783faf2767a952034514.lesson.md)
  - 时机：资源迁移阶段，编写或运行 colors.xml 到 color.json 的转换逻辑（包括编排者降级自跑脚本）时
  - 情境：源含带透明度的 8 位颜色（也可能是 4 位的 #ARGB 简写，3 位 #RGB 不带透明度；简写展开成 8 位时同样透明度在前，#ARGB 每位重复一次成 #AARRGGBB，不按 CSS 的 #RGBA 理解）；转换由自写脚本完成而不是直接按资源转换 skill 的规则执行，深色值可能从浅色转换结果派生，接手者可能被告知已完成部分“勿重做”。
- [Compose Material 图标（Icons.Rounded、AutoMirrored.Rounded 等变体）从可核来源提取同变体 pathData 并登记来源，不凭记忆写路径标称官方](lesson-74d535afb21b2270119e.lesson.md)
  - 时机：资源迁移或页面转换阶段，为源码引用的 Material 库图标生成目标 SVG 资源时
  - 情境：源码通过 Compose Icons.Rounded.*、Icons.AutoMirrored.Rounded.*（或 Outlined、Sharp 等变体）引用 material-icons 库矢量，工程 res 下没有对应 drawable；派工要求使用官方 path 数据、缺失写 MISSING 占位；本机可能有 Android Studio 自带的 android.jar 或 Gradle 缓存中的 material-icons 包，生成环境能否读取需当场确认。 也包括 Icons.Outlined、Icons.Filled 等常规变体，而资源 skill 的参考把下载源指向 Material Symbols。
  - 例外：Icons.AutoMirrored.* 的矢量带自动镜像标记，在从右到左的布局里会左右翻转；转成静态 SVG 后这一行为不在资源里了，换路径时保留镜像：显示它的 Image 设 matchTextDirection(true)，或保留已有的按布局方向翻转处理，不因路径已取自官方就删掉。
- [VectorDrawable 转 SVG 时 viewBox 取 viewport、width/height 取显示尺寸，vector 根的 android:tint 按解析色烘焙到每个可见 path](lesson-4e306a66aba5f1d76fdf.lesson.md)
  - 时机：资源迁移阶段，编写 VectorDrawable 到 SVG 的批量转换脚本时
  - 情境：源 vector 的 android:width/height（dp 显示尺寸）与 viewportWidth/Height（路径坐标系）常不相等，部分 fillColor 引用主题属性；也有 vector 根写 android:tint（含框架 color state list，如 control_checkable_material），path 的 fillColor 却是字面色（如不透明黑），并带 fillAlpha=0 的动画用 path。
  - 例外：第 3 步的整体替换只在 vector 根没有另设 android:tintMode（按默认 src_in 混合）时成立；另设了 multiply、screen 等其他模式时，tint 是和原填色混合而不是替换，不能直接把 tint 色写进每个 path。tint 链里的主题属性（如 colorControlActivated、colorControlNormal）按应用实际使用的主题逐层解析，应用或其父主题覆盖过 colorAccent 等属性时取覆盖值，不直接套框架主题的默认。
- [adaptive-icon 转 layered-image 时前景与背景生成同尺寸图层，前景先裁出启动器可见区再缩放，不直接拷贝 108dp 全层](lesson-d838f9236f7452b82738.lesson.md)
  - 时机：资源迁移阶段，把 Android adaptive-icon 转成鸿蒙 layered-image 并生成前景、背景图层 PNG 时；核验应用图标或维护资源转换规则时
  - 情境：Android 应用图标是 adaptive-icon（规范：图层 108dp，启动器只显示中央 72dp）：背景为 @color 纯色或 108dp 图层，前景为 mipmap 下 108dp 全层 PNG或 drawable 下的矢量（如 ic_launcher_foreground.xml），工程里通常还有旧版合成的 ic_launcher.png；鸿蒙侧用 layered_image.json 的 foreground/background 两个 $media 图层；转换规则写“mipmap 直接拷贝”“纯色背景任意尺寸（如 1×1 或 108×108）”。
  - 例外：72/108 的裁切只对 adaptive-icon 的前景、背景层成立：源端应用图标不是 adaptive-icon（没有 &lt;adaptive-icon&gt; 资源，只有旧版 ic_launcher.png 一类整张位图）时，那张图本身就是完整的可见图形，不按 72/108 再裁，按目标图层尺寸等比放入即可。
- [strings.xml 转 string.json 按 aapt2 编译语义计算值：引号外空白折叠、值中任何位置的未转义双引号都剥离（不只首尾成对，\\" 保留为引号）、\\n \\t \\uXXXX \\' 还原；带内联标记的键取完整内容（样式入口存 HTML、纯字符串入口取全部文字），不用 el.text](lesson-f88b9c824280ce239dea.lesson.md)
  - 时机：资源转换阶段，编写批量脚本把 Android strings.xml 转成 HarmonyOS string.json、确定转义、引号、空白与内联标记的处理规则时
  - 情境：values*/strings.xml 中有跨行书写（换行加缩进）、\\n、\\t、\\uXXXX 转义、\\' \\" 或未转义双引号（整值包裹，或出现在值中间，如 below "APM"）的字符串，有的键内联 `&lt;b&gt;`/`&lt;i&gt;`/`&lt;a href&gt;`/`&lt;p&gt;` 子元素（值可能以子元素开头）或用 CDATA 包裹 HTML，由 setMessage(resId)、android:text、Html.fromHtml 或 getString/stringResource 消费；目标 string.json 的值在运行时原样显示，不再经过 aapt2；资源转换 skill 的汇总表只写“\\n、\\t → preserved”“CDATA 提取文本”“整值被引号包裹时去外层引号”，没写值中间的引号与未包 CDATA 的子元素如何取值。
- [values 批量转 element JSON 按目标格式出口：颜色只写 hex 或已定义的 $color:，数组项写成 {value} 对象并映射引用，不可解析值不原样写出](lesson-94a3f7a5ec5ad8f8a3e8.lesson.md)
  - 时机：资源转换阶段，编写并运行把 Android values（colors.xml、arrays.xml 等）转成 HarmonyOS element JSON 的批量脚本，决定无法解析的值与数组项怎样输出时；宣布资源阶段完成、把产物镜像到其他限定目录之前
  - 情境：资源源为 Android res 或反编译 APK；颜色值含 @android:color/* 系统色或指向本次未转换条目的 @color/ 引用，string-array 含 @string/ 引用；转换规则文档已给出目标格式，但转换由自写脚本完成，运行后控制台只报 unresolved 计数。
  - 例外：源端值是指向本应用颜色的 @color/x 引用、且 x 已转换时，写 $color:x 保留引用，不为了“只写 hex”把它解析成字面值：x 在深色或其他限定目录里有不同取值时，引用会跟着当前的深浅色模式取值，字面 hex 不会。第 1 步的固定值映射只用于平台颜色和确实无法引用的值。
- [从 apktool 反编译 APK 转资源时，把 $父名__N 内联片段单独分类；库前缀按父名匹配，写后校验输出文件名只含字母、数字与下划线](lesson-850dc758d337c4780ae9.lesson.md)
  - 时机：资源转换阶段，从反编译 APK 的 res/ 批量生成 media 文件并过滤库资源时
  - 情境：资源源是 apktool 反编译的 APK，drawable 目录里有 aapt 从 animated-vector、animation-list、selector 等拆出的内联子资源 $&lt;父名&gt;__N.xml；转换脚本按原文件名输出 SVG，并用锚定在名称开头的前缀正则跳过库资源。
- [语言限定目录只放源端 values-&lt;locale&gt; 实际有的资源类型：不为补齐键集审计把 base 的颜色、尺寸、布尔、整数文件复制进语言目录](lesson-f9f923ac13560dc4a114.lesson.md)
  - 时机：资源迁移收口阶段，i18n 或资源完整性审计报告语言目录缺键、缺文件，决定如何补齐时；编写按 base 批量补齐限定目录的脚本时
  - 情境：Android 源的 values-&lt;locale&gt; 通常只有 strings、arrays、plurals；HarmonyOS 目标按语言目录放 element JSON，base 之外还有 horizontal、dark、ldpi 等配置目录覆盖颜色与尺寸；审计脚本以“base 键集合＝每个语言目录键集合”为门槛，findings 列出具体缺失键与所在文件。
  - 例外：源端该语言目录本身定义了颜色、尺寸等非文字资源（如 values-&lt;locale&gt;/dimens.xml），此时按源端镜像该文件
- [转换快捷方式等图标资源时同时落实画布尺寸与图形显示区；测量墨迹范围后再宣告合规，低分辨率源图不插值放大充当正式资源](lesson-66e082374dc8992f48ae.lesson.md)
  - 时机：资源迁移阶段，把源端快捷方式等小图标转换成目标规范尺寸的图标资源时
  - 情境：源端只有低分辨率透明小图标（如 Android xxhdpi 72px 的快捷方式图标）；目标图标规范给出 1024×1024 透明图层且前景显示区约 450×450px（或分层前景加背景）。
  - 例外：约 450×450px 的显示区只约束分层图标的前景层：背景层就是 1024×1024px 的整张图，铺满画布，不按显示区缩小；源端已有矢量或足够大的图（如自适应图标的前景矢量）时，按显示区直接生成正式资源，不属于第 3 步“待设计方提供”的情形。
