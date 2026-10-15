# values 批量转 element JSON 时颜色只写 hex 或可解析的 $color:，数组项写成 {value} 对象，不可解析值不原样写出

ID：`lesson-94a3f7a5ec5ad8f8a3e8` · 版本：3

[本主题](index.md)

## 何时使用

资源转换阶段，编写并运行把 Android values（colors.xml、arrays.xml 等）转成 HarmonyOS element JSON 的批量脚本，决定无法解析的值与数组项怎样输出时；宣布资源阶段完成、把产物镜像到其他限定目录之前

## 适用情境

资源源为 Android res 或反编译 APK；颜色值含 @android:color/* 系统色或指向本次未转换条目的 @color/ 引用，string-array 含 @string/ 引用；转换规则文档已给出目标格式，但转换由自写脚本完成，运行后控制台只报 unresolved 计数。

## 原因

HarmonyOS 资源编译只接受 #rgb/#argb/#rrggbb/#aarrggbb 或指向已定义条目的 $color:xxx 颜色值，strarray 的 value 必须是 [{"value": ...}] 对象数组、引用写成 $string:xxx；把解析不到的值原样返回、把 XML 列表直接当作 value，编译时会报 Invalid color value 或 value 类型不符（Expected type: object），镜像到其他限定目录还会复制同一错误。

## 做法

1. 颜色值只有两个出口：十六进制（8 位保持 #AARRGGBB，见颜色字节序一条），或指向当前模块（含限定目录与已声明依赖的 HAR）可解析的已定义条目的 $color:name。@android:color 的 black、white、transparent 按定义值映射（#FF000000、#FFFFFFFF、#00000000）。system_accent/neutral/error 等 Android 12+ 动态色先确认源主题是否实际使用：零引用时可不输出；有引用时取本机 SDK platforms/android-<api>/data/res/values/colors.xml 中该色的默认定义，并注明它是默认种子下的值，需随系统配色变化时另按目标动态配色方案决策。解析不到时不 return 原值。
2. strarray/intarray 的 value 写成对象数组，每项 {"value": ...}；plural 写成 {quantity, value} 对象数组。数组项里的 @string/、@color/ 引用与标量值走同一套映射（@string/x → $string:x）。
3. 写完 element JSON、镜像到 zh_CN 等限定目录之前，按规则扫描产物：颜色值全文正则、$color:/$string: 目标存在、数组项都是含 value 键的对象、没有残留 @ 前缀引用；unresolved 清单按值形态分组列出（@android:、@color/、?attr），?attr 沿主题父链到项目、依赖库与 SDK 解析，结果为零再宣布资源阶段通过。

来源支持：3 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-66bbb9dcd4568f498efa](../../../store/cases/case-66bbb9dcd4568f498efa/a668b37585e092e10f862a75cefefce50ae7d604fbfea6e2d82f302822a41ab1.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`a668b37585e092e10f862a75cefefce50ae7d604fbfea6e2d82f302822a41ab1`
- [case-6f9262e95abc71d3d226](../../../store/cases/case-6f9262e95abc71d3d226/ebab5464ffd9b729b37c56b2359ad4809980ad92d0cff0a559e58291b8285ba8.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ebab5464ffd9b729b37c56b2359ad4809980ad92d0cff0a559e58291b8285ba8`
- [case-e218dc5f282b590164d7](../../../store/cases/case-e218dc5f282b590164d7/056764ebed6d4c1387978637a83a7a79f61e1c8678cde51a272452261973e389.json) · 结论：recommendation:1
  卡片版本：`056764ebed6d4c1387978637a83a7a79f61e1c8678cde51a272452261973e389`
