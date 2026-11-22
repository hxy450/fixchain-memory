# 备份/导出 JSON 按 org.json 或 Gson 库语义序列化（null 删键或省略、“/”与 HTML 转义），不用 JSON.stringify

## 何时使用

规格提取与数据层实现阶段，把源端用 JSONObject.put、JSONArray.toString(n) 或 Gson.toJson 生成的备份、导出或请求 JSON 写成目标契约与序列化代码时

## 适用情境

源端 serialize() 对可空值直接 put（如 put(key, steps?.serialize())、put(key, time)），再以 JSONObject/JSONArray 的 toString() 或 toString(indent) 写文件；对应 Kotlin 字段声明为可空；目标准备用 DTO 加 JSON.stringify(obj, null, n) 输出，规格可能写“null 字段输出 JSON null（键保留）”。也包括源端以 Gson 反射序列化实体（new Gson().toJson(obj)，未调 serializeNulls/disableHtmlEscaping），目标手写 toJson 或照抄标注为推断的示例 JSON。

## 例外与边界

- “/”一律写成“\/”是安卓系统自带 org.json 的行为；源端是纯 JVM 模块、依赖的是 Maven 上的 org.json:json 时，put 的值为 null 同样删键，但“/”只在紧跟“<”时才转义——先确认源端实际用的是哪一份实现，再定转义规则。Gson 反射序列化默认跳过 transient 与 static 字段，字段带 @SerializedName 时键名取注解值，源端注册了 TypeAdapter / JsonSerializer 或字段带 @JsonAdapter 时由它们决定输出；这些字段照源端的定义输出，不按字段名和反射默认规则重写。

## 原因

org.json 的 put 值为 null 时删除该键（只有 JSONObject.NULL 才写出 null 值），toString 会把 “/” 转义为 “\/”；JSON.stringify 保留值为 null 的键、不转义 “/”。由 Kotlin 字段可空推出“null 键保留”写进契约后，实现照契约输出，导出文件的键集与字节都与源端不同。Gson 反射按类层级的字段顺序输出、值为 null 的字段默认省略、boolean 写 true/false，默认 htmlSafe 把 <、>、&、=、' 写成 \u003c 一类转义，并总是转义 U+2028/U+2029；按目标模型或推断示例拼出的 JSON 在键序、布尔形态与转义上都会不同。

## 做法

1. 规格按库语义写序列化契约：put 的值为 null 时不输出该键，只有显式 put(JSONObject.NULL) 才输出 null 值；toString 转义 “/”；其余值类型照源端 put 的类型输出。不由字段可空性推出“null 键保留”。
2. 实现封装或移植与 org.json 等价的序列化工具（跳过 null 值、转义 “/”、缩进照源端 toString(n)），模型 toJson 与导出服务统一调用，不直接用 JSON.stringify。
3. 源端用 Gson 时按库实现写序列化器：键序取 Gson 反射对该类层级的遍历结果（读 ReflectiveTypeAdapterFactory 或用源端实际导出样本核对），null 字段省略（源端开启 serializeNulls 才保留），boolean 写 true/false，htmlSafe 转义与 U+2028/U+2029 转义逐字符写出；正则字面量里不放 U+2028/U+2029 原字符，写成 \u2028 转义。不照抄标注为推断的示例 JSON。

## 可选检查

- 用含 null 字段与 “/” 的样例，与源端输出逐字节比对；Gson 输出再加含 <、&、' 与 U+2028 的字符串样例

来源支持：2 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码；com.google.code.gson:gson 2.10.1（字节码）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1、2 步〕安卓内置 org.json 的 JSONObject.put(name, value) 在 value 为 null 时删除该键已有的映射、输出里不出现这个键；只有 put 的值是 JSONObject.NULL 时，编码出的 JSON 里才有这个键且值为 null
- 〔原因 / 做法第 1、2 步〕org.json 的 toString()、toString(indentSpaces) 经 JSONStringer 写字符串值时，在 "、\、/ 前加反斜杠（'/' 写成 \/），\t、\b、\n、\r、\f 写成对应转义，其余 0x1F 及以下的控制字符写成 \u00XX
- 〔原因〕目标端用 JSON.stringify 序列化同一对象时，值为 null 的键保留在输出里、'/' 原样输出不转义，导出文件的键集与字节都和源端 org.json 的输出不同
- 〔原因 / 做法第 3 步〕卡里核对过的源端 Gson 反射序列化输出：键按反射遍历该类层级字段的顺序排列，Boolean 字段写 true/false 字面量，值为 null 的字段不出现，字符串按 htmlSafe 转义
- 〔原因 / 做法第 3 步〕应用直接 new Gson()、没有经 GsonBuilder 调 serializeNulls()、disableHtmlEscaping() 时：serializeNulls 为 false（值为 null 的字段不输出），htmlSafe 为 true（gson 2.10.1）
- 〔原因 / 做法第 3 步〕Gson 的 JsonWriter 在 htmlSafe 为 true 时把 <、>、&、=、' 写成 \u003c、\u003e、\u0026、\u003d、\u0027；不论 htmlSafe 与否，都把 U+2028、U+2029 写成 \u2028、\u2029（gson 2.10.1）
