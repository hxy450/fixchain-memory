# app/resources

资源批量转换：Android values 转 element JSON（颜色值形态、数组项结构、引用写法）与 drawable 转 media（反编译 APK 的内联片段、资源文件名合法性），以及宣布资源阶段完成前的产物校验，以及快捷方式等图标的画布尺寸与图形显示区（低分辨率源图的处理）

[上一级](../index.md)

## 本级经验

- [values 批量转 element JSON 按目标格式出口：颜色只写 hex 或已定义的 $color:，数组项写成 {value} 对象并映射引用，不可解析值不原样写出](lesson-94a3f7a5ec5ad8f8a3e8.lesson.md)
  - 时机：资源转换阶段，编写并运行把 Android values（colors.xml、arrays.xml 等）转成 HarmonyOS element JSON 的批量脚本，决定无法解析的值与数组项怎样输出时；宣布资源阶段完成、把产物镜像到其他限定目录之前
  - 情境：资源源为 Android res 或反编译 APK；颜色值含 @android:color/* 系统色或指向本次未转换条目的 @color/ 引用，string-array 含 @string/ 引用；转换规则文档已给出目标格式，但转换由自写脚本完成，运行后控制台只报 unresolved 计数。
- [从 apktool 反编译 APK 转资源时，把 $父名__N 内联片段单独分类；库前缀按父名匹配，写后校验输出文件名只含字母、数字与下划线](lesson-850dc758d337c4780ae9.lesson.md)
  - 时机：资源转换阶段，从反编译 APK 的 res/ 批量生成 media 文件并过滤库资源时
  - 情境：资源源是 apktool 反编译的 APK，drawable 目录里有 aapt 从 animated-vector、animation-list、selector 等拆出的内联子资源 $&lt;父名&gt;__N.xml；转换脚本按原文件名输出 SVG，并用锚定在名称开头的前缀正则跳过库资源。
- [转换快捷方式等图标资源时同时落实画布尺寸与图形显示区；测量墨迹范围后再宣告合规，低分辨率源图不插值放大充当正式资源](lesson-66e082374dc8992f48ae.lesson.md)
  - 时机：资源迁移阶段，把源端快捷方式等小图标转换成目标规范尺寸的图标资源时
  - 情境：源端只有低分辨率透明小图标（如 Android xxhdpi 72px 的快捷方式图标）；目标图标规范给出 1024×1024 透明图层且前景显示区约 450×450px（或分层前景加背景）。
