# app/resources

资源批量转换：Android values 转 element JSON（颜色值形态与 #AARRGGBB 字节序、数组项结构、引用写法）与 drawable 转 media（VectorDrawable 转 SVG 的 viewBox 与显示尺寸、反编译 APK 的内联片段、资源文件名合法性），以及宣布资源阶段完成前的产物校验，以及快捷方式等图标的画布尺寸与图形显示区（低分辨率源图的处理），以及自适应图标转分层图标的图层尺寸与可见区裁切，以及 strings.xml 转 string.json 的 aapt2 编译语义（转义、引号、空白）与内联样式标记的保留；Compose Material 库图标（Rounded 等变体）的矢量来源

[上一级](../index.md)

## 本级经验

- [8 位颜色保持 #AARRGGBB 字节序，转换后与源逐项往返核对](lesson-783faf2767a952034514.lesson.md)
  - 时机：资源迁移阶段，编写或运行 colors.xml 到 color.json 的转换逻辑（包括编排者降级自跑脚本）时
  - 情境：源含带透明度的 8 位颜色；转换由自写脚本完成而不是直接按资源转换 skill 的规则执行，深色值可能从浅色转换结果派生，接手者可能被告知已完成部分“勿重做”。
- [Compose Material 图标（Icons.Rounded、AutoMirrored.Rounded 等变体）从可核来源提取同变体 pathData 并登记来源，不凭记忆写路径标称官方](lesson-74d535afb21b2270119e.lesson.md)
  - 时机：资源迁移或页面转换阶段，为源码引用的 Material 库图标生成目标 SVG 资源时
  - 情境：源码通过 Compose Icons.Rounded.*、Icons.AutoMirrored.Rounded.*（或 Outlined、Sharp 等变体）引用 material-icons 库矢量，工程 res 下没有对应 drawable；派工要求使用官方 path 数据、缺失写 MISSING 占位；本机可能有 Android Studio 自带的 android.jar 或 Gradle 缓存中的 material-icons 包，生成环境能否读取需当场确认。
- [VectorDrawable 转 SVG 时 viewBox 取 viewport，width/height 取显示尺寸](lesson-4e306a66aba5f1d76fdf.lesson.md)
  - 时机：资源迁移阶段，编写 VectorDrawable 到 SVG 的批量转换脚本时
  - 情境：源 vector 的 android:width/height（dp 显示尺寸）与 viewportWidth/Height（路径坐标系）常不相等，部分 fillColor 引用主题属性。
- [adaptive-icon 转 layered-image 时前景与背景生成同尺寸图层，前景先裁出启动器可见区再缩放，不直接拷贝 108dp 全层](lesson-d838f9236f7452b82738.lesson.md)
  - 时机：资源迁移阶段，把 Android adaptive-icon 转成鸿蒙 layered-image 并生成前景、背景图层 PNG 时；核验应用图标或维护资源转换规则时
  - 情境：Android 应用图标是 adaptive-icon：背景为 @color 纯色或 108dp 图层，前景为 mipmap 下 108dp 全层 PNG（启动器只显示中央 72dp）；鸿蒙侧用 layered_image.json 的 foreground/background 两个 $media 图层；转换规则写“mipmap 直接拷贝”“纯色背景任意尺寸（如 1×1 或 108×108）”。
- [strings.xml 转 string.json 按 aapt2 编译语义计算值：引号外空白折叠、值中任何位置的未转义双引号都剥离（不只首尾成对，\\" 保留为引号）、\\n \\t \\uXXXX \\' 还原；带内联标记的键取完整内容（样式入口存 HTML、纯字符串入口取全部文字），不用 el.text](lesson-f88b9c824280ce239dea.lesson.md)
  - 时机：资源转换阶段，编写批量脚本把 Android strings.xml 转成 HarmonyOS string.json、确定转义、引号、空白与内联标记的处理规则时
  - 情境：values*/strings.xml 中有跨行书写（换行加缩进）、\\n、\\t、\\uXXXX 转义、\\' \\" 或未转义双引号（整值包裹，或出现在值中间，如 below "APM"）的字符串，有的键内联 `&lt;b&gt;`/`&lt;i&gt;`/`&lt;a href&gt;`/`&lt;p&gt;` 子元素（值可能以子元素开头）或用 CDATA 包裹 HTML，由 setMessage(resId)、android:text、Html.fromHtml 或 getString/stringResource 消费；目标 string.json 的值在运行时原样显示，不再经过 aapt2；资源转换 skill 的汇总表只写“\\n、\\t → preserved”“CDATA 提取文本”“整值被引号包裹时去外层引号”，没写值中间的引号与未包 CDATA 的子元素如何取值。
- [values 批量转 element JSON 按目标格式出口：颜色只写 hex 或已定义的 $color:，数组项写成 {value} 对象并映射引用，不可解析值不原样写出](lesson-94a3f7a5ec5ad8f8a3e8.lesson.md)
  - 时机：资源转换阶段，编写并运行把 Android values（colors.xml、arrays.xml 等）转成 HarmonyOS element JSON 的批量脚本，决定无法解析的值与数组项怎样输出时；宣布资源阶段完成、把产物镜像到其他限定目录之前
  - 情境：资源源为 Android res 或反编译 APK；颜色值含 @android:color/* 系统色或指向本次未转换条目的 @color/ 引用，string-array 含 @string/ 引用；转换规则文档已给出目标格式，但转换由自写脚本完成，运行后控制台只报 unresolved 计数。
- [从 apktool 反编译 APK 转资源时，把 $父名__N 内联片段单独分类；库前缀按父名匹配，写后校验输出文件名只含字母、数字与下划线](lesson-850dc758d337c4780ae9.lesson.md)
  - 时机：资源转换阶段，从反编译 APK 的 res/ 批量生成 media 文件并过滤库资源时
  - 情境：资源源是 apktool 反编译的 APK，drawable 目录里有 aapt 从 animated-vector、animation-list、selector 等拆出的内联子资源 $&lt;父名&gt;__N.xml；转换脚本按原文件名输出 SVG，并用锚定在名称开头的前缀正则跳过库资源。
- [转换快捷方式等图标资源时同时落实画布尺寸与图形显示区；测量墨迹范围后再宣告合规，低分辨率源图不插值放大充当正式资源](lesson-66e082374dc8992f48ae.lesson.md)
  - 时机：资源迁移阶段，把源端快捷方式等小图标转换成目标规范尺寸的图标资源时
  - 情境：源端只有低分辨率透明小图标（如 Android xxhdpi 72px 的快捷方式图标）；目标图标规范给出 1024×1024 透明图层且前景显示区约 450×450px（或分层前景加背景）。
