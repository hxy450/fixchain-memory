# values 批量转 element JSON 按目标格式出口：颜色只写 hex 或已定义的 $color:，数组项写成 {value} 对象并映射引用，不可解析值不原样写出

## 何时使用

资源转换阶段，编写并运行把 Android values（colors.xml、arrays.xml 等）转成 HarmonyOS element JSON 的批量脚本，决定无法解析的值与数组项怎样输出时；宣布资源阶段完成、把产物镜像到其他限定目录之前

## 适用情境

资源源为 Android res 或反编译 APK；颜色值含 @android:color/* 系统色或指向本次未转换条目的 @color/ 引用，string-array 含 @string/ 引用；转换规则文档已给出目标格式，但转换由自写脚本完成，运行后控制台只报 unresolved 计数。

## 例外与边界

- 源端值是指向本应用颜色的 @color/x 引用、且 x 已转换时，写 $color:x 保留引用，不为了“只写 hex”把它解析成字面值：x 在深色或其他限定目录里有不同取值时，引用会跟着当前的深浅色模式取值，字面 hex 不会。第 1 步的固定值映射只用于平台颜色和确实无法引用的值。

## 原因

HarmonyOS 资源编译只接受 #rgb/#argb/#rrggbb/#aarrggbb 或指向已定义条目的 $color:xxx 颜色值，strarray 的 value 必须是 [{"value": ...}] 对象数组、引用写成 $string:xxx；脚本把解析不到的值原样返回、把 XML 列表直接当作 value，编译门会按资源类别逐个报 CompileResource 错误。来源的转换规则文档已写明这些格式，脚本仍把 @android:color 与未定义的 @color/ 原样写进 color.json、把 string-array 写成纯字符串并保留 @string/；运行后只看了 unresolved 总数就宣布通过，错误结构还被镜像到 zh_CN。

## 做法

1. 颜色值只有两个出口：十六进制，或指向本文件已定义条目的 $color:name。@android:color 的 black、white、transparent 按固定值映射（#FF000000、#FFFFFFFF、#00000000）；system_accent/neutral/error 等 Android 12+ 动态色没有对应，确认零引用时可不输出，有引用则给明确的 hex 回退并在映射报告注明近似。解析不到时不 return 原值。
2. strarray/intarray 的 value 写成对象数组，每项 {"value": ...}；plural 写成 {quantity, value} 对象数组。数组项里的 @string/、@color/ 引用与标量值走同一套映射（@string/x → $string:x）。
3. 写完 element JSON、镜像到 zh_CN 等限定目录之前，按规则扫描产物：颜色值全文正则、$color:/$string: 目标存在、数组项都是含 value 键的对象、没有残留 @ 前缀引用；unresolved 清单按值形态分组列出（@android:、@color/、?attr），结果为零再宣布资源阶段通过。

来源支持：3 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-37.0 的平台资源。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕鸿蒙 color.json 的八位十六进制颜色值前两位表示透明度，后六位表示颜色值
- 〔做法第 1 步〕安卓平台颜色 @android:color/black 为 #ff000000，white 为 #ffffffff，transparent 为 #00000000
- 〔原因 / 做法第 2 步〕卡里工程里 strarray.json 的数组项保留安卓写法 '@string/xxx' 时，运行时读回的就是这个字面字符串，界面显示原始资源名
