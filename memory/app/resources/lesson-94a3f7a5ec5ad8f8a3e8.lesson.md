# values 批量转 element JSON 按目标格式出口：颜色只写 hex 或已定义的 $color:，数组项写成 {value} 对象并映射引用，不可解析值不原样写出

ID：`lesson-94a3f7a5ec5ad8f8a3e8` · 版本：1

[本主题](index.md)

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

