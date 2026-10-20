# 备份/导出 JSON 按 org.json 或 Gson 库语义序列化（null 删键或省略、“/”与 HTML 转义），不用 JSON.stringify

ID：`lesson-0caaa4efc70dad90a15f` · 版本：2

[本主题](index.md)

## 何时使用

规格提取与数据层实现阶段，把源端用 JSONObject.put、JSONArray.toString(n) 或 Gson.toJson 生成的备份、导出或请求 JSON 写成目标契约与序列化代码时

## 适用情境

源端 serialize() 对可空值直接 put（如 put(key, steps?.serialize())、put(key, time)），再以 JSONObject/JSONArray 的 toString() 或 toString(indent) 写文件；对应 Kotlin 字段声明为可空；目标准备用 DTO 加 JSON.stringify(obj, null, n) 输出，规格可能写“null 字段输出 JSON null（键保留）”。也包括源端以 Gson 反射序列化实体（new Gson().toJson(obj)，未调 serializeNulls/disableHtmlEscaping），目标手写 toJson 或照抄标注为推断的示例 JSON。

## 原因

org.json 的 put 值为 null 时删除该键（只有 JSONObject.NULL 才写出 null 值），toString 会把 “/” 转义为 “\/”；JSON.stringify 保留值为 null 的键、不转义 “/”。由 Kotlin 字段可空推出“null 键保留”写进契约后，实现照契约输出，导出文件的键集与字节都与源端不同。Gson 反射按类层级的字段顺序输出、值为 null 的字段默认省略、boolean 写 true/false，默认 htmlSafe 把 <、>、&、=、' 写成 \u003c 一类转义，并总是转义 U+2028/U+2029；按目标模型或推断示例拼出的 JSON 在键序、布尔形态与转义上都会不同。

## 做法

1. 规格按库语义写序列化契约：put 的值为 null 时不输出该键，只有显式 put(JSONObject.NULL) 才输出 null 值；toString 转义 “/”；其余值类型照源端 put 的类型输出。不由字段可空性推出“null 键保留”。
2. 实现封装或移植与 org.json 等价的序列化工具（跳过 null 值、转义 “/”、缩进照源端 toString(n)），模型 toJson 与导出服务统一调用，不直接用 JSON.stringify。
3. 源端用 Gson 时按库实现写序列化器：键序取 Gson 反射对该类层级的遍历结果（读 ReflectiveTypeAdapterFactory 或用源端实际导出样本核对），null 字段省略（源端开启 serializeNulls 才保留），boolean 写 true/false，htmlSafe 转义与 U+2028/U+2029 转义逐字符写出；正则字面量里不放 U+2028/U+2029 原字符，写成 \u2028 转义。不照抄标注为推断的示例 JSON。

## 可选检查

- 用含 null 字段与 “/” 的样例，与源端输出逐字节比对；Gson 输出再加含 <、&、' 与 U+2028 的字符串样例

来源支持：2 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

## 来源（按需复核）

- [case-5e7f81b1b1ef0753d249](../../../store/cases/case-5e7f81b1b1ef0753d249/203ae9a24100267c1011c082352849d2f6596b184a230d8213699ec0075fa03b.json) · 结论：diagnosis, recommendation:6
  卡片版本：`203ae9a24100267c1011c082352849d2f6596b184a230d8213699ec0075fa03b`
- [case-7e6984a7fa6d5845737b](../../../store/cases/case-7e6984a7fa6d5845737b/28061d97667de8051e1a704ca4104b16d7db6a03989478ec6a0298430dae5dba.json) · 结论：diagnosis, recommendation:1, recommendation:4
  卡片版本：`28061d97667de8051e1a704ca4104b16d7db6a03989478ec6a0298430dae5dba`
