# values 批量转 element JSON 按目标格式出口：颜色只写 hex 或已定义的 $color:，数组项写成 {value} 对象并映射引用，不可解析值不原样写出

## 何时使用

资源转换阶段，编写并运行把 Android values（colors.xml、arrays.xml 等）转成 HarmonyOS element JSON 的批量脚本，决定无法解析的值与数组项怎样输出时；宣布资源阶段完成、把产物镜像到其他限定目录之前

## 适用情境

资源源为 Android res 或反编译 APK；颜色值含 @android:color/* 系统色或指向本次未转换条目的 @color/ 引用，string-array 含 @string/ 引用；转换规则文档已给出目标格式，但转换由自写脚本完成，运行后控制台只报 unresolved 计数。

## 原因

HarmonyOS 资源编译只接受 #rgb/#argb/#rrggbb/#aarrggbb 或指向已定义条目的 $color:xxx 颜色值，strarray 的 value 必须是 [{"value": ...}] 对象数组、引用写成 $string:xxx；脚本把解析不到的值原样返回、把 XML 列表直接当作 value，编译门会按资源类别逐个报 CompileResource 错误。来源的转换规则文档已写明这些格式，脚本仍把 @android:color 与未定义的 @color/ 原样写进 color.json、把 string-array 写成纯字符串并保留 @string/；运行后只看了 unresolved 总数就宣布通过，错误结构还被镜像到 zh_CN。

## 做法

1. 颜色值只有两个出口：十六进制，或指向本文件已定义条目的 $color:name。@android:color 的 black、white、transparent 按固定值映射（#FF000000、#FFFFFFFF、#00000000）；system_accent/neutral/error 等 Android 12+ 动态色没有对应，确认零引用时可不输出，有引用则给明确的 hex 回退并在映射报告注明近似。解析不到时不 return 原值。
2. strarray/intarray 的 value 写成对象数组，每项 {"value": ...}；plural 写成 {quantity, value} 对象数组。数组项里的 @string/、@color/ 引用与标量值走同一套映射（@string/x → $string:x）。
3. 写完 element JSON、镜像到 zh_CN 等限定目录之前，按规则扫描产物：颜色值全文正则、$color:/$string: 目标存在、数组项都是含 value 键的对象、没有残留 @ 前缀引用；unresolved 清单按值形态分组列出（@android:、@color/、?attr），结果为零再宣布资源阶段通过。

来源支持：3 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 平台资源 android-30、android-34、android-36.1、android-37.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕安卓平台资源里 @android:color/black、white、transparent 是 #ff000000、#ffffffff、#00000000；同为固定值的还有 background_dark #ff000000、background_light #ffffffff、darker_gray #aaa（三位简写），holo_* 也是固定 ARGB 值（如 holo_blue_light #ff33b5e5、holo_red_dark #ffcc0000、holo_orange_dark #ffff8800）。〔成立范围：对象：@android:color 下公开的固定色。条件：android-30、34、36.1、37.0 平台资源里这些取值相同。不成立：system_* 动态色和 primary_text_* 等文字色不是单一固定值，见条目 2、3。〕
- 〔做法第 1 步〕@android:color/primary_text_light、primary_text_dark、secondary_text_*、tertiary_text_*、tab_indicator_text、widget_edittext_dark 是 res/color 下的颜色状态列表（selector），不是单个颜色；取默认项时 primary_text_light 为 #ff000000（经 bright_foreground_light → background_dark）、primary_text_dark 为 #ffffffff、secondary_text_light 为 #323232、secondary_text_dark 为 #bebebe、tertiary_text_light/dark 为 #808080；禁用态另有值（如 primary_text_light 禁用为 #80000000）。〔成立范围：对象：这些公开文字色被 @android:color/ 引用时。条件：android-30 与 android-37.0 平台资源里这几个 selector 文件内容一致。不成立：引用处按 pressed、disabled 等状态取色时，默认项以外的状态值不同。〕
- 〔做法第 1 步〕@android:color/system_accent1_*、system_neutral1_* 等 system_* 颜色在平台资源里写的十六进制只是缺省值：资源注释写明可在运行时被 OverlayManager RRO 覆盖，设备上实际取到的可能不是这些值；缺省值本身也随 API 级别变（如 system_accent1_500：android-34 为 #007FAC，android-35、36 为 #6076AC），android-36.1 起 system_* 改为按深浅色分别指向 *_light、*_dark 两组值（system_accent1_500 浅色 #6476A5、深色 #69769B）。〔成立范围：对象：@android:color/system_* 动态色。条件：依据是平台资源及其注释（android-34、35、36 的 values/colors.xml；android-36.1、37.0 的 values/colors_dynamic.xml、values-night/colors_dynamic.xml 与 values/colors.xml 里的 *_light、*_dark）；覆盖发生在设备侧。不成立：没有启用覆盖的设备取到的是对应 API 级别、对应深浅色下的平台资源值。〕
